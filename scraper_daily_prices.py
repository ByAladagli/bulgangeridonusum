import json
import os
import re
import smtplib
import ssl
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DISCOUNT_FACTOR = 0.80  # %20 azaltma (Borsa/Piyasa fiyatından %20 indirimli alım baz fiyatı)


def load_local_env():
    env_path = os.path.join(ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


BASE_MARKET_CATALOG = [
    {
        "id": "bakir",
        "name": "Bakır Hurda Fiyatları",
        "shortName": "Hurda Bakır",
        "slug": "bakir-hurda-fiyatlari.html",
        "image": "images/bakir.webp",
        "fallbackImage": "images/bakir.jpg",
        "badge": "LME Referanslı",
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
        "image": "images/kablo.webp",
        "fallbackImage": "images/kablo.jpg",
        "badge": "Randıman Analizli",
        "desc": "Şantiye, fabrika, enerji nakil hattı, yeraltı, TTR, NYA ve dalgıç pompa kablolarının soyma/kırma randımanıyla alımı.",
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
        "image": "images/demir.webp",
        "fallbackImage": "images/demir.jpg",
        "badge": "Tonajlı Saha Alımı",
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
        "image": "images/aluminyum.webp",
        "fallbackImage": "images/aluminyum.jpg",
        "badge": "Tel & Profil",
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
        "image": "images/paslanmaz.webp",
        "fallbackImage": "images/paslanmaz.jpg",
        "badge": "304 • 316 • 310",
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
        "image": "images/aku.webp",
        "fallbackImage": "images/aku.jpg",
        "badge": "UPS & Ağır Vasıta",
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
        "image": "images/cinko.webp",
        "fallbackImage": "images/cinko.jpg",
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
        "image": "images/kursun.webp",
        "fallbackImage": "images/kursun.jpg",
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
        "badge": "Saf Anot & Şablon",
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
        "image": "images/bronz.png.webp",
        "fallbackImage": "images/bronz.png.jpg",
        "badge": "Fosfor Bronz & RG5",
        "desc": "Ağır sanayi dişli yatakları, burçlar, fosfor bronz, kızıl parça RG5 ve talaş alımı.",
        "items": [
            {"code": "bronz_fosfor", "name": "Fosfor Bronz (Kalaylı) Levha & Parça", "marketPrice": 582.06, "unit": "KG"},
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
        "image": "images/elektronik.png.webp",
        "fallbackImage": "images/elektronik.png.jpg",
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
        "image": "images/klima.png.webp",
        "fallbackImage": "images/klima.png.jpg",
        "badge": "Chiller & İklimlendirme",
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
        "image": "images/plastik.webp",
        "fallbackImage": "images/plastik.jpg",
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
        "image": "images/kagit.webp",
        "fallbackImage": "images/kagit.jpg",
        "badge": "Presli & Tonajlı",
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
    source_status = "LME + Piyasa Canlı Endeksi (%20 Net Kantar İskontolu)"

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


def send_daily_price_email(payload):
    load_local_env()
    gmail_user = os.environ.get("GMAIL_USER", "bulganorhan19@gmail.com")
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "")
    if not gmail_pass:
        print("GMAIL_APP_PASSWORD not set in environment; skipping email notification.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Bulgan Hurdacılık — Günlük Hurda Fiyat Bülteni ({payload['updatedAt']})"
        msg["From"] = f"Bulgan Hurdacılık Sistem <{gmail_user}>"
        msg["To"] = gmail_user

        rows_html = ""
        for cat in payload["categories"][:8]:
            first = cat["items"][0]
            rows_html += (
                f"<tr>"
                f"<td style='padding:8px 12px;border-bottom:1px solid #e2e8f0;font-weight:600'>{cat['shortName']}</td>"
                f"<td style='padding:8px 12px;border-bottom:1px solid #e2e8f0'>{first['name']}</td>"
                f"<td style='padding:8px 12px;border-bottom:1px solid #e2e8f0;color:#64748b;text-decoration:line-through'>{first['marketPrice']:.2f} TL</td>"
                f"<td style='padding:8px 12px;border-bottom:1px solid #e2e8f0;font-weight:700;color:#15803d'>{first['price']:.2f} TL / KG</td>"
                f"</tr>"
            )

        html_body = f"""
        <div style="font-family:Segoe UI,Arial,sans-serif;max-width:680px;margin:0 auto;border:1px solid #cbd5e1;border-radius:8px;overflow:hidden">
          <div style="background:#11151c;color:#ffffff;padding:20px 24px;border-bottom:3px solid #d4a52a">
            <h2 style="margin:0;font-size:20px">BULGAN HURDACILIK & GERİ DÖNÜŞÜM</h2>
            <p style="margin:4px 0 0;color:#cbd5e1;font-size:13px">Günlük Otomatik LME & Piyasa Kazıyıcı Raporu (-%20 Net Kantar Baz Fiyatları)</p>
          </div>
          <div style="padding:20px 24px;background:#ffffff;color:#1e293b">
            <p style="margin:0 0 14px;font-size:14px">
              <strong>Tarih / Saat:</strong> {payload['updatedAt']} &nbsp;|&nbsp;
              <strong>USD/TRY:</strong> {payload['exchange']['USD_TRY']} TL &nbsp;|&nbsp;
              <strong>EUR/TRY:</strong> {payload['exchange']['EUR_TRY']} TL
            </p>
            <table style="width:100%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="background:#f1f5f9;text-align:left">
                  <th style="padding:8px 12px">Grup</th>
                  <th style="padding:8px 12px">Örnek Kalem</th>
                  <th style="padding:8px 12px">Borsa</th>
                  <th style="padding:8px 12px">Bulgan Net (-%20)</th>
                </tr>
              </thead>
              <tbody>{rows_html}</tbody>
            </table>
            <p style="margin:18px 0 0;font-size:12px;color:#64748b">
              Canlı tablo ve hesaplama aracı <a href="https://bulgangeridonusum.com.tr/hurda-fiyatlari.html">bulgangeridonusum.com.tr/hurda-fiyatlari.html</a> adresinde güncellenmiştir.
            </p>
          </div>
        </div>
        """
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=15) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, [gmail_user], msg.as_string())
        print(f"Successfully sent daily price bulletin to {gmail_user}")
        return True
    except Exception as e:
        print("Failed to send daily email:", e)
        return False


def build_prices_payload():
    usd_try, eur_try, scraped_map, source_status = fetch_live_exchange_and_scrape()
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)

    categories_out = []
    for cat in BASE_MARKET_CATALOG:
        items_out = []
        for item in cat["items"]:
            raw_market = item["marketPrice"]
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

    if "--notify-email" in sys.argv:
        send_daily_price_email(payload)


if __name__ == "__main__":
    build_prices_payload()
