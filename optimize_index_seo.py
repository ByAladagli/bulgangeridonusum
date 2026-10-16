import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
filepath = r'C:\AI-Tools\cloned-sites\bulgangeridonusum\index.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# 1. Update Title Tag
old_title_pattern = r'<title>.*?</title>'
new_title = '<title>Mardin Hurdacı | Bulgan Geri Dönüşüm - Kızıltepe & Mardin Hurda Alımı - 0545 904 38 34</title>'
c = re.sub(old_title_pattern, new_title, c, count=1, flags=re.IGNORECASE)

# 2. Update Meta Descriptions and Titles in <head>
# Standard meta description
c = re.sub(r'<meta name="description" content="[^"]*">', 
           '<meta name="description" content="Mardin hurdacı ve kurumsal geri dönüşüm hizmeti. Kızıltepe, Artuklu ve tüm Mardin genelinde yerinde hassas dijital tartım, anında nakit ödeme ile bakır, demir, kablo, alüminyum ve sarı hurda alımı. Hemen arayın: 0545 904 38 34.">', 
           c, count=1, flags=re.IGNORECASE)

# OpenGraph Description
c = re.sub(r'<meta property="og:description" content="[^"]*">', 
           '<meta property="og:description" content="Mardin ve Kızıltepe kurumsal hurdacı hizmeti. Adresten nakit ödeme ile hurda bakır, demir, alüminyum, kablo alımı. Tel: 0545 904 38 34.">', 
           c, count=1, flags=re.IGNORECASE)

# Twitter Description
c = re.sub(r'<meta name="twitter:description" content="[^"]*">', 
           '<meta name="twitter:description" content="Mardin ve Kızıltepe kurumsal hurdacı hizmeti. Adresten nakit ödeme ile hurda alımı. Tel: 0545 904 38 34.">', 
           c, count=1, flags=re.IGNORECASE)

# OG Title & Twitter Title
c = re.sub(r'<meta property="og:title" content="[^"]*">',
           '<meta property="og:title" content="Mardin Hurdacı | Bulgan Geri Dönüşüm - Kızıltepe Hurda Alımı">',
           c, count=1, flags=re.IGNORECASE)
c = re.sub(r'<meta name="twitter:title" content="[^"]*">',
           '<meta name="twitter:title" content="Mardin Hurdacı | Bulgan Geri Dönüşüm - Kızıltepe Hurda Alımı">',
           c, count=1, flags=re.IGNORECASE)

# Add Geo Meta Tags & Keywords before </head> if not present
geo_meta = '''
<meta name="keywords" content="mardin hurdacı, kızıltepe hurdacı, mardin hurda alımı, kızıltepe hurda alımı, bulgan geri dönüşüm, mardin bakır hurda, mardin demir hurda, artuklu hurdacı, midyat hurdacı, nusaybin hurdacı, mardin hurda fiyatları">
<meta name="geo.region" content="TR-47">
<meta name="geo.placename" content="Kızıltepe, Mardin">
<meta name="geo.position" content="37.1936;40.5858">
<meta name="ICBM" content="37.1936, 40.5858">
<link rel="canonical" href="https://bulgangeridonusum.com.tr/">
'''
if '<meta name="geo.region"' not in c:
    c = c.replace('</head>', geo_meta + '\n</head>', 1)

# 3. Update Hero H1 and Subtitle
old_h1_text = 'İstanbul <span>Hurdacı</span> &amp; En Yakın Kurumsal Geri Dönüşüm'
new_h1_text = 'Mardin <span>Hurdacı</span> &amp; Kızıltepe En Yakın Kurumsal Geri Dönüşüm'
c = c.replace(old_h1_text, new_h1_text)

# Also check without entity just in case
c = c.replace('İstanbul <span>Hurdacı</span> & En Yakın Kurumsal Geri Dönüşüm',
              'Mardin <span>Hurdacı</span> & Kızıltepe En Yakın Kurumsal Geri Dönüşüm')

# Update hero subtitle
old_hero_sub = 'Bakır, kablo, alüminyum, krom ve demir hurdalarınızı <strong>güncel LME borsa fiyatından</strong>, adresinizde dijital kantarla tartıp <strong>anında nakit ödeme</strong> ile satın alıyoruz.'
new_hero_sub = 'Mardin, Kızıltepe ve tüm çevre ilçelerde bakır, kablo, alüminyum, sarı, krom ve demir hurdalarınızı <strong>güncel borsa değerinde</strong>, adresinizde hassas dijital kantarla tartıp <strong>anında nakit ödeme</strong> ile satın alıyoruz.'
c = c.replace(old_hero_sub, new_hero_sub)

# 4. Update Schema JSON-LD Block 0
old_service_schema = '''{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Fabrika Tesis Yıkım Söküm ve İkinci El Malzeme Alımı",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Bulgan Geri Dönüşüm - Dev Metal Geri Dönüşüm",
    "url": "https://bulgangeridonusum.com.tr"
  },
  "areaServed": {
    "@type": "AdministrativeArea",
    "name": "İstanbul & Marmara Bölgesi"
  },'''

new_service_and_local_business_schema = '''{
  "@context": "https://schema.org",
  "@type": ["RecyclingCenter", "LocalBusiness"],
  "@id": "https://bulgangeridonusum.com.tr/#organization",
  "name": "Bulgan Geri Dönüşüm - Mardin Hurdacı",
  "alternateName": "Mardin Kızıltepe Bulgan Hurdacılık ve Geri Dönüşüm",
  "url": "https://bulgangeridonusum.com.tr",
  "logo": "https://bulgangeridonusum.com.tr/images/1-logo.png",
  "image": "https://bulgangeridonusum.com.tr/images/1-logo.png",
  "telephone": "+905459043834",
  "email": "bulganorhan19@gmail.com",
  "priceRange": "₺₺",
  "currenciesAccepted": "TRY",
  "paymentAccepted": "Cash, Credit Card, Bank Transfer",
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
    "latitude": 37.1936,
    "longitude": 40.5858
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": [
      "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ],
    "opens": "07:00",
    "closes": "21:00"
  },
  "areaServed": [
    {"@type": "AdministrativeArea", "name": "Mardin"},
    {"@type": "AdministrativeArea", "name": "Kızıltepe"},
    {"@type": "AdministrativeArea", "name": "Artuklu"},
    {"@type": "AdministrativeArea", "name": "Midyat"},
    {"@type": "AdministrativeArea", "name": "Nusaybin"},
    {"@type": "AdministrativeArea", "name": "Derik"},
    {"@type": "AdministrativeArea", "name": "Mazıdağı"},
    {"@type": "AdministrativeArea", "name": "Dargeçit"},
    {"@type": "AdministrativeArea", "name": "Savur"},
    {"@type": "AdministrativeArea", "name": "Yeşilli"},
    {"@type": "AdministrativeArea", "name": "Ömerli"}
  ],
  "description": "Mardin ve Kızıltepe genelinde adresten hurda demir, bakır, alüminyum, kablo, sarı pirinç alımı, fabrika sökümü ve yıkım hizmetleri.",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Mardin Hurda Alım Hizmetleri",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Mardin Hurda Bakır Alımı"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Mardin Hurda Kablo Alımı"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Mardin Hurda Demir Alımı"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Mardin Hurda Alüminyum Alımı"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kızıltepe Fabrika ve Tesis Yıkım Söküm"}}
    ]
  }'''

# Replace the beginning of Service schema with full LocalBusiness/RecyclingCenter
if old_service_schema in c:
    # Find full script tag
    start_ld = c.find(old_service_schema)
    end_ld = c.find('</script>', start_ld)
    c = c[:start_ld] + new_service_and_local_business_schema + '\n}' + c[end_ld:]
    print("Replaced Schema Block 0 successfully.")
else:
    print("Warning: old_service_schema snippet not found, searching with loose match...")
    # fallback replacement
    c = c.replace('"İstanbul & Marmara Bölgesi"', '"Mardin & Kızıltepe Bölgesi"')
    c = c.replace('Bulgan Geri Dönüşüm - Dev Metal Geri Dönüşüm', 'Bulgan Geri Dönüşüm - Mardin Hurdacı')

# 5. Update FAQ JSON-LD Block
c = c.replace('İstanbul genelinde adresten hurda alım süreci nasıl işler?',
              'Mardin ve Kızıltepe genelinde adresten hurda alım süreci nasıl işler?')
c = c.replace('Mardin genelinde adresten hurda alım süreci nasıl işler?',
              'Mardin ve Kızıltepe genelinde adresten hurda alım süreci nasıl işler?')

# 6. Update Visible Accordion FAQ in HTML
c = c.replace('<summary>İstanbul genelinde adresten hurda alım süreci nasıl işler?</summary>',
              '<summary>Mardin ve Kızıltepe genelinde adresten hurda alım süreci nasıl işler?</summary>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated index.html base SEO tags and schema successfully.")
