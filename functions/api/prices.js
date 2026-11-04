// Cloudflare Pages Function: GET /api/prices
// Ücretsiz Günlük Borsa & Hurda Fiyat Kazıyıcı (%20 Azaltma / x0.80 Otomatik Uygulamalı)

const DISCOUNT_FACTOR = 0.80;

const BASE_CATALOG = [
  {
    id: "bakir",
    name: "Bakır Hurda Fiyatları",
    shortName: "Hurda Bakır",
    slug: "bakir-hurda-fiyatlari.html",
    items: [
      { code: "bakir_soyma", name: "Soyma Bakır Hurdası (%99.9 Saf)", matchKey: "antigron kırma bakır", marketPrice: 686.73, unit: "KG" },
      { code: "bakir_antigron", name: "Antigron Kırma Bakır Hurdası", matchKey: "antigron kırma bakır", marketPrice: 680.50, unit: "KG" },
      { code: "bakir_katot", name: "Bakır Katot & Lama Bakır", matchKey: "bakır katot", marketPrice: 657.57, unit: "KG" },
      { code: "bakir_kazan", name: "Bakır Kazan & Boru Hurdası", matchKey: "bakır kazan", marketPrice: 620.27, unit: "KG" },
      { code: "bakir_filmasin", name: "Bakır Filmaşin (F8) Parlak", matchKey: "bakır filmaşin", marketPrice: 600.32, unit: "KG" },
      { code: "bakir_talas", name: "Temiz Bakır Talaşı Hurdası", matchKey: "bakır talaşı", marketPrice: 582.01, unit: "KG" },
      { code: "bakir_petek", name: "Bakır Petek (Radyatör) Hurdası", matchKey: "bakır petek", marketPrice: 580.55, unit: "KG" },
      { code: "bakir_tel", name: "Yanık & Bobin Bakır Tel Hurdası", matchKey: "bakır tel", marketPrice: 550.85, unit: "KG" },
      { code: "bakir_kirkambar", name: "Kırkambar Bakır Hurdası (Karışık)", matchKey: "kırkambar", marketPrice: 515.40, unit: "KG" }
    ]
  },
  {
    id: "kablo",
    name: "Kablo Hurda Fiyatları",
    shortName: "Hurda Kablo",
    slug: "kablo-hurda-fiyatlari.html",
    items: [
      { code: "kablo_dalgic", name: "Dalgıç Pompa & Tek Damar Kalın Kablo", matchKey: "dalgıç pompa kablosu", marketPrice: 540.13, unit: "KG" },
      { code: "kablo_fareyemez", name: "Fare Yemez & Enerji Kablosu", matchKey: "fare yemez kablo", marketPrice: 450.52, unit: "KG" },
      { code: "kablo_yuzde50", name: "%50 Bakırlı Sanayi Kablosu", matchKey: "%50 bakırlı kablo", marketPrice: 400.71, unit: "KG" },
      { code: "kablo_celikzirh", name: "Çelik Zırhlı & Yeraltı Enerji Kablosu", matchKey: "çelik zırh", marketPrice: 380.88, unit: "KG" },
      { code: "kablo_yuzde40", name: "%40 Bakırlı Tesisat Kablosu", matchKey: "%40 bakırlı kablo", marketPrice: 320.46, unit: "KG" },
      { code: "kablo_antigron", name: "Antigron & NYM Tesisat Kablosu", matchKey: "antigron hurda kablo", marketPrice: 295.51, unit: "KG" },
      { code: "kablo_karisik", name: "Karışık & TTR Hurda Kablo", matchKey: "karışık kablo", marketPrice: 290.51, unit: "KG" },
      { code: "kablo_yuzde30", name: "%30 Bakırlı Data / Zayıf Akım Kablosu", matchKey: "%30 bakırlı kablo", marketPrice: 245.40, unit: "KG" }
    ]
  },
  {
    id: "demir",
    name: "Demir Hurda Fiyatları",
    shortName: "Hurda Demir",
    slug: "demir-hurda-fiyatlari.html",
    items: [
      { code: "demir_ekstra", name: "Ekstra Ağır Demir & Profil Hurdası", matchKey: "extra hurda", marketPrice: 15.77, unit: "KG" },
      { code: "demir_insaat", name: "İnşaat Demir Çubuğu & Filmaşin", matchKey: "inşaat demir çubuğu", marketPrice: 15.47, unit: "KG" },
      { code: "demir_santiye", name: "Şantiye Kırpıntı & H-Demir Hurdası", matchKey: "şantiye kırpıntı", marketPrice: 15.27, unit: "KG" },
      { code: "demir_imalat", name: "İmalat Artığı Lazer Kesim Sac", matchKey: "imalat hurda", marketPrice: 15.15, unit: "KG" },
      { code: "demir_dkp", name: "DKP Sac & Kalın Demir Hurdası", matchKey: "dkp hurda", marketPrice: 15.10, unit: "KG" },
      { code: "demir_yikim", name: "Bina & Tesis Yıkım Çıkması Demir", matchKey: "inşaat yıkım", marketPrice: 12.99, unit: "KG" },
      { code: "demir_talas", name: "Demir & Çelik Torna Talaşı", matchKey: "demir talaşı", marketPrice: 12.77, unit: "KG" },
      { code: "demir_toplama", name: "Karışık Toplama & Pik Demir Hurdası", matchKey: "karışık ve toplama", marketPrice: 11.40, unit: "KG" }
    ]
  },
  {
    id: "aluminyum",
    name: "Alüminyum Hurda Fiyatları",
    shortName: "Hurda Alüminyum",
    slug: "aluminyum-hurda-fiyatlari.html",
    items: [
      { code: "alu_bakirli_radyator", name: "Bakırlı Alüminyum Klima Radyatörü", matchKey: "bakırlı alüminyum radyatör", marketPrice: 355.46, unit: "KG" },
      { code: "alu_tel", name: "Alüminyum Elektrik Teli (Saf)", matchKey: "tel alüminyum", marketPrice: 178.50, unit: "KG" },
      { code: "alu_jant", name: "Oto Jant & Araiş Levha Alüminyum", matchKey: "jant alüminyum", marketPrice: 167.10, unit: "KG" },
      { code: "alu_profil", name: "Boyasız Alüminyum Doğrama Profil", matchKey: "profil alüminyum", marketPrice: 156.40, unit: "KG" },
      { code: "alu_boyali", name: "Boyalı Levha & Çatı Alüminyumu", matchKey: "boyalı levha alüminyum", marketPrice: 145.99, unit: "KG" },
      { code: "alu_folyo", name: "Folyo & Sert Alüminyum Piston", matchKey: "folyo alüminyum", marketPrice: 115.40, unit: "KG" },
      { code: "alu_kutu", name: "Preslenmiş Kutu & Talaş Alüminyum", matchKey: "kutu alüminyum", marketPrice: 92.72, unit: "KG" }
    ]
  },
  {
    id: "sari",
    name: "Sarı Pirinç Hurda Fiyatları",
    shortName: "Sarı Pirinç",
    slug: "sari-hurda-fiyatlari.html",
    items: [
      { code: "sari_arais64", name: "Araiş Sarı Hurdası (MS-64 / MS-70)", matchKey: "araiş sarı hurdası ms-64", marketPrice: 358.13, unit: "KG" },
      { code: "sari_fermuar", name: "Fermuar Talaşı & Pirinç İmalat Artığı", matchKey: "fermuar talaşı", marketPrice: 313.36, unit: "KG" },
      { code: "sari_cubuk58", name: "Çubuk Parça Sarı (MS-58)", matchKey: "çubuk parça ms-58", marketPrice: 309.76, unit: "KG" },
      { code: "sari_kirkambar", name: "Sarı Kırkambar (Vana, Musluk, Su Saati)", matchKey: "sarı kırkambar", marketPrice: 288.38, unit: "KG" },
      { code: "sari_talas58", name: "MS-58 Sarı Çubuk Talaşı", matchKey: "çubuk talaşı ms-58", marketPrice: 252.01, unit: "KG" },
      { code: "sari_radyator", name: "Sarı Oto Radyatör Hurdası", matchKey: "sarı oto radyatör", marketPrice: 196.25, unit: "KG" }
    ]
  },
  {
    id: "paslanmaz",
    name: "Paslanmaz Krom Hurda Fiyatları",
    shortName: "Paslanmaz Krom",
    slug: "paslanmaz-hurda-fiyatlari.html",
    items: [
      { code: "krom_310", name: "310 Kalite Ateşe Dayanıklı Paslanmaz Krom", matchKey: "310 kalite paslanmaz", marketPrice: 120.50, unit: "KG" },
      { code: "krom_316", name: "316 Kalite Asitlik Paslanmaz Krom", matchKey: "316 kalite paslanmaz", marketPrice: 112.64, unit: "KG" },
      { code: "krom_316_talas", name: "316 Kalite Paslanmaz Krom Talaşı", matchKey: "316 paslanmaz talaşı", marketPrice: 86.68, unit: "KG" },
      { code: "krom_304", name: "304 Kalite Paslanmaz Krom Sac & Boru", matchKey: "304 kalite paslanmaz", marketPrice: 58.53, unit: "KG" },
      { code: "krom_304_talas", name: "304 Kalite Paslanmaz Krom Talaşı", matchKey: "304 paslanmaz talaşı", marketPrice: 44.02, unit: "KG" },
      { code: "krom_201_430", name: "201 / 430 Kalite Mıknatıslı Krom", matchKey: "201 kalite paslanmaz", marketPrice: 30.56, unit: "KG" }
    ]
  },
  {
    id: "aku",
    name: "Akü Hurda Fiyatları",
    shortName: "Hurda Akü",
    slug: "aku-hurda-fiyatlari.html",
    items: [
      { code: "aku_kuru", name: "Kuru & Bakımsız UPS Akü Hurdası", matchKey: "kuru akü", marketPrice: 35.88, unit: "KG" },
      { code: "aku_karisik", name: "Araç & Traktör Sulu Akü Hurdası", matchKey: "karışık akü", marketPrice: 35.77, unit: "KG" },
      { code: "aku_jel", name: "Jel & Güneş Enerjisi (GES) Aküsü", matchKey: "jel akü", marketPrice: 35.11, unit: "KG" },
      { code: "aku_kucuk", name: "Küçük Tip Santral Akü Hurdası", matchKey: "küçük akü", marketPrice: 30.46, unit: "KG" }
    ]
  },
  {
    id: "cinko",
    name: "Çinko Hurda Fiyatları",
    shortName: "Hurda Çinko",
    slug: "cinko-hurda-fiyatlari.html",
    items: [
      { code: "cinko_cati", name: "Çinko Çatı & Oluk Söküm Hurdası", matchKey: "çinko hurda çatı", marketPrice: 105.15, unit: "KG" },
      { code: "cinko_levha", name: "Temiz Çinko Levha & Zamak", matchKey: "çinko levha", marketPrice: 83.48, unit: "KG" },
      { code: "cinko_kulce", name: "Külçe Çinko Hurdası", matchKey: "külçe çinko", marketPrice: 79.13, unit: "KG" }
    ]
  },
  {
    id: "kursun",
    name: "Kurşun Hurda Fiyatları",
    shortName: "Hurda Kurşun",
    slug: "kursun-hurda-fiyatlari.html",
    items: [
      { code: "kursun_kirkambar", name: "Soyma & Kırkambar Yumuşak Kurşun", matchKey: "kurşun kırkambar", marketPrice: 98.19, unit: "KG" },
      { code: "kursun_boru", name: "Hurda Kurşun Boru & Kablo Zırhı", matchKey: "kurşun boru", marketPrice: 87.89, unit: "KG" },
      { code: "kursun_cati", name: "Çatı & Minare Söküm Levha Kurşun", matchKey: "kurşun çatı", marketPrice: 82.48, unit: "KG" }
    ]
  },
  {
    id: "nikel",
    name: "Nikel Hurda Fiyatları",
    shortName: "Hurda Nikel",
    slug: "nikel-hurda-fiyatlari.html",
    items: [
      { code: "nikel_anot", name: "Nikel %99.9 Anot & Şablon Hurdası", matchKey: "nikel 99,99% anot", marketPrice: 516.03, unit: "KG" },
      { code: "nikel_capak", name: "Nikel Çapağı & İmalat Artığı", matchKey: "nikel çapağı", marketPrice: 355.51, unit: "KG" },
      { code: "nikel_turbo", name: "Turbo Nikel & Alaşımlı Nikel", matchKey: "turbo nikel", marketPrice: 270.39, unit: "KG" }
    ]
  },
  {
    id: "bronz",
    name: "Bronz & Kızıl Hurda Fiyatları",
    shortName: "Bronz & Kızıl",
    slug: "bronz-hurda-fiyatlari.html",
    items: [
      { code: "bronz_fosfor", name: "Fosfor Bronz (Kalaylı) Levha & Parça", matchKey: "fosfor bronz", marketPrice: 582.06, unit: "KG" },
      { code: "bronz_parca", name: "Bronz Dişli, Burç & Yatak Parça", matchKey: "bronz parça", marketPrice: 497.80, unit: "KG" },
      { code: "bronz_talas", name: "Bronz Torna Talaşı", matchKey: "bronz talaşı", marketPrice: 467.54, unit: "KG" },
      { code: "bronz_rg5", name: "Kızıl Parça (RG5 / RG7 Vana & Burç)", matchKey: "kızıl parça", marketPrice: 330.26, unit: "KG" }
    ]
  },
  {
    id: "elektronik",
    name: "Elektronik Kart Hurda Fiyatları",
    shortName: "Elektronik Hurda",
    slug: "elektronik-hurda-fiyatlari.html",
    items: [
      { code: "elek_ram", name: "RAM, İşlemci & Telekom Santral Kartları", matchKey: "rami işlemci", marketPrice: 130.48, unit: "KG" },
      { code: "elek_server", name: "Server (Sunucu) & Laptop Anakartları", matchKey: "server laptop", marketPrice: 130.26, unit: "KG" },
      { code: "elek_hdd", name: "Harddisk & Yeni Nesil Anakart Hurdası", matchKey: "harddisk", marketPrice: 123.18, unit: "KG" },
      { code: "elek_modem", name: "Uydu, Modem & Güç Kaynağı Kartları", matchKey: "uydu modem", marketPrice: 105.90, unit: "KG" }
    ]
  },
  {
    id: "klima",
    name: "Klima & Chiller Hurda Fiyatları",
    shortName: "Klima & Chiller",
    slug: "klima-hurda-fiyatlari.html",
    items: [
      { code: "klima_bakir_petek", name: "Klima & Chiller Bakır/Alüminyum Radyatör", matchKey: "bakırlı alüminyum radyatör", marketPrice: 355.46, unit: "KG" },
      { code: "klima_komple", name: "Hurda Split & Salon Tipi Klima (Komple)", matchKey: "hurda klima fiyatları", marketPrice: 50.33, unit: "KG" },
      { code: "klima_motor", name: "Klima & Chiller Kompresör Motoru", matchKey: "motor hurdası", marketPrice: 46.86, unit: "KG" }
    ]
  },
  {
    id: "plastik",
    name: "Plastik & PVC Hurda Fiyatları",
    shortName: "Hurda Plastik",
    slug: "plastik-hurda-fiyatlari.html",
    items: [
      { code: "plastik_naylon", name: "Beyaz Şeffaf Naylon & Sera Örtüsü", matchKey: "beyaz şeffaf naylon", marketPrice: 19.36, unit: "KG" },
      { code: "plastik_moblen", name: "Polipropilen (Moblen) Kasa & Çuval", matchKey: "polipropilen moblen", marketPrice: 16.02, unit: "KG" },
      { code: "plastik_kristal", name: "Polistiren Kristal & Temiz PET", matchKey: "polistiren kristal", marketPrice: 14.83, unit: "KG" },
      { code: "plastik_abs", name: "ABS Sanayi Plastiği & Pimapen Profil", matchKey: "abs hurda plastik", marketPrice: 13.78, unit: "KG" }
    ]
  },
  {
    id: "kagit",
    name: "Kağıt & Karton Hurda Fiyatları",
    shortName: "Kağıt & Karton",
    slug: "kagit-hurda-fiyatlari.html",
    items: [
      { code: "kagit_gazete", name: "Matbaa Artığı Baskısız / Temiz Kağıt", matchKey: "kullanılmamış gazete", marketPrice: 7.20, unit: "KG" },
      { code: "kagit_beyaz", name: "1. Hamur Beyaz Kağıt & Okul Kitabı", matchKey: "beyaz kağıt", marketPrice: 6.00, unit: "KG" },
      { code: "kagit_a4", name: "Kurumsal Arşiv & A4 Evrak Hurdası", matchKey: "a4 fotokopi", marketPrice: 4.50, unit: "KG" },
      { code: "kagit_karton", name: "Oluklu Mukavva & Koli Karton Hurdası", matchKey: "hurda karton", marketPrice: 4.30, unit: "KG" }
    ]
  }
];

export async function onRequestGet(context) {
  let usdTry = 49.99;
  let eurTry = 54.10;
  const scrapedMap = {};

  try {
    const fxRes = await fetch("https://open.er-api.com/v6/latest/USD", {
      cf: { cacheTtl: 14400, cacheEverything: true }
    });
    if (fxRes.ok) {
      const fxData = await fxRes.json();
      if (fxData?.rates?.TRY) {
        usdTry = Number(fxData.rates.TRY.toFixed(2));
        const eurRate = fxData.rates.EUR || 0.92;
        eurTry = Number((usdTry / eurRate).toFixed(2));
      }
    }
  } catch (_) {}

  try {
    const srcRes = await fetch("https://www.hurdaadresi.com/hurda-fiyatlari/", {
      headers: { "User-Agent": "Mozilla/5.0 (compatible; BulganPriceBot/2.0)" },
      cf: { cacheTtl: 14400, cacheEverything: true }
    });
    if (srcRes.ok) {
      const html = await srcRes.text();
      const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
      let match;
      while ((match = rowRegex.exec(html)) !== null) {
        const tdRegex = /<td[^>]*>([\s\S]*?)<\/td>/gi;
        const cells = [];
        let tdMatch;
        while ((tdMatch = tdRegex.exec(match[1])) !== null) {
          cells.push(tdMatch[1].replace(/<[^>]+>/g, "").trim());
        }
        if (cells.length >= 2) {
          const priceMatch = cells[1].match(/(\d+[\.,]\d+)/);
          if (priceMatch) {
            const val = parseFloat(priceMatch[1].replace(",", "."));
            if (val > 0) {
              scrapedMap[cells[0].toLowerCase()] = val;
            }
          }
        }
      }
    }
  } catch (_) {}

  const nowTr = new Date(Date.now() + 3 * 3600 * 1000);
  const dd = String(nowTr.getUTCDate()).padStart(2, "0");
  const mm = String(nowTr.getUTCMonth() + 1).padStart(2, "0");
  const yyyy = nowTr.getUTCFullYear();
  const hh = String(nowTr.getUTCHours()).padStart(2, "0");
  const min = String(nowTr.getUTCMinutes()).padStart(2, "0");

  const categories = BASE_CATALOG.map((cat) => ({
    ...cat,
    items: cat.items.map((item) => {
      let rawMarket = item.marketPrice;
      for (const [k, v] of Object.entries(scrapedMap)) {
        if (k.includes(item.matchKey)) {
          rawMarket = v;
          break;
        }
      }
      // Sanity guard: Demir should never exceed 40 TL/KG
      if (cat.id === "demir" && rawMarket > 40) {
        rawMarket = item.marketPrice;
      }
      const discounted = Number((rawMarket * DISCOUNT_FACTOR).toFixed(2));
      return {
        code: item.code,
        name: item.name,
        price: discounted,
        unit: item.unit,
        tonPrice: Number((discounted * 1000).toFixed(2))
      };
    })
  }));

  const body = JSON.stringify({
    updatedAt: `${dd}.${mm}.${yyyy} ${hh}:${min}`,
    dateIso: `${yyyy}-${mm}-${dd}`,
            exchange: { USD_TRY: usdTry, EUR_TRY: eurTry },
    categories
  });

  return new Response(body, {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=1800, s-maxage=7200, stale-while-revalidate=86400",
      "Access-Control-Allow-Origin": "*"
    }
  });
}
