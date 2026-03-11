# 🎬 LikeTube

LikeTube, YouTube hesabınızdan beğendiğiniz videoları çekip, filtreleyip kolayca bulmanızı sağlar. Kullanıcılar kendi YouTube hesaplarına giriş yaparak beğendikleri videoları görüntüleyebilir, filtreleyebilir ve hızlıca izleyebilirler.

## 🎯 Özellikler

- ✅ YouTube OAuth ile güvenli giriş
- 📹 Beğenilen videoları otomatik çekme ve cache'leme
- 🔍 Gelişmiş filtreleme (başlık, kanal, açıklama)
- ⚡ Client-side filtreleme ile hızlı arama
- 💾 Veritabanı ile video cache (API çağrılarını azaltır)
- 🔄 Token otomatik yenileme
- 📊 İstatistikler ve senkronizasyon bilgileri

## 🚀 Hızlı Başlangıç

### Geliştirme Ortamı

1. **Gerekli paketleri yükleyin:**

```bash
pip install -r requirements.txt
```

2. **Google Cloud Console Ayarları:**

   - [Google Cloud Console](https://console.cloud.google.com/) üzerinden proje oluşturun
   - **YouTube Data API v3**'ü etkinleştirin
   - **OAuth 2.0 Client ID** oluşturun (Web uygulaması):
     - Yetkili JavaScript kaynakları: `http://localhost:5000`
     - Yetkili yönlendirme URI'leri: `http://localhost:5000/oauth2callback`
   - `client_secret.json` dosyasını indirip proje klasörüne koyun

3. **Environment Variables:**

`.env` dosyası oluşturun:

```env
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here-change-this
YOUTUBE_API_KEY=your_youtube_api_key_here
REDIRECT_URI=http://localhost:5000/oauth2callback
CLIENT_SECRETS_FILE=client_secret.json
DATABASE_URL=sqlite:///youtube_filter.db
```

4. **Veritabanını başlatın:**

Uygulama ilk çalıştığında otomatik oluşturulur.

5. **Uygulamayı çalıştırın:**

```bash
# Development için
python app.py

# veya run.py ile (önerilen)
python run.py

# Production için (Gunicorn ile)
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

6. **Tarayıcınızda açın:**

`http://localhost:5000`

## 📖 Kullanım

1. "YouTube ile Giriş Yap" butonuna tıklayın
2. Google hesabınızla giriş yapın ve izinleri onaylayın
3. Beğenilen videolarınız otomatik olarak çekilir ve cache'lenir
4. Arama kutusuna yazarak videoları filtreleyin (anlık filtreleme)
5. Filtre tipini seçin: Tümü, Başlık, Kanal veya Açıklama
6. Videoyu tıklayarak YouTube'da izleyin
7. "Senkronize Et" ile videoları güncelleyin

## 🏗️ Production Deployment

Production'a almak için rehberlere bakın:

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Genel deployment rehberi
- **[HTTPS_SETUP.md](HTTPS_SETUP.md)** - HTTPS/SSL kurulum rehberi (ÖNEMLİ!)
- **[PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)** - Kontrol listesi

### Hızlı Özet:

1. Environment variable'ları ayarlayın
2. PostgreSQL kullanın (SQLite yerine)
3. **HTTPS kurun** (SSL sertifikası - ZORUNLU!)
4. Güvenli encryption key kullanın
5. Gunicorn ile çalıştırın
6. Google Cloud Console'da Redirect URI'yi güncelleyin

> ⚠️ **ÖNEMLİ:** Production'da HTTPS zorunludur! OAuth çalışması için gereklidir.

## 🔒 Güvenlik

- Token'lar şifrelenmiş olarak veritabanında saklanır
- HTTPS kullanımı zorunludur (production)
- Session güvenliği yapılandırılmıştır
- OAuth 2.0 ile güvenli kimlik doğrulama

## 📝 Notlar

- **API Kotası:** YouTube Data API v3 günlük 10,000 birim limitine sahiptir
- **Cache Süresi:** Videolar 24 saat cache'lenir (ayarlanabilir)
- **Maksimum Video:** Varsayılan olarak 1000 video çekilir (ayarlanabilir)
- **Veritabanı:** Development'ta SQLite, production'da PostgreSQL önerilir

## 🛠️ Teknolojiler

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy (SQLite/PostgreSQL)
- **API:** YouTube Data API v3
- **Authentication:** OAuth 2.0
- **Frontend:** HTML, CSS, JavaScript (Vanilla)

## 📄 Lisans

Bu proje özgürce kullanılabilir.

## 🤝 Katkıda Bulunma

Önerileriniz ve katkılarınız için issue açabilir veya pull request gönderebilirsiniz.
