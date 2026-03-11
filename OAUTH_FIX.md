# OAuth "Erişim Engellendi" Hatası Çözümü

## 🔴 Hata Mesajı:

```
Erişim engellendi: LikedTube, Google doğrulama sürecini tamamlamadı
```

Bu hata, OAuth Consent Screen'in "Testing" modunda olduğu ve kullanıcının test listesinde olmadığı anlamına gelir.

---

## ✅ Çözüm 1: Test Kullanıcısı Ekleme (ÖNERİLEN - Hızlı)

### Adım 1: Google Cloud Console'a Gidin

1. https://console.cloud.google.com/ adresine gidin
2. Projenizi seçin

### Adım 2: OAuth Consent Screen'e Gidin

1. Sol menüden **"APIs & Services"** → **"OAuth consent screen"** seçin

### Adım 3: Test Users Bölümünü Bulun

1. Sayfayı aşağı kaydırın
2. **"Test users"** bölümünü bulun
3. **"+ ADD USERS"** butonuna tıklayın

### Adım 4: Email'inizi Ekleyin

1. Açılan pencerede **"Add test users"** kısmına gidin
2. **"USER EMAIL OR NAME"** kutusuna **kendi Google email adresinizi** yazın
   - YouTube'a giriş yapmak için kullandığınız email adresi
3. **"ADD"** butonuna tıklayın
4. Email adresiniz listeye eklenecek

### Adım 5: Kaydedin

1. Sayfanın alt kısmındaki **"SAVE AND CONTINUE"** butonuna tıklayın
2. Son sayfada **"BACK TO DASHBOARD"** butonuna tıklayın

### Adım 6: Test Edin

1. Tarayıcınızda uygulamanıza geri dönün: `http://localhost:5000`
2. **"YouTube ile Giriş Yap"** butonuna tekrar tıklayın
3. Bu sefer giriş yapabilmelisiniz!

> ✅ **NOT:** Eğer hala çalışmıyorsa, birkaç dakika bekleyin (Google'ın sistemlerinin güncellenmesi gerekebilir)

---

## ✅ Çözüm 2: Uygulamayı Production Moduna Alma (Uzun Vadeli)

Eğer uygulamayı herkesin kullanmasını istiyorsanız:

### Adım 1: OAuth Consent Screen'e Gidin

1. Google Cloud Console → **"APIs & Services"** → **"OAuth consent screen"**

### Adım 2: Publishing Status'u Kontrol Edin

1. Sayfanın üst kısmında **"Publishing status"** görünecek
2. Şu anda **"Testing"** olmalı

### Adım 3: Production'a Alın

1. **"PUBLISH APP"** butonuna tıklayın
2. Uyarı mesajını okuyun ve onaylayın
3. Uygulamanız artık herkes tarafından kullanılabilir

> ⚠️ **DİKKAT:** Production modunda, Google uygulamanızı inceleyebilir ve gerekirse geri çekebilir. Küçük testler için Çözüm 1 daha uygundur.

---

## 🔍 Hala Çalışmıyor mu?

### Kontrol Listesi:

- [ ] Email adresiniz test users listesinde mi?
- [ ] Email adresini doğru yazdınız mı? (büyük/küçük harf önemli değil)
- [ ] "SAVE" butonuna tıkladınız mı?
- [ ] 2-3 dakika beklediniz mi? (Google'ın güncellenmesi gerekebilir)
- [ ] Tarayıcı cache'ini temizlediniz mi? (Ctrl+F5)
- [ ] Gizli sekme/başka tarayıcıda denediniz mi?

### Hala Sorun Varsa:

1. **Browser Console'u kontrol edin:**

   - Tarayıcıda F12 tuşuna basın
   - "Console" sekmesine gidin
   - Hataları kontrol edin

2. **OAuth Consent Screen ayarlarını kontrol edin:**

   - Scopes (İzinler) bölümünde `youtube.readonly` var mı?
   - App domain'ler doğru mu?

3. **Credentials'ı kontrol edin:**
   - Authorized redirect URIs: `http://localhost:5000/oauth2callback` var mı?
   - Tam olarak aynı olmalı (büyük/küçük harf, slash, port)

---

## 📝 Hızlı Kontrol:

Eğer hızlıca test etmek istiyorsanız:

1. Google Cloud Console → OAuth consent screen
2. Test users → + ADD USERS
3. Email'inizi ekleyin
4. SAVE
5. Uygulamada tekrar dene

Bu işlem genellikle 1-2 dakika içinde çalışır!
