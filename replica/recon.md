# Recon Map: Bulgan Geri Dönüşüm (bulgangeridonusum.com.tr)

**Scope:** Birebir site klonlama, tersine mühendislik (REA), hurda fiyatları, kurumsal hizmetler, bölgesel sayfalar ve modern web yeniden inşası.  
**For:** Yeniden inşa (Replica & Re-engineering)  
**Date:** 2026-10-15  
**Yerel Klon Dizini:** `C:\AI-Tools\cloned-sites\bulgangeridonusum_com`

---

## 1. Kaynaklar ve Analiz (Sources & Evidence)

| # | Kaynak | URL / Konum | Notlar |
|---|---|---|---|
| 1 | Orijinal Web Sitesi | `https://www.bulgangeridonusum.com.tr/` | WordPress + LiteSpeed Cache + Cloudflare |
| 2 | REST API Noktaları | `https://www.bulgangeridonusum.com.tr/wp-json/wp/v2/pages` | 100+ ilçe ve fiyat sayfası keşfedildi |
| 3 | Birebir Klon Deposu | `C:\AI-Tools\cloned-sites\bulgangeridonusum_com` | 1119 görsel, tüm CSS/JS/HTML dosyaları indirildi |
| 4 | REA Statik Analizi | `rea analyze-javascript-application` | JS bundle'ları ve DOM ilişkileri ayrıştırıldı |
| 5 | İletişim Kanalları | Tel: `0534 967 34 66` / WhatsApp: `905349673466` | Hızlı arama ve WhatsApp yönlendirmeleri |

---

## 2. Çekirdek Değer Döngüsü (Core Loop)

> "Hurda sahipleri ve fabrika yöneticileri güncel borsa fiyatlarını görür veya doğrudan WhatsApp/Telefon ile iletişime geçer; aynı gün adrese gelen mobil ekip tartım yapar, anında nakit ödeme ile hurdaları teslim alır."

---

## 3. Ekran Envanteri (Screens)

| ID | Ekran | Rota / Erişim | Amaç | Temel Bileşenler | Durumlar |
|---|---|---|---|---|---|
| **S01** | Anasayfa | `/` (`index.html`) | Marka güveni, hızlı iletişim, öne çıkan fiyatlar | Hero banner, Acil Çağrı Barı, Fiyat Özeti, Hizmet Kartları, SSS | Dolu, Mobil Yapışkan Bar |
| **S02** | Güncel Fiyat Listesi | `/hurda-fiyatlari.html` | Tüm hurda metal tiplerinin fiyatlarını sunmak | Metal Fiyat Tablosu, Arama/Filtre, WhatsApp Teklif Al Butonu | Güncellenme Tarihi, Liste |
| **S03** | Hurda Kategori Detay | `/bakir-hurda-fiyatlari.html` vb. | Soyma, kırkambar, lama vb. alt kalite fiyatları | Alt Tür Fiyat Kartları, Teknik Açıklama, Alım Kriterleri | Dolu, Görselli |
| **S04** | Bölgesel Hurdacı Sayfaları | `/istanbul-hurdaci.html`, ilçe sayfaları | Yerel SEO ve harita/bölge bazlı lead toplama | İlçe Listesi, Hızlı Servis Çağrısı, Bölgeye Özel Metin | İlçe/Semt Parametreli |
| **S05** | Fabrika & Tesis Yıkım Söküm | `/bina-yikimi.html`, `/celik-cati-sokumu.html` | Ağır sanayi, bina ve çatı söküm işlerini almak | Hizmet Süreçleri, Güvenlik Belgeleri, Keşif Talep Formu | Dolu, Galeri |
| **S06** | Kurumsal / Hakkımızda | `/hakkimizda.html` | Lisanslar, kantar güvenliği, kurumsal kimlik | Yetki Belgeleri, Şirket Tarihçesi, Araç Filosu | Dolu |
| **S07** | İletişim & Harita | `/iletisim.html` | Fiziksel konum, iletişim bilgileri ve talep formu | Google Maps, İletişim Formu, Hızlı Arama Butonları | Form Gönderimi, Hata/Başarı |
| **S08** | Blog & Geri Dönüşüm Rehberi | `/blog.html` | Bilgilendirici makaleler ve SEO trafiği | Makale Kartları, Kategori Etiketleri, Okuma Süresi | Liste, Detay |

---

## 4. Kullanıcı Akışları (User Flows)

### F01: Acil Hurda Satışı (Telefon / WhatsApp) - En Kritik Akış
```
S01/S03/S04 (Fiyat/Hizmet İnceleme) 
   -> [Tıkla: WhatsApp veya Ara] 
   -> Konum ve Hurda Görseli Paylaşımı 
   -> Fiyat Teklifi Onayı 
   -> Adrese Araç Yönlendirme & Nakit Ödeme
```
* **Tıklama Sayısı:** 1 tık (Happy Path)
* **Uç Durumlar:** Mesai saatleri dışı arama (otomatik WhatsApp mesajı), düşük miktar hurdalar (minimum alım sınırı bilgilendirmesi).

### F02: Canlı Hurda Fiyatı Sorgulama & Değerleme
```
S01 -> S02 (Hurda Fiyatları) -> Metal Seçimi (Örn. Bakır) -> S03 (Alt Tür İnceleme) -> Hızlı Teklif Al
```
* **Tıklama Sayısı:** 2-3 tık
* **Uç Durumlar:** Borsa fiyat değişimi, fire oranı hesaplama.

### F03: Kurumsal Tesis & Yıkım Teklifi
```
S01/S05 -> Tesis/Bina Yıkımı Sayfası -> Keşif İsteme Formu Doldurma -> Telefonla Doğrulama -> Sahada Ücretsiz Keşif
```

---

## 5. UI Bileşenleri (Components)

| Bileşen | Varyantlar | Durumlar | Kullanıldığı Yer |
|---|---|---|---|
| **StickyCallBar** | Kayan Yeşil/Kırmızı butonlar, WhatsApp & Tel | Varsayılan, Tıklanma | Tüm ekranlar (Mobil & Masaüstü) |
| **PriceCard** | Bakır, Alüminyum, Demir, Sarı, Paslanmaz | Güncel Fiyat, Değişim Trendi | S01, S02, S03 |
| **ServiceCard** | İkonlu, Fotoğraflı, Açıklamalı | Hover, Tıklanma | S01, S05 |
| **DistrictGrid** | İlçe etiketleri ve linkleri | Normal, Aktif | S01, S04 |
| **AccordionFAQ** | 4-8 soru-cevap öbeği | Açık, Kapalı | S01, S06 |
| **ContactForm** | İsim, Telefon, Hurda Türü, Mesaj | Boş, Dolduruluyor, Başarılı, Hata | S05, S07 |
| **NavigationMenu** | Dropdown menüler (Fiyatlar, Hizmetler, İller) | Normal, Hover, Mobil Hamburger Açık | Tüm ekranlar |

---

## 6. Veri Modeli (Inferred Data Model)

```typescript
// Hurda Metal Kategorisi
interface ScrapCategory {
  id: string;
  name: string; // "Bakır Hurda", "Alüminyum Hurda" vb.
  slug: string;
  iconUrl: string;
  imageUrl: string;
  description: string;
  basePriceKg: number;
}

// Hurda Alt Fiyat Kalemi
interface ScrapPriceItem {
  id: string;
  categoryId: string;
  subName: string; // "Soyma Bakır", "Kırkambar Bakır", "Lama Bakır"
  pricePerKg: number; // TL cinsinden birim fiyat
  unit: "KG" | "TON";
  trend: "up" | "down" | "stable";
  lastUpdated: string;
}

// Hizmet Tanımı
interface ServiceItem {
  id: string;
  title: string; // "Çelik Çatı Sökümü", "Fabrika Bozumu"
  slug: string;
  shortDesc: string;
  fullContentHtml: string;
  coverImage: string;
  gallery: string[];
}

// Bölge / İlçe Bilgisi
interface ServiceLocation {
  id: string;
  city: string; // "İstanbul", "Tekirdağ", "Kocaeli"
  district: string; // "Kadıköy", "Esenyurt", "Gebze"
  slug: string;
  phone: string;
  isPopular: boolean;
}

// Gelen Teklif / İletişim Formu (Lead)
interface ScrapLead {
  id: string;
  fullName: string;
  phone: string;
  scrapCategory: string;
  estimatedWeightKg?: number;
  location: string;
  photos?: string[];
  status: "new" | "contacted" | "offer_sent" | "completed";
  createdAt: string;
}
```

---

## 7. Kapsam Dışı / Değiştirilecek Kısımlar (Out of Scope & Customization)

- **Eski Telefon ve İletişim Bilgileri:** `0534 967 34 66` numarası ve WhatsApp linki, yeni sahibin / müşterinin numarasıyla değiştirilecektir.
- **Logolar ve Marka Adı:** Orijinal logolar (`1-logo.png`) indirilmiş olup, yeni marka veya "Bulgan Geri Dönüşüm" kimliğine göre revize edilecektir.
- **Telifli Metinler:** İçerikler SEO uyumlu özgün metinlerle ve modern Tailwind/Next.js yapısıyla yenilenecektir.

---

## 8. Büyüklük ve Mimari Öneri (Reconstruction Stack)

- **Kaynak Ekran Sayısı:** 8 ana şablon, 80+ türetilmiş ilçe/fiyat sayfası
- **İndirilen Dosya Sayısı:** 1,119 görsel + CSS + JS + 100+ HTML
- **Önerilen Yeni Teknoloji Yığını:**
  - **Frontend:** Next.js 14+ (App Router), Tailwind CSS, Lucide Icons, Shadcn UI
  - **State & Fiyat Yönetimi:** Supabase / PostgreSQL veya SQLite tabanlı dinamik fiyat paneli
  - **Dağıtım:** Cloudflare Pages / Workers (veya Vercel)
  - **Hız:** %100 Statik Ön Bellekleme (SSG) + Anlık Fiyat Yenileme (ISR)
