# Deployment Rehberi

Bu uygulamayı production'a almak için aşağıdaki adımları takip edin.

## 1. Gereksinimler

- Python 3.8+
- PostgreSQL (veya SQLite - sadece küçük ölçek için)
- Google Cloud Console hesabı

## 2. Google Cloud Console Ayarları

1. [Google Cloud Console](https://console.cloud.google.com/) üzerinden yeni proje oluşturun
2. **YouTube Data API v3**'ü etkinleştirin
3. **OAuth 2.0 Client ID** oluşturun:
   - Uygulama türü: Web uygulaması
   - Yetkili JavaScript kaynakları: `https://yourdomain.com`
   - Yetkili yönlendirme URI'leri: `https://yourdomain.com/oauth2callback`
4. `client_secret.json` dosyasını indirip sunucunuza yükleyin

## 3. Environment Variables

Production'da aşağıdaki environment variable'ları ayarlayın:

> 📋 **Detaylı kontrol listesi için:** [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) dosyasına bakın

```bash
# Flask
FLASK_ENV=production
FLASK_SECRET_KEY=<güvenli-random-string-oluşturun>

# Database (PostgreSQL için)
DATABASE_URL=postgresql://user:password@localhost/youtube_filter

# YouTube API
YOUTUBE_API_KEY=<api-key-iniz>

# OAuth
REDIRECT_URI=https://yourdomain.com/oauth2callback
CLIENT_SECRETS_FILE=client_secret.json

# Security (Production için ÖNEMLİ!)
ENCRYPTION_KEY=<fernet-key-oluşturun>
SESSION_COOKIE_SECURE=True
# ÖNEMLİ: Production'da OAUTHLIB_INSECURE_TRANSPORT tanımlı OLMAMALI!

# Optional
VIDEO_SYNC_MAX=1000
CACHE_DURATION_HOURS=24
PORT=5000
```

### Encryption Key Oluşturma

Python'da şu komutu çalıştırın:

```python
from cryptography.fernet import Fernet
import base64
key = Fernet.generate_key()
print(base64.urlsafe_b64encode(key).decode())
```

Bu çıktıyı `ENCRYPTION_KEY` olarak kullanın.

## 4. Deployment Platformları

### Heroku

1. Heroku CLI ile giriş yapın
2. Uygulama oluşturun: `heroku create your-app-name`
3. PostgreSQL addon ekleyin: `heroku addons:create heroku-postgresql:hobby-dev`
4. Environment variable'ları ayarlayın:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_SECRET_KEY=<your-secret-key>
   heroku config:set ENCRYPTION_KEY=<your-encryption-key>
   # ... diğer değişkenler
   ```
5. `client_secret.json` dosyasını Heroku'ya yükleyin (Config Vars veya S3 kullanın)
6. Deploy edin: `git push heroku main`

### DigitalOcean / AWS / VPS

1. Gunicorn ile çalıştırın:

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
   ```

2. Nginx reverse proxy kurulumu (önerilir):

   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. SSL sertifikası için Let's Encrypt kullanın:
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

### Docker

1. `Dockerfile` oluşturun (aşağıda örnek)
2. Build edin: `docker build -t youtube-filter .`
3. Çalıştırın: `docker run -p 5000:5000 --env-file .env youtube-filter`

## 5. Güvenlik Kontrolleri

- [ ] `FLASK_SECRET_KEY` güçlü ve rastgele
- [ ] `ENCRYPTION_KEY` güçlü ve güvenli saklanıyor
- [ ] `SESSION_COOKIE_SECURE=True` (HTTPS için)
- [ ] `client_secret.json` dosyası güvenli ve erişilemez
- [ ] Database şifrelenmiş bağlantı kullanıyor
- [ ] Environment variable'lar production'da doğru ayarlanmış

## 6. Performans İyileştirmeleri

- PostgreSQL kullanın (SQLite yerine)
- Redis cache ekleyin (opsiyonel)
- CDN kullanın (statik dosyalar için)
- Rate limiting ekleyin (Flask-Limiter)

## 7. Monitoring

- Sentry veya benzeri hata takip sistemi
- Uptime monitoring
- Log aggregation (Papertrail, Loggly, vb.)

## 8. Backup

- Database düzenli backup alın
- Encryption key'leri güvenli yerde saklayın
