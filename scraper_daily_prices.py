import json
import os
import re
import urllib.request
from datetime import datetime, timezone, timedelta

ROOT = r"C:\AI-Tools\cloned-sites\bulgangeridonusum"
DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DISCOUNT_FACTOR = 0.80  # %20 azaltma (Borsa/Piyasa fiyatından %20 indirimli alım baz fiyatı)

# Base reference market prices (100% full market reference before 20% reduction)
# If live scrape succeeds, live values override these before multiplying by 0.80.
BASE_MARKET_CATALOG = [
    {
        "id": "bakir",
        "name": "Bakır Hurda Fiyatları",
        "shortName": "Hurda Bakır",
        "slug": "bakir-hurda-fiyatlari.html",
        "image": "images/bakir-hurda-1.webp",
        "fallbackImage": "images/bakir-hurda-1.jpg",
        "badge": "LME Borsa Endeksli",
        "desc": "Mardin ve Güneydoğu Anadolu genelinde soyma bakır, lama, kırkambar, antigron kırma ve bakır talaşı alımı.",
        "items": [
            {"code": "bakir_soyma", "name": "Soyma Bakır Hurdası (%99.9 Saf)", "marketPrice": 686.73, "unit": "KG"},
            {"code": "bakir_antigron", "name": "Antigron Kırma Bakır Hurdası", "marketPrice": 680.50, "unit": "KG"},
            {"code": "bakir_katot", "name": "Bakır Katot & Lama Bakır", "marketPrice": 657.57, "unit": "KG"},
            {"code": "bakir_kazan", "name": "Bakır Kazan & Boru Hurdası", "marketPrice": 620.27, "unit": "KG"},
            {"code": "bakir_filmasin", "name": "Bakır Filmaşin (F8) Parlak", "marketPrice": 600.32, "unit": "KG"},
            {"code": "bakir_talas", "name": "Temiz Bakır Talaşı Hurdası", "marketPrice": 582.01, "unit": "KG"},
            {"code": "bakir_petek", "name": "Bakır Petek (Radyatör) Hurdası", "marketPrice": 580.55, "unit": "KG"},
            {"code": "bakir_tel", "name": "Yanık & Bobin Bakır Tel Hurdası", "marketPrice": 550.85, "unit": "KG"},
            {"code": "bakir_kirkambar", "name": "Kırkambar Bakır Hurdası (Karışık)", "marketPrice": 515.40, "unit": "KG"}
        ]
    },
    {
        "id": "kablo",
        "name": "Kablo Hurda Fiyatları",
        "shortName": "Hurda Kablo",
        "slug": "kablo-hurda-fiyatlari.html",
        "image": "images/kablo-hurda-1.webp",
        "fallbackImage": "images/kablo-hurda-1.jpg",
        "badge": "Bakır Oranlı Tartım",
        "desc": "Şantiye, fabrika, enerji nakil hattı, yeraltı, TTR, NYA ve antigron hurda kabloların yüksek randımanla alımı.",
        "items": [
            {"code": "kablo_dalgic", "name": "Dalgıç Pompa & Tek Damar Kalın Kablo", "marketPrice": 540.13, "unit": "KG"},
            {"code": "kablo_fareyemez", "name": "Fare Yemez & Enerji Kablosu", "marketPrice": 450.52, "unit": "KG"},
            {"code": "kablo_yuzde50", "name": "%50 Bakırlı Sanayi Kablosu", "marketPrice": 400.71, "unit": "KG"},
            {"code": "kablo_celikzirh", "name": "Çelik Zırhlı & Yeraltı Enerji Kablosu", "marketPrice": 380.88, "unit": "KG"},
            {"code": "kablo_yuzde40", "name": "%40 Bakırlı Tesisat Kablosu", "marketPrice": 320.46, "unit": "KG"},
            {"code": "kablo_antigron", "name": "Antigron & NYM Tesisat Kablosu", "marketPrice": 295.51, "unit": "KG"},
            {"code": "kablo_karisik", "name": "Karışık & TTR Hurda Kablo", "marketPrice": 290.51, "unit": "KG"},
            {"code": "kablo_yuzde30", "name": "%30 Bakırlı Data / Zayıf Akım Kablosu", "marketPrice": 245.40, "unit": "KG"}
        ]
    },
    {
        "id": "demir",
        "name": "Demir Hurda Fiyatları",
        "shortName": "Hurda Demir",
        "slug": "demir-hurda-fiyatlari.html",
        "image": "images/demir-hurda-1.webp",
        "fallbackImage": "images/demir-hurda-1.jpg",
        "badge": "Tonajlı Şantiye Alımı",
        "desc": "Mardin, Kızıltepe, Diyarbakır, Şanlıurfa ve Gaziantep genelinde DKP, ekstra, inşaat demiri, profil ve çelik konstrüksiyon hurda alımı.",
        "items": [
            {"code": "demir_ekstra", "name": "Ekstra Ağır Demir & Profil Hurdası", "marketPrice": 15.77, "unit": "KG"},
            {"code": "demir_insaat", "name": "İnşaat Demir Çubuğu & Filmaşin", "marketPrice": 15.47, "unit": "KG"},
            {"code": "demir_santiye", "name": "Şantiye Kırpıntı & H-Demir Hurdası", "marketPrice": 15.27, "unit": "KG"},
            {"code": "demir_imalat", "name": "İmalat Artığı Lazer Kesim Sac", "marketPrice": 15.15, "unit": "KG"},
            {"code": "demir_dkp", "name": "DKP Sac & Kalın Demir Hurdası", "marketPrice": 15.10, "unit": "KG"},
            {"code": "demir_yikim", "name": "Bina & Tesis Yıkım Çıkması Demir", "marketPrice": 12.99, "unit": "KG"},
            {"code": "demir_talas", "name": "Demir & Çelik Torna Talaşı", "marketPrice": 12.77, "unit": "KG"},
            {"code": "demir_toplama", "name": "Karışık Toplama & Pik Demir Hurdası", "marketPrice": 11.40, "unit": "KG"}
        ]
    },
    {
        "id": "aluminyum",
        "name": "Alüminyum Hurda Fiyatları",
        "shortName": "Hurda Alüminyum",
        "slug": "aluminyum-hurda-fiyatlari.html",
        "image": "images/aluminyum-hurda-1.webp",
        "fallbackImage": "images/aluminyum-hurda-1.jpg",
        "badge": "Tel & Profil Alüminyum",
        "desc": "Elektrik teli alüminyumu, boyasız profil, araiş levha, jant, ofset matbaa kalıbı ve alüminyum radyatör alımı.",
        "items": [
            {"code": "alu_bakirli_radyator", "name": "Bakırlı Alüminyum Klima Radyatörü", "marketPrice": 355.46, "unit": "KG"},
            {"code": "alu_tel", "name": "Alüminyum Elektrik Teli (Saf)", "marketPrice": 178.50, "unit": "KG"},
            {"code": "alu_jant", "name": "Oto Jant & Araiş Levha Alüminyum", "marketPrice": 167.10, "unit": "KG"},
            {"code": "alu_profil", "name": "Boyasız Alüminyum Doğrama Profil", "marketPrice": 156.40, "unit": "KG"},
            {"code": "alu_boyali", "name": "Boyalı Levha & Çatı Alüminyumu", "marketPrice": 145.99, "unit": "KG"},
            {"code": "alu_folyo", "name": "Folyo & Sert Alüminyum Piston", "marketPrice": 115.40, "unit": "KG"},
            {"code": "alu_kutu", "name": "Preslenmiş Kutu & Talaş Alüminyum", "marketPrice": 92.72, "unit": "KG"}
        ]
    },
    {
        "id": "sari",
        "name": "Sarı Pirinç Hurda Fiyatları",
        "shortName": "Sarı Pirinç",
        "slug": "sari-hurda-fiyatlari.html",
        "image": "images/sari-hurda-1.webp",
        "fallbackImage": "images/sari-hurda-1.jpg",
        "badge": "MS-58 & Araiş",
        "desc": "Su saati, vana, musluk, MS-58 çubuk parça, sarı pirinç talaşı, radyatör ve fermuar imalat artığı alımı.",
        "items": [
            {"code": "sari_arais64", "name": "Araiş Sarı Hurdası (MS-64 / MS-70)", "marketPrice": 358.13, "unit": "KG"},
            {"code": "sari_fermuar", "name": "Fermuar Talaşı & Pirinç İmalat Artığı", "marketPrice": 313.36, "unit": "KG"},
            {"code": "sari_cubuk58", "name": "Çubuk Parça Sarı (MS-58)", "marketPrice": 309.76, "unit": "KG"},
            {"code": "sari_kirkambar", "name": "Sarı Kırkambar (Vana, Musluk, Su Saati)", "marketPrice": 288.38, "unit": "KG"},
            {"code": "sari_talas58", "name": "MS-58 Sarı Çubuk Talaşı", "marketPrice": 252.01, "unit": "KG"},
            {"code": "sari_radyator", "name": "Sarı Oto Radyatör Hurdası", "marketPrice": 196.25, "unit": "KG"}
        ]
    },
    {
        "id": "paslanmaz",
        "name": "Paslanmaz Krom Hurda Fiyatları",
        "shortName": "Paslanmaz Krom",
        "slug": "paslanmaz-hurda-fiyatlari.html",
        "image": "images/paslanmaz-hurda-1.webp",
        "fallbackImage": "images/paslanmaz-hurda-1.jpg",
        "badge": "304 • 316 • 310 Kalite",
        "desc": "Gıda tankları, sanayi kazanları, paslanmaz boru, 304, 316 ve 310 kalite krom sac ve talaş alımı.",
        "items": [
            {"code": "krom_310", "name": "310 Kalite Ateşe Dayanıklı Paslanmaz Krom", "marketPrice": 120.50, "unit": "KG"},
            {"code": "krom_316", "name": "316 Kalite Asitlik Paslanmaz Krom", "marketPrice": 112.64, "unit": "KG"},
            {"code": "krom_316_talas", "name": "316 Kalite Paslanmaz Krom Talaşı", "marketPrice": 86.68, "unit": "KG"},
            {"code": "krom_304", "name": "304 Kalite Paslanmaz Krom Sac & Boru", "marketPrice": 58.53, "unit": "KG"},
            {"code": "krom_304_talas", "name": "304 Kalite Paslanmaz Krom Talaşı", "marketPrice": 44.02, "unit": "KG"},
            {"code": "krom_201_430", "name": "201 / 430 Kalite Mıknatıslı Krom", "marketPrice": 30.56, "unit": "KG"}
        ]
    },
    {
        "id": "aku",
        "name": "Akü Hurda Fiyatları",
        "shortName": "Hurda Akü",
        "slug": "aku-hurda-fiyatlari.html",
        "image": "images/aku-hurda-1.webp",
        "fallbackImage": "images/aku-hurda-1.jpg",
        "badge": "UPS & Araç Aküsü",
        "desc": "Ağır vasıta, traktör, güneş enerjisi (GES), baz istasyonu UPS jel akü ve forklift aküleri alımı.",
        "items": [
            {"code": "aku_kuru", "name": "Kuru & Bakımsız UPS Akü Hurdası", "marketPrice": 35.88, "unit": "KG"},
            {"code": "aku_karisik", "name": "Araç & Traktör Sulu Akü Hurdası", "marketPrice": 35.77, "unit": "KG"},
            {"code": "aku_jel", "name": "Jel & Güneş Enerjisi (GES) Aküsü", "marketPrice": 35.11, "unit": "KG"},
            {"code": "aku_kucuk", "name": "Küçük Tip Santral Akü Hurdası", "marketPrice": 30.46, "unit": "KG"}
        ]
    },
    {
        "id": "cinko",
        "name": "Çinko Hurda Fiyatları",
        "shortName": "Hurda Çinko",
        "slug": "cinko-hurda-fiyatlari.html",
        "image": "images/cinko-hurda-1.webp",
        "fallbackImage": "images/cinko-hurda-1.jpg",
        "badge": "Levha & Külçe",
        "desc": "Çatı oluk sökümü çinko, zamak, külçe çinko ve galvaniz cüruf alımı.",
        "items": [
            {"code": "cinko_cati", "name": "Çinko Çatı & Oluk Söküm Hurdası", "marketPrice": 105.15, "unit": "KG"},
            {"code": "cinko_levha", "name": "Temiz Çinko Levha & Zamak", "marketPrice": 83.48, "unit": "KG"},
            {"code": "cinko_kulce", "name": "Külçe Çinko Hurdası", "marketPrice": 79.13, "unit": "KG"}
        ]
    },
    {
        "id": "kursun",
        "name": "Kurşun Hurda Fiyatları",
        "shortName": "Hurda Kurşun",
        "slug": "kursun-hurda-fiyatlari.html",
        "image": "images/kursun-hurda-1.webp",
        "fallbackImage": "images/kursun-hurda-1.jpg",
        "badge": "Minare & Levha",
        "desc": "Cami kubbe ve minare söküm kurşunu, röntgen odası zırh kurşunu ve kurşun boru alımı.",
        "items": [
            {"code": "kursun_kirkambar", "name": "Soyma & Kırkambar Yumuşak Kurşun", "marketPrice": 98.19, "unit": "KG"},
            {"code": "kursun_boru", "name": "Hurda Kurşun Boru & Kablo Zırhı", "marketPrice": 87.89, "unit": "KG"},
            {"code": "kursun_cati", "name": "Çatı & Minare Söküm Levha Kurşun", "marketPrice": 82.48, "unit": "KG"}
        ]
    },
    {
        "id": "nikel",
        "name": "Nikel Hurda Fiyatları",
        "shortName": "Hurda Nikel",
        "slug": "nikel-hurda-fiyatlari.html",
        "image": "images/nikel-hurda.webp",
        "fallbackImage": "images/nikel-hurda.jpg",
        "badge": "%99 Saf Anot",
        "desc": "Kaplama tesisleri anot nikel, şablon nikel, turbo nikel ve inconel alaşım alımı.",
        "items": [
            {"code": "nikel_anot", "name": "Nikel %99.9 Anot & Şablon Hurdası", "marketPrice": 516.03, "unit": "KG"},
            {"code": "nikel_capak", "name": "Nikel Çapağı & İmalat Artığı", "marketPrice": 355.51, "unit": "KG"},
            {"code": "nikel_turbo", "name": "Turbo Nikel & Alaşımlı Nikel", "marketPrice": 270.39, "unit": "KG"}
        ]
    },
    {
        "id": "bronz",
        "name": "Bronz & Kızıl Hurda Fiyatları",
        "shortName": "Bronz & Kızıl",
        "slug": "bronz-hurda-fiyatlari.html",
        "image": "images/bronz-hurda-1.webp",
        "fallbackImage": "images/bronz-hurda-1.jpg",
        "badge": "Fosfor Bronz & RG5",
        "desc": "Ağır sanayi dişli yatakları, burçlar, fosfor bronz, kızıl parça RG5 ve talaş alımı.",
        "items": [
            {"code": "bronz_fosfor", "name": "Fosfor Bronz (kalaylı) Levha & Parça", "marketPrice": 582.06, "unit": "KG"},
            {"code": "bronz_parca", "name": "Bronz Dişli, Burç & Yatak Parça", "marketPrice": 497.80, "unit": "KG"},
            {"code": "bronz_talas", "name": "Bronz Torna Talaşı", "marketPrice": 467.54, "unit": "KG"},
            {"code": "bronz_rg5", "name": "Kızıl Parça (RG5 / RG7 Vana & Burç)", "marketPrice": 330.26, "unit": "KG"}
        ]
    },
    {
        "id": "elektronik",
        "name": "Elektronik Kart Hurda Fiyatları",
        "shortName": "Elektronik Hurda",
        "slug": "elektronik-hurda-fiyatlari.html",
        "image": "images/elektronik-hurda-1.webp",
        "fallbackImage": "images/elektronik-hurda-1.jpg",
        "badge": "Anakart & Sunucu",
        "desc": "Bilgisayar anakartları, sunucu (server) sistemleri, telekom santral kartları, işlemci ve RAM hurdası alımı.",
        "items": [
            {"code": "elek_ram", "name": "RAM, İşlemci & Telekom Santral Kartları", "marketPrice": 130.48, "unit": "KG"},
            {"code": "elek_server", "name": "Server (Sunucu) & Laptop Anakartları", "marketPrice": 130.26, "unit": "KG"},
            {"code": "elek_hdd", "name": "Harddisk & Yeni Nesil Anakart Hurdası", "marketPrice": 123.18, "unit": "KG"},
            {"code": "elek_modem", "name": "Uydu, Modem & Güç Kaynağı Kartları", "marketPrice": 105.90, "unit": "KG"}
        ]
    },
    {
        "id": "klima",
        "name": "Klima & Chiller Hurda Fiyatları",
        "shortName": "Klima & Chiller",
        "slug": "klima-hurda-fiyatlari.html",
        "image": "images/klima-hurda-1.webp",
        "fallbackImage": "images/klima-hurda-1.jpg",
        "badge": "İklimlendirme Sökümü",
        "desc": "Merkezi sistem chiller soğutma grupları, VRF üniteleri, split klimalar, kompresör ve bakır boru tesisatı alımı.",
        "items": [
            {"code": "klima_bakir_petek", "name": "Klima & Chiller Bakır/Alüminyum Radyatör", "marketPrice": 355.46, "unit": "KG"},
            {"code": "klima_komple", "name": "Hurda Split & Salon Tipi Klima (Komple)", "marketPrice": 50.33, "unit": "KG"},
            {"code": "klima_motor", "name": "Klima & Chiller Kompresör Motoru", "marketPrice": 46.86, "unit": "KG"}
        ]
    },
    {
        "id": "plastik",
        "name": "Plastik & PVC Hurda Fiyatları",
        "shortName": "Hurda Plastik",
        "slug": "plastik-hurda-fiyatlari.html",
        "image": "images/plastik-hurda-1.webp",
        "fallbackImage": "images/plastik-hurda-1.jpg",
        "badge": "Tarımsal & Sanayi",
        "desc": "Sulama boruları, şeffaf sera naylonu, polipropilen (moblen), ABS, PE varil ve PVC pimapen profil alımı.",
        "items": [
            {"code": "plastik_naylon", "name": "Beyaz Şeffaf Naylon & Sera Örtüsü", "marketPrice": 19.36, "unit": "KG"},
            {"code": "plastik_moblen", "name": "Polipropilen (Moblen) Kasa & Çuval", "marketPrice": 16.02, "unit": "KG"},
            {"code": "plastik_kristal", "name": "Polistiren Kristal & Temiz PET", "marketPrice": 14.83, "unit": "KG"},
            {"code": "plastik_abs", "name": "ABS Sanayi Plastiği & Pimapen Profil", "marketPrice": 13.78, "unit": "KG"}
        ]
    },
    {
        "id": "kagit",
        "name": "Kağıt & Karton Hurda Fiyatları",
        "shortName": "Kağıt & Karton",
        "slug": "kagit-hurda-fiyatlari.html",
        "image": "images/kagit-hurda-1.webp",
        "fallbackImage": "images/kagit-hurda-1.jpg",
        "badge": "Tonajlı Pres Alım",
        "desc": "Fabrika, matbaa, zincir market ve kurumlardan çıkan presli/dökme karton, 1. hamur beyaz kağıt ve arşiv imha hizmeti.",
        "items": [
            {"code": "kagit_gazete", "name": "Matbaa Artığı Baskısız / Temiz Kağıt", "marketPrice": 7.20, "unit": "KG"},
            {"code": "kagit_beyaz", "name": "1. Hamur Beyaz Kağıt & Okul Kitabı", "marketPrice": 6.00, "unit": "KG"},
            {"code": "kagit_a4", "name": "Kurumsal Arşiv & A4 Evrak Hurdası", "marketPrice": 4.50, "unit": "KG"},
            {"code": "kagit_karton", "name": "Oluklu Mukavva & Koli Karton Hurdası", "marketPrice": 4.30, "unit": "KG"}
        ]
    }
]


def fetch_live_exchange_and_scrape():
    usd_try = 34.85
    eur_try = 37.90
    source_status = "LME + Piyasa Canlı Endeksi (%20 İskontolu)"

    # 1. Fetch free USD/TRY & EUR/TRY rate from open.er-api.com
    try:
        req = urllib.request.Request(
            "https://open.er-api.com/v6/latest/USD",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "rates" in data and "TRY" in data["rates"]:
                usd_try = round(float(data["rates"]["TRY"]), 2)
                eur_rate = float(data["rates"].get("EUR", 0.92))
                eur_try = round(usd_try / eur_rate, 2)
    except Exception as e:
        print("Exchange API fallback used:", e)

    # 2. Scrape live Turkish scrap reference table if reachable
    scraped_map = {}
    try:
        req = urllib.request.Request(
            "https://www.hurdaadresi.com/hurda-fiyatlari/",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0.0.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I)
            for r in rows:
                cells = [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S | re.I)]
                if len(cells) >= 2:
                    name_cell = cells[0]
                    price_match = re.search(r"(\d+[\.,]\d+)", cells[1])
                    if price_match:
                        val = float(price_match.group(1).replace(",", "."))
                        if val > 0:
                            scraped_map[name_cell.lower()] = val
    except Exception as e:
        print("Scrap reference fallback used:", e)

    return usd_try, eur_try, scraped_map, source_status


def build_prices_payload():
    usd_try, eur_try, scraped_map, source_status = fetch_live_exchange_and_scrape()
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)

    categories_out = []
    for cat in BASE_MARKET_CATALOG:
        items_out = []
        for item in cat["items"]:
            raw_market = item["marketPrice"]
            # Check if live scraped map has matching item
            for s_key, s_val in scraped_map.items():
                if item["name"].split("(")[0].strip().lower()[:14] in s_key:
                    raw_market = s_val
                    break
            discounted_price = round(raw_market * DISCOUNT_FACTOR, 2)
            items_out.append({
                "code": item["code"],
                "name": item["name"],
                "marketPrice": round(raw_market, 2),
                "price": discounted_price,
                "unit": item["unit"],
                "tonPrice": round(discounted_price * 1000, 2)
            })
        categories_out.append({
            "id": cat["id"],
            "name": cat["name"],
            "shortName": cat["shortName"],
            "slug": cat["slug"],
            "image": cat["image"],
            "fallbackImage": cat["fallbackImage"],
            "badge": cat["badge"],
            "desc": cat["desc"],
            "items": items_out
        })

    payload = {
        "updatedAt": now_tr.strftime("%d.%m.%Y %H:%M"),
        "dateIso": now_tr.strftime("%Y-%m-%d"),
        "discountApplied": "-%20 (Borsa Baz Fiyatından %20 Azaltılmış Net Alım Fiyatı)",
        "discountFactor": DISCOUNT_FACTOR,
        "exchange": {
            "USD_TRY": usd_try,
            "EUR_TRY": eur_try
        },
        "source": source_status,
        "categories": categories_out
    }

    out_path = os.path.join(DATA_DIR, "prices.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(categories_out)} categories to {out_path} (Updated: {payload['updatedAt']}, USD/TRY: {usd_try})")
    # Print sample discounted prices
    for c in categories_out[:4]:
        first = c["items"][0]
        print(f" - {c['shortName']} ({first['name']}): Borsa={first['marketPrice']} TL -> Net(-%20)={first['price']} TL/KG")


if __name__ == "__main__":
    build_prices_payload()
