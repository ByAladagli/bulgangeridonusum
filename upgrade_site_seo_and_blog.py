import json
import os
import re
import sys
import build_complete_site as bcs

sys.stdout.reconfigure(encoding='utf-8')

ROOT = bcs.ROOT
DOMAIN = bcs.DOMAIN
BRAND_NAME = bcs.BRAND_NAME
PHONE_DISPLAY = bcs.PHONE_DISPLAY
PHONE_TEL = bcs.PHONE_TEL
PHONE_WA = bcs.PHONE_WA
EMAIL = bcs.EMAIL
ADDRESS = bcs.ADDRESS

# All extra URLs that exist in the repo or Google index — each gets its own 100% unique Title, Meta Desc, Keywords & Content!
ADDITIONAL_SERVICE_PAGES = [
    {
        "slug": "bina-yikimi.html",
        "cat_id": "demir",
        "image": "images/sokulecek.png.webp",
        "title": "Hurda Karşılığı Bina Yıkımı Mardin & Güneydoğu | Bulgan Hurdacılık",
        "h1": "Mardin ve Güneydoğu Anadolu'da Hurda Karşılığı Bina ve Tesis Yıkımı",
        "desc": "Mardin, Kızıltepe, Artuklu, Midyat, Diyarbakır ve Şanlıurfa'da hurda demir ve metal karşılığı güvenli bina yıkımı, fabrika bozumu ve hafriyat ayrıştırma hizmeti.",
        "keywords": "mardin bina yıkımı, hurda karşılığı yıkım mardin, kızıltepe bina yıkım hurdacısı, diyarbakır hurda karşılığı bina yıkımı, çıkma yıkım demiri alımı"
    },
    {
        "slug": "celik-cati-sokumu.html",
        "cat_id": "demir",
        "image": "images/demir.webp",
        "title": "Çelik Çatı ve Hangar Sökümü Mardin, Diyarbakır, Gaziantep | Bulgan",
        "h1": "Endüstriyel Çelik Çatı, Hangar ve Konstrüksiyon Sökümü",
        "desc": "Mardin OSB, Kızıltepe, Diyarbakır, Şanlıurfa ve Gaziantep'te fabrika çelik çatıları, hangarlar, NPU/NPI/HEA kolon ve trapez sacların vinçli kesim ve nakit alımı.",
        "keywords": "çelik çatı sökümü mardin, hangar sökümü güneydoğu, çıkma çelik konstrüksiyon alımı, kızıltepe fabrika çatı sökümü, gaziantep çelik çatı hurdası"
    },
    {
        "slug": "sokulecek-hurda-fiyatlari.html",
        "cat_id": "demir",
        "image": "images/sokulecek.png.webp",
        "title": "Sökülecek Tesis, Makine Parkuru ve Kazan Dairesi Hurda Fiyatları 2026",
        "h1": "Sökülecek Fabrika, Kazan Dairesi ve Ağır Makine Hurdası Alımı",
        "desc": "Mardin ve Güneydoğu Anadolu'da yerinde oksijen/plazma kesimi gerektiren kazan dairesi, çırçır ve un fabrikası makine parkuru sökülecek hurda fiyatları.",
        "keywords": "sökülecek hurda fiyatları, kazan dairesi sökümü mardin, fabrika makine hurdası alımı, çırçır fabrikası söküm hurdası, oksijen kesim hurdacı"
    },
    {
        "slug": "hurda-chiller-grubu-sogutma-sistemleri-fiyatlari-alimi.html",
        "cat_id": "klima",
        "image": "images/chiller.png.webp",
        "title": "Hurda Chiller Soğutma Grubu Alımı & 2026 Fiyatları | Mardin & Güneydoğu",
        "h1": "Hurda Chiller Grubu, VRF ve Merkezi Soğutma Sistemleri Sökümü & Alımı",
        "desc": "Otel, hastane, AVM ve fabrikalardan çıkan su/hava soğutmalı hurda chiller grupları, eşanjör bakırları ve kompresörlerin Mardin ve Güneydoğu'da nakit alımı.",
        "keywords": "hurda chiller fiyatları, chiller soğutma grubu hurdası, mardin chiller hurdası alımı, diyarbakır merkezi klima hurdası, chiller eşanjör bakırı"
    },
    {
        "slug": "2-el-endustriyel-mutfak-malzemeleri-alimi.html",
        "cat_id": "paslanmaz",
        "image": "images/endustriyel-mutfak.webp",
        "title": "Endüstriyel Mutfak Hurdası & Paslanmaz Krom Ekipman Alımı | Bulgan",
        "h1": "Otel, Yemekhane ve Restoran Endüstriyel Mutfak Hurdası Alımı",
        "desc": "Mardin, Midyat, Artuklu, Diyarbakır, Gaziantep ve Şanlıurfa'da 304 kalite paslanmaz krom tezgah, sanayi fırını, davlumbaz ve kazan hurdalarının peşin alımı.",
        "keywords": "endüstriyel mutfak hurdası, paslanmaz tezgah hurdası mardin, krom mutfak malzemeleri alımı, lokanta otel mutfak hurdası, 304 kalite krom hurda"
    },
    {
        "slug": "evrak-imhasi.html",
        "cat_id": "kagit",
        "image": "images/kagit.webp",
        "title": "Kurumsal Arşiv & Evrak İmhası Hizmeti Mardin & Güneydoğu | Bulgan",
        "h1": "KVKK Uyumlu Kurumsal Arşiv, Belge ve Kağıt Hurdası İmha & Alım Hizmeti",
        "desc": "Mardin, Kızıltepe, Diyarbakır ve Şanlıurfa'daki kamu kurumları, bankalar, hastaneler ve şirketler için tutanaklı arşiv kağıt hurdası alımı ve güvenli evrak imhası.",
        "keywords": "mardin arşiv imha, kurumsal evrak imhası güneydoğu, hurda kağıt arşiv alımı kızıltepe, tutanaklı belge imhası, a4 evrak hurdası fiyatı"
    },
    {
        "slug": "karton-hurda-fiyatlari.html",
        "cat_id": "kagit",
        "image": "images/karton.webp",
        "title": "Karton & Oluklu Mukavva Hurda Fiyatları 2026 | Mardin Tonajlı Alım",
        "h1": "Karton, Koli ve Oluklu Mukavva Hurdası Fiyatları — Tonajlı Pres Alım",
        "desc": "Mardin, Kızıltepe, Nusaybin ve Güneydoğu Anadolu genelinde zincir market, tekstil ve gıda fabrikalarından çıkan presli/dökme koli karton hurdası alımı.",
        "keywords": "karton hurda fiyatları 2026, mardin hurda karton alımı, kızıltepe presli karton fiyatı, oluklu mukavva hurdası kilosu, market koli hurdası"
    },
    {
        "slug": "hurda-alan-yerler.html",
        "cat_id": "bakir",
        "image": "images/bakir.webp",
        "title": "Mardin ve Güneydoğu Anadolu Hurda Alan Yerler | Merkez Kantar Rehberi",
        "h1": "Mardin, Kızıltepe ve Güneydoğu Anadolu'da Nakit Hurda Alan Yerler",
        "desc": "Mardin (Kızıltepe, Artuklu, Midyat, Nusaybin), Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman ve Kilis'te adresten nakit hurda alan kantar merkezi.",
        "keywords": "mardin hurda alan yerler, kızıltepe hurda alan firmalar, güneydoğu hurda alım merkezi, en yakın hurdacı mardin, nakit hurda alan kantar"
    },
    {
        "slug": "hurda-cesitleri.html",
        "cat_id": "bakir",
        "image": "images/aluminyum.webp",
        "title": "Alımını Yaptığımız Hurda Metal Çeşitleri & Kalite Sınıfları | Bulgan",
        "h1": "Metal ve Endüstriyel Hurda Çeşitleri: Bakır, Kablo, Demir, Krom ve Sarı",
        "desc": "Bulgan Hurdacılık tarafından Mardin ve Güneydoğu Anadolu'da satın alınan 15 ana hurda grubu ve 75 alt metal kalitesinin teknik sınıflandırma rehberi.",
        "keywords": "hurda çeşitleri nelerdir, metal hurda sınıfları, soyma bakır kırkambar farkı, dkp ekstra demir çeşitleri, sarı pirinç ms58 çeşitleri"
    },
    {
        "slug": "teklif-formu.html",
        "cat_id": "bakir",
        "image": "images/bakir.webp",
        "title": "Online Hurda Ekspertiz, Fiyat Teklifi & Mobil Kantar Çağrı Formu",
        "h1": "Hızlı Hurda Fiyat Teklifi ve Adresten Mobil Kantar Talep Formu",
        "desc": "Mardin ve Güneydoğu Anadolu'daki hurdalarınız için online fiyat teklifi alın. Formunuz doğrudan bulganorhan19@gmail.com kantar merkezimize ve saha şefimize ulaşır.",
        "keywords": "hurda fiyat teklifi al, mardin mobil kantar çağır, online hurda ekspertiz formu, bulgan hurdacılık teklif formu, whatsapp hurda fiyat"
    }
]


def generate_page_keywords(slug, title, h1):
    base = ["bulgan hurdacılık", "bulgan geri dönüşüm", "kızıltepe hurdacı", "mardin hurdacı"]
    clean_words = re.sub(r"[^\w\sğüşıöçĞÜŞİÖÇ]", " ", f"{title} {h1}".lower()).split()
    stop = {"ve", "ile", "için", "ne", "kadar", "nedir", "tüm", "en", "bir", "bu", "de", "da", "2026"}
    filtered = []
    for w in clean_words:
        if len(w) > 2 and w not in stop and w not in filtered:
            filtered.append(w)
    phrases = [
        " ".join(filtered[:3]),
        " ".join(filtered[1:4]),
        f"{filtered[0]} mardin" if filtered else "mardin hurda fiyatları",
        f"{filtered[0]} kızıltepe" if filtered else "kızıltepe kantar",
        slug.replace(".html", "").replace("-", " ")
    ]
    combined = []
    for item in phrases + base:
        item = item.strip()
        if item and item not in combined:
            combined.append(item)
    return ", ".join(combined[:10])


def enhanced_build_json_ld(slug, title, desc, breadcrumbs, faqs=None, product_cat=None, geo_info=None, date_iso="2026-11-03", is_blog=False):
    lat = geo_info["lat"] if geo_info else "37.1939"
    lng = geo_info["lng"] if geo_info else "40.5861"
    area_name = geo_info["name"] if geo_info else "Mardin ve Güneydoğu Anadolu Bölgesi"

    graph = [
        {
            "@type": ["RecyclingCenter", "LocalBusiness", "Organization"],
            "@id": f"{DOMAIN}/#organization",
            "name": BRAND_NAME,
            "legalName": "Bulgan Hurdacılık ve Metal Geri Dönüşüm Ticaret",
            "alternateName": ["Bulgan Hurdacılık Mardin", "Bulgan Geri Dönüşüm Kızıltepe"],
            "url": DOMAIN,
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/images/bulgan-logo.webp",
                "width": 420,
                "height": 146
            },
            "image": [
                f"{DOMAIN}/images/og-cover.jpg",
                f"{DOMAIN}/images/icon-512.png"
            ],
            "telephone": PHONE_TEL,
            "email": EMAIL,
            "priceRange": "₺₺₺",
            "currenciesAccepted": "TRY, USD, EUR",
            "paymentAccepted": "Nakit, Banka Havalesi, FAST, EFT",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Atatürk Mahallesi, İpekyolu Sanayi Aksı",
                "addressLocality": "Kızıltepe",
                "addressRegion": "Mardin",
                "postalCode": "47400",
                "addressCountry": "TR"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": float(lat),
                "longitude": float(lng)
            },
            "hasMap": "https://www.google.com/maps/search/?api=1&query=Atat%C3%BCrk+Mahallesi+K%C4%B1z%C4%B1ltepe+Mardin+Bulgan+Hurdac%C4%B1l%C4%B1k",
            "sameAs": [
                f"https://wa.me/{PHONE_WA}",
                "https://www.google.com/maps/search/?api=1&query=Bulgan+Hurdac%C4%B1l%C4%B1k+Atat%C3%BCrk+Mahallesi+K%C4%B1z%C4%B1ltepe+Mardin"
            ],
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "bestRating": "5",
                "worstRating": "1",
                "ratingCount": "148",
                "reviewCount": "148"
            },
            "areaServed": [
                {"@type": "AdministrativeArea", "name": area_name},
                {"@type": "City", "name": "Mardin"},
                {"@type": "City", "name": "Kızıltepe"},
                {"@type": "City", "name": "Artuklu"},
                {"@type": "City", "name": "Midyat"},
                {"@type": "City", "name": "Nusaybin"},
                {"@type": "City", "name": "Derik"},
                {"@type": "City", "name": "Mazıdağı"},
                {"@type": "City", "name": "Dargeçit"},
                {"@type": "City", "name": "Savur"},
                {"@type": "City", "name": "Yeşilli"},
                {"@type": "City", "name": "Ömerli"},
                {"@type": "City", "name": "Diyarbakır"},
                {"@type": "City", "name": "Şanlıurfa"},
                {"@type": "City", "name": "Gaziantep"},
                {"@type": "City", "name": "Batman"},
                {"@type": "City", "name": "Şırnak"},
                {"@type": "City", "name": "Siirt"},
                {"@type": "City", "name": "Adıyaman"},
                {"@type": "City", "name": "Kilis"}
            ],
            "openingHoursSpecification": [
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "07:30",
                    "closes": "21:00"
                }
            ]
        },
        {
            "@type": "WebSite",
            "@id": f"{DOMAIN}/#website",
            "url": DOMAIN,
            "name": BRAND_NAME,
            "inLanguage": "tr-TR",
            "publisher": {"@id": f"{DOMAIN}/#organization"}
        },
        {
            "@type": "WebPage",
            "@id": f"{DOMAIN}/{slug if slug != 'index.html' else ''}#webpage",
            "url": f"{DOMAIN}/{slug if slug != 'index.html' else ''}",
            "name": title,
            "description": desc,
            "inLanguage": "tr-TR",
            "dateModified": date_iso,
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "about": {"@id": f"{DOMAIN}/#organization"},
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".hero-lead", ".page-banner p", ".article-sheet h2"]
            }
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": idx + 1,
                    "name": b_name,
                    "item": f"{DOMAIN}/{b_slug if b_slug != 'index.html' else ''}"
                }
                for idx, (b_name, b_slug) in enumerate(breadcrumbs)
            ]
        }
    ]

    if is_blog:
        graph.append({
            "@type": "BlogPosting",
            "headline": title,
            "description": desc,
            "datePublished": date_iso,
            "dateModified": date_iso,
            "author": {"@id": f"{DOMAIN}/#organization"},
            "publisher": {"@id": f"{DOMAIN}/#organization"},
            "mainEntityOfPage": f"{DOMAIN}/{slug}"
        })

    if product_cat:
        prices_list = [it["price"] for it in product_cat["items"]]
        low_p = min(prices_list)
        high_p = max(prices_list)
        offers_list = [
            {
                "@type": "Offer",
                "name": it["name"],
                "price": f"{it['price']:.2f}",
                "priceCurrency": "TRY",
                "availability": "https://schema.org/InStock",
                "priceValidUntil": "2026-12-31"
            }
            for it in product_cat["items"][:6]
        ]
        graph.append({
            "@type": "Product",
            "name": f"{product_cat['name']} (Mardin & Güneydoğu Net Kantar)",
            "description": product_cat["desc"],
            "image": f"{DOMAIN}/{product_cat['image']}",
            "brand": {"@type": "Brand", "name": BRAND_NAME},
            "offers": {
                "@type": "AggregateOffer",
                "priceCurrency": "TRY",
                "lowPrice": f"{low_p:.2f}",
                "highPrice": f"{high_p:.2f}",
                "offerCount": len(product_cat["items"]),
                "priceValidUntil": "2026-12-31",
                "availability": "https://schema.org/InStock",
                "seller": {"@id": f"{DOMAIN}/#organization"},
                "offers": offers_list
            }
        })

    if faqs:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}
                }
                for q, a in faqs
            ]
        })

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def enhanced_wrap_html_document(slug, title, desc, body_html, json_ld_str, og_image="images/og-cover.jpg", noindex=False, keywords=None):
    canonical = f"{DOMAIN}/" if slug == "index.html" else f"{DOMAIN}/{slug}"
    robots_content = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    kw = keywords or generate_page_keywords(slug, title, desc)
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{kw}">
  <meta name="author" content="{BRAND_NAME}">
  <meta name="publisher" content="{BRAND_NAME} - Kızıltepe / Mardin">
  <meta name="robots" content="{robots_content}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="tr-TR" href="{canonical}">

  <!-- AI Agents, LLM Citation & WebMCP Discovery Links -->
  <link rel="alternate" type="text/markdown" href="/llms.txt" title="AI Summary (llms.txt)">
  <link rel="alternate" type="text/markdown" href="/llms-full.txt" title="Full AI Knowledge Base (llms-full.txt)">
  <link rel="agent-permissions" href="/agent-permissions.json">
  <link rel="mcp-actions" href="/mcp-actions.json">

  <!-- Yeni Kare Amblem Favicon & Uygulama İkonları -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico?v=202611">
  <link rel="icon" type="image/png" sizes="16x16" href="/images/favicon-16x16.png?v=202611">
  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png?v=202611">
  <link rel="icon" type="image/png" sizes="48x48" href="/images/favicon-48x48.png?v=202611">
  <link rel="icon" type="image/png" sizes="192x192" href="/images/icon-192.png?v=202611">
  <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png?v=202611">
  <link rel="manifest" href="/site.webmanifest?v=202611">
  <meta name="theme-color" content="#11151c">

  <!-- Google İşletme Profili (GBP) & Coğrafi Konum Meta Etiketleri -->
  <meta name="geo.region" content="TR-47">
  <meta name="geo.placename" content="Atatürk Mahallesi, Kızıltepe, Mardin">
  <meta name="geo.position" content="37.1939;40.5861">
  <meta name="ICBM" content="37.1939, 40.5861">
  <meta name="DC.title" content="{title}">
  <meta name="DC.description" content="{desc}">
  <meta name="DC.spatial" content="Mardin, Güneydoğu Anadolu, Türkiye">
  <meta name="DC.language" content="tr-TR">

  <!-- Open Graph / WhatsApp / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:site_name" content="{BRAND_NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAIN}/{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{title}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{DOMAIN}/{og_image}">

  <!-- Kurumsal Tipografi -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/bulgan-theme.css?v=202611">

  <script type="application/ld+json">{json_ld_str}</script>
</head>
<body>
  <a href="#mainContent" class="skip-link">Ana İçeriğe Geç</a>
{body_html}
</body>
</html>
"""


def build_blog_index_page(prices):
    slug = "blog.html"
    title = "Mardin & Güneydoğu Hurdacılık Blog ve Sektör Rehberi | Bulgan Hurdacılık"
    desc = "Güneydoğu Anadolu metal geri dönüşüm rehberi: hurda kablo bakır randıman hesabı, dalgıç pompa kablosu alımı, OSB fabrika sökümü ve LME kantar analizleri."

    cards = []
    for post in bcs.BLOG_POSTS:
        cards.append(f"""
        <article class="catalog-item">
          <a href="/{post['slug']}" class="catalog-img-wrap">
            <img src="/{post['image']}" alt="{post['h1']} - Bulgan Hurdacılık" width="480" height="320" loading="lazy">
          </a>
          <div class="catalog-body">
            <h2 class="catalog-title" style="font-size:1.1rem"><a href="/{post['slug']}">{post['h1']}</a></h2>
            <p class="catalog-desc">{post['desc']}</p>
            <div class="catalog-price-strip">
              <span style="color:var(--text-muted);font-size:0.78rem">Güncelleme: {post['date']}</span>
              <a href="/{post['slug']}" style="font-weight:700">Rehberi Oku &rarr;</a>
            </div>
          </div>
        </article>""")

    body = f"""{bcs.render_topbar(prices)}
{bcs.render_header(prices, slug)}
{bcs.render_ticker(prices)}
  <main id="mainContent">
    <section class="page-banner">
      <div class="container">
        <ol class="breadcrumb">
          <li><a href="/index.html">Ana Sayfa</a></li>
          <li>/</li>
          <li>Sektörel Rehber &amp; Blog</li>
        </ol>
        <h1>Mardin ve Güneydoğu Anadolu Metal Geri Dönüşüm Blog &amp; Rehberi</h1>
        <p>{desc}</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="catalog-grid">
{"".join(cards)}
        </div>
      </div>
    </section>
  </main>
{bcs.render_footer(prices)}"""

    json_ld = enhanced_build_json_ld(slug, title, desc, [("Ana Sayfa", "index.html"), ("Blog & Rehber", slug)], date_iso=prices.get("dateIso", "2026-11-03"))
    return enhanced_wrap_html_document(slug, title, desc, body, json_ld)


def build_single_blog_post(post, prices):
    slug = post["slug"]
    cat = next((c for c in prices["categories"] if c["id"] == post["cat_id"]), prices["categories"][0])

    sections_html = "\n".join(
        f"<h2>{sec_title}</h2>\n<p>{sec_body}</p>"
        for sec_title, sec_body in post["sections"]
    )

    cat_rows = "\n".join(
        f'<tr data-item-code="{it["code"]}"><td>{it["name"]}</td><td class="col-market" data-col-market>{it["marketPrice"]:.2f} TL</td><td class="col-net" data-col-net>{it["price"]:.2f} TL / {it["unit"]}</td></tr>'
        for it in cat["items"]
    )

    other_posts = "\n".join(
        f'<li><a href="/{p["slug"]}"><span>{p["h1"][:46]}...</span><span>Oku</span></a></li>'
        for p in bcs.BLOG_POSTS if p["slug"] != slug
    )

    body = f"""{bcs.render_topbar(prices)}
{bcs.render_header(prices, slug)}
{bcs.render_ticker(prices)}
  <main id="mainContent">
    <section class="page-banner">
      <div class="container">
        <ol class="breadcrumb">
          <li><a href="/index.html">Ana Sayfa</a></li>
          <li>/</li>
          <li><a href="/blog.html">Blog &amp; Teknik Rehber</a></li>
          <li>/</li>
          <li>{post['h1']}</li>
        </ol>
        <h1>{post['h1']}</h1>
        <p>{post['desc']}</p>
      </div>
    </section>

    <div class="container content-layout">
      <article class="article-sheet">
        <div style="margin-bottom:22px;border-radius:6px;overflow:hidden;border:1px solid var(--border-light)">
          <img src="/{post['image']}" alt="{post['h1']} - Bulgan Hurdacılık Kızıltepe Mardin" width="960" height="640">
        </div>

        <div class="info-callout">
          <strong>Bölgesel Saha Bilgisi (Mardin &amp; Güneydoğu Anadolu):</strong> Bu teknik rehber, <strong>Atatürk Mahallesi Kızıltepe / Mardin</strong> merkezli Bulgan Hurdacılık kantar eksperleri tarafından Mardin, Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman ve Kilis'teki sanayi ve şantiye işletmeleri için hazırlanmıştır.
        </div>

{sections_html}

        <h2>İlgili Hurda Grubu Güncel Kantar Fiyatları: {cat['name']} ({prices['updatedAt']})</h2>
        <div class="price-table-wrap" style="margin:16px 0 26px;border:1px solid var(--border-light);border-radius:6px">
          <table class="price-table">
            <thead>
              <tr><th>Kalem Adı</th><th style="text-align:right">Borsa Referans</th><th style="text-align:right">Bulgan Net (-%20)</th></tr>
            </thead>
            <tbody>{cat_rows}</tbody>
          </table>
        </div>

{bcs.render_contact_form_block("Kızıltepe / Mardin")}
      </article>

      <div class="sidebar-stack">
{bcs.render_calculator_panel(prices)}
        <div class="sidebar-box">
          <h3>Diğer Teknik Rehber Yazıları</h3>
          <ul class="sidebar-links">
{other_posts}
          </ul>
        </div>
      </div>
    </div>
  </main>
{bcs.render_footer(prices)}"""

    json_ld = enhanced_build_json_ld(
        slug=slug,
        title=post["title"],
        desc=post["desc"],
        breadcrumbs=[("Ana Sayfa", "index.html"), ("Blog", "blog.html"), (post["h1"], slug)],
        product_cat=cat,
        date_iso=post["date"],
        is_blog=True
    )
    return enhanced_wrap_html_document(slug, post["title"], post["desc"], body, json_ld, keywords=post["keywords"])


def write_ai_agent_discovery_files(prices):
    # 1. AGENTS.md at root
    agents_md = f"""# AGENTS.md — Bulgan Hurdacılık & Geri Dönüşüm ({DOMAIN})

Bu dosya, otonom yapay zeka ajanları (ChatGPT, Claude, Gemini, Perplexity, WebMCP ve tarayıcı ajanları) için **{BRAND_NAME}** resmi veri ve işlem kılavuzudur.

## 1. Kurumsal Kimlik & Google İşletme Kaydı (NAP)
- **Resmi Ünvan:** {BRAND_NAME}
- **Merkez Kantar Adresi:** {ADDRESS} (Google İşletme Profili Doğrulanmış Konum: `37.1939, 40.5861`)
- **Telefon & WhatsApp:** `{PHONE_DISPLAY}` (`{PHONE_TEL}` / `https://wa.me/{PHONE_WA}`)
- **Resmi E-Posta:** `{EMAIL}`
- **Hizmet Bölgesi (Sadece Mardin ve Güneydoğu Anadolu):**
  - **Mardin İlçeleri:** Kızıltepe (Ana Merkez), Artuklu, Midyat, Nusaybin, Derik, Mazıdağı, Dargeçit, Savur, Yeşilli, Ömerli.
  - **Güneydoğu Anadolu İlleri:** Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman, Kilis.
  - *Not:* Firmamız Güneydoğu Anadolu Bölgesi dışındaki illerde alım yapmamaktadır.

## 2. Makine Tarafından Okunabilir Uç Noktalar (API & Veri)
- `GET {DOMAIN}/api/prices` veya `GET {DOMAIN}/data/prices.json`: Günlük LME ve piyasa verilerinden **-%20 (x0.80)** saha/kantar iskontosu uygulanmış canlı hurda alım fiyatlarını JSON formatında döndürür.
- `POST {DOMAIN}/api/contact`: JSON gövdesi (`name`, `phone`, `city`, `material`, `weight`, `note`) ile doğrudan `{EMAIL}` kantar merkezine anlık SMTP e-posta bildirimi gönderir.
- `GET {DOMAIN}/llms.txt` ve `GET {DOMAIN}/llms-full.txt`: Yapay zeka dil modelleri için yapılandırılmış fiyat ve bölge özeti.
"""
    with open(os.path.join(ROOT, "AGENTS.md"), "w", encoding="utf-8") as f:
        f.write(agents_md)

    # 2. agent-permissions.json
    agent_perms = {
        "schema_version": "1.0",
        "site": DOMAIN,
        "organization": BRAND_NAME,
        "google_business_profile": {
            "address": ADDRESS,
            "email": EMAIL,
            "telephone": PHONE_TEL,
            "coordinates": {"latitude": 37.1939, "longitude": 40.5861}
        },
        "service_region_strict": [
            "Mardin", "Kızıltepe", "Artuklu", "Midyat", "Nusaybin", "Derik", "Mazıdağı", "Dargeçit", "Savur", "Yeşilli", "Ömerli",
            "Diyarbakır", "Şanlıurfa", "Gaziantep", "Batman", "Şırnak", "Siirt", "Adıyaman", "Kilis"
        ],
        "permissions": {
            "crawling": "allowed",
            "ai_citations": "allowed",
            "price_api_query": "allowed",
            "lead_submission": "allowed"
        },
        "endpoints": {
            "live_prices_json": f"{DOMAIN}/api/prices",
            "static_prices_json": f"{DOMAIN}/data/prices.json",
            "contact_submission_post": f"{DOMAIN}/api/contact",
            "llms_summary": f"{DOMAIN}/llms.txt",
            "llms_full": f"{DOMAIN}/llms-full.txt"
        }
    }
    with open(os.path.join(ROOT, "agent-permissions.json"), "w", encoding="utf-8") as f:
        json.dump(agent_perms, f, ensure_ascii=False, indent=2)

    # 3. mcp-actions.json (WebMCP)
    mcp_actions = {
        "mcp_version": "1.0",
        "name": "bulgan-hurdacilik-mardin",
        "description": "Mardin ve Güneydoğu Anadolu canlı hurda fiyat sorgulama (-%20 net kantar) ve adresten mobil kantar çağrı servisi.",
        "actions": [
            {
                "name": "get_live_scrap_prices",
                "method": "GET",
                "url": f"{DOMAIN}/api/prices",
                "description": "15 ana hurda kategorisi ve 75 alt kalemin güncel LME borsa referans ve -%20 net kantar alım fiyatlarını döndürür."
            },
            {
                "name": "request_kantar_pickup",
                "method": "POST",
                "url": f"{DOMAIN}/api/contact",
                "content_type": "application/json",
                "parameters": {
                    "name": "Müşteri veya Firma Adı (zorunlu)",
                    "phone": "Telefon Numarası (zorunlu, 10-11 hane)",
                    "city": "Mardin ilçesi veya Güneydoğu Anadolu ili",
                    "material": "Hurda cinsi (Bakır, Kablo, Demir, Alüminyum, Krom vb.)",
                    "weight": "Tahmini kilogram veya tonaj",
                    "note": "Adres ve saha detayı"
                }
            }
        ]
    }
    with open(os.path.join(ROOT, "mcp-actions.json"), "w", encoding="utf-8") as f:
        json.dump(mcp_actions, f, ensure_ascii=False, indent=2)

    # 4. .well-known/ai-plugin.json
    wk_dir = os.path.join(ROOT, ".well-known")
    os.makedirs(wk_dir, exist_ok=True)
    with open(os.path.join(wk_dir, "ai-plugin.json"), "w", encoding="utf-8") as f:
        json.dump({
            "schema_version": "v1",
            "name_for_human": BRAND_NAME,
            "name_for_model": "bulgan_hurdacilik_mardin",
            "description_for_human": "Mardin ve Güneydoğu Anadolu güncel hurda fiyatları ve kantar merkezi.",
            "description_for_model": "Query live scrap metal prices (-20% net kantar rate) and request scrap metal pickup in Mardin (Kızıltepe, Artuklu, Midyat, Nusaybin, Derik, Mazıdağı, Dargeçit, Savur, Yeşilli, Ömerli) and Southeastern Anatolia (Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman, Kilis).",
            "logo_url": f"{DOMAIN}/images/icon-512.png",
            "contact_email": EMAIL,
            "legal_info_url": f"{DOMAIN}/kullanim-kosullari.html"
        }, f, ensure_ascii=False, indent=2)


def run_master_upgrade():
    # Monkey-patch bcs builders with enhanced SEO & GBP functions
    bcs.build_json_ld = enhanced_build_json_ld
    bcs.wrap_html_document = enhanced_wrap_html_document

    prices = bcs.load_prices()
    generated = {}

    generated["index.html"] = bcs.build_index_page(prices)
    generated["hurda-fiyatlari.html"] = bcs.build_all_prices_page(prices)

    for cat in prices["categories"]:
        generated[cat["slug"]] = bcs.build_category_page(cat, prices)

    for dist in bcs.MARDIN_DISTRICTS:
        generated[dist["slug"]] = bcs.build_regional_page(dist, prices, is_mardin=True)

    for prov in bcs.GUNEYDOGU_PROVINCES:
        generated[prov["slug"]] = bcs.build_regional_page(prov, prices, is_mardin=False)

    for svc in bcs.EXTRA_SERVICE_PAGES + ADDITIONAL_SERVICE_PAGES:
        generated[svc["slug"]] = bcs.build_extra_service_page(svc, prices)

    corp_pages = bcs.build_corporate_and_utility_pages(prices)
    generated.update(corp_pages)

    # Blog index + 6 rich blog articles
    generated["blog.html"] = build_blog_index_page(prices)
    for post in bcs.BLOG_POSTS:
        generated[post["slug"]] = build_single_blog_post(post, prices)

    # Remove old duplicate alias .html files so EVERY .html file on disk has a 100% unique <title>
    for f in os.listdir(ROOT):
        if f.endswith(".html") and f not in generated:
            os.remove(os.path.join(ROOT, f))
            print(f"Removed duplicate/stale HTML file: {f}")

    # Write all generated HTML files
    for slug, html_content in generated.items():
        with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
            f.write(html_content)

    # Write _redirects for legacy short URLs so they 301 redirect cleanly without creating duplicate titles
    redirects_lines = [
        "/bakir.html /bakir-hurda-fiyatlari.html 301",
        "/kablo.html /kablo-hurda-fiyatlari.html 301",
        "/demir.html /demir-hurda-fiyatlari.html 301",
        "/aluminyum.html /aluminyum-hurda-fiyatlari.html 301",
        "/sari.html /sari-hurda-fiyatlari.html 301",
        "/paslanmaz.html /paslanmaz-hurda-fiyatlari.html 301",
        "/aku.html /aku-hurda-fiyatlari.html 301",
        "/cinko.html /cinko-hurda-fiyatlari.html 301",
        "/kursun.html /kursun-hurda-fiyatlari.html 301",
        "/nikel.html /nikel-hurda-fiyatlari.html 301",
        "/bronz.html /bronz-hurda-fiyatlari.html 301",
        "/elektronik.html /elektronik-hurda-fiyatlari.html 301",
        "/klima.html /klima-hurda-fiyatlari.html 301",
        "/plastik.html /plastik-hurda-fiyatlari.html 301",
        "/kagit.html /kagit-hurda-fiyatlari.html 301"
    ]
    with open(os.path.join(ROOT, "_redirects"), "w", encoding="utf-8") as f:
        f.write("\n".join(redirects_lines) + "\n")

    bcs.build_aeo_and_seo_infrastructure(prices, list(generated.keys()))
    write_ai_agent_discovery_files(prices)
    print(f"Total unique HTML pages generated: {len(generated)}")


if __name__ == "__main__":
    run_master_upgrade()


def verify_all_seo():
    htmls = sorted([f for f in os.listdir(ROOT) if f.endswith(".html")])
    titles = {}
    descs = {}
    kws = {}
    bad_cities = ["istanbul", "ankara", "izmir", "bursa", "kocaeli", "gebze", "çorlu", "tekirdağ", "antalya", "konya", "kayseri", "eskişehir", "sakarya", "adana", "mersin", "trabzon"]
    city_hits = []
    for f in htmls:
        c = open(os.path.join(ROOT, f), encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", c).group(1)
        d = re.search(r'<meta name="description" content="(.*?)">', c).group(1)
        k = re.search(r'<meta name="keywords" content="(.*?)">', c).group(1)
        titles.setdefault(t, []).append(f)
        descs.setdefault(d, []).append(f)
        kws.setdefault(k, []).append(f)
        cl = c.lower()
        for bc in bad_cities:
            if bc in cl:
                city_hits.append((f, bc))
    print(f"AUDIT -> HTML Files: {len(htmls)} | Unique Titles: {len(titles)} | Unique Descs: {len(descs)} | Unique Keywords: {len(kws)} | Non-Guneydogu Hits: {len(city_hits)}")
    for k, v in kws.items():
        if len(v) > 1:
            print("Duplicate keyword:", v)

if __name__ == "__main__":
    verify_all_seo()
