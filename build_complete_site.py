import json
import os
import sys
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, "data", "prices.json")
DOMAIN = "https://bulgangeridonusum.com.tr"
BRAND_NAME = "Bulgan Hurdacılık & Geri Dönüşüm"
PHONE_DISPLAY = "0545 904 38 34"
PHONE_TEL = "+905459043834"
PHONE_WA = "905459043834"
EMAIL = "bulganorhan19@gmail.com"
ADDRESS = "Atatürk Mahallesi, İpekyolu Sanayi Aksı, 47400 Kızıltepe / Mardin"

# Crisp 1.75px stroke inline SVGs (Zero Emoji Doctrine)
SVG_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SVG_WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
SVG_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
SVG_SCALE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v18"/><path d="M5 7h14"/><path d="M3 14l2-7 2 7a3 3 0 0 1-4 0z"/><path d="M17 14l2-7 2 7a3 3 0 0 1-4 0z"/><path d="M8 21h8"/></svg>'
SVG_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
SVG_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
SVG_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'

MARDIN_DISTRICTS = [
    {
        "slug": "mardin-hurdaci.html",
        "name": "Mardin İl Geneli",
        "short": "Mardin Merkez & Tüm İlçeler",
        "lat": "37.3129",
        "lng": "40.7350",
        "eta": "15 - 40 Dakika",
        "zone": "Mardin 1. ve 2. OSB, Artuklu Yenişehir, Kızıltepe İpekyolu Sanayi Aksı",
        "title": "Mardin Hurdacı | Adresten Nakit Hurda Alımı & Kantar Merkezi",
        "h1": "Mardin Hurdacı — İl Geneli Mobil Kantarlı Hurda Alım Merkezi",
        "desc": "Mardin genelinde bakır, kablo, demir, alüminyum, sarı pirinç ve paslanmaz krom hurdalarınızı adresinizde dijital kantarla tartıp anında nakit alıyoruz.",
        "focus": "Mardin Organize Sanayi Bölgesi (OSB), kamu kurum ihaleleri, inşaat şantiyeleri ve tarımsal sulama tesislerindeki tüm metal hurdaları kendi araç filomuzla yerinden teslim alıyoruz."
    },
    {
        "slug": "kiziltepe-hurdaci.html",
        "name": "Kızıltepe",
        "short": "Kızıltepe (Ana Kantar Merkezimiz)",
        "lat": "37.1939",
        "lng": "40.5861",
        "eta": "15 Dakika (Ana Merkez)",
        "zone": "Atatürk Mah., Kızıltepe Hububat Ticaret Merkezi, Küçük Sanayi Sitesi, İpekyolu",
        "title": "Kızıltepe Hurdacı | Atatürk Mah. Ana Kantar & Sanayi Hurda Alımı",
        "h1": "Kızıltepe Hurdacı — Atatürk Mahallesi Merkez Kantar ve Saha Ekibi",
        "desc": "Kızıltepe Atatürk Mahallesi merkezli Bulgan Hurdacılık; Hububat Merkezi, Kızıltepe Sanayi Sitesi ve tüm mahallelerden 15 dakikada adresten nakit hurda alır.",
        "focus": "Kızıltepe ovasındaki derin kuyu dalgıç pompa kabloları, trafo bakırları, un ve bulgur fabrikası söküm metalleri ile sanayi sitesi torna talaşlarında bölge ana alıcısıyız."
    },
    {
        "slug": "artuklu-hurdaci.html",
        "name": "Artuklu",
        "short": "Artuklu (Mardin Merkez)",
        "lat": "37.3164",
        "lng": "40.7339",
        "eta": "25 Dakika",
        "zone": "Yenişehir, 13 Mart Mah., Kabala, Ortaköy, İstasyon ve Mardin OSB",
        "title": "Artuklu Hurdacı | Mardin Merkez Yenişehir & İstasyon Hurda Alımı",
        "h1": "Artuklu Hurdacı — Yenişehir, İstasyon ve OSB Saha Alım Ekibi",
        "desc": "Mardin Artuklu ilçesinde bina yıkım demiri, tesisat bakırı, chiller klima üniteleri, alüminyum doğrama ve kablo hurdalarınızı yerinde tartarak nakit alıyoruz.",
        "focus": "Artuklu Yenişehir konut projeleri, kamu binaları yenileme çalışmaları ve İstasyon bölgesindeki sanayi depolarından çıkan hurda metaller için aynı gün araç sevk ediyoruz."
    },
    {
        "slug": "midyat-hurdaci.html",
        "name": "Midyat",
        "short": "Midyat & Estel",
        "lat": "37.4192",
        "lng": "41.3411",
        "eta": "45 Dakika",
        "zone": "Estel, Midyat Sanayi Sitesi, Bahçelievler, Gölcük ve Turizm Oteller Bölgesi",
        "title": "Midyat Hurdacı | Estel & Midyat Sanayi Adresten Hurda Alımı",
        "h1": "Midyat Hurdacı — Estel ve Midyat Sanayi Bölgesi Mobil Kantar Hizmeti",
        "desc": "Midyat ve Estel bölgesinde otel yenileme hurdaları, paslanmaz mutfak ekipmanları, bakır boru, kablo ve inşaat demiri hurdalarınızı adresinizden nakit alıyoruz.",
        "focus": "Midyat ve Estel'deki konaklama tesisleri, mermer ve taş işleme atölyeleri ile şantiyelerden çıkan ağır demir, krom ve bakır hurdalar için vinçli kamyonlarımızla hizmet veriyoruz."
    },
    {
        "slug": "nusaybin-hurdaci.html",
        "name": "Nusaybin",
        "short": "Nusaybin & İpekyolu",
        "lat": "37.0778",
        "lng": "41.2153",
        "eta": "35 Dakika",
        "zone": "Uluslararası İpekyolu Lojistik Hattı, Nusaybin Küçük Sanayi, Gırnavas",
        "title": "Nusaybin Hurdacı | İpekyolu Lojistik & Sanayi Nakit Hurda Alımı",
        "h1": "Nusaybin Hurdacı — İpekyolu Lojistik Koridoru ve Sanayi Hurda Alımı",
        "desc": "Nusaybin'de ağır vasıta dorse hurdaları, akü, bakır radyatör, şantiye demiri ve enerji kablosu hurdalarınızı hassas kantarla yerinde tartıp nakit ödüyoruz.",
        "focus": "Uluslararası İpekyolu tır garajları, lojistik depolar ve Nusaybin kentsel dönüşüm şantiyelerinden çıkan tonajlı demir, alüminyum jant ve bakır hurdaları firesiz tartıyoruz."
    },
    {
        "slug": "derik-hurdaci.html",
        "name": "Derik",
        "short": "Derik & Üçyol",
        "lat": "37.3653",
        "lng": "40.2689",
        "eta": "30 Dakika",
        "zone": "Üçyol Tarım İşletmeleri, Derik Merkez, Zeytinlik ve GES Sahaları",
        "title": "Derik Hurdacı | Tarımsal Sulama Kablosu, Trafo & Demir Hurda Alımı",
        "h1": "Derik Hurdacı — Tarımsal Sulama, Dalgıç Pompa ve Şantiye Hurda Alımı",
        "desc": "Mardin Derik ilçesinde dalgıç pompa kablosu, yanık motor bakırı, trafo, sulama borusu ve ağır tarım makinesi hurdalarını adresinizden nakit alıyoruz.",
        "focus": "Derik ve Üçyol hattındaki tarımsal sulama kuyularından çıkan kalın kesitli bakır kabloları, paslanmaz pompa gövdelerini ve GES şantiye hurdalarını yüksek randımanla satın alıyoruz."
    },
    {
        "slug": "mazidagi-hurdaci.html",
        "name": "Mazıdağı",
        "short": "Mazıdağı Sanayi & Maden",
        "lat": "37.4792",
        "lng": "40.4864",
        "eta": "35 Dakika",
        "zone": "Mazıdağı Fosfat ve Metal Kompleksi Çevresi, Poyraz, Kocakent",
        "title": "Mazıdağı Hurdacı | Endüstriyel Tesis, Ağır Demir & Kablo Hurda Alımı",
        "h1": "Mazıdağı Hurdacı — Ağır Sanayi, Çelik Konstrüksiyon ve Metal Hurda Alımı",
        "desc": "Mazıdağı bölgesindeki fabrika, maden ve taş ocağı şantiyelerinden çıkan ağır makine parçaları, çelik halat, bakır, bronz burç ve kablo hurdalarını nakit alıyoruz.",
        "focus": "Mazıdağı endüstriyel havzasında aşınmış kırıcı elekleri, ağır H-profil demirler, yüksek gerilim kabloları ve paslanmaz tank hurdaları için profesyonel kesim ve nakliye sağlıyoruz."
    },
    {
        "slug": "dargecit-hurdaci.html",
        "name": "Dargeçit",
        "short": "Dargeçit & Ilısu",
        "lat": "37.5453",
        "lng": "41.7172",
        "eta": "60 Dakika",
        "zone": "Dargeçit Merkez, Ilısu Baraj Havzası, Bahçebaşı ve Şantiye Alanları",
        "title": "Dargeçit Hurdacı | Enerji Şantiyesi, Kablo & Demir Hurda Alımı",
        "h1": "Dargeçit Hurdacı — Enerji Altyapı ve Şantiye Hurdası Alım Hizmeti",
        "desc": "Mardin Dargeçit ilçesinde baraj, altyapı ve inşaat şantiyelerinden çıkan demir, çelik zırhlı enerji kablosu, bakır ve alüminyum tel hurdalarını yerinden alıyoruz.",
        "focus": "Dargeçit ve Ilısu hattındaki enerji nakil projelerinden artan alüminyum iletken teller, bakır topraklama hatları ve iş makinesi hurdaları için tonajlı alım yapıyoruz."
    },
    {
        "slug": "savur-hurdaci.html",
        "name": "Savur",
        "short": "Savur & Sürgücü",
        "lat": "37.5403",
        "lng": "40.8886",
        "eta": "45 Dakika",
        "zone": "Savur Merkez, Sürgücü, Pınardere ve Yeşilalan",
        "title": "Savur Hurdacı | Adresten Bakır, Demir, Alüminyum & Akü Hurda Alımı",
        "h1": "Savur Hurdacı — Savur Merkez ve Köylerinden Nakit Hurda Alımı",
        "desc": "Mardin Savur ilçesinde bakır kazan, tarım ekipmanı demiri, alüminyum, sarı pirinç ve akü hurdalarınızı adresinize gelerek hassas kantarla nakit alıyoruz.",
        "focus": "Savur ve bağlı mahallelerdeki tarımsal işletmeler, bağ evleri ve inşaatlardan çıkan her nevi metal hurdayı kapınızda tartıp anında nakit ödeme yapıyoruz."
    },
    {
        "slug": "yesilli-hurdaci.html",
        "name": "Yeşilli",
        "short": "Yeşilli",
        "lat": "37.3367",
        "lng": "40.8194",
        "eta": "25 Dakika",
        "zone": "Yeşilli Merkez, Tepebaşı, Gül ve Bahçebaşı",
        "title": "Yeşilli Hurdacı | Mardin Yeşilli En Yakın Hurdacı & Mobil Kantar",
        "h1": "Yeşilli Hurdacı — 25 Dakikada Adresten Tartım ve Peşin Ödeme",
        "desc": "Mardin Yeşilli ilçesinde ev, depo ve şantiyelerden çıkan bakır, demir, kablo, alüminyum doğrama ve sarı hurdalarınızı güncel borsa fiyatıyla alıyoruz.",
        "focus": "Mardin merkeze komşu Yeşilli ilçemizde kentsel dönüşüm, bina yıkım ve tesisat yenilemelerinden çıkan tüm metalleri aynı gün adresinizden teslim alıyoruz."
    },
    {
        "slug": "omerli-hurdaci.html",
        "name": "Ömerli",
        "short": "Ömerli",
        "lat": "37.4028",
        "lng": "40.9553",
        "eta": "35 Dakika",
        "zone": "Ömerli Merkez, Midyat Karayolu Hattı ve Sanayi Atölyeleri",
        "title": "Ömerli Hurdacı | Mardin Ömerli Yerinde Tartım & Nakit Hurda Alımı",
        "h1": "Ömerli Hurdacı — Ömerli ve Midyat Yolu Üzeri Mobil Kantar Ekibi",
        "desc": "Mardin Ömerli ilçesinde hurda bakır, demir, kablo, alüminyum, paslanmaz krom ve akü alımlarında yerinde tartım ve anında nakit ödeme güvencesi.",
        "focus": "Artuklu - Midyat karayolu güzergahındaki Ömerli ilçemizde şantiye, atölye ve bağ tesislerinden çıkan hurdalar için kesintisiz saha alımı gerçekleştiriyoruz."
    }
]

GUNEYDOGU_PROVINCES = [
    {
        "slug": "diyarbakir-hurdaci.html",
        "name": "Diyarbakır",
        "short": "Diyarbakır OSB & Tüm İlçeler",
        "lat": "37.9144",
        "lng": "40.2306",
        "eta": "Aynı Gün Tır & Kamyon Sevk",
        "zone": "Diyarbakır 1-2-3. OSB, Kayapınar, Bağlar, Yenişehir, Sur, Bismil, Ergani",
        "title": "Diyarbakır Hurdacı | OSB Fabrika Sökümü & Tonajlı Metal Hurda Alımı",
        "h1": "Diyarbakır Hurdacı — Organize Sanayi ve Şantiyelerden Tonajlı Hurda Alımı",
        "desc": "Diyarbakır OSB, Kayapınar, Bağlar, Bismil ve Ergani genelinde fabrika sökümü, soyma bakır, enerji kablosu, DKP demir ve krom hurdalarını peşin alıyoruz.",
        "focus": "Diyarbakır Organize Sanayi Bölgesi'ndeki mermer, tekstil, gıda ve metal imalat fabrikalarından çıkan imalat artığı sac, bakır pano, chiller ve çelik konstrüksiyonları sözleşmeli olarak satın alıyoruz."
    },
    {
        "slug": "sanliurfa-hurdaci.html",
        "name": "Şanlıurfa",
        "short": "Şanlıurfa OSB, Viranşehir & Siverek",
        "lat": "37.1591",
        "lng": "38.7969",
        "eta": "Aynı Gün Mobil Filo",
        "zone": "Şanlıurfa 1. ve 2. OSB, Evren Sanayi Sitesi, Viranşehir, Ceylanpınar, Siverek",
        "title": "Şanlıurfa Hurdacı | Evren Sanayi, OSB & Viranşehir Tonajlı Hurda Alımı",
        "h1": "Şanlıurfa Hurdacı — OSB, Evren Sanayi ve Tarımsal Tesis Hurda Alımı",
        "desc": "Şanlıurfa merkez, Viranşehir, Ceylanpınar ve Siverek'te çırçır fabrikası sökümü, dalgıç pompa kablosu, bakır, demir ve alüminyum hurdalarını nakit alıyoruz.",
        "focus": "Kızıltepe merkezimize komşu Viranşehir ve Ceylanpınar başta olmak üzere tüm Şanlıurfa genelinde pamuk çırçır tesisleri, tekstil fabrikaları ve GES santrallerinin hurdalarını yerinde tartıyoruz."
    },
    {
        "slug": "gaziantep-hurdaci.html",
        "name": "Gaziantep",
        "short": "Gaziantep Başpınar OSB & KÜSGET",
        "lat": "37.0662",
        "lng": "37.3833",
        "eta": "Planlı Tonajlı Lojistik",
        "zone": "Başpınar 1-5. OSB, KÜSGET Sanayi Sitesi, Şehitkamil, Şahinbey, Nizip",
        "title": "Gaziantep Hurdacı | Başpınar OSB & KÜSGET Sanayi Metal Hurda Alımı",
        "h1": "Gaziantep Hurdacı — Başpınar OSB ve KÜSGET Endüstriyel Hurda Alımı",
        "desc": "Gaziantep Başpınar OSB ve KÜSGET'te fabrika imalat artığı bakır, sarı pirinç talaşı, paslanmaz krom, alüminyum, kablo ve makine hurdalarını peşin alıyoruz.",
        "focus": "Gaziantep'teki halı, tekstil, gıda ve makine imalat tesislerinden çıkan yüksek tonajlı motor, pano, paslanmaz kazan, bronz dişli ve DKP sac hurdalarını banka EFT/FAST güvencesiyle alıyoruz."
    },
    {
        "slug": "batman-hurdaci.html",
        "name": "Batman",
        "short": "Batman Merkez & OSB",
        "lat": "37.8812",
        "lng": "41.1351",
        "eta": "Aynı Gün Saha Ekibi",
        "zone": "Batman OSB, Rafineri ve Enerji Sahaları, Kozluk, Beşiri, Gercüş",
        "title": "Batman Hurdacı | Endüstriyel Boru, Kablo, Bakır & Demir Hurda Alımı",
        "h1": "Batman Hurdacı — Enerji Sahaları, OSB ve Şantiye Hurda Alım Merkezi",
        "desc": "Batman merkez ve OSB genelinde kalın etli çelik boru, zırhlı enerji kablosu, bakır, vana, sarı pirinç ve fabrika söküm hurdalarını yerinde tartıp nakit alıyoruz.",
        "focus": "Batman'daki enerji, petrol yan sanayi ve inşaat projelerinden çıkan ağır çelik borular, vanalar, trafo bakırları ve şantiye demirleri için vinçli araçlarımızla yerinde alım yapıyoruz."
    },
    {
        "slug": "sirnak-hurdaci.html",
        "name": "Şırnak",
        "short": "Şırnak, Cizre & Silopi",
        "lat": "37.5164",
        "lng": "42.4611",
        "eta": "Aynı Gün Cizre / Silopi Hattı",
        "zone": "Cizre OSB, Silopi Habur Lojistik Hattı, İdil ve Şırnak Merkez",
        "title": "Şırnak & Cizre Hurdacı | Silopi, İdil ve Habur Hattı Nakit Hurda Alımı",
        "h1": "Şırnak, Cizre ve Silopi Hurdacı — Ağır Vasıta ve Şantiye Hurda Alımı",
        "desc": "Şırnak, Cizre, Silopi ve İdil bölgelerinde şantiye demiri, tır dorse hurdası, akü, bakır radyatör, enerji kablosu ve alüminyum hurdalarını adresinizden alıyoruz.",
        "focus": "İpekyolu koridoru üzerindeki İdil, Cizre ve Silopi lojistik merkezleri ile maden ve yol şantiyelerinden çıkan tüm metal hurdaları kendi tır filomuzla yerinden teslim alıyoruz."
    },
    {
        "slug": "siirt-hurdaci.html",
        "name": "Siirt",
        "short": "Siirt Merkez & Kurtalan",
        "lat": "37.9333",
        "lng": "41.9500",
        "eta": "Aynı Gün Mobil Ekip",
        "zone": "Siirt OSB, Kurtalan, Baykan ve Baraj / Maden Şantiyeleri",
        "title": "Siirt Hurdacı | Kurtalan & Siirt OSB Bakır, Kablo ve Demir Hurda Alımı",
        "h1": "Siirt Hurdacı — Merkez, Kurtalan ve Sanayi Tesisleri Hurda Alımı",
        "desc": "Siirt ve Kurtalan genelinde bakır, enerji kablosu, inşaat yıkım demiri, alüminyum tel ve paslanmaz krom hurdalarınızı adresinizde tartarak peşin alıyoruz.",
        "focus": "Siirt ve Kurtalan'daki sanayi işletmeleri, enerji projeleri ve kentsel yenileme alanlarından çıkan metal hurdalar için yüksek fiyat ve anında ödeme sağlıyoruz."
    },
    {
        "slug": "adiyaman-hurdaci.html",
        "name": "Adıyaman",
        "short": "Adıyaman OSB, Kahta & Gölbaşı",
        "lat": "37.7648",
        "lng": "38.2786",
        "eta": "Planlı Tonajlı Sevkiyat",
        "zone": "Adıyaman OSB, Kahta, Besni, Gölbaşı ve Yeniden İnşa Şantiyeleri",
        "title": "Adıyaman Hurdacı | Şantiye Demiri, Fabrika Sökümü & Kablo Hurda Alımı",
        "h1": "Adıyaman Hurdacı — OSB ve İnşaat Şantiyeleri Tonajlı Metal Alımı",
        "desc": "Adıyaman merkez, Kahta ve Besni'de şantiye kırpıntı demiri, çelik konstrüksiyon, bakır tesisat, kablo ve alüminyum hurdalarınızı yerinde tartıp nakit alıyoruz.",
        "focus": "Adıyaman'daki konut ve altyapı şantiyeleri ile Organize Sanayi Bölgesi'ndeki tekstil ve gıda tesislerinden çıkan tonajlı hurdaları resmi kantar fişiyle satın alıyoruz."
    },
    {
        "slug": "kilis-hurdaci.html",
        "name": "Kilis",
        "short": "Kilis OSB & Polateli",
        "lat": "36.7184",
        "lng": "37.1212",
        "eta": "Planlı Tonajlı Sevkiyat",
        "zone": "Kilis OSB, Polateli Şahinbey Tekstil İhtisas OSB ve Merkez Sanayi",
        "title": "Kilis Hurdacı | Organize Sanayi & Şantiye Metal Hurda Alımı",
        "h1": "Kilis Hurdacı — OSB ve Endüstriyel Tesislerden Tonajlı Hurda Alımı",
        "desc": "Kilis ve Polateli OSB bölgesinde fabrika hurdası, bakır, enerji kablosu, demir profil, alüminyum ve paslanmaz krom hurdalarını güncel kantar fiyatıyla alıyoruz.",
        "focus": "Kilis'teki zeytinyağı tesisleri, paketleme fabrikaları ve Polateli sanayi bölgesinden çıkan paslanmaz tank, bakır motor ve demir hurdalarını peşin ödemeyle teslim alıyoruz."
    }
]

EXTRA_SERVICE_PAGES = [
    {
        "slug": "chiller-hurda-fiyatlari.html",
        "cat_id": "klima",
        "image": "images/chiller.png.webp",
        "title": "Hurda Chiller Fiyatları 2026 | Soğutma Grubu Sökümü & Alımı",
        "h1": "Hurda Chiller ve Merkezi Soğutma Grubu Alımı",
        "desc": "Mardin ve Güneydoğu Anadolu genelinde kullanım dışı su soğutmalı ve hava soğutmalı chiller gruplarını, bakır eşanjör ve kompresörlerini yerinde sökerek nakit alıyoruz."
    },
    {
        "slug": "hurda-raf-fiyatlari.html",
        "cat_id": "demir",
        "image": "images/hurda-raf-1.webp",
        "title": "Hurda Raf Fiyatları 2026 | Depo, Market & Ağır Yük Rafı Alımı",
        "h1": "Hurda Depo Rafı, Market Reyonu ve Çelik Raf Alımı",
        "desc": "Lojistik depo, fabrika ambarı, arşiv ve zincir marketlerden çıkan ağır yük raflarını, çelik arşiv dolaplarını ve profil sistemlerini yerinde söküp peşin alıyoruz."
    },
    {
        "slug": "endustriyel-mutfak-hurda.html",
        "cat_id": "paslanmaz",
        "image": "images/endustriyel-mutfak.webp",
        "title": "Endüstriyel Mutfak Hurdası | 304 Paslanmaz Tezgah & Kazan Alımı",
        "h1": "Endüstriyel Paslanmaz Mutfak Ekipmanı ve Krom Hurda Alımı",
        "desc": "Otel, yemekhane, restoran ve gıda fabrikalarından çıkan 304/316 kalite paslanmaz krom tezgah, davlumbaz, fırın, soğuk hava deposu ve kazan hurdalarını nakit alıyoruz."
    },
    {
        "slug": "fabrika-sokumu-yikim.html",
        "cat_id": "demir",
        "image": "images/sokulecek.png.webp",
        "title": "Fabrika Sökümü ve Çelik Konstrüksiyon Yıkım Hizmeti | Bulgan Hurdacılık",
        "h1": "Fabrika Sökümü, Tesis Tasfiyesi ve Çelik Konstrüksiyon Kesimi",
        "desc": "Mardin, Diyarbakır, Şanlıurfa ve Gaziantep'te çırçır, un, tekstil fabrikaları ve çelik çatı yapıların İSG kurallarına uygun oksijen/plazma kesimi ve hurda karşılığı sökümü."
    },
    {
        "slug": "ikinci-el-demir-profil-boru.html",
        "cat_id": "demir",
        "image": "images/demir.webp",
        "title": "Çıkma Demir Profil, Boru ve Sac Alımı | Şantiye & Çatı Malzemesi",
        "h1": "Söküm Çıkması Sağlam Demir Profil, Kutu Profil, Boru ve Sac Alımı",
        "desc": "Fabrika ve çatı sökümlerinden çıkan yeniden kullanıma uygun NPU, NPI, HEA çelik kolon, kutu profil, trapez sac ve çelik boruların değerinde alımı."
    }
]


def load_prices():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def render_topbar(prices):
    usd = prices.get("exchange", {}).get("USD_TRY", 34.85)
    eur = prices.get("exchange", {}).get("EUR_TRY", 37.90)
    updated = prices.get("updatedAt", "Bugün")
    return f"""
  <div class="topbar">
    <div class="container topbar-inner">
      <div class="topbar-left">
        <span class="status-indicator"><span class="status-dot"></span>Kızıltepe / Mardin Merkez Kantar Açık (07:30 - 21:00)</span>
        <span class="topbar-item">{SVG_PIN} <strong>Merkez:</strong> Atatürk Mah. Kızıltepe / Mardin</span>
      </div>
      <div class="topbar-right">
        <span class="topbar-item">{SVG_CLOCK} Son Borsa Güncellemesi: <strong data-live-updated>{updated}</strong></span>
        <span class="topbar-item tabular">USD/TRY: <strong data-live-usd>{usd:.2f} TL</strong></span>
        <span class="topbar-item tabular">EUR/TRY: <strong data-live-eur>{eur:.2f} TL</strong></span>
      </div>
    </div>
  </div>"""


def render_header(prices, active_slug=""):
    cat_links = "\n".join(
        f'              <a href="/{c["slug"]}"><span>{c["shortName"]} Fiyatları</span><span class="tabular">{c["items"][0]["price"]:.2f} TL</span></a>'
        for c in prices["categories"]
    )
    mardin_links = "\n".join(
        f'              <a href="/{d["slug"]}"><span>{d["name"]} Hurdacı</span><span>{d["eta"].split()[0]} dk</span></a>'
        for d in MARDIN_DISTRICTS[:8]
    )
    gd_links = "\n".join(
        f'              <a href="/{p["slug"]}"><span>{p["name"]} Hurdacı</span><span>Bölge Sevkiyat</span></a>'
        for p in GUNEYDOGU_PROVINCES
    )
    return f"""
  <header class="site-header">
    <div class="container header-inner">
      <a href="/index.html" class="brand-logo" aria-label="{BRAND_NAME} Ana Sayfa">
        <img src="/images/bulgan-logo.webp" alt="Bulgan Hurdacılık Mardin Geri Dönüşüm Logosu" width="165" height="62" fetchpriority="high">
        <div class="brand-text">
          <span class="brand-title">BULGAN HURDACILIK</span>
          <span class="brand-subtitle">MARDİN &amp; GÜNEYDOĞU METAL GERİ DÖNÜŞÜM</span>
        </div>
      </a>

      <button type="button" class="mobile-menu-toggle" id="mobileMenuBtn" aria-expanded="false" aria-controls="mainNav">
        {SVG_MENU} Menü
      </button>

      <nav class="main-nav" id="mainNav" aria-label="Ana Navigasyon">
        <a href="/index.html" class="nav-link {'active' if active_slug == 'index.html' else ''}">Ana Sayfa</a>
        <div class="nav-dropdown">
          <a href="/hurda-fiyatlari.html" class="nav-link {'active' if 'fiyatlari' in active_slug else ''}">Hurda Fiyatları</a>
          <div class="nav-dropdown-menu">
            <a href="/hurda-fiyatlari.html"><strong>Tüm Güncel Fiyat Listesi</strong><span>-%20 Baz</span></a>
{cat_links}
          </div>
        </div>
        <div class="nav-dropdown">
          <a href="/mardin-hurdaci.html" class="nav-link {'active' if active_slug in [d['slug'] for d in MARDIN_DISTRICTS] else ''}">Mardin Hurdacı</a>
          <div class="nav-dropdown-menu">
{mardin_links}
          </div>
        </div>
        <div class="nav-dropdown">
          <a href="/diyarbakir-hurdaci.html" class="nav-link {'active' if active_slug in [p['slug'] for p in GUNEYDOGU_PROVINCES] else ''}">Güneydoğu Bölgeler</a>
          <div class="nav-dropdown-menu">
{gd_links}
          </div>
        </div>
        <a href="/fabrika-sokumu-yikim.html" class="nav-link {'active' if active_slug == 'fabrika-sokumu-yikim.html' else ''}">Fabrika Sökümü</a>
        <a href="/hakkimizda.html" class="nav-link {'active' if active_slug == 'hakkimizda.html' else ''}">Kurumsal</a>
        <a href="/iletisim.html" class="nav-link {'active' if active_slug == 'iletisim.html' else ''}">İletişim</a>
      </nav>

      <div class="header-actions">
        <a href="tel:{PHONE_TEL}" class="header-phone-btn tabular">{SVG_PHONE} {PHONE_DISPLAY}</a>
        <a href="https://wa.me/{PHONE_WA}?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20hurda%20fiyat%20teklifi%20ve%20kantar%20bilgisi%20almak%20istiyorum." class="header-wa-btn" target="_blank" rel="noopener">{SVG_WA} WhatsApp</a>
      </div>
    </div>
  </header>"""


def render_ticker(prices):
    chips = []
    for c in prices["categories"][:9]:
        first = c["items"][0]
        chips.append(
            f'<span class="ticker-item">'
            f'<span class="ticker-name">{c["shortName"]}:</span>'
            f'<span class="ticker-old">{first["marketPrice"]:.2f}</span>'
            f'<span class="ticker-price">{first["price"]:.2f} TL/KG</span>'
            f'</span>'
        )
    return f"""
  <div class="ticker-bar" aria-label="Güncel Kantar Baz Fiyat Şeridi">
    <div class="container ticker-inner">
      <span class="ticker-label">Canlı Kantar (-%20 Baz)</span>
      {"".join(chips)}
    </div>
  </div>"""


def render_calculator_panel(prices):
    city_opts = "\n".join(
        [f'<option value="{d["name"]} / Mardin">{d["name"]} (Mardin)</option>' for d in MARDIN_DISTRICTS[1:]] +
        [f'<option value="{p["name"]}">{p["name"]} (Güneydoğu Sevkiyat)</option>' for p in GUNEYDOGU_PROVINCES]
    )
    first_item = prices["categories"][0]["items"][0]
    return f"""
        <aside class="calc-panel" id="hesaplama-araci" aria-label="Canlı Hurda Fiyat Hesaplama Aracı">
          <div class="calc-header">
            <div>
              <h2 class="calc-title">Canlı Hurda Hesaplama Aracı</h2>
              <p class="calc-sub">Borsa kazıyıcı verisiyle (%20 kantar iskontosu uygulanmış) net tutar hesabı</p>
            </div>
            <span class="calc-tag">Günlük Borsa</span>
          </div>

          <div class="form-group">
            <label class="form-label" for="calcCategory">1. Ana Metal / Hurda Grubu</label>
            <select id="calcCategory" class="form-control"></select>
          </div>

          <div class="form-group">
            <label class="form-label" for="calcItem">2. Alt Kalite / Hurda Cinsi</label>
            <select id="calcItem" class="form-control"></select>
          </div>

          <div class="calc-row-2">
            <div class="form-group">
              <label class="form-label" for="calcWeight">3. Miktar (Tartım)</label>
              <input type="number" id="calcWeight" class="form-control tabular" value="100" min="1" step="10">
            </div>
            <div class="form-group">
              <label class="form-label" for="calcUnit">Birim</label>
              <select id="calcUnit" class="form-control">
                <option value="KG">Kilogram (KG)</option>
                <option value="TON">Ton (1.000 KG)</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="calcCity">4. Alım Yapılacak İlçe / Şehir</label>
            <select id="calcCity" class="form-control">
              {city_opts}
            </select>
          </div>

          <div class="calc-result-box">
            <div class="calc-result-grid">
              <div>
                <div class="calc-stat-label">Borsa Referans (100%)</div>
                <div class="calc-stat-val" style="text-decoration:line-through;color:#94a3b8" id="calcMarketUnit">{first_item['marketPrice']:.2f} TL / KG</div>
              </div>
              <div>
                <div class="calc-stat-label">Bulgan Net Alım (-%20)</div>
                <div class="calc-stat-val" style="color:#86efac" id="calcNetUnit">{first_item['price']:.2f} TL / KG</div>
              </div>
            </div>
            <div style="margin-top:12px;padding-top:10px;border-top:1px solid #2c3646;display:flex;justify-content:space-between;align-items:baseline">
              <span class="calc-stat-label" style="font-size:0.85rem;color:#e2e8f0;font-weight:700">Tahmini Peşin Ödeme:</span>
              <span class="calc-total-val" id="calcTotalAmount">{first_item['price']*100:,.2f} TL</span>
            </div>
          </div>

          <div id="calcBasketList" class="calc-Multi-list"></div>

          <div style="display:grid;grid-template-columns:1fr 1.3fr;gap:10px;margin-top:12px">
            <button type="button" id="calcAddBasketBtn" class="btn btn-outline-light" style="padding:11px 12px;font-size:0.84rem">
              + Listeye Ekle
            </button>
            <a href="https://wa.me/{PHONE_WA}" id="calcWaBtn" target="_blank" rel="noopener" class="btn btn-primary" style="padding:11px 14px;font-size:0.88rem">
              {SVG_WA} Hesabı WhatsApp'a Aktar
            </a>
          </div>
        </aside>"""


def render_contact_form_block(default_city="Kızıltepe / Mardin"):
    return f"""
        <div class="contact-sheet" id="kantar-cagri-formu">
          <h3 style="font-size:1.25rem;font-weight:800;color:var(--text-ink);margin-bottom:6px">Adresten Kantar &amp; Ekspertiz Çağrı Formu</h3>
          <p style="font-size:0.9rem;color:var(--text-muted);margin-bottom:18px">
            Bilgilerinizi bırakın; Kızıltepe merkez kantar ekibimiz ve saha aracımız aynı gün adresinize ulaşsın. Form doğrudan <strong>{EMAIL}</strong> sistemimize düşer.
          </p>
          <form class="js-bulgan-form" novalidate>
            <div class="calc-row-2">
              <div class="form-group">
                <label class="form-label" style="color:var(--text-ink)" for="fName">Adınız Soyadınız / Firma Adı *</label>
                <input type="text" id="fName" name="name" class="light-input" placeholder="Örn: Ahmet Yılmaz / Özdemir İnşaat" required>
                <div class="field-error-msg" id="errName">Lütfen adınızı ve soyadınızı girin (en az 2 karakter).</div>
              </div>
              <div class="form-group">
                <label class="form-label" style="color:var(--text-ink)" for="fPhone">Telefon Numaranız *</label>
                <input type="tel" id="fPhone" name="phone" class="light-input tabular" placeholder="05XX XXX XX XX" required>
                <div class="field-error-msg" id="errPhone">Lütfen geçerli bir telefon numarası girin.</div>
              </div>
            </div>
            <div class="calc-row-2">
              <div class="form-group">
                <label class="form-label" style="color:var(--text-ink)" for="fCity">İl / İlçe Konumu</label>
                <input type="text" id="fCity" name="city" class="light-input" value="{default_city}">
              </div>
              <div class="form-group">
                <label class="form-label" style="color:var(--text-ink)" for="fMaterial">Hurda Cinsi &amp; Tahmini Tonaj</label>
                <input type="text" id="fMaterial" name="material" class="light-input" placeholder="Örn: 450 KG Soyma Bakır / 3 Ton Demir">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" style="color:var(--text-ink)" for="fNote">Saha / Adres Notunuz (İsteğe Bağlı)</label>
              <textarea id="fNote" name="note" rows="2" class="light-input" placeholder="Mahalle, şantiye konumu veya söküm detayı..."></textarea>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:14px">
              <button type="submit" class="btn btn-primary">{SVG_SCALE} Kantar &amp; Fiyat Teklifi İste</button>
              <a href="https://wa.me/{PHONE_WA}?text=Merhaba%2C%20hurda%20foto%C4%9Fraf%C4%B1%20ve%20konum%20g%C3%B6ndermek%20istiyorum." target="_blank" rel="noopener" class="btn btn-outline-dark">
                {SVG_WA} WhatsApp'tan Fotoğraf Gönder
              </a>
            </div>
          </form>
        </div>"""


def render_footer(prices):
    cat_links = "\n".join(
        f'            <li><a href="/{c["slug"]}">{c["name"]} ({c["items"][0]["price"]:.2f} TL)</a></li>'
        for c in prices["categories"][:9]
    )
    mardin_links = "\n".join(
        f'            <li><a href="/{d["slug"]}">{d["name"]} Hurdacı</a></li>'
        for d in MARDIN_DISTRICTS[:9]
    )
    gd_links = "\n".join(
        f'            <li><a href="/{p["slug"]}">{p["name"]} Hurdacı</a></li>'
        for p in GUNEYDOGU_PROVINCES
    )
    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <a href="/index.html" class="brand-logo" style="margin-bottom:14px">
            <img src="/images/bulgan-logo.webp" alt="Bulgan Hurdacılık Logo" width="150" height="56" loading="lazy">
          </a>
          <p style="margin-bottom:14px;line-height:1.6">
            <strong>{BRAND_NAME}</strong>; Mardin (Kızıltepe merkez kantar) ve Güneydoğu Anadolu genelinde lisanslı metal geri dönüşüm, fabrika sökümü ve adresten nakit hurda alım kuruluşudur.
          </p>
          <p class="tabular" style="color:#ffffff;font-weight:700;margin-bottom:6px">Telefon &amp; Kantar: <a href="tel:{PHONE_TEL}" style="color:var(--brand-gold-bright)">{PHONE_DISPLAY}</a></p>
          <p style="margin-bottom:6px">E-Posta: <a href="mailto:{EMAIL}" style="color:#e2e8f0">{EMAIL}</a></p>
          <p>Merkez Adres: {ADDRESS}</p>
        </div>

        <div class="footer-col">
          <h4>Güncel Hurda Fiyatları (-%20 Baz)</h4>
          <ul class="footer-links">
            <li><a href="/hurda-fiyatlari.html"><strong>2026 Tüm Hurda Fiyat Listesi</strong></a></li>
{cat_links}
          </ul>
        </div>

        <div class="footer-col">
          <h4>Mardin İlçe Kantar Hizmeti</h4>
          <ul class="footer-links">
{mardin_links}
          </ul>
        </div>

        <div class="footer-col">
          <h4>Güneydoğu Anadolu &amp; Kurumsal</h4>
          <ul class="footer-links">
{gd_links}
            <li style="margin-top:8px;padding-top:8px;border-top:1px solid #2c3646"><a href="/gizlilik-politikasi.html">KVKK &amp; Gizlilik Politikası</a></li>
            <li><a href="/kullanim-kosullari.html">Kullanım Koşulları &amp; Ticari Şartlar</a></li>
            <li><a href="/llms.txt">AI &amp; Veri Özeti (llms.txt)</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 {BRAND_NAME} (bulgangeridonusum.com.tr). Tüm hakları saklıdır.</div>
        <div>LME Borsa Endeksli (%20 Kantar İskontolu) Günlük Otomatik Fiyat Sistemi</div>
      </div>
    </div>
  </footer>

  <div class="mobile-sticky-bar" role="region" aria-label="Hızlı Mobil İletişim">
    <a href="tel:{PHONE_TEL}" class="btn-primary tabular">{SVG_PHONE} Hemen Ara</a>
    <a href="https://wa.me/{PHONE_WA}?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20konum%20ve%20hurda%20fiyat%C4%B1%20i%C3%A7in%20yaz%C4%B1yorum." target="_blank" rel="noopener" class="btn-gold">{SVG_WA} WhatsApp Konum</a>
  </div>

  <div class="cookie-bar" id="cookieBanner" role="dialog" aria-label="Çerez ve KVKK Bilgilendirmesi">
    <p>
      <strong>KVKK &amp; Çerez Bilgilendirmesi:</strong> Sitemizde canlı borsa hurda fiyatlarının doğru görüntülenmesi ve kantar hesaplama aracının çalışması için zorunlu ve analitik çerezler kullanılmaktadır. Detaylar için <a href="/gizlilik-politikasi.html" style="color:var(--brand-gold-bright);text-decoration:underline">Gizlilik Politikamızı</a> inceleyebilirsiniz.
    </p>
    <div class="cookie-actions">
      <button type="button" id="cookieAcceptBtn" class="btn btn-primary" style="padding:7px 14px;font-size:0.8rem">Tümünü Kabul Et</button>
      <button type="button" id="cookieEssentialBtn" class="btn btn-outline-light" style="padding:7px 12px;font-size:0.8rem">Sadece Zorunlu</button>
    </div>
  </div>
  <script src="/js/bulgan-app.js" defer></script>"""


def build_json_ld(slug, title, desc, breadcrumbs, faqs=None, product_cat=None, geo_info=None, date_iso="2026-11-03"):
    lat = geo_info["lat"] if geo_info else "37.1939"
    lng = geo_info["lng"] if geo_info else "40.5861"
    area_name = geo_info["name"] if geo_info else "Mardin ve Güneydoğu Anadolu"

    graph = [
        {
            "@type": ["RecyclingCenter", "LocalBusiness"],
            "@id": f"{DOMAIN}/#organization",
            "name": BRAND_NAME,
            "alternateName": "Bulgan Hurdacılık Mardin",
            "url": DOMAIN,
            "logo": f"{DOMAIN}/images/bulgan-logo.webp",
            "image": f"{DOMAIN}/images/og-cover.jpg",
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
            "hasMap": f"https://www.google.com/maps?q={lat},{lng}",
            "areaServed": [
                {"@type": "AdministrativeArea", "name": area_name},
                {"@type": "City", "name": "Mardin"},
                {"@type": "City", "name": "Kızıltepe"},
                {"@type": "City", "name": "Diyarbakır"},
                {"@type": "City", "name": "Şanlıurfa"},
                {"@type": "City", "name": "Gaziantep"},
                {"@type": "City", "name": "Batman"},
                {"@type": "City", "name": "Şırnak"},
                {"@type": "City", "name": "Siirt"}
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
            "@type": "WebPage",
            "@id": f"{DOMAIN}/{slug if slug != 'index.html' else ''}#webpage",
            "url": f"{DOMAIN}/{slug if slug != 'index.html' else ''}",
            "name": title,
            "description": desc,
            "inLanguage": "tr-TR",
            "dateModified": date_iso,
            "isPartOf": {"@id": f"{DOMAIN}/#organization"},
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", ".hero-lead", ".page-banner p"]
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

    if product_cat:
        prices_list = [it["price"] for it in product_cat["items"]]
        low_p = min(prices_list)
        high_p = max(prices_list)
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
                "seller": {"@id": f"{DOMAIN}/#organization"}
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


def wrap_html_document(slug, title, desc, body_html, json_ld_str, og_image="images/og-cover.jpg", noindex=False):
    canonical = f"{DOMAIN}/" if slug == "index.html" else f"{DOMAIN}/{slug}"
    robots_content = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="{robots_content}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="tr-TR" href="{canonical}">

  <!-- Favicon & App Manifest -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#11151c">

  <!-- Geo & Local Business Meta -->
  <meta name="geo.region" content="TR-47">
  <meta name="geo.placename" content="Kızıltepe, Mardin">
  <meta name="geo.position" content="37.1939;40.5861">
  <meta name="ICBM" content="37.1939, 40.5861">

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

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{DOMAIN}/{og_image}">

  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/bulgan-theme.css">

  <script type="application/ld+json">{json_ld_str}</script>
</head>
<body>
  <a href="#mainContent" class="skip-link">Ana İçeriğe Geç</a>
{body_html}
</body>
</html>
"""


def render_category_ledger_card(cat):
    rows = "\n".join(
        f'                <tr data-item-code="{it["code"]}">'
        f'<td>{it["name"]}</td>'
        f'<td class="col-market" data-col-market>{it["marketPrice"]:.2f} TL</td>'
        f'<td class="col-net" data-col-net>{it["price"]:.2f} TL / {it["unit"]}</td>'
        f'</tr>'
        for it in cat["items"]
    )
    return f"""
        <article class="ledger-card">
          <div class="ledger-card-top">
            <img src="/{cat['image']}" alt="{cat['name']} - Bulgan Hurdacılık Mardin" class="ledger-thumb" width="68" height="48" loading="lazy">
            <div>
              <h3 class="ledger-card-title"><a href="/{cat['slug']}">{cat['name']}</a></h3>
              <div class="ledger-card-sub">{cat['badge']} &bull; Borsa -%20 Net Kantar Bazı</div>
            </div>
          </div>
          <div class="price-table-wrap">
            <table class="price-table" aria-label="{cat['name']} Tablosu">
              <thead>
                <tr>
                  <th>Hurda Kalemi</th>
                  <th style="text-align:right">Borsa</th>
                  <th style="text-align:right">Net Alım (-%20)</th>
                </tr>
              </thead>
              <tbody>
{rows}
              </tbody>
            </table>
          </div>
          <div class="ledger-card-footer">
            <a href="/{cat['slug']}" class="ledger-link">Detaylı Kalite Analizi {SVG_ARROW}</a>
            <a href="https://wa.me/{PHONE_WA}?text=Merhaba%2C%20{cat['shortName']}%20fiyat%C4%B1%20i%C3%A7in%20yaz%C4%B1yorum." target="_blank" rel="noopener" style="font-weight:700;color:var(--brand-green)">Fiyat Teyit Al</a>
          </div>
        </article>"""


def build_index_page(prices):
    slug = "index.html"
    title = "Bulgan Hurdacılık | Mardin & Güneydoğu Hurda Alım ve Kantar Merkezi"
    desc = "Mardin (Kızıltepe merkez) ve Güneydoğu Anadolu genelinde bakır, kablo, demir, alüminyum, sarı pirinç ve krom hurda alımı. Günlük LME borsa endeksli (%20 net kantar) fiyatlar ve anında nakit ödeme."

    ledger_cards_html = "\n".join(render_category_ledger_card(c) for c in prices["categories"][:6])

    photo_cards = []
    for c in prices["categories"]:
        first = c["items"][0]
        photo_cards.append(f"""
        <article class="catalog-item">
          <a href="/{c['slug']}" class="catalog-img-wrap">
            <img src="/{c['image']}" alt="{c['name']} Mardin Bulgan Hurdacılık" width="480" height="320" loading="lazy">
          </a>
          <div class="catalog-body">
            <h3 class="catalog-title"><a href="/{c['slug']}">{c['name']}</a></h3>
            <p class="catalog-desc">{c['desc']}</p>
            <div class="catalog-price-strip">
              <span>Baz Kalem ({first['name'][:20]}):</span>
              <span class="catalog-price-val">{first['price']:.2f} TL/KG</span>
            </div>
          </div>
        </article>""")

    mardin_list_html = "\n".join(
        f'              <li><a href="/{d["slug"]}"><span>{d["name"]} Hurdacı</span><span class="region-meta">{d["eta"].split()[0]} dk</span></a></li>'
        for d in MARDIN_DISTRICTS
    )
    gd_list_html = "\n".join(
        f'              <li><a href="/{p["slug"]}"><span>{p["name"]} Hurdacı</span><span class="region-meta">Tonajlı Alım</span></a></li>'
        for p in GUNEYDOGU_PROVINCES
    )

    faqs = [
        ("Bulgan Hurdacılık Mardin'in hangi ilçelerinden adresten hurda alıyor?",
         "Ana kantar merkezimiz Kızıltepe Atatürk Mahallesi'nde yer almakta olup; Artuklu (Mardin Merkez), Kızıltepe, Midyat, Nusaybin, Derik, Mazıdağı, Dargeçit, Savur, Yeşilli ve Ömerli ilçelerinin tamamından kendi mobil kantarlı araçlarımızla adresten hurda alımı yapıyoruz."),
        ("Tablodaki hurda fiyatları neden borsa referansından %20 indirimli hesaplanıyor?",
         "Londra Metal Borsası (LME) ve haddehane ham metal referans kurları, işlenmiş külçe metal değerleridir. Saha toplama, fire ayrıştırma, kesim, presleme ve nakliye maliyetleri düşülerek (%20 azaltma / x0.80 katsayısı) müşteriye doğrudan kantar başında ödenecek gerçekçi net peşin alım fiyatları yayınlanmaktadır."),
        ("Tartım ve ödeme süreci nasıl işliyor?",
         "WhatsApp (0545 904 38 34) üzerinden hurda fotoğrafı veya konum gönderdiğinizde en yakın saha aracımız adresinize yönlendirilir. Dijital kantarımızda sizin nezaretinizde tartım yapılır, kantar fişi kesilir ve araç başında nakit veya anında FAST/EFT ile ödeme tamamlanır."),
        ("Güneydoğu Anadolu illerine (Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak) hizmet veriyor musunuz?",
         "Evet. Tonajlı şantiye demiri, fabrika sökümü, enerji kablosu, soyma bakır, trafo ve kurumsal metal ihalelerinde Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman ve Kilis illerinin tamamına tır ve vinçli kamyon filomuzla aynı gün sevkiyat sağlıyoruz.")
    ]

    faq_html = "\n".join(
        f"""        <details class="faq-item" {'open' if i == 0 else ''}>
          <summary>{q}</summary>
          <div class="faq-answer">{a}</div>
        </details>"""
        for i, (q, a) in enumerate(faqs)
    )

    body = f"""{render_topbar(prices)}
{render_header(prices, slug)}
{render_ticker(prices)}

  <main id="mainContent">
    <section class="hero-section">
      <div class="container hero-grid">
        <div>
          <div class="hero-location-line">
            Mardin (Kızıltepe Merkez Kantar) &amp; Güneydoğu Anadolu Bölge Müdürlüğü
          </div>
          <h1 class="hero-title">
            Mardin ve Güneydoğu Anadolu'da Lisanslı Metal Geri Dönüşüm &amp; Adresten Nakit Hurda Alımı
          </h1>
          <p class="hero-lead">
            <strong>Bulgan Hurdacılık</strong> olarak Kızıltepe Atatürk Mahallesi'ndeki merkez kantarımızdan Mardin'in 10 ilçesine ve Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak hattındaki tüm sanayi tesislerine kendi araç filomuzla ulaşıyoruz. Bakır, enerji kablosu, demir, alüminyum, sarı pirinç, paslanmaz krom ve fabrika söküm hurdalarınızı şeffaf kantar tartımıyla, <strong>araç başında peşin</strong> satın alıyoruz.
          </p>

          <div class="hero-cta-group">
            <a href="tel:{PHONE_TEL}" class="btn btn-primary tabular">
              {SVG_PHONE} Kantar Hattı: {PHONE_DISPLAY}
            </a>
            <a href="https://wa.me/{PHONE_WA}?text=Merhaba%20Bulgan%20Hurdac%C4%B1l%C4%B1k%2C%20hurda%20sat%C4%B1%C5%9F%C4%B1%20i%C3%A7in%20fiyat%20ve%20kantar%20talep%20ediyorum." target="_blank" rel="noopener" class="btn btn-gold">
              {SVG_WA} WhatsApp Fotoğraf &amp; Konum Gönder
            </a>
            <a href="/hurda-fiyatlari.html" class="btn btn-outline-light">
              {SVG_SCALE} Günlük Fiyat Tablosu
            </a>
          </div>

          <div class="hero-specs">
            <div class="hero-spec-item">
              <div class="hero-spec-title">1. Dijital Kantar Güvencesi</div>
              <div class="hero-spec-desc">Kalibrasyonlu mobil ve merkez kantarlarımızda gözünüzün önünde sıfır hata ile tartım ve resmi kantar fişi.</div>
            </div>
            <div class="hero-spec-item">
              <div class="hero-spec-title">2. Günlük Borsa (-%20 Net Baz)</div>
              <div class="hero-spec-desc">LME ve piyasa verilerinden günlük otomatik çekilen, fire/işleme payı düşülmüş net peşin alım fiyatları.</div>
            </div>
            <div class="hero-spec-item">
              <div class="hero-spec-title">3. Anında Nakit / FAST Ödeme</div>
              <div class="hero-spec-desc">Tartım bittiği anda araç başında nakit veya şirket hesabınıza anında banka FAST/EFT transferi.</div>
            </div>
          </div>
        </div>

{render_calculator_panel(prices)}
      </div>
    </section>

    <section class="section" id="canli-fiyatlar">
      <div class="container">
        <div class="section-header">
          <div>
            <h2 class="section-title">Güncel Hurda Fiyatları ({prices['updatedAt']})</h2>
            <p class="section-desc">
              Borsa kazıyıcı sistemimiz tarafından günlük güncellenen, Mardin ve Güneydoğu Anadolu saha alımlarında geçerli <strong>-%20 net kantar</strong> alım listesi. Yüksek tonajlı fabrika ve şantiye yüklemelerinde özel prim uygulanır.
            </p>
          </div>
          <a href="/hurda-fiyatlari.html" class="btn btn-outline-dark">Tüm 15 Kategoriyi İncele {SVG_ARROW}</a>
        </div>

        <div class="ledger-grid">
{ledger_cards_html}
        </div>
      </div>
    </section>

    <section class="section section-alt" id="hurda-alim-gruplari">
      <div class="container">
        <div class="section-header">
          <div>
            <h2 class="section-title">Alımını Yaptığımız Metal ve Sanayi Hurdaları</h2>
            <p class="section-desc">
              Soyma bakırdan yeraltı enerji kablolarına, inşaat yıkım demirinden 304/316 paslanmaz krom tanklara kadar tüm sanayi ve şantiye metallerini değerinde alıyoruz.
            </p>
          </div>
        </div>

        <div class="catalog-grid">
{"".join(photo_cards)}
        </div>
      </div>
    </section>

    <section class="section" id="saha-alim-sureci">
      <div class="container">
        <div class="section-header">
          <div>
            <h2 class="section-title">Sahada 4 Adımda Şeffaf Hurda Alım Sürecimiz</h2>
            <p class="section-desc">
              Karmaşık aracılar veya belirsiz kesintiler olmadan, doğrudan Kızıltepe merkez kantarımızdan yönetilen kurumsal alım prosedürü.
            </p>
          </div>
        </div>

        <div class="process-steps">
          <div class="process-step">
            <div class="process-step-head">
              <span class="process-step-num">ADIM 01</span>
            </div>
            <h3>WhatsApp Fotoğraf &amp; Ön Ekspertiz</h3>
            <p>Hurda malzemenizin fotoğrafını ve tahmini miktarını <strong>0545 904 38 34</strong> hattımıza gönderin; metal analiz uzmanımız dakikalar içinde net KG fiyatını bildirsin.</p>
          </div>
          <div class="process-step">
            <div class="process-step-head">
              <span class="process-step-num">ADIM 02</span>
            </div>
            <h3>Mobil Kantarlı Araç &amp; Ekip Sevk</h3>
            <p>Konumunuza ve tonajınıza uygun kamyon, vinçli araç veya konteyner sistemimizi Mardin içi 15-45 dakikada, bölge illere aynı gün sevk ediyoruz.</p>
          </div>
          <div class="process-step">
            <div class="process-step-head">
              <span class="process-step-num">ADIM 03</span>
            </div>
            <h3>Hassas Tartım &amp; Kantar Fişi</h3>
            <p>Yükleme öncesi boş ve dolu araç tartımı veya elektronik saha kantarı ile malzemenizi sizin kontrolünüzde tartıp resmi kantar fişini teslim ediyoruz.</p>
          </div>
          <div class="process-step">
            <div class="process-step-head">
              <span class="process-step-num">ADIM 04</span>
            </div>
            <h3>Araç Başında Nakit / FAST Ödeme</h3>
            <p>Tartım fişindeki net kilogram ile anlaşılan birim fiyat çarpılarak toplam tutar araç sahadan ayrılmadan nakit veya banka FAST yoluyla ödenir.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="hizmet-bolgeleri">
      <div class="container">
        <div class="section-header">
          <div>
            <h2 class="section-title">Mardin İlçeleri ve Güneydoğu Anadolu Hizmet Ağı</h2>
            <p class="section-desc">
              Kızıltepe Atatürk Mahallesi'ndeki merkez tesisimizden tüm Mardin ilçelerine ve Güneydoğu Anadolu Organize Sanayi Bölgelerine kesintisiz lojistik destek.
            </p>
          </div>
        </div>

        <div class="region-columns">
          <div class="region-panel">
            <h3>Mardin Merkez ve İlçe Şubelerimiz</h3>
            <p style="font-size:0.875rem;color:var(--text-muted);margin-bottom:14px">
              Mardin sınırları içerisindeki tüm mahalle, sanayi sitesi, OSB ve tarımsal işletmelere aynı gün mobil kantar yönlendiriyoruz:
            </p>
            <ul class="region-list">
{mardin_list_html}
            </ul>
          </div>

          <div class="region-panel">
            <h3>Güneydoğu Anadolu Bölge Sevkiyat İlleri</h3>
            <p style="font-size:0.875rem;color:var(--text-muted);margin-bottom:14px">
              Fabrika sökümü, tonajlı demir, bakır, kablo ve kurumsal ihale alımlarında aktif hizmet verdiğimiz komşu iller:
            </p>
            <ul class="region-list">
{gd_list_html}
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="sikca-sorulan-sorular">
      <div class="container">
        <div class="content-layout" style="padding:0">
          <div>
            <h2 class="section-title" style="margin-bottom:18px">Sıkça Sorulan Sorular</h2>
            <div class="faq-list">
{faq_html}
            </div>
          </div>
          <div>
{render_contact_form_block("Kızıltepe / Mardin")}
          </div>
        </div>
      </div>
    </section>
  </main>
{render_footer(prices)}"""

    json_ld = build_json_ld(
        slug=slug,
        title=title,
        desc=desc,
        breadcrumbs=[("Ana Sayfa", "index.html")],
        faqs=faqs,
        date_iso=prices.get("dateIso", "2026-11-03")
    )
    return wrap_html_document(slug, title, desc, body, json_ld)


def build_all_prices_page(prices):
    slug = "hurda-fiyatlari.html"
    title = "Güncel Hurda Fiyatları 2026 | Canlı Borsa Hurda Fiyat Listesi (-%20 Net)"
    desc = "2026 güncel bakır, kablo, demir, alüminyum, sarı pirinç, paslanmaz krom, akü, çinko ve kurşun hurda fiyatları. Günlük LME borsa endeksli (%20 net kantar) Mardin alım listesi."

    all_ledgers = "\n".join(render_category_ledger_card(c) for c in prices["categories"])

    faqs = [
        ("2026 güncel hurda fiyatları ne sıklıkla değişiyor?",
         "Hurda metal fiyatları Londra Metal Borsası (LME) ton değerleri ve USD/TRY döviz kuruna bağlı olarak her gün sabah saatlerinde otomatik kazıyıcı sistemimiz tarafından güncellenmektedir."),
        ("Soyma bakır ve kırkambar bakır arasındaki fiyat farkı neden kaynaklanır?",
         "Soyma bakır (%99.9 saflıkta, kablosu sıyrılmış parlak iletken tel) doğrudan ergitmeye girdiği için en yüksek birim fiyattan alınır. Kırkambar veya yanık bakırda ise kalay, boya veya oksit firesi bulunduğundan haddehane randımanına göre fiyatlandırılır."),
        ("Tonajlı hurda satışında tablodaki fiyatların üzerinde teklif veriyor musunuz?",
         "Evet. 1 ton ve üzeri bakır, kablo, sarı pirinç, alüminyum veya 10 ton üzeri şantiye demiri yüklemelerinde lojistik maliyet avantajımızı doğrudan müşterimize yansıtarak liste fiyatının üzerinde özel kurumsal teklif sunuyoruz.")
    ]
    faq_html = "\n".join(
        f'<details class="faq-item" {"open" if i==0 else ""}><summary>{q}</summary><div class="faq-answer">{a}</div></details>'
        for i, (q, a) in enumerate(faqs)
    )

    body = f"""{render_topbar(prices)}
{render_header(prices, slug)}
{render_ticker(prices)}

  <main id="mainContent">
    <section class="page-banner">
      <div class="container">
        <ol class="breadcrumb">
          <li><a href="/index.html">Ana Sayfa</a></li>
          <li>/</li>
          <li>Güncel Hurda Fiyatları 2026</li>
        </ol>
        <h1>Güncel Hurda Fiyatları 2026 — LME Borsa &amp; Net Kantar Listesi</h1>
        <p>
          Son Güncelleme: <strong data-live-updated>{prices['updatedAt']}</strong> &bull; Tablomuzdaki net alım fiyatları, piyasa/borsa ham referans değerlerinden <strong>%20 saha ve işleme indirimi (x0.80)</strong> uygulanarak hesaplanmış gerçek peşin ödeme rakamlarıdır.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="ledger-grid">
{all_ledgers}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <div class="hero-grid">
          <div class="article-sheet">
            <h2>Mardin ve Güneydoğu Anadolu Hurda Fiyatlandırma Metodolojisi</h2>
            <p>
              <strong>{BRAND_NAME}</strong> olarak fiyat şeffaflığını esas alıyoruz. İnternette pek çok sitede yüksek yazılıp sahada kantar başında düşürülen yanıltıcı rakamlar yerine, borsa referans fiyatını ve <strong>-%20 net saha kantar fiyatımızı</strong> yan yana yayınlıyoruz.
            </p>
            <h3>Hurda Birim Fiyatını Belirleyen 4 Teknik Kriter</h3>
            <ul>
              <li><strong>Metal Saflık ve Alaşım Oranı:</strong> Bakırda %99.9 elektrolitik saflık, paslanmaz kromda 304/316/310 nikel-molibden oranı, kabloda ise net bakır iç randıman yüzdesi birim fiyatı doğrudan belirler.</li>
              <li><strong>Yabancı Madde ve Fire Durumu:</strong> Demir, plastik, yağ, toprak veya izolasyon malzemesinden arındırılmış temiz hurdalar en üst kademeden işlem görür.</li>
              <li><strong>Toplam Tonaj:</strong> Kızıltepe merkez kantarımıza teslim edilen veya tek seferde kamyon/tır bazında yüklenen tonajlı partilerde nakliye avantajı fiyata eklenir.</li>
              <li><strong>Güncel LME &amp; Döviz Kuru:</strong> Küresel metal kurları (USD/TRY: <span class="tabular" data-live-usd>{prices['exchange']['USD_TRY']:.2f} TL</span>) anlık olarak baz alınır.</li>
            </ul>
            <h3 style="margin-top:24px">Sıkça Sorulan Fiyat Soruları</h3>
            <div class="faq-list" style="margin-top:12px">
{faq_html}
            </div>
          </div>
{render_calculator_panel(prices)}
        </div>
      </div>
    </section>
  </main>
{render_footer(prices)}"""

    json_ld = build_json_ld(
        slug=slug,
        title=title,
        desc=desc,
        breadcrumbs=[("Ana Sayfa", "index.html"), ("Güncel Hurda Fiyatları", slug)],
        faqs=faqs,
        product_cat=prices["categories"][0],
        date_iso=prices.get("dateIso", "2026-11-03")
    )
    return wrap_html_document(slug, title, desc, body, json_ld)


def build_category_page(cat, prices):
    slug = cat["slug"]
    first = cat["items"][0]
    low_p = min(i["price"] for i in cat["items"])
    high_p = max(i["price"] for i in cat["items"])

    title = f"{cat['name']} 2026 | KG: {low_p:.2f} TL - {high_p:.2f} TL (Mardin Net Kantar)"
    desc = f"Güncel {cat['name'].lower()} ({prices['updatedAt']}): {first['name']} {first['price']:.2f} TL/KG. Mardin, Kızıltepe ve Güneydoğu Anadolu genelinde yerinde tartım ve nakit ödeme."

    rows = "\n".join(
        f'              <tr data-item-code="{it["code"]}">'
        f'<td><strong>{it["name"]}</strong></td>'
        f'<td class="col-market" data-col-market>{it["marketPrice"]:.2f} TL / {it["unit"]}</td>'
        f'<td class="col-net" data-col-net>{it["price"]:.2f} TL / {it["unit"]}</td>'
        f'<td class="tabular" style="text-align:right;font-weight:700">{it["tonPrice"]:,.0f} TL / TON</td>'
        f'</tr>'
        for it in cat["items"]
    )

    other_cats = "\n".join(
        f'              <li><a href="/{c["slug"]}"><span>{c["name"]}</span><span class="tabular">{c["items"][0]["price"]:.2f} TL</span></a></li>'
        for c in prices["categories"] if c["slug"] != slug
    )

    faqs = [
        (f"Bugün Mardin'de {cat['shortName'].lower()} kilosu ne kadar?",
         f"{prices['updatedAt']} itibarıyla Mardin ve Güneydoğu Anadolu kantarlarımızda {cat['shortName'].lower()} kilogram fiyatları kalitesine göre {low_p:.2f} TL ile {high_p:.2f} TL arasında değişmektedir. {first['name']} net alım fiyatımız {first['price']:.2f} TL/KG'dır."),
        (f"{cat['shortName']} alımında adresimizden tartım yapıyor musunuz?",
         f"Evet. Kızıltepe merkezimiz başta olmak üzere Artuklu, Midyat, Nusaybin, Derik, Mazıdağı ve tüm Güneydoğu Anadolu illerinde {cat['shortName'].lower()} partilerinizi kendi dijital kantarlı araçlarımızla adresinizde tartıp nakit alıyoruz."),
        (f"Karışık veya imalat artığı {cat['shortName'].lower()} nasıl sınıflandırılır?",
         f"Uzman eksperlerimiz sahanızda malzemenin saflık oranını ve varsa yabancı madde (plastik, boya, demir eki) oranını şeffaf biçimde ayırarak her kalemi kendi yüksek birim fiyatından ayrı ayrı tartar.")
    ]
    faq_html = "\n".join(
        f'<details class="faq-item" {"open" if i==0 else ""}><summary>{q}</summary><div class="faq-answer">{a}</div></details>'
        for i, (q, a) in enumerate(faqs)
    )

    body = f"""{render_topbar(prices)}
{render_header(prices, slug)}
{render_ticker(prices)}

  <main id="mainContent">
    <section class="page-banner">
      <div class="container">
        <ol class="breadcrumb">
          <li><a href="/index.html">Ana Sayfa</a></li>
          <li>/</li>
          <li><a href="/hurda-fiyatlari.html">Hurda Fiyatları</a></li>
          <li>/</li>
          <li>{cat['name']}</li>
        </ol>
        <h1>{cat['name']} — 2026 Mardin &amp; Güneydoğu Net Kantar Listesi</h1>
        <p>{cat['desc']} Güncel fiyat aralığı: <strong class="tabular">{low_p:.2f} TL/KG – {high_p:.2f} TL/KG</strong>.</p>
      </div>
    </section>

    <div class="container content-layout">
      <div class="article-sheet">
        <div style="margin-bottom:24px;border-radius:6px;overflow:hidden;border:1px solid var(--border-light)">
          <img src="/{cat['image']}" alt="{cat['name']} - Bulgan Hurdacılık Kızıltepe Mardin Kantar" width="960" height="640" style="width:100%;height:auto">
        </div>

        <h2>Güncel {cat['name']} Tablosu ({prices['updatedAt']})</h2>
        <p>
          Aşağıdaki tabloda yer alan <strong>Net Alım (-%20)</strong> sütunu, LME ve Türkiye metal piyasası referans verilerinden %20 işleme/fire indirimi düşülerek oluşturulmuş <strong>peşin kantar ödeme</strong> fiyatlarımızdır.
        </p>

        <div class="price-table-wrap" style="margin:18px 0 28px;border:1px solid var(--border-light);border-radius:6px">
          <table class="price-table">
            <thead>
              <tr>
                <th>Alt Kalite / Malzeme Tanımı</th>
                <th style="text-align:right">Borsa Referans</th>
                <th style="text-align:right">Net Alım (-%20)</th>
                <th style="text-align:right">1 Ton Net Tutar</th>
              </tr>
            </thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>

        <div class="info-callout">
          <strong>Tonajlı Alım Avantajı:</strong> 500 KG ve üzeri <strong>{cat['shortName'].lower()}</strong> satışlarınızda Mardin, Diyarbakır, Şanlıurfa, Gaziantep ve Batman genelinde özel nakliye ve tonaj primi uygulanır. Hemen <a href="tel:{PHONE_TEL}" style="font-weight:800">{PHONE_DISPLAY}</a> hattımızdan kantar şefimizle görüşebilirsiniz.
        </div>

        <h2>Mardin ve Güneydoğu'da {cat['shortName']} Alım ve Ekspertiz Kriterlerimiz</h2>
        <p>
          <strong>{BRAND_NAME}</strong> olarak Kızıltepe Atatürk Mahallesi'ndeki merkez tesisimizde ve mobil saha araçlarımızda her türlü <strong>{cat['shortName'].lower()}</strong> grubunu kalitesine göre ayrıştırıyoruz. Sanayi tesisleri, elektrik taahhüt firmaları, inşaat şantiyeleri ve tarımsal işletmelerden çıkan malzemelerinizde fire kesintisini minimumda tutarak tam ağırlık üzerinden nakit ödeme gerçekleştiriyoruz.
        </p>

        <h3>Sıkça Sorulan Sorular ({cat['name']})</h3>
        <div class="faq-list" style="margin-top:14px;margin-bottom:28px">
{faq_html}
        </div>

{render_contact_form_block("Kızıltepe / Mardin")}
      </div>

      <div class="sidebar-stack">
{render_calculator_panel(prices)}
        <div class="sidebar-box">
          <h3>Diğer Hurda Fiyat Grupları</h3>
          <ul class="sidebar-links">
{other_cats}
          </ul>
        </div>
      </div>
    </div>
  </main>
{render_footer(prices)}"""

    json_ld = build_json_ld(
        slug=slug,
        title=title,
        desc=desc,
        breadcrumbs=[("Ana Sayfa", "index.html"), ("Hurda Fiyatları", "hurda-fiyatlari.html"), (cat["name"], slug)],
        faqs=faqs,
        product_cat=cat,
        date_iso=prices.get("dateIso", "2026-11-03")
    )
    return wrap_html_document(slug, title, desc, body, json_ld, og_image=cat["fallbackImage"])


def build_regional_page(reg, prices, is_mardin=True):
    slug = reg["slug"]
    name = reg["name"]
    title = reg["title"]
    h1 = reg["h1"]
    desc = reg["desc"]

    # Summary table of top categories for this city
    summary_rows = []
    for c in prices["categories"][:10]:
        first = c["items"][0]
        summary_rows.append(
            f'<tr data-item-code="{first["code"]}">'
            f'<td><a href="/{c["slug"]}" style="font-weight:700;color:var(--text-ink)">{c["shortName"]}</a> ({first["name"]})</td>'
            f'<td class="col-market" data-col-market>{first["marketPrice"]:.2f} TL</td>'
            f'<td class="col-net" data-col-net>{first["price"]:.2f} TL / KG</td>'
            f'</tr>'
        )
    summary_table = "\n".join(summary_rows)

    sibling_list = MARDIN_DISTRICTS if is_mardin else GUNEYDOGU_PROVINCES
    sidebar_region_links = "\n".join(
        f'              <li><a href="/{r["slug"]}"><span>{r["name"]} Hurdacı</span><span>{r["eta"].split()[0]}</span></a></li>'
        for r in sibling_list if r["slug"] != slug
    )

    faqs = [
        (f"{name} bölgesinde adresimizden hurda alımı için ne kadar sürede geliyorsunuz?",
         f"Kızıltepe Atatürk Mahallesi'ndeki ana kantar merkezimizden {name} bölgesine ortalama varış ve araç sevk süremiz: {reg['eta']}. WhatsApp üzerinden konum paylaştığınızda en yakın mobil kantarlı ekibimiz yönlendirilir."),
        (f"{name} sanayi ve şantiyelerinden hangi hurdaları alıyorsunuz?",
         f"{reg['zone']} başta olmak üzere tüm {name} genelinde soyma bakır, enerji ve dalgıç pompa kabloları, DKP ve inşaat yıkım demiri, alüminyum, sarı pirinç, 304/316 paslanmaz krom, chiller soğutma grupları ve akü hurdalarını alıyoruz."),
        (f"{name} hurda alımlarında ödeme nasıl yapılıyor?",
         f"{name} saha alımlarımızda tartım işlemi dijital kantarımızda tamamlandığı anda, araç sahadan ayrılmadan elden nakit veya şirket/şahıs IBAN hesabınıza anında FAST/EFT ile ödenir.")
    ]
    faq_html = "\n".join(
        f'<details class="faq-item" {"open" if i==0 else ""}><summary>{q}</summary><div class="faq-answer">{a}</div></details>'
        for i, (q, a) in enumerate(faqs)
    )

    body = f"""{render_topbar(prices)}
{render_header(prices, slug)}
{render_ticker(prices)}

  <main id="mainContent">
    <section class="page-banner">
      <div class="container">
        <ol class="breadcrumb">
          <li><a href="/index.html">Ana Sayfa</a></li>
          <li>/</li>
          <li><a href="/{'mardin-hurdaci.html' if is_mardin else 'diyarbakir-hurdaci.html'}">{'Mardin Hizmet Bölgeleri' if is_mardin else 'Güneydoğu Anadolu Bölgeleri'}</a></li>
          <li>/</li>
          <li>{name} Hurdacı</li>
        </ol>
        <h1>{h1}</h1>
        <p>{desc}</p>
      </div>
    </section>

    <div class="container content-layout">
      <div class="article-sheet">
        <div class="hero-specs" style="margin-top:0;margin-bottom:24px;padding-top:0;border-top:none">
          <div class="hero-spec-item" style="background:var(--bg-page);border-color:var(--border-light)">
            <div class="hero-spec-title" style="color:var(--brand-green)">Saha Sevk Süresi</div>
            <div class="hero-spec-desc" style="color:var(--text-ink);font-weight:700">{reg['eta']}</div>
          </div>
          <div class="hero-spec-item" style="background:var(--bg-page);border-color:var(--border-light)">
            <div class="hero-spec-title" style="color:var(--brand-green)">Aktif Sanayi &amp; Saha Hattı</div>
            <div class="hero-spec-desc" style="color:var(--text-ink);font-weight:600">{reg['zone']}</div>
          </div>
          <div class="hero-spec-item" style="background:var(--bg-page);border-color:var(--border-light)">
            <div class="hero-spec-title" style="color:var(--brand-green)">Kantar &amp; Ödeme</div>
            <div class="hero-spec-desc" style="color:var(--text-ink);font-weight:700">Yerinde Dijital Tartım &bull; Peşin</div>
          </div>
        </div>

        <h2>{name} Hurda Alım Hizmetlerimiz ve Bölgesel Saha Çözümleri</h2>
        <p>
          <strong>{BRAND_NAME}</strong> olarak {name} genelinde bireysel, kurumsal, şantiye ve fabrika ölçekli tüm metal geri dönüşüm taleplerine doğrudan kendi araç filomuzla yanıt veriyoruz. {reg['focus']}
        </p>

        <h2>{name} Güncel Hurda Fiyatları ({prices['updatedAt']})</h2>
        <p>
          {name} adresinizden yapılan alımlarda geçerli, günlük LME borsa verilerinden <strong>-%20 net kantar</strong> bazıyla hesaplanmış güncel fiyat özetimiz:
        </p>

        <div class="price-table-wrap" style="margin:16px 0 26px;border:1px solid var(--border-light);border-radius:6px">
          <table class="price-table">
            <thead>
              <tr>
                <th>Hurda Metal Grubu &amp; Baz Kalem</th>
                <th style="text-align:right">Borsa Referans</th>
                <th style="text-align:right">{name} Net Alım (-%20)</th>
              </tr>
            </thead>
            <tbody>
{summary_table}
            </tbody>
          </table>
        </div>

        <h3>{name} Bölgesinde Sıkça Sorulan Sorular</h3>
        <div class="faq-list" style="margin:14px 0 28px">
{faq_html}
        </div>

{render_contact_form_block(name)}
      </div>

      <div class="sidebar-stack">
{render_calculator_panel(prices)}
        <div class="sidebar-box">
          <h3>{'Diğer Mardin İlçelerimiz' if is_mardin else 'Diğer Güneydoğu İllerimiz'}</h3>
          <ul class="sidebar-links">
{sidebar_region_links}
          </ul>
        </div>
      </div>
    </div>
  </main>
{render_footer(prices)}"""

    json_ld = build_json_ld(
        slug=slug,
        title=title,
        desc=desc,
        breadcrumbs=[("Ana Sayfa", "index.html"), (f"{name} Hurdacı", slug)],
        faqs=faqs,
        geo_info=reg,
        date_iso=prices.get("dateIso", "2026-11-03")
    )
    return wrap_html_document(slug, title, desc, body, json_ld)


def build_extra_service_page(svc, prices):
    slug = svc["slug"]
    cat = next((c for c in prices["categories"] if c["id"] == svc["cat_id"]), prices["categories"][0])
    rows = "\n".join(
        f'<tr data-item-code="{it["code"]}"><td>{it["name"]}</td><td class="col-market" data-col-market>{it["marketPrice"]:.2f} TL</td><td class="col-net" data-col-net>{it["price"]:.2f} TL / {it["unit"]}</td></tr>'
        for it in cat["items"]
    )
    faqs = [
        (f"{svc['h1']} işleminde söküm ve nakliye kime ait?",
         "Bulgan Hurdacılık olarak oksijen/plazma kesim ustalarımız, vinçli kamyonlarımız ve iş güvenliği ekipmanlarımızla yerinde söküm ve yükleme işlemini tamamen kendi bünyemizde gerçekleştiriyoruz."),
        ("Söküm öncesi ücretsiz keşif yapıyor musunuz?",
         "Evet. Mardin merkez, Kızıltepe ve tüm Güneydoğu Anadolu illerindeki tesis, fabrika, soğutma grubu veya depo rafı sökümlerinde yerinde ücretsiz ekspertiz yaparak net tonaj veya götürü bedel teklifi sunuyoruz.")
    ]
    faq_html = "\n".join(
        f'<details class="faq-item" {"open" if i==0 else ""}><summary>{q}</summary><div class="faq-answer">{a}</div></details>'
        for i, (q, a) in enumerate(faqs)
    )
    body = f"""{render_topbar(prices)}
{render_header(prices, slug)}
{render_ticker(prices)}

  <main id="mainContent">
    <section class="page-banner">
      <div class="container">
        <ol class="breadcrumb">
          <li><a href="/index.html">Ana Sayfa</a></li>
          <li>/</li>
          <li><a href="/hizmetlerimiz.html">Hizmetlerimiz</a></li>
          <li>/</li>
          <li>{svc['h1']}</li>
        </ol>
        <h1>{svc['h1']}</h1>
        <p>{svc['desc']}</p>
      </div>
    </section>

    <div class="container content-layout">
      <div class="article-sheet">
        <div style="margin-bottom:22px;border-radius:6px;overflow:hidden;border:1px solid var(--border-light)">
          <img src="/{svc['image']}" alt="{svc['h1']} - Bulgan Hurdacılık" width="960" height="640">
        </div>
        <h2>Profesyonel Saha Sökümü ve Peşin Metal Değerleme</h2>
        <p>{svc['desc']}</p>
        <p>
          Kızıltepe Atatürk Mahallesi'ndeki merkezimizden Mardin, Diyarbakır, Şanlıurfa, Gaziantep, Batman ve Şırnak genelindeki tüm sanayi tesislerine uzman kesim ekibi ve mobil kantar yönlendiriyoruz.
        </p>

        <h3>İlgili Metal Grubu Güncel Kantar Fiyatları ({cat['name']})</h3>
        <div class="price-table-wrap" style="margin:16px 0 26px;border:1px solid var(--border-light);border-radius:6px">
          <table class="price-table">
            <thead>
              <tr><th>Malzeme Cinsi</th><th style="text-align:right">Borsa</th><th style="text-align:right">Net Alım (-%20)</th></tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>

        <h3>Sıkça Sorulan Sorular</h3>
        <div class="faq-list" style="margin:14px 0 28px">{faq_html}</div>
{render_contact_form_block("Kızıltepe / Mardin")}
      </div>
      <div class="sidebar-stack">
{render_calculator_panel(prices)}
      </div>
    </div>
  </main>
{render_footer(prices)}"""

    json_ld = build_json_ld(
        slug=slug,
        title=svc["title"],
        desc=svc["desc"],
        breadcrumbs=[("Ana Sayfa", "index.html"), (svc["h1"], slug)],
        faqs=faqs,
        product_cat=cat,
        date_iso=prices.get("dateIso", "2026-11-03")
    )
    return wrap_html_document(slug, svc["title"], svc["desc"], body, json_ld)


def build_corporate_and_utility_pages(prices):
    pages = {}

    # 1. Hakkımızda
    pages["hakkimizda.html"] = (
        "Hakkımızda | Bulgan Hurdacılık & Geri Dönüşüm (Kızıltepe / Mardin)",
        "Mardin Kızıltepe Atatürk Mahallesi merkezli Bulgan Hurdacılık; Güneydoğu Anadolu genelinde lisanslı metal geri dönüşüm, fabrika sökümü ve hassas kantar hizmetleri sunar.",
        f"""
        <h2>Kurumsal Kimliğimiz ve Kızıltepe Merkez Kantar Altyapımız</h2>
        <p><strong>{BRAND_NAME}</strong>, Mardin'in ticaret ve lojistik kalbi olan <strong>Kızıltepe Atatürk Mahallesi</strong>'ndeki merkez tesisinden tüm Mardin ilçelerine ve Güneydoğu Anadolu sanayi havzasına hizmet veren köklü bir metal geri dönüşüm kuruluşudur.</p>
        <p>Sektörde güvenin temeli olan <strong>doğru tartım</strong> ve <strong>anında nakit ödeme</strong> ilkelerini tavizsiz uyguluyoruz. Elektronik kantarlarımız düzenli kalibrasyona tabi tutulmakta olup, her alımda müşterimize şeffaf kantar fişi teslim edilmektedir.</p>
        <h3>Neden Bulgan Hurdacılık?</h3>
        <ul>
          <li><strong>Bölgesel Saha Hakimiyeti:</strong> Mardin OSB, Kızıltepe Hububat Merkezi, Nusaybin İpekyolu koridoru, Diyarbakır, Şanlıurfa, Gaziantep ve Batman sanayi bölgelerine kendi araç filomuzla doğrudan erişim.</li>
          <li><strong>Şeffaf Borsa Endeksli Fiyatlama:</strong> Londra Metal Borsası (LME) ve yurt içi haddehane verilerine dayalı, sürpriz kesinti içermeyen net fiyat politikası.</li>
          <li><strong>Endüstriyel Kesim ve Söküm Yetkinliği:</strong> Fabrika tasfiyesi, çelik çatı kesimi, chiller ve kazan dairelerinin İSG kurallarına uygun güvenli sökümü.</li>
        </ul>
        {render_contact_form_block("Kızıltepe / Mardin")}
        """,
        False
    )

    # 2. Hizmetlerimiz
    pages["hizmetlerimiz.html"] = (
        "Hizmetlerimiz | Adresten Hurda Alımı, Fabrika Sökümü & Mobil Kantar",
        "Bulgan Hurdacılık hizmetleri: Mardin ve Güneydoğu Anadolu'da adresten metal hurda alımı, fabrika ve çelik konstrüksiyon sökümü, trafo/kablo geri dönüşümü.",
        f"""
        <h2>Mardin ve Güneydoğu Anadolu Metal Geri Dönüşüm Hizmetlerimiz</h2>
        <p>Sanayi kuruluşları, inşaat müteahhitleri, elektrik taahhüt firmaları, tarımsal işletmeler ve bireysel müşterilerimiz için uçtan uca hurda yönetimi sağlıyoruz:</p>
        <ul>
          <li><strong>Adresten Mobil Kantarlı Hurda Alımı:</strong> Bakır, sarı pirinç, alüminyum, kablo, demir, paslanmaz krom, çinko, kurşun ve akü hurdalarının kapınızda tartılarak nakit alınması.</li>
          <li><strong><a href="/fabrika-sokumu-yikim.html">Fabrika, Tesis ve Çelik Konstrüksiyon Sökümü</a>:</strong> Kullanım dışı fabrika binaları, çırçır ve un tesisleri ile çelik çatıların hurda karşılığı güvenli sökümü.</li>
          <li><strong><a href="/chiller-hurda-fiyatlari.html">Chiller, İklimlendirme ve Kazan Dairesi Sökümü</a>:</strong> Otel, hastane ve AVM'lerdeki merkezi soğutma gruplarının yerinde kesimi ve nakliyesi.</li>
          <li><strong>Şantiye Konteyner Sistemi:</strong> Devam eden inşaat ve imalat projelerine hurda biriktirme konteyneri bırakılması ve periyodik kantar tartımı.</li>
        </ul>
        {render_contact_form_block("Kızıltepe / Mardin")}
        """,
        False
    )

    # 3. İletişim
    pages["iletisim.html"] = (
        "İletişim & Kantar Konumu | Bulgan Hurdacılık Kızıltepe / Mardin (0545 904 38 34)",
        "Bulgan Hurdacılık iletişim bilgileri: Atatürk Mahallesi, Kızıltepe / Mardin. Kantar ve WhatsApp hattı: 0545 904 38 34. E-posta: bulganorhan19@gmail.com.",
        f"""
        <h2>Merkez Kantar ve Müşteri İletişim Bilgilerimiz</h2>
        <div class="hero-specs" style="margin:0 0 24px;padding:0;border:none">
          <div class="hero-spec-item" style="background:var(--bg-page);border-color:var(--border-light)">
            <div class="hero-spec-title" style="color:var(--brand-green)">Kantar &amp; WhatsApp Hattı</div>
            <div class="hero-spec-desc"><a href="tel:{PHONE_TEL}" class="tabular" style="font-size:1.1rem;font-weight:800;color:var(--text-ink)">{PHONE_DISPLAY}</a></div>
          </div>
          <div class="hero-spec-item" style="background:var(--bg-page);border-color:var(--border-light)">
            <div class="hero-spec-title" style="color:var(--brand-green)">Kurumsal E-Posta</div>
            <div class="hero-spec-desc"><a href="mailto:{EMAIL}" style="font-weight:700;color:var(--text-ink)">{EMAIL}</a></div>
          </div>
          <div class="hero-spec-item" style="background:var(--bg-page);border-color:var(--border-light)">
            <div class="hero-spec-title" style="color:var(--brand-green)">Merkez Kantar Adresi</div>
            <div class="hero-spec-desc" style="color:var(--text-ink);font-weight:600">{ADDRESS}</div>
          </div>
        </div>
        <div style="margin-bottom:28px;border:1px solid var(--border-light);border-radius:6px;overflow:hidden">
          <iframe title="Bulgan Hurdacılık Kızıltepe Mardin Harita Konumu" src="https://www.google.com/maps?q=Atat%C3%BCrk+Mahallesi+K%C4%B1z%C4%B1ltepe+Mardin&output=embed" width="100%" height="340" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        {render_contact_form_block("Kızıltepe / Mardin")}
        """,
        False
    )

    # 4. KVKK & Gizlilik Politikası
    pages["gizlilik-politikasi.html"] = (
        "KVKK ve Gizlilik Politikası | Bulgan Hurdacılık & Geri Dönüşüm",
        "Bulgan Hurdacılık (bulgangeridonusum.com.tr) 6698 sayılı KVKK aydınlatma metni, kişisel verilerin korunması ve çerez gizlilik politikası.",
        f"""
        <h2>6698 Sayılı Kişisel Verilerin Korunması Kanunu (KVKK) Aydınlatma Metni</h2>
        <p><strong>Veri Sorumlusu:</strong> {BRAND_NAME} ({ADDRESS} — Tel: {PHONE_DISPLAY} — E-posta: {EMAIL})</p>
        <p>Web sitemiz (<strong>bulgangeridonusum.com.tr</strong>) üzerinden ilettiğiniz ad-soyad, telefon numarası, konum ve hurda malzeme bilgileri; yalnızca tarafınıza doğru hurda fiyat teklifi sunulması, saha kantar aracımızın adresinize yönlendirilmesi ve ticari alım sürecinin yürütülmesi amacıyla işlenmektedir.</p>
        <h3>1. Kişisel Verilerin Aktarımı ve Güvenliği</h3>
        <p>Paylaştığınız iletişim verileri üçüncü taraf reklam veya pazarlama şirketleriyle <strong>kesinlikle paylaşılmaz</strong>. Verileriniz SSL şifreli bağlantı üzerinden doğrudan kantar yönetim e-postamıza ({EMAIL}) iletilir.</p>
        <h3>2. Çerez (Cookie) Kullanımı</h3>
        <p>Sitemizde kullanıcı çerez tercihini hatırlamak ve canlı borsa fiyat tablolarının performansını ölçmek amacıyla temel yerel depolama (localStorage) çerezleri kullanılmaktadır.</p>
        <h3>3. KVKK Madde 11 Kapsamındaki Haklarınız</h3>
        <p>Verilerinizin silinmesini veya güncellenmesini talep etmek için her zaman <a href="mailto:{EMAIL}">{EMAIL}</a> adresimize yazılı başvuruda bulunabilirsiniz.</p>
        """,
        False
    )

    # 5. Kullanım Koşulları
    pages["kullanim-kosullari.html"] = (
        "Kullanım Koşulları ve Ticari Şartlar | Bulgan Hurdacılık",
        "bulgangeridonusum.com.tr web sitesi kullanım koşulları, canlı borsa hurda fiyat tablosu bilgilendirme şartları ve telif hakları.",
        f"""
        <h2>Web Sitesi Kullanım Koşulları ve Fiyat Bilgilendirme Şartları</h2>
        <p><strong>bulgangeridonusum.com.tr</strong> internet sitesine erişim sağlayan tüm ziyaretçiler aşağıdaki ticari ve hukuki şartları kabul etmiş sayılır:</p>
        <ul>
          <li><strong>Canlı Fiyat Tabloları ve Hesaplama Aracı:</strong> Sitemizde yayınlanan hurda fiyatları, günlük borsa/piyasa verilerinden %20 saha ve işleme indirimi düşülerek oluşturulmuş baz kantar fiyatlarıdır. Kesin ödeme tutarı, malzemenin sahada yapılacak fiziksel saflık/fire kontrolü ve resmi dijital kantar tartımı sonucunda netleşir.</li>
          <li><strong>Ticari Mülkiyet ve Görsel Hakları:</strong> Sitedeki tüm <strong>Bulgan Hurdacılık</strong> logolu saha görselleri, fiyat kazıyıcı yazılımlar ve içerikler firmamıza aittir; izinsiz kopyalanamaz.</li>
          <li><strong>Resmi İşlem ve Kantar Fişi:</strong> Tüm alımlarımız resmi tartım fişi ve yürürlükteki çevre/geri dönüşüm mevzuatına uygun olarak gerçekleştirilir.</li>
        </ul>
        """,
        False
    )

    # 6. Teşekkürler Sayfası
    pages["tesekkurler.html"] = (
        "Talebiniz Alındı | Bulgan Hurdacılık Kantar Merkezi",
        "Hurda fiyat teklifi ve mobil kantar talebiniz Bulgan Hurdacılık merkezine ulaştı.",
        f"""
        <h2>Kantar ve Fiyat Teklifi Talebiniz Merkezimize Ulaştı</h2>
        <p>Formunuz başarıyla <strong>{EMAIL}</strong> kantar yönetim sistemimize iletilmiştir. Saha şefimiz en kısa sürede telefon numaranız üzerinden sizinle iletişime geçecektir.</p>
        <div class="info-callout">
          <strong>Beklemeden Anında Fiyat Almak İçin:</strong> Hurdanızın fotoğrafını doğrudan WhatsApp hattımıza göndererek 5 dakika içinde net KG fiyatını öğrenebilirsiniz.
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:20px">
          <a href="tel:{PHONE_TEL}" class="btn btn-primary tabular">{SVG_PHONE} Hemen Ara: {PHONE_DISPLAY}</a>
          <a href="https://wa.me/{PHONE_WA}?text=Merhaba%2C%20web%20sitenizden%20form%20doldurdum%2C%20h%C4%B1zl%C4%B1%20fiyat%20almak%20istiyorum." target="_blank" rel="noopener" class="btn btn-gold">{SVG_WA} WhatsApp'a Geç</a>
          <a href="/index.html" class="btn btn-outline-dark">Ana Sayfaya Dön</a>
        </div>
        """,
        True
    )

    # 7. Özel 404 Sayfası
    pages["404.html"] = (
        "Sayfa Bulunamadı (404) | Bulgan Hurdacılık & Geri Dönüşüm",
        "Aradığınız sayfa taşınmış veya kaldırılmış olabilir. Güncel Mardin hurda fiyatlarına ve kantar hesaplama aracına buradan ulaşabilirsiniz.",
        f"""
        <h2>Aradığınız Sayfa Bulunamadı (Hata Kodu: 404)</h2>
        <p>Aradığınız bağlantı değişmiş veya kaldırılmış olabilir. Güncel hurda fiyat listemize, canlı kantar hesaplama aracımıza veya iletişim hattımıza aşağıdaki bağlantılardan doğrudan ulaşabilirsiniz:</p>
        <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:20px">
          <a href="/index.html" class="btn btn-primary">Ana Sayfaya Dön</a>
          <a href="/hurda-fiyatlari.html" class="btn btn-outline-dark">2026 Güncel Hurda Fiyatları</a>
          <a href="tel:{PHONE_TEL}" class="btn btn-gold tabular">{SVG_PHONE} {PHONE_DISPLAY}</a>
        </div>
        """,
        True
    )

    out = {}
    for slug, (title, desc, inner_html, noindex) in pages.items():
        h1_text = title.split("|")[0].strip()
        body = f"""{render_topbar(prices)}
{render_header(prices, slug)}
{render_ticker(prices)}
  <main id="mainContent">
    <section class="page-banner">
      <div class="container">
        <ol class="breadcrumb">
          <li><a href="/index.html">Ana Sayfa</a></li>
          <li>/</li>
          <li>{h1_text}</li>
        </ol>
        <h1>{h1_text}</h1>
        <p>{desc}</p>
      </div>
    </section>
    <div class="container content-layout">
      <div class="article-sheet">{inner_html}</div>
      <div class="sidebar-stack">{render_calculator_panel(prices)}</div>
    </div>
  </main>
{render_footer(prices)}"""
        json_ld = build_json_ld(slug, title, desc, [("Ana Sayfa", "index.html"), (h1_text, slug)], date_iso=prices.get("dateIso", "2026-11-03"))
        out[slug] = wrap_html_document(slug, title, desc, body, json_ld, noindex=noindex)
    return out


def build_aeo_and_seo_infrastructure(prices, all_generated_slugs):
    # 1. AI-aware robots.txt (per agency-aeo-foundations-architect)
    robots_txt = f"""# Bulgan Hurdacılık & Geri Dönüşüm — SEO & AEO Crawler Policy
# Domain: {DOMAIN}

User-agent: *
Allow: /
Disallow: /api/contact
Disallow: /tesekkurler.html

# AI Search & Citation Engines (Explicitly Allowed)
User-agent: Googlebot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Yandex
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)

    # 2. llms.txt & llms-full.txt (for ChatGPT, Perplexity, Gemini, Claude citations)
    price_lines = []
    for c in prices["categories"]:
        first = c["items"][0]
        price_lines.append(f"- [{c['name']}]({DOMAIN}/{c['slug']}): {first['name']} = {first['price']:.2f} TL/KG (Borsa Referans: {first['marketPrice']:.2f} TL/KG)")

    llms_txt = f"""# {BRAND_NAME}

> Mardin (Kızıltepe Atatürk Mahallesi merkez kantar) ve Güneydoğu Anadolu Bölgesi (Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman, Kilis) lisanslı metal geri dönüşüm, fabrika sökümü ve adresten nakit hurda alım merkezi.

## Kurumsal İletişim & Kantar Bilgileri
- **Resmi Web Sitesi:** {DOMAIN}
- **Telefon & WhatsApp Kantar Hattı:** {PHONE_DISPLAY} ({PHONE_TEL})
- **E-Posta:** {EMAIL}
- **Merkez Kantar Adresi:** {ADDRESS}
- **Çalışma Saatleri:** Haftanın 7 günü 07:30 - 21:00
- **Ödeme Yöntemi:** Dijital kantar tartımı sonrası araç başında anında Nakit, FAST veya EFT.

## Güncel Hurda Fiyatları ({prices['updatedAt']} — Borsa -%20 Net Kantar Bazı)
{chr(10).join(price_lines)}

## Mardin İlçe Şubeleri
{chr(10).join(f"- [{d['name']} Hurdacı]({DOMAIN}/{d['slug']}): {d['desc']}" for d in MARDIN_DISTRICTS)}

## Güneydoğu Anadolu Hizmet İlleri
{chr(10).join(f"- [{p['name']} Hurdacı]({DOMAIN}/{p['slug']}): {p['desc']}" for p in GUNEYDOGU_PROVINCES)}
"""
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(llms_txt)
    with open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8") as f:
        f.write(llms_txt)

    # 3. Image-enriched sitemap.xml
    date_iso = prices.get("dateIso", "2026-11-03")
    url_entries = []
    for slug in all_generated_slugs:
        if slug in ("404.html", "tesekkurler.html"):
            continue
        loc = f"{DOMAIN}/" if slug == "index.html" else f"{DOMAIN}/{slug}"
        prio = "1.0" if slug == "index.html" else ("0.9" if "fiyatlari" in slug or slug == "mardin-hurdaci.html" or slug == "kiziltepe-hurdaci.html" else "0.8")
        freq = "daily" if ("fiyatlari" in slug or slug == "index.html") else "weekly"
        url_entries.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{date_iso}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>""")

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_entries)}
</urlset>
"""
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)


def generate_all():
    prices = load_prices()
    generated = {}

    # 1. Index & Master Price Page
    generated["index.html"] = build_index_page(prices)
    generated["hurda-fiyatlari.html"] = build_all_prices_page(prices)

    # 2. 15 Category Price Pages
    for cat in prices["categories"]:
        generated[cat["slug"]] = build_category_page(cat, prices)

    # 3. 11 Mardin District Pages
    for dist in MARDIN_DISTRICTS:
        generated[dist["slug"]] = build_regional_page(dist, prices, is_mardin=True)

    # 4. 8 Güneydoğu Province Pages
    for prov in GUNEYDOGU_PROVINCES:
        generated[prov["slug"]] = build_regional_page(prov, prices, is_mardin=False)

    # 5. 5 Extra Industrial Service Pages
    for svc in EXTRA_SERVICE_PAGES:
        generated[svc["slug"]] = build_extra_service_page(svc, prices)

    # 6. 7 Corporate & Legal Pages
    corp_pages = build_corporate_and_utility_pages(prices)
    generated.update(corp_pages)

    # 7. Legacy URL aliases so existing bookmarks/links never break
    alias_map = {
        "bakir.html": "bakir-hurda-fiyatlari.html",
        "kablo.html": "kablo-hurda-fiyatlari.html",
        "demir.html": "demir-hurda-fiyatlari.html",
        "aluminyum.html": "aluminyum-hurda-fiyatlari.html",
        "sari.html": "sari-hurda-fiyatlari.html",
        "paslanmaz.html": "paslanmaz-hurda-fiyatlari.html",
        "aku.html": "aku-hurda-fiyatlari.html",
        "cinko.html": "cinko-hurda-fiyatlari.html",
        "kursun.html": "kursun-hurda-fiyatlari.html",
        "nikel.html": "nikel-hurda-fiyatlari.html",
        "bronz.html": "bronz-hurda-fiyatlari.html",
        "elektronik.html": "elektronik-hurda-fiyatlari.html",
        "klima.html": "klima-hurda-fiyatlari.html",
        "plastik.html": "plastik-hurda-fiyatlari.html",
        "kagit.html": "kagit-hurda-fiyatlari.html",
    }

    for slug, html_content in generated.items():
        with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
            f.write(html_content)

    for alias_slug, target_slug in alias_map.items():
        # Write canonical redirect/copy for legacy short filenames
        with open(os.path.join(ROOT, alias_slug), "w", encoding="utf-8") as f:
            f.write(generated[target_slug])

    build_aeo_and_seo_infrastructure(prices, list(generated.keys()))
    print(f"Generated {len(generated)} primary HTML pages + {len(alias_map)} alias pages + llms.txt + robots.txt + sitemap.xml")


if __name__ == "__main__":
    generate_all()


# ==============================================================================
# BLOG YAZILARI (TAMAMI MARDİN & GÜNEYDOĞU ANADOLU ODAKLI, ÖZGÜN & DERİN İÇERİK)
# ==============================================================================
BLOG_POSTS = [
    {
        "slug": "hurda-kablo-fiyati-2026-guncel-kablo-hurda-cesitleri-ve-kilosu-ne-kadar.html",
        "title": "Hurda Kablo Fiyatı 2026: Bakır Randıman Oranı ve Kilosu Ne Kadar?",
        "h1": "2026 Hurda Kablo Fiyatları: Bakır Randıman Analizi ve Soyma/Kırma Hesabı",
        "desc": "Mardin, Kızıltepe, Diyarbakır ve Şanlıurfa'da dalgıç pompa kablosu, NYA, TTR, antigron ve yeraltı enerji kablolarının bakır randıman oranı ve 2026 KG fiyatları.",
        "keywords": "hurda kablo fiyatı 2026, dalgıç pompa kablosu hurda fiyatı, mardin kablo hurdası, kızıltepe hurda kablo alımı, %50 bakırlı kablo fiyatı, yeraltı enerji kablosu hurdası",
        "image": "images/kablo.webp",
        "cat_id": "kablo",
        "date": "2026-11-03",
        "sections": [
            ("Güneydoğu Anadolu'da Hurda Kablo Fiyatları Nasıl Hesaplanır?",
             "Hurda kablo alımında birim kilogram fiyatını belirleyen temel mühendislik kriteri, kablonun dış PVC/kauçuk izolasyonu sıyrıldıktan sonra içerisinden çıkan saf elektrolitik bakırın ağırlık yüzdesidir (randıman oranı). Kızıltepe Atatürk Mahallesi'ndeki merkez kantarımızda ve mobil saha araçlarımızda kablolarınızı ezbere 'karışık kablo' fiyatından değil, numune soyma veya kırma testi yaparak gerçek bakır oranı üzerinden değerlendiriyoruz."),
            ("Kızıltepe, Derik ve Viranşehir Hattında Dalgıç Pompa Kabloları",
             "Mardin Kızıltepe ovası, Derik, Nusaybin ile Şanlıurfa Viranşehir ve Ceylanpınar tarım havzalarında derin kuyu sulama sistemlerinde kullanılan 3x16, 3x25, 3x35 ve 3x50 mm² yassı/yuvarlak dalgıç pompa kabloları en yüksek bakır randımanına (%62 ila %78 arası saf bakır) sahip kablo grubudur. Bu kablolar kantarımızda soyma bakır değerine en yakın üst kademeden nakit satın alınmaktadır."),
            ("Sanayi ve Şantiye Kablo Çeşitlerinin Bakır Randıman Sınıfları",
             "Diyarbakır OSB, Gaziantep Başpınar OSB, Mardin OSB ve Batman enerji sahalarından çıkan başlıca kablo grupları şunlardır: Tek damar kalın NYA ve enerji nakil kabloları (%65-%75 randıman), Çelik zırhlı yeraltı yüksek gerilim kabloları (%45-%55 randıman), Antigron NYM bina tesisat kabloları (%38-%44 randıman) ve TTR esnek çok telli şantiye kabloları (%30-%38 randıman).")
        ]
    },
    {
        "slug": "geri-donusum-nedir-geri-donusumun-faydalari-nelerdir-ve-kisaca-onemi-nedir.html",
        "title": "Endüstriyel Metal Geri Dönüşümü Nedir? Güneydoğu Sanayisine Katkıları",
        "h1": "Endüstriyel Metal Geri Dönüşümü ve Güneydoğu Anadolu Sanayi Ekonomisi",
        "desc": "Mardin, Gaziantep, Diyarbakır ve Şanlıurfa organize sanayi bölgelerinde bakır, alüminyum, demir-çelik ve paslanmaz krom geri dönüşümünün enerji ve hammadde katkısı.",
        "keywords": "metal geri dönüşüm nedir, mardin geri dönüşüm firmaları, güneydoğu anadolu hurda metal, bakır geri dönüşüm enerji tasarrufu, bulgan geri dönüşüm kızıltepe",
        "image": "images/bakir.webp",
        "cat_id": "bakir",
        "date": "2026-11-03",
        "sections": [
            ("Birincil Cevher Madenciliğine Karşı İkincil Metal Kazanımı",
             "Demir, bakır, alüminyum ve krom gibi endüstriyel metallerin yeraltı cevherinden sıfırdan üretilmesi yerine hurda metalden geri dönüştürülmesi; alüminyumda %95, bakırda %85 ve çelik üretiminde %74 oranında elektrik ve ısıl enerji tasarrufu sağlar. Bulgan Hurdacılık olarak Mardin ve Güneydoğu Anadolu'daki şantiye ve fabrikalardan topladığımız metalleri cinsine göre ayrıştırarak Türkiye'nin önde gelen haddehane ve izabe tesislerine doğrudan hammadde olarak sevk ediyoruz."),
            ("Mardin ve Güneydoğu Anadolu OSB'lerinde Atık Metal Yönetimi",
             "Mardin OSB, Kızıltepe Hububat ve Gıda İhtisas tesisleri, Diyarbakır, Şanlıurfa ve Gaziantep organize sanayi bölgelerinde imalat sırasında ortaya çıkan lazer kesim DKP sac fireleri, torna talaşları, yanık motor sargıları ve ömrünü tamamlamış makine parkurları, tesis içinde bekletildiğinde hem iş güvenliği riski oluşturur hem de finansal değer kaybeder. Konteyner bırakma ve periyodik kantar tartımı modelimizle fabrikaların hurda stoklarını anında nakde çeviriyoruz."),
            ("Kayıtlı ve Lisanslı Kantar Tartımının Kurumsal Önemi",
             "Kurumsal şirketler ve kamu kurumları için hurda çıkışı yapılırken resmi kantar fişi, sevk irsaliyesi ve şeffaf banka ödemesi (FAST/EFT) şarttır. Kızıltepe merkez kantarımız tüm resmi tartım ve belgelendirme standartlarını eksiksiz karşılamaktadır.")
        ]
    },
    {
        "slug": "geri-donusum-proje-ornekleri-ve-fikirleri-nelerdir.html",
        "title": "Sanayi ve Şantiyelerde Hurda Ayrıştırma & Geri Dönüşüm Uygulamaları",
        "h1": "Fabrika, Şantiye ve Tarımsal İşletmelerde Kazançlı Hurda Ayrıştırma Rehberi",
        "desc": "Şantiye ve fabrikalarda bakır, sarı pirinç, alüminyum ve demir hurdalarını kaynağında ayrıştırarak %30 daha yüksek kantar geliri elde etmenin teknik yöntemleri.",
        "keywords": "şantiye hurda ayrıştırma, fabrika atık metal yönetimi, mardin şantiye hurdası, kırkambar bakır ayrıştırma, kurumsal geri dönüşüm uygulamaları",
        "image": "images/demir.webp",
        "cat_id": "demir",
        "date": "2026-11-03",
        "sections": [
            ("Kaynağında Metal Ayrıştırma Neden %25-%35 Daha Fazla Kazandırır?",
             "Şantiyelerde ve üretim atölyelerinde yapılan en büyük hata; bakır boru parçalarını, sarı pirinç vanaları, alüminyum profilleri ve demir kırpıntılarını aynı konteynerde karıştırmaktır. Karışık (kırkambar) malzeme her zaman ayrıştırma işçiliği nedeniyle alt kademeden fiyatlandırılır. Oysa bakır, sarı, alüminyum ve kromu ayrı çuval veya kasalarda biriktiren işletmeler, kantar başında her metalin en üst saf birim fiyatından ödeme alır."),
            ("İnşaat ve Kentsel Dönüşüm Şantiyelerinde 3'lü Konteyner Sistemi",
             "Artuklu, Kızıltepe, Midyat, Nusaybin, Diyarbakır ve Adıyaman şantiyelerinde uyguladığımız 3 bölmeli saha toplama planında; 1. alanda inşaat demiri ve H-profiller, 2. kapalı kasada tesisat kablosu ve bakır borular, 3. alanda ise alüminyum doğrama ve PVC pimapen profiller toplanır."),
            ("Tarımsal ve Gıda Tesislerinde Paslanmaz Krom ve Motor Hurdaları",
             "Mardin ve Şanlıurfa'daki un, bulgur, yem ve çırçır fabrikalarında revizyon dönemlerinde çıkan 304/316 kalite paslanmaz krom helezonlar, elek sacları ve yanık elektrik motorları demir hurdasıyla karıştırılmadan ayrı tartılarak işletmeye yüksek ek gelir sağlanır.")
        ]
    },
    {
        "slug": "geri-donusum-sloganlari-nelerdir-geri-donusum-ile-ilgili-sozler.html",
        "title": "Mardin & Güneydoğu Anadolu Hurda Piyasası, Kantar İlkeleri ve Sektör Rehberi",
        "h1": "Bulgan Hurdacılık Saha İlkeleri: Doğru Tartım, Şeffaf Borsa ve Peşin Ticaret",
        "desc": "Mardin Kızıltepe merkezli Bulgan Hurdacılık'ın Güneydoğu Anadolu metal ticaretinde uyguladığı şeffaf kantar, sıfır sürpriz fire ve araç başında nakit ödeme ilkeleri.",
        "keywords": "mardin güvenilir hurdacı, kızıltepe kantar hurdacı, şeffaf hurda tartımı, güneydoğu hurda ticaret ilkeleri, bulgan hurdacılık mardin",
        "image": "images/paslanmaz.webp",
        "cat_id": "paslanmaz",
        "date": "2026-11-03",
        "sections": [
            ("Güneydoğu Anadolu Hurda Ticaretinde Güven ve Kantar Şeffaflığı",
             "Hurda metal sektöründe satıcıların en sık yaşadığı mağduriyet; telefonda yüksek fiyat söylenip sahaya gelindiğinde 'fire var, boya var, kantar farkı var' denilerek fiyatın yarı yarıya düşürülmesidir. Bulgan Hurdacılık olarak Kızıltepe Atatürk Mahallesi'ndeki merkezimizde bu anlayışı tamamen ortadan kaldırdık. Web sitemizde borsa referans fiyatını ve -%20 net kantar alım fiyatımızı açıkça ilan ediyoruz."),
            ("Müşteri Nezaretinde Dijital Tartım ve Anında Ödeme",
             "İster 100 kilogram bakır ister 50 ton fabrika söküm demiri olsun; her tartım işlemi müşterimizin gözü önünde, kalibrasyonlu dijital kantarımızda yapılır. Tartım fişi çıktığı anda ödeme nakit veya FAST ile saniyeler içinde tamamlanır."),
            ("Bölge Ekonomisine ve İstihdama Doğrudan Katkı",
             "Mardin, Diyarbakır, Şanlıurfa, Gaziantep, Batman, Şırnak, Siirt, Adıyaman ve Kilis illerindeki yerel sanayicimizin ve esnafımızın atıl metallerini en yüksek ekonomik değerle yeniden üretim döngüsüne kazandırıyoruz.")
        ]
    },
    {
        "slug": "mardin-kiziltepe-dalgic-pompa-ve-tarimsal-kablo-hurdasi-alimi.html",
        "title": "Mardin & Kızıltepe Dalgıç Pompa, Trafo ve Tarımsal Sulama Hurdası Alımı",
        "h1": "Kızıltepe, Derik ve Nusaybin'de Dalgıç Pompa, Trafo ve Sulama Kablosu Hurdası Alımı",
        "desc": "Mardin Kızıltepe, Derik, Nusaybin ve Şanlıurfa Viranşehir'de yanık dalgıç pompa motoru, kalın kesitli bakır pompa kablosu, pano ve trafo hurdalarının nakit alımı.",
        "keywords": "kızıltepe dalgıç pompa hurdası, mardin trafo hurdası alımı, derik sulama kablosu hurda, yanık dalgıç motor hurda fiyatı, mardin tarımsal hurda alımı",
        "image": "images/kablo.webp",
        "cat_id": "kablo",
        "date": "2026-11-03",
        "sections": [
            ("Derin Kuyu Dalgıç Pompa ve Motor Hurdalarının Değerlemesi",
             "Mezopotamya ovasının kalbi olan Kızıltepe, Derik, Nusaybin ve Viranşehir hattında binlerce tarımsal sulama kuyusu faaliyet göstermektedir. Kuyu yenilemelerinde veya arızalarda açığa çıkan paslanmaz çelik gövdeli dalgıç pompalar, sulu/yağlı sarım yanık dalgıç motorları ve bakır sargılar kantarımızda içerdikleri krom ve bakır miktarına göre en yüksek fiyattan satın alınır."),
            ("Trafo, Kompanzasyon Panosu ve Alüminyum/Bakır Nakil Hatları",
             "Tarımsal işletmeler ve güneş enerjisi (GES) sahalarında kullanım dışı kalan direk tipi trafolar, bakır/alüminyum sargılı güç trafoları, şalt sahası bakır baraları ve çelik zırhlı yeraltı kabloları uzman ekibimizce yerinde sökülerek nakit ödenir.")
        ]
    },
    {
        "slug": "guneydogu-anadolu-osb-fabrika-sokumu-ve-metal-geri-donusum-rehberi.html",
        "title": "Güneydoğu Anadolu OSB Fabrika Sökümü & Çelik Konstrüksiyon Tasfiye Rehberi",
        "h1": "Mardin, Diyarbakır, Şanlıurfa ve Gaziantep OSB Fabrika Sökümü Rehberi",
        "desc": "Güneydoğu Anadolu'daki un, çırçır, tekstil ve gıda fabrikalarının İSG kurallarına uygun çelik konstrüksiyon kesimi, makine sökümü ve hurda karşılığı tasfiyesi.",
        "keywords": "güneydoğu fabrika sökümü, mardin osb hurdacı, diyarbakır fabrika yıkım söküm, şanlıurfa çırçır fabrikası sökümü, gaziantep çelik çatı sökümü",
        "image": "images/sokulecek.png.webp",
        "cat_id": "demir",
        "date": "2026-11-03",
        "sections": [
            ("Endüstriyel Tesis ve Fabrika Sökümünde İSG ve Teknik Planlama",
             "Fabrika, depo, hangar ve üretim tesislerinin sökümü; sıradan bir yıkım işlemi değil, mühendislik ve İş Sağlığı Güvenliği (İSG) disiplini gerektiren teknik bir operasyondur. Bulgan Hurdacılık olarak Mardin, Diyarbakır, Şanlıurfa, Gaziantep ve Batman OSB'lerinde gerçekleştirdiğimiz söküm projelerinde enerji kesimi, çatı sandviç panel indirme, vinçli makine tahliyesi ve oksijen/plazma çelik kesim aşamalarını sigortalı ekibimizle yürütüyoruz."),
            ("Hurda Karşılığı Bina Yıkımı ve Çelik Çatı Sökümü",
             "Tesisinizden çıkacak çelik kolon (HEA, HEB, NPI, NPU), kutu profil, trapez sac, bakır enerji altyapısı ve makine parkurunun toplam kantar değeri hesaplanarak, yıkım/söküm işçiliği düşüldükten sonra kalan net metal bedeli tarafınıza peşin olarak ödenir.")
        ]
    }
]
