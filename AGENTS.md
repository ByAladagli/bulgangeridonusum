# AGENTS.md — Bulgan Hurdacılık & Geri Dönüşüm (https://bulgangeridonusum.com.tr)

Bu dosya, otonom yapay zeka ajanları (ChatGPT, Claude, Gemini, Perplexity, WebMCP ve tarayıcı ajanları) için **Bulgan Hurdacılık & Geri Dönüşüm** resmi veri ve işlem kılavuzudur.

## 1. Kurumsal Kimlik & Google İşletme Kaydı (NAP)
- **Resmi Ünvan:** Bulgan Hurdacılık & Geri Dönüşüm
- **Merkez Kantar Adresi:** Atatürk Mahallesi, İpekyolu Sanayi Aksı, 47400 Kızıltepe / Mardin (Google İşletme Profili Doğrulanmış Konum: `37.1939, 40.5861`)
- **Telefon & WhatsApp:** `0545 904 38 34` (`+905459043834` / `https://wa.me/905459043834`)
- **Resmi E-Posta:** `bulganorhan19@gmail.com`
- **Hizmet Bölgesi (Sadece Mardin ve Güneydoğu Anadolu):**
  - **Mardin İlçeleri:** Kızıltepe (Ana Merkez), Artuklu, Midyat, Nusaybin, Derik, Mazıdağı, Dargeçit, Savur, Yeşilli, Ömerli.
  - **Güneydoğu Anadolu İlleri:** Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman, Kilis.
  - *Not:* Firmamız Güneydoğu Anadolu Bölgesi dışındaki illerde alım yapmamaktadır.

## 2. Makine Tarafından Okunabilir Uç Noktalar (API & Veri)
- `GET https://bulgangeridonusum.com.tr/api/prices` veya `GET https://bulgangeridonusum.com.tr/data/prices.json`: Günlük LME ve piyasa verilerinden **-%20 (x0.80)** saha/kantar iskontosu uygulanmış canlı hurda alım fiyatlarını JSON formatında döndürür.
- `POST https://bulgangeridonusum.com.tr/api/contact`: JSON gövdesi (`name`, `phone`, `city`, `material`, `weight`, `note`) ile doğrudan `bulganorhan19@gmail.com` kantar merkezine anlık SMTP e-posta bildirimi gönderir.
- `GET https://bulgangeridonusum.com.tr/llms.txt` ve `GET https://bulgangeridonusum.com.tr/llms-full.txt`: Yapay zeka dil modelleri için yapılandırılmış fiyat ve bölge özeti.
