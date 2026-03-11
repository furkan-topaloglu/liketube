# Production Deployment Kontrol Listesi

Bu liste, uygulamanızı production'a almadan önce kontrol etmeniz gereken tüm adımları içerir.

## ✅ Ön Hazırlık

- [ ] Domain name satın alındı/ayarlandı
- [ ] DNS kayıtları doğru yapılandırıldı (A record veya CNAME)
- [ ] Google Cloud Console'da proje oluşturuldu
- [ ] YouTube Data API v3 etkinleştirildi
- [ ] OAuth 2.0 Client ID oluşturuldu
- [ ] `client_secret.json` dosyası hazır

## 🔐 SSL/HTTPS

- [ ] SSL sertifikası kuruldu (Let's Encrypt veya platform SSL)
- [ ] HTTPS çalışıyor (`https://yourdomain.com`)
- [ ] HTTP → HTTPS yönlendirmesi çalışıyor
- [ ] SSL sertifikası geçerli (tarayıcıda kilit ikonu görünüyor)
- [ ] SSL Labs testi A veya A+ veriyor (opsiyonel ama önerilir)

## 🌐 Google Cloud Console Ayarları

- [ ] OAuth Consent Screen yapılandırıldı

  - [ ] App name ve email ayarlandı
  - [ ] Scopes eklendi (`youtube.readonly`)
  - [ ] Test users eklendi VEYA uygulama production modunda

- [ ] OAuth 2.0 Client ID ayarları:
  - [ ] Authorized JavaScript origins: `https://yourdomain.com`
  - [ ] Authorized redirect URIs: `https://yourdomain.com/oauth2callback`
  - [ ] Her ikisi de HTTPS ile başlıyor!

## 🔑 Environment Variables

Production environment variables kontrolü:

- [ ] `FLASK_ENV=production`
- [ ] `FLASK_SECRET_KEY` güçlü ve rastgele (en az 32 karakter)
- [ ] `ENCRYPTION_KEY` güçlü Fernet key (base64 encoded)
- [ ] `REDIRECT_URI=https://yourdomain.com/oauth2callback`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `OAUTHLIB_INSECURE_TRANSPORT` tanımlı DEĞİL veya `0`
- [ ] `DATABASE_URL` ayarlandı (PostgreSQL önerilir)
- [ ] `YOUTUBE_API_KEY` ayarlandı (opsiyonel ama önerilir)

### Environment Variables Örneği:

```bash
FLASK_ENV=production
FLASK_SECRET_KEY=your-very-long-and-random-secret-key-here-min-32-chars
ENCRYPTION_KEY=your-fernet-base64-encoded-key-here-44-chars
REDIRECT_URI=https://yourdomain.com/oauth2callback
SESSION_COOKIE_SECURE=True
DATABASE_URL=postgresql://user:password@localhost/youtube_filter
YOUTUBE_API_KEY=your-youtube-api-key
CLIENT_SECRETS_FILE=client_secret.json
```

## 📁 Dosya Kontrolü

- [ ] `client_secret.json` dosyası production sunucuda
- [ ] `.env` dosyası production sunucuda (veya platform environment variables)
- [ ] `.gitignore` dosyası `.env` ve `client_secret.json` içeriyor
- [ ] Gerekli Python paketleri yüklendi (`requirements.txt`)

## 🗄️ Veritabanı

- [ ] PostgreSQL kurulu ve çalışıyor (SQLite sadece küçük testler için)
- [ ] Database oluşturuldu
- [ ] Connection string doğru (`DATABASE_URL`)
- [ ] Database migration çalıştırıldı (tablolar oluşturuldu)
- [ ] Backup stratejisi planlandı

## 🚀 Deployment

- [ ] Uygulama çalışıyor (Gunicorn veya platform servisi)
- [ ] Port doğru yapılandırıldı (5000 veya platform port)
- [ ] Nginx/Reverse proxy yapılandırıldı (kendi sunucunuzda)
- [ ] Firewall kuralları ayarlandı
- [ ] Process manager kullanılıyor (systemd, PM2, vb.)

## 🧪 Test

- [ ] Ana sayfa açılıyor (`https://yourdomain.com`)
- [ ] HTTP → HTTPS yönlendirmesi çalışıyor
- [ ] "YouTube ile Giriş Yap" butonu görünüyor
- [ ] OAuth girişi çalışıyor
- [ ] Videolar yükleniyor
- [ ] Filtreleme çalışıyor
- [ ] Video tıklanınca YouTube'da açılıyor
- [ ] Çıkış yapma çalışıyor

## 🔒 Güvenlik Kontrolleri

- [ ] Debug mode kapalı (`DEBUG=False`)
- [ ] Secret key'ler güçlü ve güvenli saklanıyor
- [ ] `client_secret.json` public erişilemez
- [ ] `.env` dosyası public erişilemez
- [ ] Database credentials güvenli
- [ ] SSL sertifikası geçerli
- [ ] Session cookie secure flag aktif
- [ ] HTTPS zorunlu

## 📊 Monitoring (Opsiyonel ama Önerilir)

- [ ] Uptime monitoring kuruldu (UptimeRobot, Pingdom, vb.)
- [ ] Error tracking kuruldu (Sentry, vb.)
- [ ] Log aggregation ayarlandı
- [ ] Database backup otomatikleştirildi

## 📝 Dokümantasyon

- [ ] Production URL not edildi
- [ ] Admin paneline erişim bilgileri güvenli yerde
- [ ] Backup prosedürleri dokümante edildi
- [ ] Rollback planı hazır

---

## 🎯 Hızlı Test Komutları

### HTTPS Test:

```bash
curl -I https://yourdomain.com
# Status: 200 OK görmelisiniz
```

### SSL Test:

```bash
openssl s_client -connect yourdomain.com:443
# Certificate verify ok görmelisiniz
```

### OAuth Redirect Test:

```bash
# Google Cloud Console'da redirect URI doğru mu kontrol edin
# Browser'da https://yourdomain.com adresine gidin
# "YouTube ile Giriş Yap" butonuna tıklayın
```

---

## 🚨 Acil Durum Planı

Bir şeyler yanlış giderse:

1. **Hemen geri al:** Deployment'ı geri alın
2. **Log kontrolü:** Hata loglarını kontrol edin
3. **Environment variables:** Tüm environment variables doğru mu kontrol edin
4. **SSL sertifikası:** Sertifika geçerli mi kontrol edin
5. **Database:** Database bağlantısı çalışıyor mu kontrol edin

---

**Tüm maddeleri kontrol ettikten sonra production'a alabilirsiniz!** 🎉
