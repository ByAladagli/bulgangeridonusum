import os
import re

template_path = r'C:\AI-Tools\cloned-sites\bulgangeridonusum\kadikoy-hurdaci.html'
with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
    template = f.read()

pages = [
    {
        "filename": "mardin-hurdaci.html",
        "district": "Mardin",
        "title": "Mardin Hurdacı | Bulgan Geri Dönüşüm - En Yakın Hurda Alımı 0545 904 38 34",
        "desc": "Mardin hurdacı arıyorsanız Bulgan Geri Dönüşüm adrese gelerek bakır, demir, kablo, alüminyum ve sarı hurdalarınızı en yüksek fiyattan nakit alır. Tel: 0545 904 38 34.",
        "h1": "Mardin Hurdacı Firması Telefonu ☎️ 0545 904 38 34 ✔️",
        "h2_sub": "Mardin genelinde adresten nakit hurda alımı, yerinde hassas dijital tartım ve kurumsal geri dönüşüm.",
        "about": "Mardin genelinde uzun yıllardır hurdacılık ve geri dönüşüm sektöründe faaliyet gösteren Bulgan Geri Dönüşüm, demir, bakır, alüminyum, krom, sarı pirinç ve kablo hurdalarınızı piyasanın en yüksek fiyat garantisiyle satın alır. Mardin merkez Artuklu başta olmak üzere Kızıltepe, Midyat ve tüm çevre ilçelere araçlarımız 30-45 dakika içinde ulaşmaktadır.",
        "lat": "37.3129",
        "lon": "40.7339",
        "neighborhoods": [
            ("Artuklu & Mardin Merkez", "Artuklu & 13 Mart Mahallesi Hurdacı"),
            ("Kızıltepe & Sanayi", "Kızıltepe & Sanayi Sitesi Hurdacı"),
            ("Midyat & Estel", "Midyat & Estel Bölgesi Hurdacı"),
            ("Nusaybin & İpekyolu", "Nusaybin & İpekyolu Hurdacı"),
            ("Derik & Mazıdağı", "Derik & Mazıdağı Hurdacı"),
            ("Dargeçit & Savur", "Dargeçit & Savur Hurdacı")
        ]
    },
    {
        "filename": "kiziltepe-hurdaci.html",
        "district": "Kızıltepe",
        "title": "Kızıltepe Hurdacı | Bulgan Geri Dönüşüm - Yerinde Tartım Nakit Ödeme 0545 904 38 34",
        "desc": "Kızıltepe hurdacı ve kurumsal geri dönüşüm. Atatürk Mahallesi ve tüm Kızıltepe köylerinden demir, bakır, alüminyum, kablo alımı. Hemen arayın: 0545 904 38 34.",
        "h1": "Kızıltepe Hurdacı Firması Telefonu ☎️ 0545 904 38 34 ✔️",
        "h2_sub": "Kızıltepe'de adrese en yakın hurdacı: Hassas kantar, anında nakit ve değerinde alım.",
        "about": "Bulgan Geri Dönüşüm ana merkezimiz Kızıltepe Atatürk Mahallesi'ndedir. Kızıltepe genelinde ev, iş yeri, fabrika, şantiye ve tarımsal tesislerden her nevi hurda demir, bakır, alüminyum, sarı, kablo, akü ve çinko hurdasını kendi araçlarımız ve uzman personelimizle yerinden alıyoruz.",
        "lat": "37.1936",
        "lon": "40.5858",
        "neighborhoods": [
            ("Atatürk Mahallesi", "Atatürk Mahallesi Hurdacı"),
            ("Cumhuriyet & Tepebaşı", "Cumhuriyet & Tepebaşı Hurdacı"),
            ("Yeni Mahalle & Sanayi", "Yeni Mahalle & Küçük Sanayi Sitesi Hurdacı"),
            ("Aşiti & Ersoylu", "Aşiti & Ersoylu Mahallesi Hurdacı"),
            ("Dunaysır & İpek Yolu", "Dunaysır & İpekyolu Çevresi Hurdacı"),
            ("Kızıltepe Köy ve Mezraları", "Kızıltepe Tüm Çevre Köyleri Hurdacı")
        ]
    },
    {
        "filename": "midyat-hurdaci.html",
        "district": "Midyat",
        "title": "Midyat Hurdacı | Bulgan Geri Dönüşüm - Adresten Hurda Alımı 0545 904 38 34",
        "desc": "Midyat hurdacı arayanlar için Bulgan Geri Dönüşüm aynı gün adrese geliyor. Bakır, demir, kablo, sarı pirinç hurdasını değerinde nakit alıyoruz. Tel: 0545 904 38 34.",
        "h1": "Midyat Hurdacı Firması Telefonu ☎️ 0545 904 38 34 ✔️",
        "h2_sub": "Midyat ve Estel bölgesinde kurumsal adresten hurda alım hizmeti.",
        "about": "Bulgan Geri Dönüşüm, Midyat ve Estel bölgesinde inşaat şantiyeleri, atölyeler, taş ocakları ve konutlardan çıkan her çeşit metal hurdayı yerinde tartar, LME borsa fiyatlarına göre en iyi teklifi vererek nakit öder.",
        "lat": "37.4187",
        "lon": "41.3387",
        "neighborhoods": [
            ("Estel Bölgesi", "Estel & Işıklar Hurdacı"),
            ("Bağlar & Akçakaya", "Bağlar & Akçakaya Hurdacı"),
            ("Cumhuriyet Mahallesi", "Cumhuriyet Mahallesi Hurdacı"),
            ("Midyat Sanayi", "Midyat Sanayi Çevresi Hurdacı"),
            ("Gölcük & Bahçelievler", "Gölcük & Bahçelievler Hurdacı"),
            ("Midyat Köyleri", "Midyat Çevre Köyleri Hurdacı")
        ]
    },
    {
        "filename": "nusaybin-hurdaci.html",
        "district": "Nusaybin",
        "title": "Nusaybin Hurdacı | Bulgan Geri Dönüşüm - En Yakın Hurdacı 0545 904 38 34",
        "desc": "Nusaybin hurdacı hizmeti: Bulgan Geri Dönüşüm adresten hurda demir, bakır, alüminyum, kablo alımı yapar. Anında nakit ödeme. Hemen arayın: 0545 904 38 34.",
        "h1": "Nusaybin Hurdacı Firması Telefonu ☎️ 0545 904 38 34 ✔️",
        "h2_sub": "Nusaybin ve İpekyolu hattında adresten tartım ve anında nakit hurda alımı.",
        "about": "Nusaybin ilçesinde her türlü hurda alımı ve fabrika/tesis sökümü hizmeti sunmaktayız. Bakır, kablo, alüminyum, paslanmaz sac ve ağır demir hurdalarınızı piyasa değerinde satın alıyoruz.",
        "lat": "37.0758",
        "lon": "41.2164",
        "neighborhoods": [
            ("Yenişehir & Barış", "Yenişehir & Barış Mahallesi Hurdacı"),
            ("8 Mart & Selahaddin Eyyubi", "8 Mart & Selahaddin Eyyubi Hurdacı"),
            ("Dicle & Kışla", "Dicle & Kışla Mahallesi Hurdacı"),
            ("İpekyolu Sanayi", "Nusaybin İpekyolu Sanayi Hurdacı"),
            ("Fırat & Abdulkadir Paşa", "Fırat & Abdulkadir Paşa Hurdacı"),
            ("Girmeli & Çevre Köyler", "Girmeli & Sınır Boyu Köyleri Hurdacı")
        ]
    }
]

for p in pages:
    content = template
    # Title
    content = re.sub(r'<title>.*?</title>', f'<title>{p["title"]}</title>', content, flags=re.IGNORECASE)
    # Meta Description
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{p["desc"]}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{p["desc"]}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{p["desc"]}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{p["title"]}">', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{p["title"]}">', content, flags=re.IGNORECASE)

    # Geo tags
    geo_tags = f'''
<meta name="geo.region" content="TR-47">
<meta name="geo.placename" content="{p['district']}, Mardin">
<meta name="geo.position" content="{p['lat']};{p['lon']}">
<meta name="ICBM" content="{p['lat']}, {p['lon']}">
<link rel="canonical" href="https://bulgangeridonusum.com.tr/{p['filename']}">
'''
    content = content.replace('</head>', geo_tags + '\n</head>', 1)

    # Replace H1
    old_h1_pattern = r'<h1[^>]*>.*?</h1>'
    new_h1 = f'<h1 class="fusion-title-heading title-heading-left fusion-responsive-typography-calculated" style="font-family: Poppins; font-style: normal; font-weight: 600; margin: 0px; font-size: 1em; --fontSize: 30; line-height: 1.2;" data-fontsize="30" data-lineheight="36px">{p["h1"]}</h1>'
    content = re.sub(old_h1_pattern, new_h1, content, count=1, flags=re.IGNORECASE)

    # Replace Kadıköy keywords with District keywords
    # Replace case-sensitive and case-insensitive
    content = content.replace("Kadıköy Hurdacı", f"{p['district']} Hurdacı")
    content = content.replace("Kadıköy hurdacı", f"{p['district']} hurdacı")
    content = content.replace("Kadıköy'de", f"{p['district']}'de")
    content = content.replace("Kadıköy’de", f"{p['district']}’de")
    content = content.replace("Kadıköy", f"{p['district']}")
    content = content.replace("kadıköy", f"{p['district'].lower()}")

    # Inject custom neighborhood list
    nh_html = f'<ul data-start="4026" data-end="4194">'
    for nh_name, nh_label in p["neighborhoods"]:
        nh_html += f'<li><p><strong>{nh_label}</strong></p></li>'
    nh_html += '</ul>'

    # Find the old neighborhood <ul> and replace
    old_ul_match = re.search(r'<ul data-start="4026"[^>]*>.*?</ul>', content, re.DOTALL)
    if old_ul_match:
        content = content[:old_ul_match.start()] + nh_html + content[old_ul_match.end():]

    # Save target file
    out_file = os.path.join(r'C:\AI-Tools\cloned-sites\bulgangeridonusum', p['filename'])
    with open(out_file, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
    print(f"Created dedicated regional page: {p['filename']} ({len(content)} bytes)")
