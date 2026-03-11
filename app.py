import os
# Development ortamında localhost için http kullanımına izin ver
# Production'da ASLA bunu yapmayın!
if os.getenv('FLASK_ENV', 'development') == 'development':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from config import config
from models import db, User, Video
from cryptography.fernet import Fernet, InvalidToken
from utils import parse_duration, format_duration, format_number
import base64

app = Flask(__name__)

# Config
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Database
db.init_app(app)

# Encryption key for tokens (production'da environment variable'dan alınmalı)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    # Dev için otomatik key oluştur (production'da ASLA böyle yapmayın!)
    key = Fernet.generate_key()  # Fernet.generate_key() zaten base64-encoded bytes döndürür
    ENCRYPTION_KEY = key.decode()  # bytes'ı string'e çevir
    print(f"⚠️  UYARI: Encryption key otomatik oluşturuldu. Production'da ENCRYPTION_KEY environment variable'ı kullanın!")
    cipher_suite = Fernet(key)  # bytes olarak kullan
else:
    # Environment variable'dan gelen key string formatında olmalı
    try:
        cipher_suite = Fernet(ENCRYPTION_KEY.encode())  # string'i bytes'a çevir
    except Exception as e:
        # Key formatı yanlışsa yeni key oluştur
        print(f"⚠️  Encryption key format hatası: {e}. Yeni key oluşturuluyor...")
        key = Fernet.generate_key()
        ENCRYPTION_KEY = key.decode()
        cipher_suite = Fernet(key)

def encrypt_token(token):
    """Token'ı şifrele"""
    if not token:
        return None
    return cipher_suite.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token):
    """Token'ı çöz (InvalidToken durumunu yakalar ve None döner)"""
    if not encrypted_token:
        return None
    try:
        return cipher_suite.decrypt(encrypted_token.encode()).decode()
    except InvalidToken:
        # Token imzası doğrulanamadı (anahtar farklı veya veri bozulmuş)
        print("⚠️ Token decryption failed: Invalid token or signature mismatch.")
        return None
    except Exception as e:
        print(f"⚠️ Token decryption error: {e}")
        return None

def get_flow():
    """OAuth flow oluştur"""
    if not os.path.exists(app.config['CLIENT_SECRETS_FILE']):
        return None
    
    flow = Flow.from_client_secrets_file(
        app.config['CLIENT_SECRETS_FILE'],
        scopes=app.config['SCOPES'],
        redirect_uri=app.config['REDIRECT_URI']
    )
    return flow

def get_current_user():
    """Session'dan mevcut kullanıcıyı al"""
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])

def refresh_user_token(user):
    """Kullanıcı token'ını yenile"""
    try:
        token = decrypt_token(user.token)
        refresh = decrypt_token(user.refresh_token) if user.refresh_token else None

        if not token and not refresh:
            print("⚠️ Token refresh error: no valid token or refresh token available. User needs to re-authenticate.")
            return None

        credentials = Credentials(
            token=token,
            refresh_token=refresh,
            token_uri=user.token_uri,
            client_id=user.client_id,
            client_secret=user.client_secret,
            scopes=app.config['SCOPES']
        )
        
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                user.token = encrypt_token(credentials.token)
                db.session.commit()
            except Exception as e:
                print(f"⚠️ Credentials refresh failed: {e}")
                return None
        
        return credentials
    except Exception as e:
        print(f"Token refresh error: {e}")
        return None

def get_youtube_service(user):
    """YouTube API servisini al"""
    token = decrypt_token(user.token)
    refresh = decrypt_token(user.refresh_token) if user.refresh_token else None

    if not token and not refresh:
        # Kullanıcı token'ı çözülemiyor veya refresh token yok => yeniden giriş gerekli
        raise Exception('Geçersiz veya bozuk token. Lütfen tekrar giriş yapın.')

    credentials = Credentials(
        token=token,
        refresh_token=refresh,
        token_uri=user.token_uri,
        client_id=user.client_id,
        client_secret=user.client_secret,
        scopes=app.config['SCOPES']
    )

    # Token'ı yenile gerekirse
    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            user.token = encrypt_token(credentials.token)
            db.session.commit()
        except Exception as e:
            print(f"⚠️ Credentials refresh failed: {e}")
            raise Exception('Token yenileme başarısız. Lütfen tekrar giriş yapın.')

    return build('youtube', 'v3', credentials=credentials)

def sync_user_videos(user, force=False):
    """Kullanıcının beğenilen videolarını senkronize et"""
    # Cache kontrolü
    if not force:
        time_diff = datetime.utcnow() - user.last_sync
        if time_diff < timedelta(hours=app.config['CACHE_DURATION_HOURS']):
            # Cache'den dön
            videos = Video.query.filter_by(user_id=user.id).all()
            return [v.to_dict() for v in videos]
    
    try:
        youtube = get_youtube_service(user)
        
        # Kullanıcı bilgilerini al
        channels_response = youtube.channels().list(
            part='contentDetails,snippet',
            mine=True
        ).execute()
        
        if not channels_response['items']:
            return []
        
        channel_info = channels_response['items'][0]
        liked_playlist_id = channel_info['contentDetails']['relatedPlaylists']['likes']
        
        # Kullanıcı bilgilerini güncelle
        if not user.email:
            user.email = channel_info['snippet'].get('email', '')
        if not user.name:
            user.name = channel_info['snippet'].get('title', '')
        
        # Eski videoları sil
        Video.query.filter_by(user_id=user.id).delete()
        
        # Yeni videoları çek
        liked_videos = []
        next_page_token = None
        max_videos = app.config['VIDEO_SYNC_MAX']
        
        while len(liked_videos) < max_videos:
            playlist_response = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=liked_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            if not playlist_response.get('items'):
                break
            
            video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]
            
            if video_ids:
                    # Playlist item'lerinin eklenme (like) zamanını al
                    added_at_map = {}
                    for item in playlist_response['items']:
                        vid = item.get('contentDetails', {}).get('videoId')
                        if vid:
                            added_at_map[vid] = item.get('snippet', {}).get('publishedAt')

                    videos_response = youtube.videos().list(
                        part='snippet,statistics,contentDetails',
                        id=','.join(video_ids)
                    ).execute()

                    for video in videos_response['items']:
                        published_at = None
                        try:
                            published_at = datetime.fromisoformat(video['snippet']['publishedAt'].replace('Z', '+00:00'))
                        except:
                            pass

                        # Playlist item'den alınan eklenme tarihini kullan
                        added_at = None
                        added_at_str = added_at_map.get(video['id'])
                        if added_at_str:
                            try:
                                added_at = datetime.fromisoformat(added_at_str.replace('Z', '+00:00'))
                            except:
                                added_at = None

                        video_obj = Video(
                            user_id=user.id,
                            video_id=video['id'],
                            title=video['snippet']['title'],
                            channel=video['snippet']['channelTitle'],
                            channel_id=video['snippet']['channelId'],
                            description=video['snippet']['description'],
                            thumbnail=video['snippet']['thumbnails']['medium']['url'],
                            published_at=published_at,
                            view_count=int(video['statistics'].get('viewCount', 0)),
                            like_count=int(video['statistics'].get('likeCount', 0)),
                            duration=video['contentDetails']['duration'],
                            url=f"https://www.youtube.com/watch?v={video['id']}",
                            added_at=added_at or datetime.utcnow()
                        )
                        db.session.add(video_obj)

                        liked_videos.append(video_obj.to_dict())
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
        
        user.last_sync = datetime.utcnow()
        db.session.commit()
        
        return liked_videos
    
    except HttpError as e:
        print(f"YouTube API error: {e}")
        raise
    except Exception as e:
        print(f"Sync error: {e}")
        raise

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Ana sayfa"""
    user = get_current_user()
    if not user:
        return render_template('index.html', authenticated=False)
    
    return render_template('index.html', authenticated=True, user_name=user.name or user.email)

@app.route('/login')
def login():
    """YouTube'a giriş yap"""
    flow = get_flow()
    if not flow:
        return "Hata: client_secret.json dosyası bulunamadı. Lütfen Google Cloud Console'dan indirin.", 500

    # Redirect URI'yi isteğin geldiği host'a göre dinamik ayarla (localhost vs IP karışıklıklarını önler)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'  # Refresh token almak için gerekli
    )
    session['state'] = state

    # Geliştirme modunda debug için authorization_url ve redirect_uri yazdır
    if app.config.get('DEBUG', False):
        print("DEBUG: authorization_url =", authorization_url)
        print("DEBUG: using redirect_uri =", flow.redirect_uri)

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    """OAuth callback işlemi"""
    flow = get_flow()
    if not flow:
        return "Hata: client_secret.json dosyası bulunamadı.", 500

    # Redirect URI'yi isteğin geldiği host'a göre dinamik ayarla
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    
    # State kontrolü
    if 'state' not in session or session['state'] != request.args.get('state'):
        # Geliştirme modunda daha fazla bilgi yazdır
        if app.config.get('DEBUG', False):
            print("DEBUG: session_state =", session.get('state'))
            print("DEBUG: returned_state =", request.args.get('state'))
            print("DEBUG: expected redirect_uri =", flow.redirect_uri)
        return "State mismatch. Lütfen tekrar deneyin.", 400
    
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials
    
    # Kullanıcı bilgilerini al
    youtube = build('youtube', 'v3', credentials=credentials)
    channels_response = youtube.channels().list(
        part='id,snippet',
        mine=True
    ).execute()
    
    if not channels_response['items']:
        return "Kullanıcı bilgisi alınamadı.", 400
    
    channel_info = channels_response['items'][0]
    google_id = channel_info['id']
    
    # Kullanıcıyı bul veya oluştur
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(
            google_id=google_id,
            email=channel_info['snippet'].get('email', ''),
            name=channel_info['snippet'].get('title', '')
        )
        db.session.add(user)
    
    # Token'ları kaydet
    user.token = encrypt_token(credentials.token)
    user.refresh_token = encrypt_token(credentials.refresh_token) if credentials.refresh_token else None
    user.token_uri = credentials.token_uri
    user.client_id = credentials.client_id
    user.client_secret = credentials.client_secret
    db.session.commit()
    
    session['user_id'] = user.id
    session.pop('state', None)
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Çıkış yap"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/videos')
def get_videos():
    """Beğenilen videoları getir (cache'den veya API'den)"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Giriş yapılmamış'}), 401
    
    try:
        # Videoları cache'den veya senkronize et
        videos = sync_user_videos(user, force=False)
        return jsonify({'videos': videos, 'count': len(videos)})
    except HttpError as e:
        error_msg = str(e)
        if 'quotaExceeded' in error_msg:
            error_msg = 'API kotası aşıldı. Lütfen daha sonra tekrar deneyin.'
        elif 'invalid_grant' in error_msg:
            error_msg = 'Oturum süresi doldu. Lütfen tekrar giriş yapın.'
            session.clear()
        return jsonify({'error': f'YouTube API hatası: {error_msg}'}), 500
    except Exception as e:
        return jsonify({'error': f'Hata: {str(e)}'}), 500

@app.route('/api/videos/sync', methods=['POST'])
def sync_videos():
    """Videoları zorla senkronize et"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Giriş yapılmamış'}), 401
    
    try:
        videos = sync_user_videos(user, force=True)
        return jsonify({'videos': videos, 'count': len(videos), 'message': 'Videolar güncellendi'})
    except HttpError as e:
        error_msg = str(e)
        if 'quotaExceeded' in error_msg:
            error_msg = 'API kotası aşıldı. Lütfen daha sonra tekrar deneyin.'
        return jsonify({'error': f'YouTube API hatası: {error_msg}'}), 500
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(tb)
        # Only include full trace in development mode
        if env == 'development':
            return jsonify({'error': f'Hata: {str(e)}', 'trace': tb}), 500
        return jsonify({'error': f'Hata: {str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    """Kullanıcı istatistiklerini getir"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Giriş yapılmamış'}), 401
    
    video_count = Video.query.filter_by(user_id=user.id).count()
    last_sync = user.last_sync.isoformat() if user.last_sync else None
    
    return jsonify({
        'video_count': video_count,
        'last_sync': last_sync,
        'user_name': user.name or user.email
    })

@app.route('/api/filter', methods=['POST'])
def filter_videos():
    """Gelişmiş video filtreleme"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Giriş yapılmamış'}), 401
    
    try:
        data = request.json or {}
        
        # Videoları al
        videos = Video.query.filter_by(user_id=user.id).all()
        videos_list = [v.to_dict() for v in videos]
        
        # Filtreleme parametreleri
        search_text = data.get('search', '').lower()
        search_type = data.get('searchType', 'all')  # all, title, channel, description
        
        # Tarih filtreleri
        date_from = data.get('dateFrom')  # ISO format string
        date_to = data.get('dateTo')
        
        # Video süresi filtreleri (saniye cinsinden)
        duration_min = data.get('durationMin')  # saniye
        duration_max = data.get('durationMax')
        
        # İstatistik filtreleri
        views_min = data.get('viewsMin')
        views_max = data.get('viewsMax')
        likes_min = data.get('likesMin')
        likes_max = data.get('likesMax')

        # Sıralama
        sort_by = data.get('sortBy', 'addedAt')  # addedAt, publishedAt, views, likes, duration, title
        sort_order = data.get('sortOrder', 'desc')  # asc, desc
        
        # Filtreleme
        filtered = []
        for video in videos_list:
            # Text arama
            if search_text:
                match = False
                if search_type == 'all':
                    match = (search_text in video['title'].lower() or
                            search_text in video['channel'].lower() or
                            search_text in (video.get('description', '') or '').lower())
                elif search_type == 'title':
                    match = search_text in video['title'].lower()
                elif search_type == 'channel':
                    match = search_text in video['channel'].lower()
                elif search_type == 'description':
                    match = search_text in (video.get('description', '') or '').lower()
                
                if not match:
                    continue
            
            # Tarih filtreleri
            if date_from:
                try:
                    from_date = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                    if video.get('addedAt'):
                        vid_date = datetime.fromisoformat(video['addedAt'].replace('Z', '+00:00'))
                        if vid_date < from_date:
                            continue
                except:
                    pass
            
            if date_to:
                try:
                    to_date = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                    if video.get('addedAt'):
                        vid_date = datetime.fromisoformat(video['addedAt'].replace('Z', '+00:00'))
                        if vid_date > to_date:
                            continue
                except:
                    pass
            
            # Süre filtreleri
            duration = video.get('durationSeconds', 0)
            if duration_min is not None and duration < duration_min:
                continue
            if duration_max is not None and duration > duration_max:
                continue
            
            # İstatistik filtreleri
            views = video.get('viewCount', 0)
            if views_min is not None and views < views_min:
                continue
            if views_max is not None and views > views_max:
                continue
            
            likes = video.get('likeCount', 0)
            if likes_min is not None and likes < likes_min:
                continue
            if likes_max is not None and likes > likes_max:
                continue
            
            filtered.append(video)
        
        # Sıralama
        reverse = (sort_order == 'desc')
        
        if sort_by == 'addedAt':
            # Tarih sıralaması için datetime objesi kullan
            def get_added_date(video):
                added_at = video.get('addedAt')
                if not added_at:
                    return datetime.min
                try:
                    return datetime.fromisoformat(added_at.replace('Z', '+00:00'))
                except:
                    return datetime.min
            filtered.sort(key=get_added_date, reverse=reverse)
        elif sort_by == 'publishedAt':
            def get_published_date(video):
                published_at = video.get('publishedAt')
                if not published_at:
                    return datetime.min
                try:
                    return datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                except:
                    return datetime.min
            filtered.sort(key=get_published_date, reverse=reverse)
        elif sort_by == 'views':
            filtered.sort(key=lambda x: x.get('viewCount', 0), reverse=reverse)
        elif sort_by == 'likes':
            filtered.sort(key=lambda x: x.get('likeCount', 0), reverse=reverse)
        elif sort_by == 'duration':
            filtered.sort(key=lambda x: x.get('durationSeconds', 0), reverse=reverse)
        elif sort_by == 'title':
            filtered.sort(key=lambda x: x.get('title', '').lower(), reverse=reverse)
        
        return jsonify({
            'videos': filtered,
            'count': len(filtered),
            'total': len(videos_list)
        })
    
    except Exception as e:
        return jsonify({'error': f'Hata: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=(env == 'development'), host='0.0.0.0', port=port)
