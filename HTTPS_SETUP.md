# HTTPS Kurulum Rehberi (Production)

Bu rehber, uygulamanızı production'a alırken HTTPS kurulumunu detaylı olarak açıklar.

## 📋 İçindekiler

1. [Genel Bilgiler](#1-genel-bilgiler)
2. [Platform Bazlı Kurulum](#2-platform-bazlı-kurulum)
3. [Kendi Sunucunuzda Kurulum (VPS/DigitalOcean/AWS)](#3-kendi-sunucunuzda-kurulum-vpsdigitaloceanaws)
4. [Uygulama Ayarları](#4-uygulama-ayarları)
5. [Test ve Doğrulama](#5-test-ve-doğrulama)

---

## 1. Genel Bilgiler

### Neden HTTPS?

- ✅ **Güvenlik:** Veriler şifrelenir
- ✅ **OAuth Zorunluluğu:** Google OAuth production'da HTTPS ister
- ✅ **SEO:** Google HTTPS kullanan siteleri önceliklendirir
- ✅ **Kullanıcı Güveni:** Tarayıcılarda "Güvenli" gösterilir

### Önemli Notlar

- Development'ta (`localhost`) HTTP kullanabilirsiniz
- Production'da **mutlaka HTTPS** kullanmalısınız
- SSL sertifikası için genellikle **Let's Encrypt** (ücretsiz) kullanılır

---

## 2. Platform Bazlı Kurulum

### 2.1. Heroku

Heroku otomatik olarak HTTPS sağlar! ✅

**Kurulum:**

1. Heroku'ya deploy edin:

   ```bash
   git push heroku main
   ```

2. HTTPS otomatik aktif olur
3. Domain'iniz: `https://your-app-name.herokuapp.com`

**Custom Domain için:**

```bash
heroku domains:add yourdomain.com
heroku domains:add www.yourdomain.com
```

Heroku otomatik olarak SSL sertifikası ekler.

---

### 2.2. Railway

Railway da otomatik HTTPS sağlar! ✅

1. Railway'a deploy edin
2. HTTPS otomatik aktif olur
3. Custom domain eklediğinizde SSL otomatik yapılandırılır

---

### 2.3. Render

Render otomatik HTTPS sağlar! ✅

1. Render'a deploy edin
2. HTTPS otomatik aktif olur
3. Custom domain için SSL otomatik yapılandırılır

---

### 2.4. PythonAnywhere

PythonAnywhere'de HTTPS farklı çalışır.

1. PythonAnywhere hesabınızda domain ekleyin
2. "SSL certificate" sekmesine gidin
3. "Let's Encrypt" seçeneğini kullanın
4. Domain'i doğrulayın
5. SSL otomatik kurulur

---

## 3. Kendi Sunucunuzda Kurulum (VPS/DigitalOcean/AWS)

Kendi sunucunuzda çalıştırıyorsanız, **Nginx** reverse proxy + **Let's Encrypt** kullanın.

### Adım 1: Nginx Kurulumu

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Adım 2: Uygulamanızı Çalıştırın

Gunicorn ile uygulamanızı çalıştırın:

```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app
```

Veya systemd service olarak:

```bash
sudo nano /etc/systemd/system/youtube-filter.service
```

Service dosyası:

```ini
[Unit]
Description=YouTube Filter Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/venv/bin"
ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app

[Install]
WantedBy=multi-user.target
```

Servisi başlatın:

```bash
sudo systemctl daemon-reload
sudo systemctl start youtube-filter
sudo systemctl enable youtube-filter
```

### Adım 3: Nginx Yapılandırması

```bash
sudo nano /etc/nginx/sites-available/youtube-filter
```

Nginx config:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Sembolik link oluşturun:

```bash
sudo ln -s /etc/nginx/sites-available/youtube-filter /etc/nginx/sites-enabled/
sudo nginx -t  # Yapılandırmayı test edin
sudo systemctl reload nginx
```

### Adım 4: Let's Encrypt SSL Kurulumu

**Certbot kurulumu:**

```bash
sudo apt install certbot python3-certbot-nginx -y
```

**SSL sertifikası alın:**

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot size sorular soracak:

- Email adresi: E-posta adresinizi girin
- Terms of Service: "A" ile kabul edin
- Redirect HTTP to HTTPS: "2" ile Yes seçin (önerilen)

**Otomatik yenileme:**
Let's Encrypt sertifikaları 90 günde bir yenilenir. Certbot otomatik yenileme için cron job oluşturur. Kontrol edin:

```bash
sudo certbot renew --dry-run
```

### Adım 5: Nginx HTTPS Yapılandırması (Otomatik)

Certbot Nginx yapılandırmanızı otomatik olarak güncelleyecek. Şöyle görünecek:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Nginx'i yeniden yükleyin:

```bash
sudo systemctl reload nginx
```

---

## 4. Uygulama Ayarları

### 4.1. Environment Variables

Production için `.env` dosyası veya environment variables:

```bash
FLASK_ENV=production
FLASK_SECRET_KEY=your-very-secure-secret-key-here
REDIRECT_URI=https://yourdomain.com/oauth2callback
SESSION_COOKIE_SECURE=True
OAUTHLIB_INSECURE_TRANSPORT=0  # Production'da 0 olmalı!
```

**ÖNEMLİ:** Production'da `OAUTHLIB_INSECURE_TRANSPORT=0` veya hiç tanımlanmamalı!

### 4.2. Google Cloud Console Ayarları

OAuth Redirect URI'yi güncelleyin:

1. Google Cloud Console → **APIs & Services** → **Credentials**
2. OAuth 2.0 Client ID'nize tıklayın
3. **Authorized redirect URIs** bölümüne ekleyin:
   - `https://yourdomain.com/oauth2callback`
4. **Authorized JavaScript origins** bölümüne ekleyin:
   - `https://yourdomain.com`
5. **SAVE** butonuna tıklayın

### 4.3. Config.py Kontrolü

`config.py` dosyanızda production ayarlarının doğru olduğundan emin olun:

```python
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # HTTPS için zorunlu
    REDIRECT_URI = os.getenv('REDIRECT_URI')  # Environment'tan alınmalı
```

---

## 5. Test ve Doğrulama

### 5.1. SSL Test

1. **SSL Labs Test:**

   - https://www.ssllabs.com/ssltest/
   - Domain'inizi girin
   - Test edin (A+ olmalı)

2. **Tarayıcı Kontrolü:**
   - `https://yourdomain.com` adresine gidin
   - Tarayıcıda kilit ikonu görünmeli ✅

### 5.2. OAuth Test

1. `https://yourdomain.com` adresine gidin
2. "YouTube ile Giriş Yap" butonuna tıklayın
3. Google OAuth sayfası açılmalı
4. Giriş yapın
5. Videolar görünmeli

### 5.3. HTTPS Yönlendirme Testi

1. `http://yourdomain.com` (HTTP) adresine gidin
2. Otomatik olarak `https://yourdomain.com` (HTTPS) yönlendirilmeli

---

## 🐛 Sorun Giderme

### Sorun 1: "Mixed Content" Uyarısı

**Sorun:** HTTPS'de HTTP kaynakları yüklenmiyor.

**Çözüm:**

- Tüm external linklerin HTTPS olduğundan emin olun
- YouTube embed'leri HTTPS kullanır (sorun olmaz)

### Sorun 2: SSL Sertifikası Hata Veriyor

**Çözüm:**

```bash
# Sertifikayı kontrol edin
sudo certbot certificates

# Sertifikayı yenileyin
sudo certbot renew

# Nginx'i yeniden başlatın
sudo systemctl reload nginx
```

### Sorun 3: OAuth Redirect URI Mismatch

**Sorun:** Google OAuth sayfasında "redirect_uri_mismatch" hatası.

**Çözüm:**

1. Google Cloud Console'da Redirect URI'nin tam olarak `https://yourdomain.com/oauth2callback` olduğundan emin olun
2. `.env` dosyasında `REDIRECT_URI=https://yourdomain.com/oauth2callback` olduğundan emin olun
3. Tam olarak aynı olmalı (büyük/küçük harf, slash, protokol)

### Sorun 4: Session Cookie Güvenli Değil

**Sorun:** Session cookie'ler HTTPS üzerinden gönderilmiyor.

**Çözüm:**

- `SESSION_COOKIE_SECURE=True` olduğundan emin olun
- `config.py`'de ProductionConfig'de doğru ayarlandığından emin olun

---

## 📝 Özet Checklist

Production'a almadan önce:

- [ ] Domain name satın alındı/ayarlandı
- [ ] DNS kayıtları doğru yapılandırıldı
- [ ] SSL sertifikası kuruldu (Let's Encrypt veya platform SSL)
- [ ] HTTPS çalışıyor (`https://yourdomain.com`)
- [ ] HTTP → HTTPS yönlendirmesi çalışıyor
- [ ] Google Cloud Console'da Redirect URI güncellendi
- [ ] Environment variables ayarlandı (FLASK_ENV=production, SESSION_COOKIE_SECURE=True)
- [ ] `OAUTHLIB_INSECURE_TRANSPORT` tanımlı değil veya 0
- [ ] OAuth girişi çalışıyor
- [ ] SSL Labs testi A+ veriyor

---

## 🎉 Hazır!

Artık uygulamanız güvenli HTTPS ile production'da çalışıyor! 🚀

Herhangi bir sorunla karşılaşırsanız, yukarıdaki "Sorun Giderme" bölümüne bakın veya platform dokümantasyonunuza danışın.
