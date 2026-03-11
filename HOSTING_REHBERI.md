# LikeTube - Hosting ve Production'a Alma Rehberi

Bu rehber, LikeTube uygulamanızı canlıya almak için tüm adımları içerir.

## 🎯 Hızlı Karar: Hangi Platform?

### Ücretsiz/Öğrenci Dostu:
- ✅ **Railway** (Önerilen - En kolay)
- ✅ **Render** (Ücretsiz tier var)
- ✅ **Fly.io** (Ücretsiz tier)

### Ücretli ama Güçlü:
- ✅ **Heroku** (Kolay, ücretli)
- ✅ **DigitalOcean App Platform** (Orta seviye)
- ✅ **AWS** (Gelişmiş, karmaşık)

### Kendi Sunucunuz:
- ✅ **DigitalOcean Droplet** (VPS)
- ✅ **AWS EC2**
- ✅ **Linode**

---

## 🚀 Seçenek 1: Railway (ÖNERİLEN - En Kolay)

Railway, en kolay ve hızlı deployment sağlar. Ücretsiz tier ile başlayabilirsiniz.

### Adımlar:

1. **Railway'a Kayıt:**
   - https://railway.app/ adresine gidin
   - "Start a New Project" → "Deploy from GitHub repo" seçin
   - GitHub hesabınızla giriş yapın

2. **Projeyi Yükle:**
   - GitHub'da repository oluşturun
   - Kodlarınızı push edin:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/kullaniciadi/liketube.git
     git push -u origin main
     ```

3. **Railway'da Deploy:**
   - Railway dashboard'da "New Project" → "Deploy from GitHub repo"
   - Repository'nizi seçin
   - Railway otomatik olarak Flask uygulamanızı algılar

4. **Environment Variables:**
   Railway dashboard'da "Variables" sekmesine gidin ve ekleyin:
   ```
   FLASK_ENV=production
   FLASK_SECRET_KEY=<güçlü-bir-anahtar>
   ENCRYPTION_KEY=<fernet-key>
   REDIRECT_URI=https://your-app-name.railway.app/oauth2callback
   DATABASE_URL=<railway-otomatik-oluşturur>
   CLIENT_SECRETS_FILE=client_secret.json
   ```

5. **PostgreSQL Ekle:**
   - Railway dashboard'da "New" → "Database" → "PostgreSQL"
   - Otomatik olarak `DATABASE_URL` environment variable'ı eklenir

6. **client_secret.json Ekle:**
   - Railway'da "Variables" sekmesine gidin
   - "Raw Editor" moduna geçin
   - `CLIENT_SECRETS_FILE` yerine direkt JSON içeriğini ekleyebilirsiniz
   - VEYA: Railway'ın file upload özelliğini kullanın

7. **Custom Domain (Opsiyonel):**
   - Railway dashboard'da "Settings" → "Domains"
   - Domain ekleyin
   - DNS ayarlarını yapın

**Maliyet:** Ücretsiz tier: $5 kredi/ay (küçük uygulamalar için yeterli)

---

## 🚀 Seçenek 2: Render

Render da kolay ve ücretsiz tier sunar.

### Adımlar:

1. **Render'a Kayıt:**
   - https://render.com/ adresine gidin
   - GitHub ile kayıt olun

2. **Yeni Web Service:**
   - "New" → "Web Service"
   - GitHub repository'nizi seçin

3. **Ayarlar:**
   ```
   Name: liketube
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
   ```

4. **Environment Variables:**
   ```
   FLASK_ENV=production
   FLASK_SECRET_KEY=<güçlü-anahtar>
   ENCRYPTION_KEY=<fernet-key>
   REDIRECT_URI=https://liketube.onrender.com/oauth2callback
   DATABASE_URL=<render-postgres-url>
   ```

5. **PostgreSQL Ekle:**
   - "New" → "PostgreSQL"
   - Otomatik bağlanır

**Maliyet:** Ücretsiz tier: 750 saat/ay (yeterli)

---

## 🚀 Seçenek 3: Heroku

Heroku klasik ve güvenilir bir seçenek.

### Adımlar:

1. **Heroku CLI Kurulum:**
   ```bash
   # Windows: https://devcenter.heroku.com/articles/heroku-cli
   # veya web üzerinden yapabilirsiniz
   ```

2. **Heroku'ya Giriş:**
   ```bash
   heroku login
   ```

3. **Uygulama Oluştur:**
   ```bash
   heroku create liketube
   ```

4. **PostgreSQL Ekle:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Environment Variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_SECRET_KEY=<güçlü-anahtar>
   heroku config:set ENCRYPTION_KEY=<fernet-key>
   heroku config:set REDIRECT_URI=https://liketube.herokuapp.com/oauth2callback
   ```

6. **client_secret.json:**
   - Heroku'da Config Vars'a ekleyin VEYA
   - S3 gibi bir storage kullanın

7. **Deploy:**
   ```bash
   git push heroku main
   ```

**Maliyet:** Ücretsiz tier yok, $7/ay başlangıç

---

## 🚀 Seçenek 4: Kendi VPS (DigitalOcean)

Daha fazla kontrol istiyorsanız kendi sunucunuzu kullanın.

### Adımlar:

1. **DigitalOcean Droplet Oluştur:**
   - https://www.digitalocean.com/
   - "Create" → "Droplets"
   - Ubuntu 22.04 seçin
   - En küçük plan ($6/ay) yeterli

2. **Sunucuya Bağlan:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Gerekli Yazılımları Kur:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql -y
   ```

4. **Uygulamayı Yükle:**
   ```bash
   cd /var/www
   git clone https://github.com/kullaniciadi/liketube.git
   cd liketube
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **PostgreSQL Kurulum:**
   ```bash
   sudo -u postgres createdb liketube
   sudo -u postgres createuser liketube_user
   sudo -u postgres psql -c "ALTER USER liketube_user WITH PASSWORD 'güçlü-şifre';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE liketube TO liketube_user;"
   ```

6. **Environment Variables:**
   ```bash
   nano /var/www/liketube/.env
   ```
   ```
   FLASK_ENV=production
   FLASK_SECRET_KEY=<güçlü-anahtar>
   ENCRYPTION_KEY=<fernet-key>
   DATABASE_URL=postgresql://liketube_user:şifre@localhost/liketube
   REDIRECT_URI=https://yourdomain.com/oauth2callback
   ```

7. **Systemd Service:**
   ```bash
   sudo nano /etc/systemd/system/liketube.service
   ```
   ```ini
   [Unit]
   Description=LikeTube Gunicorn
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/liketube
   Environment="PATH=/var/www/liketube/venv/bin"
   ExecStart=/var/www/liketube/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start liketube
   sudo systemctl enable liketube
   ```

8. **Nginx Kurulum:**
   - `HTTPS_SETUP.md` dosyasındaki adımları takip edin
   - Let's Encrypt SSL kurun

**Maliyet:** $6-12/ay (droplet) + domain ($10-15/yıl)

---

## 🔧 Google Cloud Console Ayarları (Tüm Platformlar İçin)

Production'a almadan önce:

1. **OAuth Consent Screen:**
   - Google Cloud Console → OAuth consent screen
   - "Publish App" butonuna tıklayın (test modundan çıkarın)
   - VEYA test users listesine email ekleyin

2. **OAuth 2.0 Client ID:**
   - Authorized JavaScript origins: `https://yourdomain.com`
   - Authorized redirect URIs: `https://yourdomain.com/oauth2callback`
   - **ÖNEMLİ:** HTTPS kullanın!

3. **API Kotası:**
   - YouTube Data API v3 kotasını kontrol edin
   - Gerekirse artırım talep edin

---

## 📋 Production Checklist

- [ ] Domain name satın alındı/ayarlandı
- [ ] SSL sertifikası kuruldu (HTTPS zorunlu!)
- [ ] Google Cloud Console'da Redirect URI güncellendi
- [ ] OAuth Consent Screen production modunda
- [ ] Environment variables ayarlandı
- [ ] `FLASK_ENV=production`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `OAUTHLIB_INSECURE_TRANSPORT` tanımlı DEĞİL
- [ ] Database (PostgreSQL) kuruldu
- [ ] `client_secret.json` güvenli yerde
- [ ] Uygulama çalışıyor
- [ ] OAuth girişi test edildi
- [ ] Videolar yükleniyor

---

## 💰 Maliyet Karşılaştırması

| Platform | Ücretsiz Tier | Ücretli Başlangıç | Kolaylık |
|----------|---------------|-------------------|----------|
| Railway | ✅ $5 kredi/ay | $20/ay | ⭐⭐⭐⭐⭐ |
| Render | ✅ 750 saat/ay | $7/ay | ⭐⭐⭐⭐ |
| Heroku | ❌ | $7/ay | ⭐⭐⭐⭐ |
| DigitalOcean | ❌ | $6/ay | ⭐⭐⭐ |
| Fly.io | ✅ | $0 (küçük uygulamalar) | ⭐⭐⭐⭐ |

---

## 🎯 Öneri

**Başlangıç için:** Railway veya Render (ücretsiz tier)
**Büyüme için:** DigitalOcean VPS (daha fazla kontrol)

**Hangi platformu seçerseniz seçin, `HTTPS_SETUP.md` dosyasındaki SSL kurulum adımlarını takip edin!**

---

## 🆘 Sorun mu Yaşıyorsunuz?

1. Logları kontrol edin (platform dashboard'da)
2. Environment variables doğru mu?
3. Google Cloud Console ayarları güncel mi?
4. Database bağlantısı çalışıyor mu?

Herhangi bir sorunla karşılaşırsanız, platform dokümantasyonuna bakın veya destek ekibine ulaşın.

**Başarılar! 🚀**

