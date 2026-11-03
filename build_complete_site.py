import json
import os
import glob

ROOT = r"C:\AI-Tools\cloned-sites\bulgangeridonusum"
PRICES_PATH = os.path.join(ROOT, "data", "prices.json")

with open(PRICES_PATH, "r", encoding="utf-8") as f:
    PRICES_DATA = json.load(f)

CATEGORIES = PRICES_DATA["categories"]
UPDATED_AT = PRICES_DATA["updatedAt"]
USD_TRY = PRICES_DATA["exchange"]["USD_TRY"]
EUR_TRY = PRICES_DATA["exchange"]["EUR_TRY"]

MARDIN_DISTRICTS = [
    ("mardin-hurdaci.html", "Mardin", "37.3129", "40.7339", "Mardin Merkez (Artuklu), Kızıltepe, Midyat, Nusaybin ve tüm ilçelerde 30 dakikada adresten hassas dijital tartım ve anında nakit hurda alımı.", ["Artuklu & Yenişehir", "Kızıltepe & Sanayi Sitesi", "Midyat & Estel", "Nusaybin & İpekyolu", "Derik & Mazıdağı", "Dargeçit, Savur, Yeşilli, Ömerli"]),
    ("kiziltepe-hurdaci.html", "Kızıltepe", "37.1936", "40.5858", "Ana merkezimiz Kızıltepe Atatürk Mahallesi'ndedir. Kızıltepe Küçük Sanayi Sitesi, Hububat Ticaret Merkezi, İpekyolu ve tüm mahallelerden en yüksek fiyata nakit hurda alımı.", ["Atatürk Mahallesi (Merkezimiz)", "Kızıltepe Sanayi Sitesi", "Cumhuriyet & Tepebaşı Mah.", "Yeni Mahalle & İpekyolu", "Ersoylu & Aşiti Mah.", "Kızıltepe Tüm Çevre Köyleri"]),
    ("artuklu-hurdaci.html", "Artuklu", "37.3212", "40.7245", "Mardin Merkez Artuklu, Yenişehir, 13 Mart Mahallesi, Mardin OSB ve Kabala bölgesinde şantiye, kurum ve işletmelerden yerinde nakit hurda alımı.", ["Yenişehir & 13 Mart Mah.", "Mardin Organize Sanayi Bölgesi (OSB)", "Ravza & Vali Ozan Cad.", "Nur & Yalım Mahallesi", "Kabala & Ortaköy", "Artuklu Şantiye & Kurumlar"]),
    ("midyat-hurdaci.html", "Midyat", "37.4187", "41.3387", "Midyat ve Estel bölgesinde inşaat şantiyeleri, taş ve mermer tesisleri, atölyeler ve konutlardan bakır, demir, kablo ve alüminyum hurda alımı.", ["Estel & Cumhuriyet Mah.", "Midyat Sanayi Sitesi", "Bahçelievler & Gölcük", "Bağlar & Akçakaya", "Uluköy & Ortaçarşı", "Midyat Tüm Çevre Köyleri"]),
    ("nusaybin-hurdaci.html", "Nusaybin", "37.0758", "41.2164", "Nusaybin ve uluslararası İpekyolu ticaret hattında fabrika, tır garajları, şantiye ve depolardan tonajlı demir, bakır, kablo ve sarı hurda alımı.", ["İpekyolu Sanayi & Lojistik Hattı", "Yenişehir & Barış Mah.", "8 Mart & Selahaddin Eyyubi", "Dicle & Fırat Mah.", "Abdulkadir Paşa & Kışla", "Girmeli, Akarsu & Çevre Köyler"]),
    ("derik-hurdaci.html", "Derik", "37.3653", "40.2689", "Derik genelinde tarımsal sulama tesisleri, dalgıç pompa kabloları, zeytin ve mısır kurutma tesislerinden her nevi metal hurda alımı.", ["Derik Merkez & Kale Mah.", "Dalgıç Pompa & GES Sahaları", "Üçyol & Kızıltepe Yolu Hattı", "Cevizpınar & Zeytinpınar", "Tepebağ & Bahçelievler", "Derik Tüm Ova Köyleri"]),
    ("mazidagi-hurdaci.html", "Mazıdağı", "37.4792", "40.4864", "Mazıdağı maden, gübre ve sanayi tesisleri çevresinde ağır demir, çelik konstrüksiyon, yüksek kesitli enerji kablosu ve krom hurda alımı.", ["Mazıdağı Sanayi & Maden Hattı", "Poyraz & Gündoğan Mah.", "Kayalar & Ulutaş", "Şanlı & Evciler", "Kocakent & Yücebağ", "Mazıdağı Şantiye Bölgeleri"]),
    ("dargecit-hurdaci.html", "Dargeçit", "37.5458", "41.7169", "Dargeçit ve Ilısu Barajı havzasında şantiye, enerji tesisi, atölye ve inşaatlardan bakır, demir, kablo ve alüminyum hurdası alımı.", ["Dargeçit Merkez & Bahçebaşı", "Ilısu & Baraj Şantiye Hattı", "Tepebaşı & Safa Mah.", "Sümer & Kılavuz", "Bostanlı & Çatalçam", "Dargeçit Çevre Bölgeler"]),
    ("savur-hurdaci.html", "Savur", "37.5378", "40.8886", "Savur ilçesi ve mahallelerinde tarımsal ekipman, inşaat demiri, bakır kazan ve kablo hurdalarının yerinde tartımla nakit alımı.", ["Savur Merkez & Safa Mah.", "Pınardere & Yeşilalan", "Sürgücü & İçören", "Kaplan & Başkavak", "Savur Şantiye & Atölyeler", "Savur Tüm Çevre Köyler"]),
    ("yesilli-hurdaci.html", "Yeşilli", "37.3361", "40.8181", "Yeşilli ilçesinde kentsel dönüşüm, bina yıkım söküm, demir, bakır, alüminyum ve kablo hurdalarınız için aynı gün mobil kantarlı araç hizmeti.", ["Yeşilli Merkez & Tepebaşı", "Gül & Bahçebaşı Mah.", "Kentsel Dönüşüm Sahaları", "Zeytinli & Dereyanı", "Ovaköy & Bülbül", "Yeşilli Çevre Noktalar"]),
    ("omerli-hurdaci.html", "Ömerli", "37.4036", "40.9542", "Ömerli ve Midyat-Mardin karayolu hattındaki tüm işletme, şantiye ve bağ evlerinden çıkan metal hurdaların değerinde nakit alımı.", ["Ömerli Merkez & Yeni Mah.", "Cumhuriyet & Şafak Mah.", "Midyat Yolu Sanayi Noktaları", "Kayadere & Çınaraltı", "Beşikkaya & Işıkdere", "Ömerli Tüm Köyler"])
]

GUNEYDOGU_PROVINCES = [
    ("diyarbakir-hurdaci.html", "Diyarbakır", "TR-21", "37.9144", "40.2306", "Diyarbakır Organize Sanayi Bölgesi (OSB), Bağlar, Kayapınar, Yenişehir, Sur, Bismil ve Ergani genelinde tonajlı fabrika, şantiye ve metal hurda alımı.", ["Diyarbakır OSB & KSS Sanayi", "Kayapınar & Bağlar", "Yenişehir & Sur", "Bismil & Çınar Hattı", "Ergani & Silvan", "Diyarbakır Tüm Şantiyeler"]),
    ("sanliurfa-hurdaci.html", "Şanlıurfa", "TR-63", "37.1674", "38.7955", "Şanlıurfa OSB, Evren Sanayi Sitesi, Viranşehir, Siverek, Karaköprü, Eyyübiye ve Haliliye genelinde pamuk/çırçır fabrikaları, GES sahaları ve şantiye hurda alımı.", ["Şanlıurfa 1. ve 2. OSB", "Evren Sanayi Sitesi", "Viranşehir & Ceylanpınar", "Siverek & Hilvan", "Haliliye, Eyyübiye, Karaköprü", "Birecik, Suruç & Akçakale"]),
    ("gaziantep-hurdaci.html", "Gaziantep", "TR-27", "37.0662", "37.3833", "Gaziantep Başpınar OSB, KÜSGET, Şehitkamil, Şahinbey ve Nizip genelinde tekstil, gıda ve makine fabrikalarından tonajlı imalat artığı metal, bakır, krom ve kablo alımı.", ["Başpınar 1-5. Organize Sanayi", "KÜSGET & BÜSEM Sanayi", "Şehitkamil & Şahinbey", "Nizip & İslahiye OSB", "Oğuzeli & Nurdağı", "Gaziantep Fabrika Bozumu"]),
    ("batman-hurdaci.html", "Batman", "TR-72", "37.8812", "41.1351", "Batman OSB, petrol sahası ekipmanları, rafineri ve şantiye bölgelerinden ağır demir, çelik boru, bakır, sarı pirinç ve kablo hurdası alımı.", ["Batman Organize Sanayi Bölgesi", "Batman Merkez & Yenişehir", "Kozluk & Beşiri", "Sason & Gercüş", "Hasankeyf Hattı", "Enerji & Rafineri Şantiyeleri"]),
    ("sirnak-hurdaci.html", "Şırnak", "TR-73", "37.5164", "42.4611", "Şırnak, Cizre, Silopi ve İdil hattında uluslararası lojistik depoları, maden sahaları ve inşaat şantiyelerinden tonajlı hurda demir, bakır ve kablo alımı.", ["Cizre OSB & Sanayi Sitesi", "Silopi & Habur Lojistik Hattı", "İdil & İpekyolu", "Şırnak Merkez & Kasrik", "Uludere & Beytüşşebap", "Maden & Enerji Şantiyeleri"]),
    ("siirt-hurdaci.html", "Siirt", "TR-56", "37.9333", "41.9500", "Siirt Merkez, Kurtalan, Baykan ve Şirvan maden/baraj şantiyelerinden bakır, enerji kablosu, demir, alüminyum ve krom hurda alımı.", ["Siirt Merkez & OSB", "Kurtalan Sanayi & Gar", "Şirvan Maden Sahaları", "Baykan & Veyselkarani", "Eruh & Pervari", "Baraj & HES Şantiyeleri"]),
    ("adiyaman-hurdaci.html", "Adıyaman", "TR-02", "37.7648", "38.2786", "Adıyaman OSB, Kahta, Besni ve Gölbaşı genelinde bina yıkım söküm, tekstil ve gıda fabrikası hurdaları, demir, bakır ve alüminyum alımı.", ["Adıyaman OSB & Küçük Sanayi", "Kahta & OSB", "Besni & Gölbaşı", "Kentsel Dönüşüm & Yıkım Sahaları", "Çelikhan & Samsat", "Adıyaman Şantiye Alımları"]),
    ("kilis-hurdaci.html", "Kilis", "TR-79", "36.7184", "37.1212", "Kilis Organize Sanayi Bölgesi, Polateli OSB ve sınır ticaret depolarından her nevi metal, bakır, kablo, demir ve alüminyum hurda alımı.", ["Kilis OSB & Sanayi Sitesi", "Polateli Şahinbey OSB", "Kilis Merkez", "Elbeyli & Musabeyli", "Tarımsal & Zeytinyağı Tesisleri", "Kilis Şantiye Hurdaları"])
]

EXTRA_SERVICE_PAGES = [
    ("karton-hurda-fiyatlari.html", "Karton & Oluklu Mukavva Hurda Fiyatları", "kagit", "images/karton-hurda-1.webp", "images/karton-hurda-1.jpg", "Mardin ve Güneydoğu Anadolu genelinde zincir marketler, ambalaj fabrikaları, tekstil tesisleri ve depolardan preslenmiş veya dökme koli karton hurdası alımı yapıyoruz."),
    ("sokulecek-hurda-fiyatlari.html", "Sökülecek Fabrika, Makine & Tesis Hurdası Fiyatları", "demir", "images/sokulecek-hurda-1.webp", "images/sokulecek-hurda-1.jpg", "Kullanım ömrünü tamamlamış fabrika üretim hatları, kazan daireleri, trafo merkezleri, çelik konstrüksiyon yapılar ve ağır sanayi makinelerini uzman oksijen kesim ekibimizle sökerek yüksek fiyattan nakit satın alıyoruz."),
    ("hurda-chiller-grubu-sogutma-sistemleri-fiyatlari-alimi.html", "Hurda Chiller Grubu & Sanayi Soğutma Sistemleri Alımı", "klima", "images/hurda-chiller-sogutma-grubu-1.webp", "images/hurda-chiller-sogutma-grubu-1.jpg", "AVM, hastane, otel ve endüstriyel fabrikaların kullanım dışı kalan su soğutmalı/hava soğutmalı chiller gruplarını, kondanser ve eşanjör ünitelerini yerinde sökerek bakır ve kompresör değerinde nakit alıyoruz."),
    ("hurda-raf-fiyatlari.html", "Hurda Depo Rafı & Market Raf Sistemleri Alımı", "demir", "images/hurda-raf-1.webp", "images/hurda-raf-1.jpg", "Lojistik depoları, fabrikalar, arşiv odaları ve marketlerden çıkan ağır yük rafları, çelik arşiv rafları ve tel reyon sistemlerini söküm dahil peşin ödemeyle satın alıyoruz."),
    ("2-el-endustriyel-mutfak-malzemeleri-alimi.html", "Paslanmaz Krom Sanayi & Endüstriyel Mutfak Ekipmanları Hurdası", "paslanmaz", "images/endustriyel-mutfak.webp", "images/endustriyel-mutfak.jpg", "Otel, yemekhane, restoran ve gıda fabrikalarından çıkan 304 ve 316 kalite paslanmaz krom tezgah, kazan, davlumbaz, fırın ve soğuk hava deposu ünitelerini yüksek krom fiyatıyla alıyoruz."),
    ("bina-yikimi.html", "Mardin & Güneydoğu Fabrika, Tesis ve Bina Yıkım Söküm Hizmeti", "demir", "images/sokulecek-hurda-1.webp", "images/sokulecek-hurda-1.jpg", "Bulgan Hurdacılık olarak Mardin, Kızıltepe, Diyarbakır, Şanlıurfa, Gaziantep ve Batman genelinde iş güvenliği yönetmeliklerine tam uyumlu, hurda karşılığı veya anahtar teslim fabrika, antrepo ve bina yıkım-söküm hizmeti sunuyoruz."),
    ("celik-cati-sokumu.html", "Çelik Çatı, Hangar & Konstrüksiyon Sökümü", "demir", "images/demir-hurda-1.webp", "images/demir-hurda-1.jpg", "Organize sanayi bölgelerindeki fabrika çatıları, çelik hangarlar, sandviç panel sistemleri ve uzay çatı konstrüksiyonlarını vinçli ve sertifikalı kesim ekiplerimizle güvenle söküyor, çıkan malzemeyi değerinde alıyoruz."),
    ("evrak-imhasi.html", "Kurumsal Arşiv & Güvenli Evrak İmha Hizmeti", "kagit", "images/kagit-hurda-1.webp", "images/kagit-hurda-1.jpg", "Resmi kurumlar, bankalar, hastaneler, okullar ve şirketlerin saklama süresi dolmuş arşiv belgelerini KVKK standartlarına uygun şekilde tutanakla teslim alarak geri dönüşüme kazandırıyoruz.")
]

BLOG_POSTS = [
    ("hurda-kablo-fiyati-2026-guncel-kablo-hurda-cesitleri-ve-kilosu-ne-kadar.html", "2026 Güncel Hurda Kablo Fiyatları: Bakır Oranı ve Kilosu Nasıl Hesaplanır?", "images/kablo-hurda-1.webp", "Enerji kabloları, TTR, antigron, yeraltı çelik zırhlı kablolar ve dalgıç pompa kablolarında bakır randımanı nasıl ölçülür? Mardin ve Güneydoğu Anadolu şantiyeleri için güncel rehber."),
    ("geri-donusum-nedir-geri-donusumun-faydalari-nelerdir-ve-kisaca-onemi-nedir.html", "Endüstriyel Metal Geri Dönüşümü Nedir? Ekonomiye ve Sanayiye Katkıları", "images/bakir-hurda-1.webp", "Bakır, alüminyum, demir-çelik ve paslanmaz krom geri dönüşümünün enerji tasarrufu, hammadde arz güvenliği ve Güneydoğu Anadolu sanayisi açısından kritik önemi."),
    ("geri-donusum-proje-ornekleri-ve-fikirleri-nelerdir.html", "Fabrika ve Şantiyelerde Sıfır Atık & Hurda Yönetimi Nasıl Yapılır?", "images/aluminyum-hurda-1.webp", "Üretim tesislerinde metal talaşların, kablo firelerinin ve sac kırpıntılarının türlerine göre ayrıştırılarak en yüksek ekonomik değerle nakde çevrilmesi."),
    ("geri-donusum-sloganlari-nelerdir-geri-donusum-ile-ilgili-sozler.html", "Hurda Satarken Dikkat Edilmesi Gereken 7 Altın Kural (Hassas Tartım & Borsa Takibi)", "images/sari-hurda-1.webp", "Mardin ve Güneydoğu Anadolu'da hurda bakır, demir, sarı ve alüminyum satarken kantar doğruluğu, alaşım kalitesi ve günlük LME fiyat takibi nasıl yapılmalı?")
]


def fmt_tl(val):
    s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} ₺"


def render_head(title, desc, canonical_slug, geo_region="TR-47", geo_place="Kızıltepe, Mardin", lat="37.1936", lon="40.5858", schema_extra=""):
    canonical = f"https://bulgangeridonusum.com.tr/{canonical_slug}" if canonical_slug else "https://bulgangeridonusum.com.tr/"
    base_schema = {
        "@context": "https://schema.org",
        "@type": ["RecyclingCenter", "LocalBusiness"],
        "@id": "https://bulgangeridonusum.com.tr/#organization",
        "name": "Bulgan Hurdacılık & Geri Dönüşüm",
        "alternateName": "Mardin & Güneydoğu Anadolu Merkez Hurdacı - Bulgan Hurdacılık",
        "url": "https://bulgangeridonusum.com.tr/",
        "logo": "https://bulgangeridonusum.com.tr/images/logo.png",
        "image": "https://bulgangeridonusum.com.tr/images/og-image.jpg",
        "telephone": "+905459043834",
        "email": "bulganorhan19@gmail.com",
        "priceRange": "₺₺₺",
        "currenciesAccepted": "TRY",
        "paymentAccepted": "Nakit, Havale, EFT",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Atatürk Mahallesi",
            "addressLocality": "Kızıltepe",
            "addressRegion": "Mardin",
            "postalCode": "47400",
            "addressCountry": "TR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": float(lat),
            "longitude": float(lon)
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "07:00",
            "closes": "22:00"
        }],
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Mardin"},
            {"@type": "AdministrativeArea", "name": "Kızıltepe"},
            {"@type": "AdministrativeArea", "name": "Artuklu"},
            {"@type": "AdministrativeArea", "name": "Midyat"},
            {"@type": "AdministrativeArea", "name": "Nusaybin"},
            {"@type": "AdministrativeArea", "name": "Diyarbakır"},
            {"@type": "AdministrativeArea", "name": "Şanlıurfa"},
            {"@type": "AdministrativeArea", "name": "Gaziantep"},
            {"@type": "AdministrativeArea", "name": "Batman"},
            {"@type": "AdministrativeArea", "name": "Şırnak"},
            {"@type": "AdministrativeArea", "name": "Siirt"},
            {"@type": "AdministrativeArea", "name": "Adıyaman"},
            {"@type": "AdministrativeArea", "name": "Kilis"}
        ]
    }
    schema_json = json.dumps(base_schema, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="mardin hurdacı, kızıltepe hurdacı, bulgan hurdacılık, bulgan geri dönüşüm, güneydoğu hurdacı, diyarbakır hurdacı, şanlıurfa hurdacı, batman hurdacı, şırnak hurdacı, gaziantep hurdacı, midyat hurdacı, nusaybin hurdacı, güncel hurda fiyatları, bakır hurda fiyatı, demir hurda fiyatı, kablo hurda fiyatı">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">

  <!-- Coğrafi Yerel SEO Etiketleri -->
  <meta name="geo.region" content="{geo_region}">
  <meta name="geo.placename" content="{geo_place}">
  <meta name="geo.position" content="{lat};{lon}">
  <meta name="ICBM" content="{lat}, {lon}">

  <!-- Favicon & PWA İkonları (Madde #5) -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="64x64" href="/images/favicon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#0d1015">

  <!-- Open Graph & WhatsApp Paylaşım Kartı (Madde #8) -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:site_name" content="Bulgan Hurdacılık & Geri Dönüşüm">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://bulgangeridonusum.com.tr/images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Bulgan Hurdacılık - Mardin ve Güneydoğu Anadolu Merkez Hurdacı">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://bulgangeridonusum.com.tr/images/og-image.jpg">

  <!-- Google Fonts: Chakra Petch + Plus Jakarta Sans + JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700;800&family=JetBrains+Mono:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Ana Stil Dosyası -->
  <link rel="stylesheet" href="/css/bulgan-theme.css">

  <!-- Yapısal Veri (Schema.org JSON-LD) -->
  <script type="application/ld+json">{schema_json}</script>
  {schema_extra}
</head>
"""


def render_header(active_slug=""):
    cat_links = "".join(
        f'<a href="/{c["slug"]}"><span>{c["shortName"]}</span><strong>{fmt_tl(c["items"][0]["price"])}</strong></a>'
        for c in CATEGORIES
    )
    mardin_links = "".join(
        f'<a href="/{slug}"><span>{name} Hurdacı</span><span>→</span></a>'
        for slug, name, *_ in MARDIN_DISTRICTS[:8]
    )
    gda_links = "".join(
        f'<a href="/{slug}"><span>{name} Hurdacı</span><span>→</span></a>'
        for slug, name, *_ in GUNEYDOGU_PROVINCES
    )

    return f"""<body>
  <!-- Üst Canlı Borsa & İletişim Çubuğu -->
  <div class="top-ticker">
    <div class="container top-ticker-inner">
      <div class="ticker-left">
        <span class="live-pill"><span class="live-dot"></span> CANLI BORSA ENDEKSİ (-%20 NET ALIM)</span>
        <span class="ticker-meta">Güncelleme: <strong data-updated-at>{UPDATED_AT}</strong> | USD: <strong data-usd-try>{USD_TRY} ₺</strong> | EUR: <strong data-eur-try>{EUR_TRY} ₺</strong></span>
      </div>
      <div class="ticker-right">
        <span>📍 Atatürk Mah. Kızıltepe / MARDİN</span>
        <a href="mailto:bulganorhan19@gmail.com">✉️ bulganorhan19@gmail.com</a>
        <a href="tel:+905459043834" style="color:var(--gold-bright);">📞 0545 904 38 34</a>
      </div>
    </div>
  </div>

  <!-- Ana Navigasyon & Marka Başlığı -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand-logo" aria-label="Bulgan Hurdacılık Ana Sayfa">
        <picture>
          <source srcset="/images/logo-header.webp" type="image/webp">
          <img src="/images/logo-header.png" alt="Bulgan Hurdacılık & Geri Dönüşüm - Mardin ve Güneydoğu Anadolu Hurdacı" width="210" height="70">
        </picture>
      </a>

      <nav class="main-nav" aria-label="Ana Menü">
        <div class="nav-item">
          <a href="/" class="nav-link {'active' if active_slug == 'index.html' else ''}">Ana Sayfa</a>
        </div>
        <div class="nav-item">
          <a href="/hurda-fiyatlari.html" class="nav-link {'active' if 'fiyatlari' in active_slug else ''}">Güncel Hurda Fiyatları ▾</a>
          <div class="dropdown-menu wide-grid">
            {cat_links}
          </div>
        </div>
        <div class="nav-item">
          <a href="/mardin-hurdaci.html" class="nav-link {'active' if 'mardin' in active_slug or 'kiziltepe' in active_slug else ''}">Mardin İlçeleri ▾</a>
          <div class="dropdown-menu">
            {mardin_links}
          </div>
        </div>
        <div class="nav-item">
          <a href="/hurda-alan-yerler.html" class="nav-link">Güneydoğu İlleri ▾</a>
          <div class="dropdown-menu">
            {gda_links}
          </div>
        </div>
        <div class="nav-item">
          <a href="/bina-yikimi.html" class="nav-link">Yıkım & Söküm ▾</a>
          <div class="dropdown-menu">
            <a href="/bina-yikimi.html"><span>Fabrika & Bina Yıkımı</span><span>→</span></a>
            <a href="/celik-cati-sokumu.html"><span>Çelik Çatı & Hangar Sökümü</span><span>→</span></a>
            <a href="/sokulecek-hurda-fiyatlari.html"><span>Tesis & Makine Parkuru Sökümü</span><span>→</span></a>
            <a href="/hurda-chiller-grubu-sogutma-sistemleri-fiyatlari-alimi.html"><span>Chiller & Soğutma Sökümü</span><span>→</span></a>
            <a href="/hurda-raf-fiyatlari.html"><span>Depo & Raf Sistemleri Alımı</span><span>→</span></a>
            <a href="/evrak-imhasi.html"><span>Kurumsal Arşiv & Evrak İmhası</span><span>→</span></a>
          </div>
        </div>
        <div class="nav-item">
          <a href="/hakkimizda.html" class="nav-link {'active' if active_slug == 'hakkimizda.html' else ''}">Kurumsal</a>
        </div>
        <div class="nav-item">
          <a href="/iletisim.html" class="nav-link {'active' if active_slug == 'iletisim.html' else ''}">İletişim</a>
        </div>
      </nav>

      <div class="header-cta">
        <a href="https://wa.me/905459043834?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20hurda%20fiyat%C4%B1%20almak%20istiyorum." target="_blank" rel="noopener" class="btn btn-green">💬 WhatsApp Teklif</a>
        <a href="tel:+905459043834" class="btn btn-gold">📞 0545 904 38 34</a>
      </div>

      <button type="button" id="mobileMenuBtn" class="mobile-toggle" aria-label="Menüyü Aç" aria-expanded="false">☰</button>
    </div>

    <!-- Mobil Açılır Menü -->
    <div id="mobileDrawer" class="mobile-drawer">
      <div class="mobile-drawer-links">
        <a href="/">🏠 Ana Sayfa</a>
        <a href="/hurda-fiyatlari.html">📈 Güncel Hurda Fiyatları & Hesaplama</a>
        <a href="/bakir-hurda-fiyatlari.html">🔶 Bakır Hurda Fiyatları</a>
        <a href="/kablo-hurda-fiyatlari.html">⚡ Kablo Hurda Fiyatları</a>
        <a href="/demir-hurda-fiyatlari.html">🔩 Demir Hurda Fiyatları</a>
        <a href="/aluminyum-hurda-fiyatlari.html">💿 Alüminyum & Sarı Pirinç Fiyatları</a>
        <a href="/mardin-hurdaci.html">📍 Mardin & Kızıltepe Hurdacı</a>
        <a href="/diyarbakir-hurdaci.html">📍 Diyarbakır, Şanlıurfa & Güneydoğu Hurdacı</a>
        <a href="/bina-yikimi.html">🏗️ Fabrika, Bina & Çelik Çatı Sökümü</a>
        <a href="/teklif-formu.html">📋 Online Ekspertiz & Teklif Formu</a>
        <a href="/iletisim.html">📞 İletişim (0545 904 38 34)</a>
      </div>
    </div>
  </header>
"""


def render_calculator_widget():
    return """
      <!-- Canlı Dijital Kantar & Hurda Fiyat Hesaplama Aracı -->
      <aside class="kantar-card" id="hesaplama-araci" aria-label="Canlı Hurda Fiyat Hesaplama Aracı">
        <div class="kantar-header">
          <div class="kantar-title">⚖️ CANLI HURDA HESAPLAMA</div>
          <span class="kantar-badge">BORSA -%20 GÜNCEL</span>
        </div>

        <div class="kantar-lcd">
          <div class="lcd-left">
            <span>TAHMİNİ NAKİT ÖDEME TUTARI</span>
            <strong id="lcdUnitRate">Birim: 549,38 ₺ / KG (-%20 Borsa Net)</strong>
          </div>
          <div class="lcd-amount" id="lcdTotalAmount">54.938,00 ₺</div>
        </div>

        <div class="calc-form-group">
          <label for="calcCategory">1. Hurda Ana Kategorisi Seçin</label>
          <select id="calcCategory" class="calc-select"></select>
        </div>

        <div class="calc-form-group">
          <label for="calcSubItem">2. Hurda Alt Türü ve Kalitesi</label>
          <select id="calcSubItem" class="calc-select"></select>
        </div>

        <div class="calc-row-2">
          <div class="calc-form-group">
            <label for="calcWeight">3. Miktar (Kilo veya Ton)</label>
            <input type="number" id="calcWeight" class="calc-input" value="100" min="1" step="any">
          </div>
          <div class="calc-form-group">
            <label for="calcUnit">Birim</label>
            <select id="calcUnit" class="calc-select">
              <option value="KG">KG (Kilo)</option>
              <option value="TON">TON (1000 KG)</option>
            </select>
          </div>
        </div>

        <div class="calc-form-group">
          <label for="calcCity">4. Bulunduğunuz İl / İlçe</label>
          <select id="calcCity" class="calc-select">
            <option value="Kızıltepe / Mardin">Kızıltepe / Mardin (Merkez)</option>
            <option value="Artuklu / Mardin Merkez">Artuklu / Mardin Merkez</option>
            <option value="Midyat / Mardin">Midyat / Mardin</option>
            <option value="Nusaybin / Mardin">Nusaybin / Mardin</option>
            <option value="Derik / Mazıdağı / Mardin">Derik & Mazıdağı / Mardin</option>
            <option value="Diyarbakır">Diyarbakır (OSB & Merkez)</option>
            <option value="Şanlıurfa">Şanlıurfa (OSB & Merkez)</option>
            <option value="Gaziantep">Gaziantep (Başpınar OSB & Merkez)</option>
            <option value="Batman">Batman (OSB & Merkez)</option>
            <option value="Şırnak / Cizre / Silopi">Şırnak / Cizre / Silopi</option>
            <option value="Siirt / Kurtalan">Siirt / Kurtalan</option>
            <option value="Adıyaman / Kilis">Adıyaman / Kilis</option>
          </select>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1.35fr; gap:10px; margin-top:10px;">
          <button type="button" id="calcAddBasketBtn" class="btn btn-outline" style="padding:11px 12px; font-size:0.86rem;">➕ Listeye Ekle</button>
          <button type="button" id="calcWhatsappBtn" class="btn btn-green" style="padding:11px 14px; font-size:0.9rem;">💬 WhatsApp'tan Nakit Teklif Al</button>
        </div>

        <div id="calcBasketList" class="calc-basket" style="display:none;"></div>
        <p style="font-size:0.75rem; color:var(--text-steel); margin-top:10px; text-align:center;">
          * Fiyatlar günlük LME ve Türkiye hurda borsasından otomatik çekilip %20 saha/operasyon marjı düşülerek anlık hesaplanmaktadır. Tonajlı alımlarda özel fiyat uygulanır.
        </p>
      </aside>
"""


def render_price_tables(selected_cat_id=None):
    cats = [c for c in CATEGORIES if (selected_cat_id is None or c["id"] == selected_cat_id)]
    tabs_html = ""
    if selected_cat_id is None:
        tabs_buttons = '<button type="button" class="price-tab active" data-filter="all">Tümü (15 Kategori)</button>'
        for c in CATEGORIES[:8]:
            tabs_buttons += f'<button type="button" class="price-tab" data-filter="{c["id"]}">{c["shortName"]}</button>'
        tabs_html = f"""
        <div class="price-filter-bar">
          <div class="price-tabs">{tabs_buttons}</div>
          <input type="search" id="priceSearchInput" class="price-search" placeholder="🔍 Hurda türü ara (Örn: Soyma Bakır, DKP, Kablo)...">
        </div>
        """

    blocks_html = ""
    for c in cats:
        rows_html = ""
        for it in c["items"]:
            wa_text = f"Merhaba Bulgan Hurdacılık, {it['name']} ({fmt_tl(it['price'])}/KG) için fiyat ve adresten alım talep ediyorum."
            wa_url = f"https://wa.me/905459043834?text={ urllib.parse.quote(wa_text) }"
            rows_html += f"""
              <tr>
                <td><strong>{it["name"]}</strong></td>
                <td class="price-val" data-price-code="{it["code"]}">{fmt_tl(it["price"])} / KG</td>
                <td class="price-ton" data-ton-code="{it["code"]}">{fmt_tl(it["tonPrice"])} / TON</td>
                <td><span class="live-pill" style="font-size:0.72rem;">Peşin Nakit</span></td>
                <td style="text-align:right;">
                  <a href="{wa_url}" target="_blank" rel="noopener" class="btn btn-green" style="padding:6px 12px; font-size:0.78rem;">💬 Teklif Al</a>
                </td>
              </tr>
            """
        blocks_html += f"""
        <div class="price-category-block" data-cat-id="{c['id']}">
          <div class="price-category-head">
            <h3>🔸 <a href="/{c['slug']}">{c['name']}</a> <span class="kantar-badge">{c['badge']}</span></h3>
            <span style="font-size:0.8rem; color:var(--text-silver);">Son Güncelleme: <strong data-updated-at>{UPDATED_AT}</strong></span>
          </div>
          <div class="price-table-wrap">
            <table class="price-table">
              <thead>
                <tr>
                  <th>Hurda Metal Cinsi & Kalitesi</th>
                  <th>Net KG Fiyatı (-%20 Borsa)</th>
                  <th>1 Ton (1000 KG) Fiyatı</th>
                  <th>Ödeme Şekli</th>
                  <th style="text-align:right;">Hızlı Satış</th>
                </tr>
              </thead>
              <tbody>
                {rows_html}
              </tbody>
            </table>
          </div>
        </div>
        """
    return tabs_html + blocks_html


def render_lead_form(default_region="Kızıltepe / Mardin"):
    return f"""
    <div class="form-card">
      <div class="section-eyebrow">ÜCRETSİZ EKSPERTİZ & ADRESTEN ALIM FORMU</div>
      <h3 style="font-family:var(--font-display); font-size:1.55rem; color:var(--gold-bright); margin-bottom:8px;">
        Hurdalarınız İçin 10 Dakikada Nakit Teklif Alın
      </h3>
      <p style="color:var(--text-silver); font-size:0.92rem; margin-bottom:20px;">
        Bilgilerinizi bırakın; Mardin, Kızıltepe ve tüm Güneydoğu Anadolu saha ekibimiz sizi hemen arasın veya mobil kantarlı aracımızı adresinize yönlendirsin.
      </p>
      <form data-bulgan-form novalidate>
        <div class="form-grid form-grid-2">
          <div class="calc-form-group">
            <label for="fName">Adınız Soyadınız / Firma Adı *</label>
            <input type="text" id="fName" name="fullName" class="calc-input" placeholder="Örn: Ahmet Yılmaz / Yılmaz İnşaat" required>
            <div class="field-error">Lütfen adınızı ve soyadınızı girin.</div>
          </div>
          <div class="calc-form-group">
            <label for="fPhone">Telefon Numaranız *</label>
            <input type="tel" id="fPhone" name="phone" class="calc-input" placeholder="05XX XXX XX XX" required>
            <div class="field-error">Lütfen geçerli bir telefon numarası girin (10-11 hane).</div>
          </div>
        </div>

        <div class="form-grid form-grid-2">
          <div class="calc-form-group">
            <label for="fRegion">Bulunduğunuz İl / İlçe</label>
            <select id="fRegion" name="region" class="calc-select">
              <option value="{default_region}">{default_region}</option>
              <option value="Kızıltepe / Mardin">Kızıltepe / Mardin</option>
              <option value="Artuklu / Mardin Merkez">Artuklu / Mardin Merkez</option>
              <option value="Midyat / Mardin">Midyat / Mardin</option>
              <option value="Nusaybin / Mardin">Nusaybin / Mardin</option>
              <option value="Derik & Mazıdağı / Mardin">Derik & Mazıdağı / Mardin</option>
              <option value="Diyarbakır">Diyarbakır</option>
              <option value="Şanlıurfa">Şanlıurfa</option>
              <option value="Gaziantep">Gaziantep</option>
              <option value="Batman">Batman</option>
              <option value="Şırnak / Cizre / Silopi">Şırnak / Cizre / Silopi</option>
              <option value="Siirt / Adıyaman / Kilis">Siirt / Adıyaman / Kilis</option>
            </select>
          </div>
          <div class="calc-form-group">
            <label for="fScrapType">Satmak İstediğiniz Hurda Türü</label>
            <select id="fScrapType" name="scrapType" class="calc-select">
              <option value="Bakır Hurda">Bakır Hurda (Soyma, Kırkambar, Lama)</option>
              <option value="Kablo Hurda">Kablo Hurda (Enerji, TTR, Antigron, Yeraltı)</option>
              <option value="Demir & Çelik Hurda">Demir & Şantiye Hurdası (DKP, Ekstra, İnşaat)</option>
              <option value="Alüminyum Hurda">Alüminyum Hurda (Tel, Profil, Jant, Levha)</option>
              <option value="Sarı Pirinç & Bronz">Sarı Pirinç & Bronz Hurda</option>
              <option value="Paslanmaz Krom & Nikel">Paslanmaz Krom & Nikel Hurda</option>
              <option value="Akü, Kurşun & Çinko">Akü, Kurşun & Çinko Hurda</option>
              <option value="Fabrika / Bina Söküm & Yıkım">Fabrika, Tesis veya Çelik Çatı Sökümü</option>
            </select>
          </div>
        </div>

        <div class="form-grid form-grid-2">
          <div class="calc-form-group">
            <label for="fWeight">Tahmini Miktar (KG veya Ton)</label>
            <input type="text" id="fWeight" name="weight" class="calc-input" placeholder="Örn: 500 KG veya 5 Ton">
          </div>
          <div class="calc-form-group">
            <label for="fNotes">Ek Notunuz (Varsa Adres / Detay)</label>
            <input type="text" id="fNotes" name="notes" class="calc-input" placeholder="Örn: Kızıltepe OSB şantiyesinden alınacak">
          </div>
        </div>

        <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:14px; margin-top:8px;">
          <span style="font-size:0.8rem; color:var(--text-steel);">
            🔒 Bilgileriniz <a href="/gizlilik-politikasi.html" style="text-decoration:underline; color:var(--gold-bright);">KVKK ve Gizlilik Politikası</a> kapsamında korunmaktadır.
          </span>
          <button type="submit" class="btn btn-gold" style="min-width:240px;">
            <span class="spinner"></span>
            <span>🚀 Hemen Teklif İste</span>
          </button>
        </div>
      </form>
    </div>
    """


def render_footer():
    cat_footer = "".join(f'<li><a href="/{c["slug"]}">{c["name"]}</a></li>' for c in CATEGORIES[:8])
    mardin_footer = "".join(f'<li><a href="/{slug}">{name} Hurdacı</a></li>' for slug, name, *_ in MARDIN_DISTRICTS[:8])
    gda_footer = "".join(f'<li><a href="/{slug}">{name} Hurdacı</a></li>' for slug, name, *_ in GUNEYDOGU_PROVINCES)

    return f"""
  <!-- Kurumsal Alt Bilgi (Footer) -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <a href="/" class="brand-logo" style="margin-bottom:14px;">
            <picture>
              <source srcset="/images/logo-header.webp" type="image/webp">
              <img src="/images/logo-header.png" alt="Bulgan Hurdacılık Logo" width="200" height="66" loading="lazy">
            </picture>
          </a>
          <p style="font-size:0.88rem; margin-bottom:14px;">
            <strong>Bulgan Hurdacılık & Geri Dönüşüm</strong>; Mardin, Kızıltepe merkezli olup tüm Güneydoğu Anadolu Bölgesi'nde bakır, kablo, demir, alüminyum, sarı pirinç, krom, akü alımı ve fabrika/tesis sökümü alanında yerinde dijital tartım ve anında nakit ödeme güvencesiyle hizmet verir.
          </p>
          <p style="font-size:0.88rem; color:var(--gold-bright);">
            📍 <strong>Merkez Adres:</strong> Atatürk Mahallesi, Kızıltepe / MARDİN<br>
            📞 <strong>Telefon & WhatsApp:</strong> <a href="tel:+905459043834">0545 904 38 34</a><br>
            ✉️ <strong>E-Posta:</strong> <a href="mailto:bulganorhan19@gmail.com">bulganorhan19@gmail.com</a>
          </p>
        </div>

        <div class="footer-col">
          <h4>Güncel Hurda Fiyatları</h4>
          <ul class="footer-links">
            <li><a href="/hurda-fiyatlari.html">📈 Tüm Hurda Fiyatları & Hesaplama</a></li>
            {cat_footer}
          </ul>
        </div>

        <div class="footer-col">
          <h4>Mardin Hizmet Noktalarımız</h4>
          <ul class="footer-links">
            {mardin_footer}
            <li><a href="/savur-hurdaci.html">Savur, Yeşilli & Ömerli Hurdacı</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Güneydoğu Anadolu İlleri</h4>
          <ul class="footer-links">
            {gda_footer}
            <li><a href="/bina-yikimi.html">Fabrika & Tesis Yıkım Söküm</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>
          © 2026 <strong>Bulgan Hurdacılık & Geri Dönüşüm</strong> (bulgangeridonusum.com.tr). Tüm Hakları Saklıdır.
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:16px;">
          <a href="/hakkimizda.html">Hakkımızda</a>
          <a href="/gizlilik-politikasi.html">Gizlilik Politikası & KVKK</a>
          <a href="/kullanim-kosullari.html">Kullanım Koşulları</a>
          <a href="/sitemap.xml">Site Haritası (XML)</a>
          <a href="/iletisim.html">İletişim</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Mobil Sabit Alt Çağrı & WhatsApp Barı (Madde #11) -->
  <div class="mobile-sticky-bar" aria-label="Hızlı Mobil İletişim">
    <a href="tel:+905459043834" class="btn-gold">📞 Hemen Ara</a>
    <a href="https://wa.me/905459043834?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20hurda%20fiyat%C4%B1%20almak%20istiyorum." target="_blank" rel="noopener" class="btn-green">💬 WhatsApp Fiyat Al</a>
  </div>

  <!-- Masaüstü Sabit Hızlı Erişim Butonları -->
  <div class="desktop-float-cta">
    <a href="https://wa.me/905459043834?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20hurda%20sat%C4%B1%C5%9F%C4%B1%20i%C3%A7in%20fiyat%20almak%20istiyorum." target="_blank" rel="noopener" class="btn btn-green">💬 WhatsApp Fotoğraf Gönder</a>
    <a href="tel:+905459043834" class="btn btn-gold">📞 0545 904 38 34</a>
  </div>

  <!-- Çerez Tercih Banner'ı (Madde #17) -->
  <div id="cookieBanner" class="cookie-banner" role="dialog" aria-label="Çerez Bilgilendirmesi">
    <p>
      🍪 <strong>Çerez ve Gizlilik Tercihleri:</strong> Size en güncel LME hurda borsa fiyatlarını sunmak ve site deneyiminizi iyileştirmek için çerezler kullanıyoruz. Detaylar için <a href="/gizlilik-politikasi.html" style="color:var(--gold-bright); text-decoration:underline;">KVKK ve Gizlilik Politikamızı</a> inceleyebilirsiniz.
    </p>
    <div class="cookie-actions">
      <button type="button" id="cookieAcceptAll" class="btn btn-gold" style="padding:8px 16px; font-size:0.82rem;">Tümünü Kabul Et</button>
      <button type="button" id="cookieAcceptEssential" class="btn btn-outline" style="padding:8px 14px; font-size:0.82rem;">Sadece Zorunlu Çerezler</button>
    </div>
  </div>

  <script src="/js/bulgan-app.js" defer></script>
</body>
</html>
"""

import urllib.parse


def render_metal_cards_grid():
    cards = ""
    for c in CATEGORIES:
        top_item = c["items"][0]
        cards += f"""
        <article class="metal-card">
          <a href="/{c['slug']}" class="metal-card-img">
            <picture>
              <source srcset="/{c['image']}" type="image/webp">
              <img src="/{c['fallbackImage']}" alt="{c['name']} - Bulgan Hurdacılık Mardin & Güneydoğu Anadolu" width="800" height="520" loading="lazy" decoding="async">
            </picture>
          </a>
          <div class="metal-card-body">
            <h3 class="metal-card-title"><a href="/{c['slug']}">{c['name']}</a></h3>
            <p class="metal-card-desc">{c['desc']}</p>
            <div class="metal-card-footer">
              <span class="metal-start-price" data-price-code="{top_item['code']}">{fmt_tl(top_item['price'])} / KG</span>
              <a href="/{c['slug']}" class="btn btn-outline" style="padding:7px 14px; font-size:0.82rem;">Fiyatları Gör →</a>
            </div>
          </div>
        </article>
        """
    return f'<div class="cards-grid">{cards}</div>'


def render_regional_sections():
    mardin_cards = "".join(
        f"""
        <a href="/{slug}" class="region-card">
          <h3>📍 {name} Hurdacı</h3>
          <p>{desc[:110]}...</p>
          <span style="font-size:0.78rem; color:var(--green-bright); font-weight:700;">Adresten Alım & Fiyatlar →</span>
        </a>
        """
        for slug, name, lat, lon, desc, _ in MARDIN_DISTRICTS
    )
    gda_cards = "".join(
        f"""
        <a href="/{slug}" class="region-card">
          <h3>🚛 {name} Hurdacı</h3>
          <p>{desc[:110]}...</p>
          <span style="font-size:0.78rem; color:var(--gold-bright); font-weight:700;">Tonajlı Saha Alımı →</span>
        </a>
        """
        for slug, name, reg, lat, lon, desc, _ in GUNEYDOGU_PROVINCES
    )
    return f"""
    <section class="section section-alt">
      <div class="container">
        <div class="section-header">
          <div>
            <div class="section-eyebrow">MARDİN MERKEZ VE 10 İLÇEDE 30 DAKİKADA ADRESTEYİZ</div>
            <h2 class="section-title">Mardin İlçe Hurdacı Hizmet Noktalarımız</h2>
          </div>
          <p class="section-desc">Kızıltepe Atatürk Mahallesi'ndeki ana merkezimizden Artuklu, Midyat, Nusaybin, Derik, Mazıdağı ve tüm Mardin ilçelerine mobil dijital kantarlı araçlarımızla aynı gün ulaşıyoruz.</p>
        </div>
        <div class="region-grid">{mardin_cards}</div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-header">
          <div>
            <div class="section-eyebrow">GÜNEYDOĞU ANADOLU BÖLGE FİLOSU</div>
            <h2 class="section-title">Güneydoğu Anadolu İlleri Hurda Alım Ağı</h2>
          </div>
          <p class="section-desc">Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman ve Kilis Organize Sanayi Bölgeleri (OSB), fabrikalar ve şantiyelerden tonajlı metal alımı ve tesis sökümü yapıyoruz.</p>
        </div>
        <div class="region-grid">{gda_cards}</div>
      </div>
    </section>
    """


def build_index_page():
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Mardin ve Güneydoğu Anadolu'da adresten hurda alım süreci nasıl işler?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "0545 904 38 34 numaralı hattımızdan veya WhatsApp üzerinden hurdanızın fotoğrafını ve konumunuzu gönderdiğinizde anında fiyat teklifi sunuyoruz. Onayınızla birlikte Kızıltepe merkezli mobil kantarlı ekibimiz adresinize gelerek hassas tartım yapar ve tutarı anında nakit veya EFT ile öder."
                }
            },
            {
                "@type": "Question",
                "name": "Hurda fiyatları neye göre belirlenir ve ne sıklıkla güncellenir?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Sitemizdeki hurda fiyatları Londra Metal Borsası (LME) ve Türkiye metal piyasası verilerinden otomatik kazıyıcı sistemimizle günlük olarak çekilir ve %20 saha operasyon/işleme indirimi düşülerek net alım fiyatı olarak yayınlanır."
                }
            },
            {
                "@type": "Question",
                "name": "Hangi hurda çeşitlerini satın alıyorsunuz?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Soyma ve kırkambar bakır, enerji ve tesisat kabloları, DKP ve inşaat demiri, alüminyum tel ve profil, sarı pirinç, paslanmaz krom (304-316), kurşun, çinko, nikel, akü, elektronik kartlar, chiller soğutma grupları ve fabrika/bina yıkım söküm hurdalarını satın alıyoruz."
                }
            }
        ]
    }, ensure_ascii=False)

    head = render_head(
        "Mardin Hurdacı | Bulgan Hurdacılık & Geri Dönüşüm - Kızıltepe & Güneydoğu Hurda Alımı 0545 904 38 34",
        "Mardin, Kızıltepe ve tüm Güneydoğu Anadolu (Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak) merkez hurdacı. Bakır, kablo, demir, alüminyum, sarı pirinç ve fabrika sökümünde yerinde dijital tartım ve anında nakit ödeme. Tel: 0545 904 38 34.",
        "",
        schema_extra=f'<script type="application/ld+json">{faq_schema}</script>'
    )

    province_pills = "".join(
        f'<a href="/{slug}" class="province-pill">📍 {name}</a>'
        for slug, name, *_ in (MARDIN_DISTRICTS[:5] + GUNEYDOGU_PROVINCES[:6])
    )

    body = f"""
  <!-- HERO BÖLÜMÜ (Madde #4: İlk Ekranda Net CTA + Canlı Kantar Hesaplayıcı) -->
  <section class="hero-section">
    <div class="container hero-grid">
      <div>
        <div class="region-tag">⚡ MARDİN • KIZILTEPE • GÜNEYDOĞU ANADOLU MERKEZ HURDACI</div>
        <h1 class="hero-title">
          Mardin & Güneydoğu'da <span class="gold-highlight">En Yüksek Fiyatla</span> <span class="green-highlight">Anında Nakit</span> Hurda Alımı
        </h1>
        <p class="hero-lead">
          <strong>Bulgan Hurdacılık & Geri Dönüşüm</strong> olarak Mardin (Kızıltepe, Artuklu, Midyat, Nusaybin) ve tüm Güneydoğu Anadolu illerinde <strong>bakır, enerji kablosu, demir, alüminyum, sarı pirinç, krom, akü</strong> ve <strong>fabrika/tesis söküm</strong> hurdalarınızı adresinizde dijital kantarla tartıp anında nakit ödüyoruz.
        </p>

        <div class="hero-cta-row">
          <a href="tel:+905459043834" class="btn btn-gold">📞 Hemen Ara: 0545 904 38 34</a>
          <a href="https://wa.me/905459043834?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20elimdeki%20hurda%20i%C3%A7in%20fiyat%20almak%20istiyorum." target="_blank" rel="noopener" class="btn btn-green">💬 WhatsApp Fotoğraf Gönder / Fiyat Al</a>
        </div>

        <div class="hero-trust-grid">
          <div class="trust-box">
            <strong>30 Dakikada</strong>
            <span>Mardin & Kızıltepe Mobil Araç</span>
          </div>
          <div class="trust-box">
            <strong>Hassas Dijital Kantar</strong>
            <span>Gözünüzün Önünde Şeffaf Tartım</span>
          </div>
          <div class="trust-box">
            <strong>%100 Peşin Ödeme</strong>
            <span>Tartım Anında Nakit / EFT</span>
          </div>
        </div>

        <div class="province-pills" aria-label="Hızlı Bölge Bağlantıları">
          {province_pills}
        </div>
      </div>

      {render_calculator_widget()}
    </div>
  </section>

  <!-- GÜNLÜK BORSA HURDA FİYAT TABLOSU (-%20 Otomatik İndirimli) -->
  <section class="section" id="guncel-fiyatlar">
    <div class="container">
      <div class="section-header">
        <div>
          <div class="section-eyebrow">OTOMATİK GÜNLÜK BORSA KAZIYICI SİSTEMİ (%20 AZALTILMIŞ NET ALIM)</div>
          <h2 class="section-title">📈 Güncel Hurda Fiyatları (<span data-updated-at>{UPDATED_AT}</span>)</h2>
        </div>
        <p class="section-desc">
          Tablodaki fiyatlar günlük metal borsası verilerinden otomatik çekilerek %20 operasyon/fire payı düşülmüş net saha alım fiyatlarıdır. Tonajlı fabrika ve şantiye yüklemelerinde özel yüksek kur uygulanır.
        </p>
      </div>

      {render_price_tables()}
    </div>
  </section>

  <!-- MARKALI GÖRSELLİ HURDA METAL ÇEŞİTLERİ VİTRİNİ -->
  <section class="section section-alt">
    <div class="container">
      <div class="section-header">
        <div>
          <div class="section-eyebrow">YERİNDE TARTIM • DEĞERİNDE NAKİT ALIM</div>
          <h2 class="section-title">Alım Yaptığımız Hurda Metal Kategorileri</h2>
        </div>
        <a href="/hurda-cesitleri.html" class="btn btn-outline">Tüm Hurda Çeşitlerini İncele →</a>
      </div>

      {render_metal_cards_grid()}
    </div>
  </section>

  <!-- FABRİKA, TESİS & ÇELİK ÇATI YIKIM SÖKÜM HİZMETLERİ -->
  <section class="section">
    <div class="container">
      <div class="section-header">
        <div>
          <div class="section-eyebrow">AĞIR SANAYİ, OSB VE ŞANTİYE ÇÖZÜMLERİ</div>
          <h2 class="section-title">Fabrika Bozumu, Bina Yıkımı & Çelik Çatı Sökümü</h2>
        </div>
        <p class="section-desc">Mardin OSB, Kızıltepe, Diyarbakır, Gaziantep, Şanlıurfa ve Batman genelinde sertifikalı oksijen kesim ekiplerimiz ve vinçli filomuzla anahtar teslim söküm hizmeti sunuyoruz.</p>
      </div>

      <div class="cards-grid">
        <article class="metal-card">
          <a href="/bina-yikimi.html" class="metal-card-img">
            <picture>
              <source srcset="/images/sokulecek-hurda-1.webp" type="image/webp">
              <img src="/images/sokulecek-hurda-1.jpg" alt="Fabrika ve Bina Yıkım Söküm - Bulgan Hurdacılık" width="800" height="520" loading="lazy">
            </picture>
          </a>
          <div class="metal-card-body">
            <h3 class="metal-card-title"><a href="/bina-yikimi.html">Fabrika, Tesis & Bina Yıkım Söküm</a></h3>
            <p class="metal-card-desc">Üretim ömrünü tamamlamış fabrika binaları, depolar ve tesislerin hurda karşılığı veya anahtar teslim güvenli yıkım ve sökümü.</p>
            <div class="metal-card-footer">
              <span class="metal-start-price">Ücretsiz Saha Keşfi</span>
              <a href="/bina-yikimi.html" class="btn btn-outline" style="padding:7px 14px; font-size:0.82rem;">Detaylı Bilgi →</a>
            </div>
          </div>
        </article>

        <article class="metal-card">
          <a href="/celik-cati-sokumu.html" class="metal-card-img">
            <picture>
              <source srcset="/images/demir-hurda-1.webp" type="image/webp">
              <img src="/images/demir-hurda-1.jpg" alt="Çelik Çatı ve Hangar Sökümü - Bulgan Hurdacılık" width="800" height="520" loading="lazy">
            </picture>
          </a>
          <div class="metal-card-body">
            <h3 class="metal-card-title"><a href="/celik-cati-sokumu.html">Çelik Çatı & Hangar Konstrüksiyon Sökümü</a></h3>
            <p class="metal-card-desc">Fabrika çatıları, çelik hangarlar, H-demir kolonlar ve sandviç panellerin yüksekte çalışma uzmanlarımızca hasarsız sökümü.</p>
            <div class="metal-card-footer">
              <span class="metal-start-price">Yüksek Tonaj Fiyatı</span>
              <a href="/celik-cati-sokumu.html" class="btn btn-outline" style="padding:7px 14px; font-size:0.82rem;">Detaylı Bilgi →</a>
            </div>
          </div>
        </article>

        <article class="metal-card">
          <a href="/hurda-chiller-grubu-sogutma-sistemleri-fiyatlari-alimi.html" class="metal-card-img">
            <picture>
              <source srcset="/images/hurda-chiller-sogutma-grubu-1.webp" type="image/webp">
              <img src="/images/hurda-chiller-sogutma-grubu-1.jpg" alt="Hurda Chiller ve Soğutma Grubu Alımı - Bulgan Hurdacılık" width="800" height="520" loading="lazy">
            </picture>
          </a>
          <div class="metal-card-body">
            <h3 class="metal-card-title"><a href="/hurda-chiller-grubu-sogutma-sistemleri-fiyatlari-alimi.html">Chiller, Kazan Dairesi & Trafo Sökümü</a></h3>
            <p class="metal-card-desc">Merkezi iklimlendirme chiller grupları, kazan daireleri, jeneratör ve trafo ünitelerinin yerinde demontajı ve peşin alımı.</p>
            <div class="metal-card-footer">
              <span class="metal-start-price">Bakır/Motor Değerleme</span>
              <a href="/hurda-chiller-grubu-sogutma-sistemleri-fiyatlari-alimi.html" class="btn btn-outline" style="padding:7px 14px; font-size:0.82rem;">Detaylı Bilgi →</a>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>

  {render_regional_sections()}

  <!-- SIKÇA SORULAN SORULAR VE HIZLI TEKLİF FORMU -->
  <section class="section section-alt">
    <div class="container">
      <div class="hero-grid">
        <div>
          <div class="section-eyebrow">MERAK EDİLENLER</div>
          <h2 class="section-title" style="margin-bottom:20px;">Sıkça Sorulan Sorular</h2>
          <div class="faq-list">
            <details class="faq-item" open>
              <summary>Mardin ve Güneydoğu Anadolu'da adresten hurda alım süreci nasıl işler? <span>＋</span></summary>
              <div class="faq-answer">
                <strong>0545 904 38 34</strong> numaralı hattımızdan arayarak veya WhatsApp üzerinden hurdanızın fotoğrafını göndererek anında fiyat teklifi alabilirsiniz. Anlaşma sağlandığında Kızıltepe merkezli mobil kantarlı ekibimiz adresinize gelir, hurdalarınızı gözünüzün önünde tartar ve paranızı anında nakit veya banka hesabınıza EFT/FAST olarak öder.
              </div>
            </details>
            <details class="faq-item">
              <summary>Hurda fiyatları nasıl belirleniyor ve ne sıklıkla güncelleniyor? <span>＋</span></summary>
              <div class="faq-answer">
                Fiyatlarımız Londra Metal Borsası (LME), döviz kuru ve Türkiye geri dönüşüm piyasası verilerinden otomatik kazıyıcı sistemimizle günlük olarak çekilir ve %20 saha/işleme indirimi düşülerek net alım fiyatı olarak tablolarımıza yansıtılır.
              </div>
            </details>
            <details class="faq-item">
              <summary>Şantiye ve fabrikalar için konteyner bırakma ve tonajlı alım hizmetiniz var mı? <span>＋</span></summary>
              <div class="faq-answer">
                Evet. Mardin, Kızıltepe, Diyarbakır, Şanlıurfa, Gaziantep, Batman ve Şırnak'taki organize sanayi bölgeleri (OSB) ve inşaat şantiyelerine periyodik hurda toplama konteynerleri bırakıyor, vinçli kamyonlarımızla yüksek tonajlı alım yapıyoruz.
              </div>
            </details>
            <details class="faq-item">
              <summary>Kablo hurdalarında bakır oranı (randıman) nasıl hesaplanıyor? <span>＋</span></summary>
              <div class="faq-answer">
                Numune soyma ve hassas tartım yöntemiyle kablonuzun içindeki net saf bakır ağırlığı tespit edilir. Böylece tek damar enerji kablosu, TTR, antigron veya yeraltı zırhlı kablolarınız gerçek bakır değerinden tek kuruş değer kaybetmeden satın alınır.
              </div>
            </details>
          </div>
        </div>

        <div>
          {render_lead_form("Kızıltepe / Mardin")}
        </div>
      </div>
    </div>
  </section>
"""
    return head + render_header("index.html") + body + render_footer()


def build_hurda_fiyatlari_page():
    head = render_head(
        f"Güncel Hurda Fiyatları ({UPDATED_AT[:10]}) | Bulgan Hurdacılık Mardin & Güneydoğu",
        "Mardin, Kızıltepe ve Güneydoğu Anadolu güncel hurda fiyatları listesi. Bakır, kablo, demir, alüminyum, sarı pirinç, krom ve akü kilosu ne kadar? Canlı hurda hesaplama aracı.",
        "hurda-fiyatlari.html"
    )
    body = f"""
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Güncel Hurda Fiyatları</span></div>
      <h1 class="hero-title" style="font-size:clamp(1.8rem, 3.5vw, 2.75rem); margin-bottom:10px;">
        📈 Güncel Hurda Fiyatları ve <span class="gold-highlight">Canlı Kantar Hesaplama</span>
      </h1>
      <p class="hero-lead" style="margin-bottom:0;">
        Borsa verilerinden günlük otomatik çekilen ve %20 saha marjı uygulanmış net nakit alım fiyatlarımız. Son güncelleme: <strong data-updated-at>{UPDATED_AT}</strong>
      </p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="hero-grid" style="margin-bottom:48px;">
        <div>
          <h2 class="section-title" style="margin-bottom:14px;">Anlık Borsa Endeksli Hurda Fiyat Listesi</h2>
          <p style="color:var(--text-silver); margin-bottom:16px;">
            <strong>Bulgan Hurdacılık</strong> olarak Mardin (Kızıltepe, Artuklu, Midyat, Nusaybin) ve tüm Güneydoğu Anadolu illerinde hurda alımlarımızı şeffaf dijital kantar tartımıyla gerçekleştiriyoruz. Yandaki <strong>Canlı Hurda Hesaplama Aracı</strong> ile elinizdeki hurdanın toplam nakit karşılığını saniyeler içinde hesaplayabilirsiniz.
          </p>
          <div class="hero-cta-row">
            <a href="tel:+905459043834" class="btn btn-gold">📞 0545 904 38 34</a>
            <a href="https://wa.me/905459043834?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20g%C3%BCncel%20hurda%20fiyat%C4%B1%20almak%20istiyorum." target="_blank" rel="noopener" class="btn btn-green">💬 WhatsApp'tan Fiyat Al</a>
          </div>
        </div>
        {render_calculator_widget()}
      </div>

      {render_price_tables()}
    </div>
  </section>
"""
    return head + render_header("hurda-fiyatlari.html") + body + render_footer()


def build_category_page(cat):
    top_item = cat["items"][0]
    title = f"{cat['name']} ({UPDATED_AT[:10]}) - KG: {fmt_tl(top_item['price'])} | Bulgan Hurdacılık"
    desc = f"Mardin, Kızıltepe ve Güneydoğu Anadolu güncel {cat['name'].lower()}. {cat['desc']} Yerinde dijital tartım ve anında nakit ödeme: 0545 904 38 34."
    head = render_head(title, desc, cat["slug"])
    body = f"""
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb">
        <a href="/">Ana Sayfa</a> <span>/</span> <a href="/hurda-fiyatlari.html">Hurda Fiyatları</a> <span>/</span> <span>{cat['name']}</span>
      </div>
      <h1 class="hero-title" style="font-size:clamp(1.8rem, 3.5vw, 2.75rem); margin-bottom:10px;">
        {cat['name']} <span class="gold-highlight">({fmt_tl(top_item['price'])} / KG)</span>
      </h1>
      <p class="hero-lead" style="margin-bottom:0;">{cat['desc']}</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="hero-grid" style="margin-bottom:44px;">
        <div>
          <picture>
            <source srcset="/{cat['image']}" type="image/webp">
            <img src="/{cat['fallbackImage']}" alt="{cat['name']} - Bulgan Hurdacılık" width="800" height="520" style="border-radius:14px; border:2px solid var(--gold-main); margin-bottom:22px;">
          </picture>
          <div class="prose-content">
            <h2>Mardin ve Güneydoğu Anadolu {cat['shortName']} Alımı</h2>
            <p>
              <strong>Bulgan Hurdacılık & Geri Dönüşüm</strong> olarak Mardin merkez Artuklu, Kızıltepe, Midyat, Nusaybin başta olmak üzere Diyarbakır, Şanlıurfa, Gaziantep, Batman ve Şırnak genelinde her tonajda <strong>{cat['shortName'].lower()}</strong> alımı yapıyoruz.
            </p>
            <p>
              Borsa verilerinden günlük otomatik çekilen ve %20 saha operasyon marjı düşülerek güncellenen net fiyatlarımızla, hurdalarınızı adresinizde hassas dijital kantarla tartıyor ve <strong>anında nakit</strong> ödüyoruz.
            </p>
          </div>
        </div>
        {render_calculator_widget()}
      </div>

      {render_price_tables(cat["id"])}

      <div style="margin-top:44px;">
        {render_lead_form("Kızıltepe / Mardin")}
      </div>
    </div>
  </section>
"""
    return head + render_header(cat["slug"]) + body + render_footer()


def build_regional_page(slug, name, geo_reg, lat, lon, desc, neighborhoods, is_mardin=True):
    region_label = f"{name}, Mardin" if is_mardin else f"{name}, Güneydoğu Anadolu"
    title = f"{name} Hurdacı | Bulgan Hurdacılık - Adresten Nakit Hurda Alımı 0545 904 38 34"
    meta_desc = f"{name} hurdacı ve kurumsal geri dönüşüm hizmeti. {desc} Bakır, demir, kablo, alüminyum ve sarı hurdalarınız için hemen arayın: 0545 904 38 34."
    head = render_head(title, meta_desc, slug, geo_region=geo_reg, geo_place=region_label, lat=lat, lon=lon)

    nh_cards = "".join(
        f"""
        <div class="trust-box">
          <strong>📍 {nh}</strong>
          <span>{name} Aynı Gün Mobil Kantar & Nakit Hurda Alımı</span>
        </div>
        """
        for nh in neighborhoods
    )

    body = f"""
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb">
        <a href="/">Ana Sayfa</a> <span>/</span> <a href="/hurda-alan-yerler.html">Hizmet Bölgelerimiz</a> <span>/</span> <span>{name} Hurdacı</span>
      </div>
      <div class="region-tag">📍 {region_label.upper()} YETKİLİ MERKEZ HURDACI</div>
      <h1 class="hero-title" style="font-size:clamp(1.85rem, 3.6vw, 2.85rem); margin-bottom:12px;">
        {name} Hurdacı & <span class="gold-highlight">En Yakın Kurumsal Geri Dönüşüm</span>
      </h1>
      <p class="hero-lead" style="margin-bottom:20px;">{desc}</p>
      <div class="hero-cta-row" style="margin-bottom:0;">
        <a href="tel:+905459043834" class="btn btn-gold">📞 {name} Hurdacı Ara: 0545 904 38 34</a>
        <a href="https://wa.me/905459043834?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20{urllib.parse.quote(name)}%20b%C3%B6lgesinde%20hurda%20satmak%20istiyorum." target="_blank" rel="noopener" class="btn btn-green">💬 WhatsApp Konum & Fotoğraf Gönder</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="hero-grid" style="margin-bottom:48px;">
        <div class="prose-content">
          <h2>{name} Bölgesinde Adresten Nakit Hurda Alımı</h2>
          <p>
            <strong>Bulgan Hurdacılık & Geri Dönüşüm</strong> olarak {name} genelinde sanayi siteleri, organize sanayi bölgeleri (OSB), inşaat şantiyeleri, tarımsal işletmeler, kurumlar ve konutlardan çıkan her nevi metal hurdayı adresinizden kendi araçlarımızla teslim alıyoruz.
          </p>
          <p>
            Soyma bakır, kırkambar bakır, enerji ve tesisat kabloları, DKP ve ekstra demir, inşaat demiri, alüminyum tel ve profil, sarı pirinç, paslanmaz krom (304/316), akü ve chiller soğutma gruplarınızı {name} sahasında <strong>hassas dijital kantarla</strong> tartıyor, anında nakit ödeme yapıyoruz.
          </p>
          <h3>{name} Hızlı Alım Noktalarımız ve Mahallelerimiz</h3>
          <div class="hero-trust-grid" style="margin-top:14px;">
            {nh_cards}
          </div>
        </div>
        {render_calculator_widget()}
      </div>

      <h2 class="section-title" style="margin-bottom:20px;">📈 {name} Güncel Hurda Fiyatları (<span data-updated-at>{UPDATED_AT}</span>)</h2>
      {render_price_tables()}

      <div style="margin-top:44px;">
        {render_lead_form(region_label)}
      </div>
    </div>
  </section>
"""
    return head + render_header(slug) + body + render_footer()


def build_extra_service_page(slug, title_txt, cat_id, img_webp, img_jpg, desc_txt):
    head = render_head(
        f"{title_txt} | Bulgan Hurdacılık Mardin & Güneydoğu 0545 904 38 34",
        f"{desc_txt} Ücretsiz keşif ve anında nakit ödeme için hemen arayın: 0545 904 38 34.",
        slug
    )
    body = f"""
  <section class="page-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>{title_txt}</span></div>
      <h1 class="hero-title" style="font-size:clamp(1.8rem, 3.5vw, 2.75rem); margin-bottom:12px;">
        {title_txt}
      </h1>
      <p class="hero-lead" style="margin-bottom:0;">{desc_txt}</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="hero-grid" style="margin-bottom:44px;">
        <div>
          <picture>
            <source srcset="/{img_webp}" type="image/webp">
            <img src="/{img_jpg}" alt="{title_txt} - Bulgan Hurdacılık" width="800" height="520" style="border-radius:14px; border:2px solid var(--gold-main); margin-bottom:22px;">
          </picture>
          <div class="prose-content">
            <h2>Mardin, Kızıltepe ve Güneydoğu Anadolu Kurumsal Çözüm</h2>
            <p>{desc_txt}</p>
            <ul>
              <li>✅ <strong>Ücretsiz Yerinde Ekspertiz:</strong> Mühendis ve saha uzmanlarımızla Mardin ve tüm Güneydoğu illerinde aynı gün keşif.</li>
              <li>✅ <strong>Tam İş Güvenliği (İSG):</strong> Sertifikalı oksijen kesim, vinç ve yüksekte çalışma ekipmanlarıyla sıfır riskli operasyon.</li>
              <li>✅ <strong>Hassas Tartım & Peşin Ödeme:</strong> Kantar fişiyle şeffaf tartım ve yükleme anında nakit / EFT ödeme.</li>
            </ul>
          </div>
        </div>
        {render_calculator_widget()}
      </div>

      {render_price_tables(cat_id)}

      <div style="margin-top:44px;">
        {render_lead_form("Kızıltepe / Mardin")}
      </div>
    </div>
  </section>
"""
    return head + render_header(slug) + body + render_footer()


def build_static_corporate_pages():
    pages = {}

    # 1. hurda-cesitleri.html
    h_cesit = render_head(
        "Alım Yaptığımız Hurda Metal Çeşitleri | Bulgan Hurdacılık Mardin & Güneydoğu",
        "Bakır, kablo, demir, alüminyum, sarı pirinç, paslanmaz krom, akü, çinko, kurşun, nikel, bronz ve elektronik hurda çeşitleri. Yerinde tartım ve nakit alım.",
        "hurda-cesitleri.html"
    )
    pages["hurda-cesitleri.html"] = h_cesit + render_header("hurda-cesitleri.html") + f"""
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Hurda Çeşitleri</span></div>
        <h1 class="hero-title" style="font-size:2.4rem;">Alım Yaptığımız <span class="gold-highlight">Tüm Hurda Metal Çeşitleri</span></h1>
        <p class="hero-lead" style="margin-bottom:0;">Mardin, Kızıltepe ve tüm Güneydoğu Anadolu genelinde yüksek tonajlı veya parça bazlı satın aldığımız geri dönüşüm metalleri.</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        {render_metal_cards_grid()}
      </div>
    </section>
    """ + render_footer()

    # 2. hurda-alan-yerler.html
    h_yerler = render_head(
        "Mardin & Güneydoğu Anadolu Hurda Alan Yerler | Bulgan Hurdacılık 0545 904 38 34",
        "Mardin, Kızıltepe, Artuklu, Midyat, Nusaybin, Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman ve Kilis'te adresten nakit hurda alan yerler.",
        "hurda-alan-yerler.html"
    )
    pages["hurda-alan-yerler.html"] = h_yerler + render_header("hurda-alan-yerler.html") + f"""
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Hurda Alan Yerler</span></div>
        <h1 class="hero-title" style="font-size:2.4rem;">Mardin ve Güneydoğu Anadolu <span class="gold-highlight">Hurda Alan Yerler</span></h1>
        <p class="hero-lead" style="margin-bottom:0;">Kızıltepe merkezimizden tüm Mardin ilçelerine ve Güneydoğu Anadolu illerine mobil kantarlı araçlarımızla adresten nakit alım yapıyoruz.</p>
      </div>
    </section>
    {render_regional_sections()}
    """ + render_footer()

    # 3. hakkimizda.html
    h_hak = render_head(
        "Hakkımızda | Bulgan Hurdacılık & Geri Dönüşüm - Kızıltepe / Mardin",
        "Bulgan Hurdacılık & Geri Dönüşüm kurumsal kimliği, Mardin Kızıltepe merkez tesisimiz, dijital kantar güvencemiz ve Güneydoğu Anadolu araç filomuz.",
        "hakkimizda.html"
    )
    pages["hakkimizda.html"] = h_hak + render_header("hakkimizda.html") + f"""
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Kurumsal / Hakkımızda</span></div>
        <h1 class="hero-title" style="font-size:2.4rem;">Bulgan Hurdacılık & <span class="gold-highlight">Kurumsal Geri Dönüşüm</span></h1>
        <p class="hero-lead" style="margin-bottom:0;">Mardin ve Güneydoğu Anadolu'nun güvenilir, şeffaf tartım ve anında nakit ödeme ilkeli metal geri dönüşüm merkezi.</p>
      </div>
    </section>
    <section class="section">
      <div class="container hero-grid">
        <div class="prose-content">
          <h2>Kızıltepe'den Tüm Güneydoğu Anadolu'ya Uzanan Güçlü Altyapı</h2>
          <p>
            <strong>Bulgan Hurdacılık & Geri Dönüşüm</strong>, Mardin Kızıltepe Atatürk Mahallesi'ndeki merkeziyle bölge sanayisinin, inşaat şantiyelerinin, kurumların ve bireysel müşterilerin hurda metallerini ekonomiye kazandırmak üzere faaliyet göstermektedir.
          </p>
          <p>
            Sektörde güvenin en önemli unsurunun <strong>doğru tartım</strong> ve <strong>gerçek borsa fiyatı</strong> olduğunun bilinciyle; tüm alımlarımızda kalibrasyonlu dijital kantarlar kullanıyor, tartım işlemini müşterimizin gözü önünde yapıyor ve ödemeyi araç başında nakit veya anında EFT/FAST ile gerçekleştiriyoruz.
          </p>
          <h3>Neden Bulgan Hurdacılık?</h3>
          <ul>
            <li><strong>Günlük LME & Borsa Endeksli Fiyatlama:</strong> Otomatik fiyat sistemimizle her gün güncel ve şeffaf alım fiyatları.</li>
            <li><strong>Geniş Araç Filosu:</strong> Mardin, Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman ve Kilis'e aynı gün saha sevkiyatı.</li>
            <li><strong>Uzman Söküm Ekibi:</strong> Fabrika bozumu, çelik çatı sökümü ve kazan/chiller demontajında profesyonel kadro.</li>
          </ul>
        </div>
        {render_lead_form("Kızıltepe / Mardin")}
      </div>
    </section>
    """ + render_footer()

    # 4. iletisim.html (Checklist #19)
    h_ilet = render_head(
        "İletişim & Konum | Bulgan Hurdacılık Kızıltepe / Mardin - 0545 904 38 34",
        "Bulgan Hurdacılık iletişim bilgileri: Atatürk Mahallesi, Kızıltepe / Mardin. Telefon ve WhatsApp: 0545 904 38 34. E-posta: bulganorhan19@gmail.com.",
        "iletisim.html"
    )
    pages["iletisim.html"] = h_ilet + render_header("iletisim.html") + f"""
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>İletişim</span></div>
        <h1 class="hero-title" style="font-size:2.4rem;">İletişim & <span class="gold-highlight">Merkez Konumumuz</span></h1>
        <p class="hero-lead" style="margin-bottom:0;">7/24 telefon, WhatsApp ve online ekspertiz formumuz üzerinden bize ulaşabilirsiniz.</p>
      </div>
    </section>
    <section class="section">
      <div class="container hero-grid">
        <div>
          <div class="form-card" style="margin-bottom:24px;">
            <h2 style="font-family:var(--font-display); color:var(--gold-bright); margin-bottom:16px;">Doğrudan İletişim Kanallarımız</h2>
            <div style="display:grid; gap:14px; font-size:0.98rem;">
              <div>📍 <strong>Merkez Adresimiz:</strong> Atatürk Mahallesi, Kızıltepe / MARDİN (47400)</div>
              <div>📞 <strong>Telefon Hattımız:</strong> <a href="tel:+905459043834" style="color:var(--green-bright); font-weight:800;">0545 904 38 34</a></div>
              <div>💬 <strong>WhatsApp Fiyat Hattı:</strong> <a href="https://wa.me/905459043834" target="_blank" rel="noopener" style="color:var(--gold-bright); font-weight:800;">wa.me/905459043834 (Fotoğraf Gönderin)</a></div>
              <div>✉️ <strong>Kurumsal E-Posta:</strong> <a href="mailto:bulganorhan19@gmail.com">bulganorhan19@gmail.com</a></div>
              <div>🕒 <strong>Çalışma Saatlerimiz:</strong> Pazartesi - Pazar: 07:00 – 22:00 (Tonajlı şantiye alımlarında 7/24 randevu)</div>
            </div>
          </div>
          <div style="border-radius:12px; overflow:hidden; border:2px solid var(--border-gold); height:320px;">
            <iframe
              title="Bulgan Hurdacılık Kızıltepe Mardin Harita Konumu"
              src="https://www.google.com/maps?q=Atat%C3%BCrk+Mahallesi+K%C4%B1z%C4%B1ltepe+Mardin&output=embed"
              width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade">
            </iframe>
          </div>
        </div>
        {render_lead_form("Kızıltepe / Mardin")}
      </div>
    </section>
    """ + render_footer()

    # 5. teklif-formu.html
    h_teklif = render_head(
        "Online Hurda Teklif & Ekspertiz Formu | Bulgan Hurdacılık 0545 904 38 34",
        "Mardin ve Güneydoğu Anadolu'da satmak istediğiniz bakır, demir, kablo, alüminyum ve fabrika hurdaları için online fiyat teklifi ve mobil kantar talep formu.",
        "teklif-formu.html"
    )
    pages["teklif-formu.html"] = h_teklif + render_header("teklif-formu.html") + f"""
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Online Teklif Formu</span></div>
        <h1 class="hero-title" style="font-size:2.4rem;">Online Hurda <span class="gold-highlight">Fiyat Teklifi & Kantar Çağır</span></h1>
        <p class="hero-lead" style="margin-bottom:0;">Formu doldurun veya hesaplama aracımızla anında nakit değerinizi öğrenin.</p>
      </div>
    </section>
    <section class="section">
      <div class="container hero-grid">
        {render_lead_form("Kızıltepe / Mardin")}
        {render_calculator_widget()}
      </div>
    </section>
    """ + render_footer()

    # 6. 404.html (Checklist #1: Özel 404 Sayfası)
    h_404 = render_head(
        "Sayfa Bulunamadı (404) | Bulgan Hurdacılık & Geri Dönüşüm",
        "Aradığınız sayfa taşınmış veya kaldırılmış olabilir. Güncel Mardin ve Güneydoğu Anadolu hurda fiyatlarına ana sayfamızdan ulaşabilirsiniz.",
        "404.html"
    )
    pages["404.html"] = h_404 + render_header("") + f"""
    <section class="section" style="text-align:center; padding:88px 0;">
      <div class="container" style="max-width:680px;">
        <div class="region-tag">⚠️ HATA KODU: 404 — SAYFA BULUNAMADI</div>
        <h1 class="hero-title" style="font-size:2.8rem; margin-bottom:16px;">
          Aradığınız Sayfa <span class="gold-highlight">Taşınmış veya Kaldırılmış</span>
        </h1>
        <p class="hero-lead" style="margin:0 auto 28px;">
          Endişelenmeyin! Güncel hurda fiyat listemize, canlı kantar hesaplama aracımıza veya doğrudan Mardin & Güneydoğu Anadolu saha ekibimize aşağıdaki bağlantılardan hemen ulaşabilirsiniz.
        </p>
        <div class="hero-cta-row" style="justify-content:center;">
          <a href="/" class="btn btn-gold">🏠 Ana Sayfaya Dön</a>
          <a href="/hurda-fiyatlari.html" class="btn btn-outline">📈 Güncel Hurda Fiyatları</a>
          <a href="tel:+905459043834" class="btn btn-green">📞 0545 904 38 34</a>
        </div>
      </div>
    </section>
    """ + render_footer()

    # 7. tesekkurler.html (Checklist #14: Teşekkür Sayfası)
    h_tsk = render_head(
        "Talebiniz Alındı - Teşekkür Ederiz | Bulgan Hurdacılık",
        "Hurda fiyat teklifi ve ekspertiz talebiniz başarıyla alındı. Saha ekibimiz en kısa sürede sizinle iletişime geçecektir.",
        "tesekkurler.html"
    )
    pages["tesekkurler.html"] = h_tsk + render_header("") + f"""
    <section class="section" style="text-align:center; padding:80px 0;">
      <div class="container" style="max-width:720px;">
        <div class="region-tag" style="border-color:var(--green-main); color:var(--green-bright);">✅ TALEBİNİZ BAŞARIYLA ALINDI</div>
        <h1 class="hero-title" style="font-size:2.6rem; margin-bottom:14px;">
          Teşekkür Ederiz! <span class="gold-highlight">Ekibimiz Sizi Hemen Arayacak</span>
        </h1>
        <p class="hero-lead" style="margin:0 auto 24px;">
          Ekspertiz ve fiyat talebiniz Mardin / Kızıltepe merkez operasyon birimimize iletildi. Beklemeden anında fotoğraf gönderip saniyeler içinde nakit teklif almak isterseniz aşağıdaki WhatsApp butonuna tıklayabilirsiniz.
        </p>
        <div class="hero-cta-row" style="justify-content:center;">
          <a href="https://wa.me/905459043834?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20web%20sitenizden%20teklif%20formu%20doldurdum.%20Hurdalar%C4%B1m%C4%B1n%20bilgisi%3A" target="_blank" rel="noopener" class="btn btn-green">💬 Talebi WhatsApp'tan Hızlandır</a>
          <a href="tel:+905459043834" class="btn btn-gold">📞 Doğrudan Ara: 0545 904 38 34</a>
          <a href="/" class="btn btn-outline">🏠 Ana Sayfaya Dön</a>
        </div>
      </div>
    </section>
    """ + render_footer()

    # 8. gizlilik-politikasi.html (Checklist #15: KVKK & Gizlilik Politikası)
    h_giz = render_head(
        "Gizlilik Politikası ve KVKK Aydınlatma Metni | Bulgan Hurdacılık",
        "Bulgan Hurdacılık & Geri Dönüşüm 6698 sayılı KVKK kapsamında kişisel verilerin korunması, işlenmesi ve gizlilik politikası.",
        "gizlilik-politikasi.html"
    )
    pages["gizlilik-politikasi.html"] = h_giz + render_header("") + """
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Gizlilik Politikası ve KVKK</span></div>
        <h1 class="hero-title" style="font-size:2.2rem;">Gizlilik Politikası ve <span class="gold-highlight">KVKK Aydınlatma Metni</span></h1>
      </div>
    </section>
    <section class="section">
      <div class="container prose-content" style="max-width:920px;">
        <h2>1. Veri Sorumlusu Kimliği</h2>
        <p>6698 sayılı Kişisel Verilerin Korunması Kanunu (“KVKK”) uyarınca, kişisel verileriniz veri sorumlusu sıfatıyla <strong>Bulgan Hurdacılık & Geri Dönüşüm</strong> (Adres: Atatürk Mahallesi, Kızıltepe / Mardin, Tel: 0545 904 38 34, E-posta: bulganorhan19@gmail.com) tarafından aşağıda açıklanan kapsamda işlenmektedir.</p>
        <h2>2. Toplanan Kişisel Veriler ve İşleme Amaçları</h2>
        <p>Web sitemiz (bulgangeridonusum.com.tr) üzerindeki teklif formları, canlı hurda hesaplama aracı, telefon veya WhatsApp iletişim kanalları aracılığıyla paylaştığınız ad-soyad, telefon numarası, konum ve hurda malzeme bilgileri; yalnızca size fiyat teklifi sunulması, adresinize mobil tartım aracı yönlendirilmesi ve ticari alım-satım sürecinin yürütülmesi amacıyla işlenir.</p>
        <h2>3. Kişisel Verilerin Aktarımı ve Güvenliği</h2>
        <p>Paylaştığınız iletişim ve konum verileri üçüncü şahıs reklam veya pazarlama firmalarıyla kesinlikle paylaşılmaz. Sitemiz SSL/TLS şifreleme ve Cloudflare güvenlik duvarı ile korunmaktadır.</p>
        <h2>4. Çerez (Cookie) Kullanımı</h2>
        <p>Sitemizde kullanıcı tercihlerinizi hatırlamak ve sayfa performansını ölçümlemek amacıyla zorunlu ve analitik çerezler kullanılmaktadır. Çerez tercihlerinizi dilediğiniz zaman alt kısımdaki çerez yönetim panelinden değiştirebilirsiniz.</p>
        <h2>5. KVKK Madde 11 Kapsamındaki Haklarınız</h2>
        <p>KVKK’nın 11. maddesi uyarınca kişisel verilerinizin işlenip işlenmediğini öğrenme, düzeltilmesini veya silinmesini talep etme hakkına sahipsiniz. Taleplerinizi <strong>bulganorhan19@gmail.com</strong> adresine iletebilirsiniz.</p>
      </div>
    </section>
    """ + render_footer()

    # 9. kullanim-kosullari.html (Checklist #16: Kullanım Koşulları)
    h_kul = render_head(
        "Kullanım Koşulları ve Hizmet Şartları | Bulgan Hurdacılık",
        "bulgangeridonusum.com.tr web sitesi kullanım koşulları, günlük borsa hurda fiyatlandırma esasları ve saha tartım şartları.",
        "kullanim-kosullari.html"
    )
    pages["kullanim-kosullari.html"] = h_kul + render_header("") + """
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Kullanım Koşulları</span></div>
        <h1 class="hero-title" style="font-size:2.2rem;">Web Sitesi <span class="gold-highlight">Kullanım Koşulları ve Hizmet Şartları</span></h1>
      </div>
    </section>
    <section class="section">
      <div class="container prose-content" style="max-width:920px;">
        <h2>1. Genel Hükümler</h2>
        <p>Bu web sitesini (bulgangeridonusum.com.tr) kullanan tüm ziyaretçiler aşağıdaki kullanım koşullarını kabul etmiş sayılır. Sitedeki tüm görsel, logo (Bulgan Hurdacılık) ve yazılı içeriklerin telif hakları Bulgan Hurdacılık & Geri Dönüşüm'e aittir.</p>
        <h2>2. Fiyat Listesi ve Canlı Hesaplama Aracı Koşulları</h2>
        <p>Sitemizde yer alan hurda fiyatları ve canlı hesaplama aracı verileri, Londra Metal Borsası (LME) ve Türkiye metal piyasası verilerinden otomatik olarak çekilip %20 operasyonel iskonto düşülerek bilgilendirme amacıyla sunulmaktadır. Hurdanın saflık oranı, fire durumu, tonajı ve nakliye mesafesine göre nihai alım fiyatı yerinde yapılan hassas dijital kantar tartımı ve ekspertiz sonrasında kesinleşir.</p>
        <h2>3. Saha Tartım ve Ödeme Esasları</h2>
        <p>Alımı yapılan tüm hurda metaller müşterinin nezaretinde dijital kantarla tartılır ve mutabık kalınan tutar teslimat anında nakit veya banka havalesi/EFT/FAST yoluyla ödenir.</p>
      </div>
    </section>
    """ + render_footer()

    # 10. blog.html & Blog Posts
    blog_cards = ""
    for b_slug, b_title, b_img, b_desc in BLOG_POSTS:
        blog_cards += f"""
        <article class="metal-card">
          <a href="/{b_slug}" class="metal-card-img">
            <img src="/{b_img}" alt="{b_title}" width="800" height="520" loading="lazy">
          </a>
          <div class="metal-card-body">
            <h3 class="metal-card-title"><a href="/{b_slug}">{b_title}</a></h3>
            <p class="metal-card-desc">{b_desc}</p>
            <div class="metal-card-footer">
              <span class="metal-start-price">Rehber & Analiz</span>
              <a href="/{b_slug}" class="btn btn-outline" style="padding:7px 14px; font-size:0.82rem;">Devamını Oku →</a>
            </div>
          </div>
        </article>
        """
        b_head = render_head(f"{b_title} | Bulgan Hurdacılık Blog", b_desc, b_slug)
        pages[b_slug] = b_head + render_header("blog.html") + f"""
        <section class="page-hero">
          <div class="container">
            <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <a href="/blog.html">Blog</a> <span>/</span> <span>{b_title}</span></div>
            <h1 class="hero-title" style="font-size:2.1rem;">{b_title}</h1>
            <p class="hero-lead" style="margin-bottom:0;">{b_desc}</p>
          </div>
        </section>
        <section class="section">
          <div class="container hero-grid">
            <div class="prose-content">
              <img src="/{b_img}" alt="{b_title}" width="800" height="520" style="border-radius:12px; border:2px solid var(--gold-main); margin-bottom:20px;">
              <h2>Mardin ve Güneydoğu Anadolu Geri Dönüşüm Sektör Rehberi</h2>
              <p>{b_desc}</p>
              <p><strong>Bulgan Hurdacılık & Geri Dönüşüm</strong> olarak Mardin, Kızıltepe, Artuklu, Midyat, Nusaybin, Diyarbakır, Şanlıurfa, Gaziantep ve Batman'daki tüm sanayi kuruluşlarına ve bireysel müşterilerimize en güncel borsa bilgileriyle rehberlik ediyoruz.</p>
              {render_price_tables()}
            </div>
            {render_calculator_widget()}
          </div>
        </section>
        """ + render_footer()

    h_blog = render_head(
        "Geri Dönüşüm Blog & Hurda Piyasası Rehberi | Bulgan Hurdacılık",
        "Hurda kablo bakır oranı hesaplama, LME metal borsası analizleri ve Mardin & Güneydoğu Anadolu geri dönüşüm sektörü rehber yazıları.",
        "blog.html"
    )
    pages["blog.html"] = h_blog + render_header("blog.html") + f"""
    <section class="page-hero">
      <div class="container">
        <div class="breadcrumb"><a href="/">Ana Sayfa</a> <span>/</span> <span>Blog & Rehber</span></div>
        <h1 class="hero-title" style="font-size:2.4rem;">Geri Dönüşüm <span class="gold-highlight">Rehberi & Piyasa Analizleri</span></h1>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="cards-grid">{blog_cards}</div>
      </div>
    </section>
    """ + render_footer()

    return pages


def generate_all():
    # 1. Remove ALL old HTML files and temporary scripts in ROOT first
    old_htmls = glob.glob(os.path.join(ROOT, "*.html"))
    old_names_removed = []
    for f in old_htmls:
        old_names_removed.append(os.path.basename(f))
        os.remove(f)
    print(f"Removed {len(old_names_removed)} old HTML files.")

    # Remove old junk files in ROOT
    for junk in ["3.0", "closedhand.cur", "closedhand_1.cur", "closedhand_2.cur", "js_1", "js_2", "js_3",
                 "analyze_links.py", "create_regional_pages.py", "extract_seo.py", "generate_sitemap.py",
                 "inspect_kadikoy.py", "optimize_index_seo.py", "update_index_grid_menu.py"]:
        jp = os.path.join(ROOT, junk)
        if os.path.exists(jp):
            os.remove(jp)

    all_pages = {}
    all_pages["index.html"] = build_index_page()
    all_pages["hurda-fiyatlari.html"] = build_hurda_fiyatlari_page()

    for cat in CATEGORIES:
        all_pages[cat["slug"]] = build_category_page(cat)

    for slug, name, lat, lon, desc, nhs in MARDIN_DISTRICTS:
        all_pages[slug] = build_regional_page(slug, name, "TR-47", lat, lon, desc, nhs, is_mardin=True)

    for slug, name, geo_reg, lat, lon, desc, nhs in GUNEYDOGU_PROVINCES:
        all_pages[slug] = build_regional_page(slug, name, geo_reg, lat, lon, desc, nhs, is_mardin=False)

    for slug, title_txt, cat_id, img_webp, img_jpg, desc_txt in EXTRA_SERVICE_PAGES:
        all_pages[slug] = build_extra_service_page(slug, title_txt, cat_id, img_webp, img_jpg, desc_txt)

    all_pages.update(build_static_corporate_pages())

    for fname, html_content in all_pages.items():
        with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
            f.write(html_content)

    print(f"Generated {len(all_pages)} brand-new HTML pages.")

    # 2. Generate sitemap.xml (Checklist #7)
    today_iso = PRICES_DATA["dateIso"]
    sitemap_entries = []
    for fname in sorted(all_pages.keys()):
        if fname in ("404.html", "tesekkurler.html"):
            continue
        loc = "https://bulgangeridonusum.com.tr/" if fname == "index.html" else f"https://bulgangeridonusum.com.tr/{fname}"
        prio = "1.0" if fname == "index.html" else ("0.95" if "mardin" in fname or "kiziltepe" in fname or fname == "hurda-fiyatlari.html" else "0.85")
        sitemap_entries.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{prio}</priority>
  </url>""")

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sitemap_entries) + "\n</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    # 3. Generate robots.txt (Checklist #6)
    robots_txt = """User-agent: *
Allow: /
Disallow: /admin.html
Disallow: /tesekkurler.html

Sitemap: https://bulgangeridonusum.com.tr/sitemap.xml
"""
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)

    # 4. Generate site.webmanifest (Checklist #5)
    manifest = {
        "name": "Bulgan Hurdacılık & Geri Dönüşüm - Mardin & Güneydoğu",
        "short_name": "Bulgan Hurdacılık",
        "description": "Mardin, Kızıltepe ve Güneydoğu Anadolu güncel hurda fiyatları, canlı hurda hesaplama ve adresten nakit hurda alımı.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0d1015",
        "theme_color": "#e5a913",
        "icons": [
            {"src": "/images/favicon-32x32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/images/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": "/images/favicon-512.png", "sizes": "512x512", "type": "image/png"}
        ]
    }
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 5. Generate _headers (Security Headers & Performance Caching)
    headers_content = """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(self), microphone=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

/images/*
  Cache-Control: public, max-age=31536000, immutable

/css/*
  Cache-Control: public, max-age=604800

/js/*
  Cache-Control: public, max-age=86400
"""
    with open(os.path.join(ROOT, "_headers"), "w", encoding="utf-8") as f:
        f.write(headers_content)

    # 6. Generate _redirects (301 Redirects from all old Istanbul/Marmara URLs to Mardin!)
    old_istanbul_slugs = [n for n in old_names_removed if n not in all_pages and n.endswith("-hurdaci.html")]
    redirect_lines = [f"/{slug} /mardin-hurdaci.html 301" for slug in sorted(old_istanbul_slugs)]
    redirect_lines.append("/index_1.html / 301")
    redirect_lines.append("/index_2.html / 301")
    redirect_lines.append("/index_3.html / 301")
    redirect_lines.append("/index_4.html / 301")
    with open(os.path.join(ROOT, "_redirects"), "w", encoding="utf-8") as f:
        f.write("\n".join(redirect_lines) + "\n")

    print(f"Created sitemap.xml ({len(sitemap_entries)} URLs), robots.txt, site.webmanifest, _headers, and _redirects ({len(redirect_lines)} 301 rules).")


if __name__ == "__main__":
    generate_all()
