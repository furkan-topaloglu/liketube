# Google Cloud Console Kurulum Rehberi (Adım Adım)

Bu rehber, YouTube Data API v3'ü etkinleştirme ve OAuth 2.0 Client ID oluşturma işlemlerini detaylı olarak açıklar.

## 📋 İçindekiler

1. [Google Cloud Console'a Giriş ve Proje Oluşturma](#1-google-cloud-consolea-giriş-ve-proje-oluşturma)
2. [YouTube Data API v3'ü Etkinleştirme](#2-youtube-data-api-v3ü-etkinleştirme)
3. [OAuth 2.0 Client ID Oluşturma](#3-oauth-20-client-id-oluşturma)
4. [client_secret.json Dosyasını İndirme](#4-client_secretjson-dosyasını-indirme)
5. [Doğrulama ve Test](#5-doğrulama-ve-test)

---

## 1. Google Cloud Console'a Giriş ve Proje Oluşturma

### Adım 1.1: Google Cloud Console'a Giriş Yapın

1. Tarayıcınızda şu adrese gidin: https://console.cloud.google.com/
2. Google hesabınızla giriş yapın (YouTube kullanacağınız hesapla aynı olmalı)

### Adım 1.2: Yeni Proje Oluşturun

1. Sayfanın üst kısmında **proje seçici** dropdown menüsünü bulun (genellikle "My First Project" veya mevcut bir proje adı yazar)
2. **"NEW PROJECT"** butonuna tıklayın
3. Açılan pencerede:
   - **Project name:** Projenize bir isim verin (örn: "YouTube Filter App")
   - **Location:** "No organization" veya varsa organizasyonunuzu seçin
4. **"CREATE"** butonuna tıklayın
5. Proje oluşturma işlemi birkaç saniye sürebilir, bekleyin
6. Oluşturulduktan sonra proje seçici menüden yeni projenizi seçin

> 💡 **İpucu:** Proje oluşturulduktan sonra, sayfanın üst kısmında seçili projenin adını göreceksiniz.

---

## 2. YouTube Data API v3'ü Etkinleştirme

### Adım 2.1: API Library'ye Gidin

1. Sol taraftaki **hamburger menü** (☰) simgesine tıklayın
2. Menüden **"APIs & Services"** seçin
3. Açılan alt menüden **"Library"** seçeneğine tıklayın

### Adım 2.2: YouTube Data API v3'ü Bulun

1. Arama kutusuna **"YouTube Data API v3"** yazın
2. Arama sonuçlarından **"YouTube Data API v3"** seçeneğini seçin
   - Google tarafından sağlanan, resmi API olmalı
   - İkonunda YouTube logosu olabilir

### Adım 2.3: API'yi Etkinleştirin

1. API sayfasında **"ENABLE"** (Etkinleştir) butonuna tıklayın
2. İşlem birkaç saniye sürebilir
3. Etkinleştirildikten sonra yeşil bir onay mesajı göreceksiniz

> ✅ **Başarılı!** YouTube Data API v3 artık aktif. Sayfanın üstünde "API enabled" yazısını görebilirsiniz.

---

## 3. OAuth 2.0 Client ID Oluşturma

### Adım 3.1: OAuth Consent Screen'i Yapılandırın (İlk Kez Yapıyorsanız)

OAuth Client ID oluşturmadan önce OAuth Consent Screen'i yapılandırmanız gerekir.

1. Sol menüden **"APIs & Services"** → **"OAuth consent screen"** seçin
2. **User Type** seçin:
   - **External** (Dış kullanıcılar için - çoğu durumda bu seçenek)
   - **Internal** (Sadece Google Workspace organizasyonu içindeki kullanıcılar için)
3. **"CREATE"** butonuna tıklayın

#### OAuth Consent Screen Bilgilerini Doldurun:

**App information:**
- **App name:** Uygulamanızın adı (örn: "YouTube Video Filter")
- **User support email:** E-posta adresiniz (dropdown'dan seçin)
- **App logo:** (Opsiyonel) Uygulama logosu yükleyebilirsiniz

**App domain:** (Bu aşamada atlayabilirsiniz veya localhost ekleyebilirsiniz)
- **Application home page:** `http://localhost:5000` (geliştirme için)
- **Authorized domains:** Boş bırakabilirsiniz (local development için)

**Developer contact information:**
- **Email addresses:** E-posta adresiniz (otomatik doldurulmuş olabilir)

4. **"SAVE AND CONTINUE"** butonuna tıklayın

#### Scopes (İzinler) Ekleme:

1. **"ADD OR REMOVE SCOPES"** butonuna tıklayın
2. Arama kutusuna **"youtube.readonly"** yazın
3. **"https://www.googleapis.com/auth/youtube.readonly"** seçeneğini bulun ve **checkbox'ını işaretleyin**
4. **"UPDATE"** butonuna tıklayın
5. **"SAVE AND CONTINUE"** butonuna tıklayın

#### Test users (Opsiyonel - Geliştirme için):

Eğer uygulamanız henüz "In production" durumunda değilse:
1. **Test users** bölümüne kendi Google e-posta adresinizi ekleyin
2. **"ADD USERS"** butonuna tıklayın
3. E-posta adresinizi girip **"ADD"** butonuna tıklayın
4. **"SAVE AND CONTINUE"** butonuna tıklayın

**Summary (Özet)** sayfasında bilgileri kontrol edip **"BACK TO DASHBOARD"** butonuna tıklayın.

### Adım 3.2: OAuth 2.0 Client ID Oluşturun

1. Sol menüden **"APIs & Services"** → **"Credentials"** seçin
2. Sayfanın üst kısmında **"+ CREATE CREDENTIALS"** butonuna tıklayın
3. Açılan menüden **"OAuth client ID"** seçeneğini seçin

#### Application type seçimi:

1. **Application type** dropdown menüsünden **"Web application"** seçin

#### Name (İsim):

1. **Name** alanına bir isim verin (örn: "YouTube Filter Web Client")

#### Authorized JavaScript origins (Yetkili JavaScript kaynakları):

Geliştirme için:
- **"+ ADD URI"** butonuna tıklayın
- `http://localhost:5000` yazın
- Enter'a basın

Production için (daha sonra ekleyebilirsiniz):
- `https://yourdomain.com` (domain adresinizi yazın)

#### Authorized redirect URIs (Yetkili yönlendirme URI'leri):

Geliştirme için:
- **"+ ADD URI"** butonuna tıklayın
- `http://localhost:5000/oauth2callback` yazın
- Enter'a basın

Production için (daha sonra ekleyebilirsiniz):
- `https://yourdomain.com/oauth2callback`

> ⚠️ **ÖNEMLİ:** Redirect URI'lerin tam olarak eşleşmesi gerekir. Harf ve noktalama işaretleri önemlidir!

#### Oluşturma:

1. Tüm bilgileri girdikten sonra **"CREATE"** butonuna tıklayın
2. Bir pop-up penceresi açılacak (Client ID ve Client Secret gösterilir)

> ⚠️ **UYARI:** Bu pencereyi kapatmadan önce Client Secret'ı not alın veya JSON dosyasını indirin!

---

## 4. client_secret.json Dosyasını İndirme

### Yöntem 1: Doğrudan İndirme (Önerilen)

1. OAuth Client ID oluşturduktan sonra açılan pop-up penceresinde:
   - **"DOWNLOAD JSON"** butonuna tıklayın
   - Dosya otomatik olarak `client_secret_XXXXX.json` adıyla indirilecek

2. İndirilen dosyayı:
   - Proje klasörünüze taşıyın (`C:\Users\90532\Desktop\YouTube_Filter\`)
   - İsmini `client_secret.json` olarak değiştirin

### Yöntem 2: Manuel Oluşturma

Eğer JSON dosyasını indirmediyseniz:

1. **"APIs & Services"** → **"Credentials"** sayfasına gidin
2. Oluşturduğunuz OAuth 2.0 Client ID'nin sağındaki **download (indirme)** ikonuna tıklayın
3. Dosya indirilecek, ismini `client_secret.json` olarak değiştirin

### Yöntem 3: Manuel JSON Oluşturma

1. **"APIs & Services"** → **"Credentials"** sayfasına gidin
2. OAuth 2.0 Client ID'ye tıklayın
3. **Client ID** ve **Client secret** değerlerini kopyalayın
4. Proje klasörünüzde `client_secret.json` dosyası oluşturun
5. Şu formatta içerik ekleyin:

```json
{
  "web": {
    "client_id": "BURAYA_CLIENT_ID_YAPIŞTIRIN.apps.googleusercontent.com",
    "project_id": "BURAYA_PROJECT_ID_YAPIŞTIRIN",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "BURAYA_CLIENT_SECRET_YAPIŞTIRIN",
    "redirect_uris": [
      "http://localhost:5000/oauth2callback"
    ]
  }
}
```

> 💡 **İpucu:** Project ID'yi bulmak için Google Cloud Console ana sayfasına gidin. Proje seçici menüsünden projenize tıklayın, proje detayları açılır, orada Project ID görünür.

---

## 5. Doğrulama ve Test

### Adım 5.1: Dosya Kontrolü

Proje klasörünüzde şu dosyanın olduğundan emin olun:
- ✅ `client_secret.json`

### Adım 5.2: Dosya Konumu Kontrolü

`client_secret.json` dosyası şu konumda olmalı:
```
C:\Users\90532\Desktop\YouTube_Filter\client_secret.json
```

### Adım 5.3: Uygulamayı Test Edin

1. Terminal/PowerShell'de proje klasörüne gidin:
   ```bash
   cd C:\Users\90532\Desktop\YouTube_Filter
   ```

2. Uygulamayı çalıştırın:
   ```bash
   python run.py
   ```

3. Tarayıcıda `http://localhost:5000` adresine gidin
4. **"YouTube ile Giriş Yap"** butonuna tıklayın
5. Google hesabınızla giriş yapın
6. İzinleri onaylayın

> ✅ **Başarılı!** Eğer beğenilen videolarınız görünüyorsa, kurulum başarılıdır!

---

## 🐛 Sorun Giderme

### Sorun 1: "redirect_uri_mismatch" Hatası

**Çözüm:**
1. Google Cloud Console → Credentials → OAuth 2.0 Client ID'nize gidin
2. Authorized redirect URIs kısmında `http://localhost:5000/oauth2callback` olduğundan emin olun
3. Tam olarak aynı olmalı (büyük/küçük harf, slash, port numarası)

### Sorun 2: "client_secret.json bulunamadı" Hatası

**Çözüm:**
1. Dosyanın proje klasöründe olduğundan emin olun
2. Dosya isminin tam olarak `client_secret.json` olduğundan emin olun
3. `.env` dosyasında `CLIENT_SECRETS_FILE=client_secret.json` olduğundan emin olun

### Sorun 3: "API not enabled" Hatası

**Çözüm:**
1. Google Cloud Console → APIs & Services → Library
2. YouTube Data API v3'ün "ENABLED" durumunda olduğundan emin olun
3. Değilse, "ENABLE" butonuna tıklayın

### Sorun 4: "Insufficient permissions" Hatası

**Çözüm:**
1. OAuth Consent Screen'de scopes (izinler) bölümüne gidin
2. `https://www.googleapis.com/auth/youtube.readonly` scope'unun eklendiğinden emin olun

### Sorun 5: "Quota exceeded" Hatası

**Çözüm:**
1. YouTube Data API v3'ün günlük kotası dolmuş olabilir (10,000 birim)
2. Bir sonraki gün bekleyin veya Google Cloud Console'dan quota artırımı talep edin

---

## 📸 Görsel Yardım

Eğer adımlarda takıldıysanız, Google'ın resmi dokümantasyonuna bakabilirsiniz:
- YouTube Data API: https://developers.google.com/youtube/v3/getting-started
- OAuth 2.0: https://developers.google.com/identity/protocols/oauth2

---

## ✅ Kontrol Listesi

Kurulumu tamamladıktan sonra şunları kontrol edin:

- [ ] Google Cloud Console'da proje oluşturuldu
- [ ] YouTube Data API v3 etkinleştirildi
- [ ] OAuth Consent Screen yapılandırıldı
- [ ] OAuth 2.0 Client ID oluşturuldu
- [ ] `client_secret.json` dosyası proje klasöründe
- [ ] Redirect URI: `http://localhost:5000/oauth2callback`
- [ ] Uygulama başarıyla çalışıyor
- [ ] YouTube girişi çalışıyor
- [ ] Videolar görüntüleniyor

---

**🎉 Tebrikler!** Artık uygulamanızı kullanmaya hazırsınız!

