import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')

BRAIN_DIR = r"C:\Users\mehme\.gemini\antigravity\brain\c9a180af-f2c1-440d-bf0d-2c3b8dfb3e4d"
LOGO_PATH = os.path.join(BRAIN_DIR, ".user_uploaded", "media_1793722873528_09cfb922.png")
OUT_DIR = r"C:\AI-Tools\cloned-sites\bulgangeridonusum\images"
os.makedirs(OUT_DIR, exist_ok=True)

# Map all 20 target images to the 16 generated AI originals (with distinct crops/angles for the 4 derived ones)
SOURCE_MAP = {
    "bakir": ("bakir_1793724442901.jpg", None, "Soyma & Lama Bakır Hurdası"),
    "kablo": ("kablo_1793724462636.jpg", None, "Enerji & TTR Kablo Hurdası"),
    "demir": ("demir_1793724486061.jpg", None, "DKP & Ekstra Demir Hurdası"),
    "aluminyum": ("aluminyum_1793724507883.jpg", None, "Profil & Tel Alüminyum Hurdası"),
    "paslanmaz": ("paslanmaz_1793724443807.jpg", None, "304 / 316 Krom Paslanmaz Hurda"),
    "aku": ("aku_1793724464107.jpg", None, "Sulu & Kuru Akü Hurdası"),
    "cinko": ("cinko_1793724486215.jpg", None, "Çinko Levha & Külçe Hurdası"),
    "kursun": ("kursun_1793724520195.jpg", None, "Levha & Boru Kurşun Hurdası"),
    "bronz.png": ("bronz_png_1793724449425.jpg", None, "Kızıl & Fosfor BronzBurç Hurdası"),
    "elektronik.png": ("elektronik_png_1793724469379.jpg", None, "Anakart & Pano Elektronik Hurda"),
    "klima.png": ("klima_png_1793724491172.jpg", None, "Split & Salon Tipi Klima Hurdası"),
    "chiller.png": ("chiller_png_1793724515057.jpg", None, "Endüstriyel Chiller Soğutma Grubu"),
    "plastik": ("plastik_1793724456173.jpg", None, "Polietilen & ПП Plastik Hurdası"),
    "kagit": ("kagit_1793724475372.jpg", None, "1. Hamur & Arşiv Kağıt Hurdası"),
    "karton": ("karton_1793724508220.jpg", None, "Oluklu Mukavva & Koli Karton"),
    "sokulecek.png": ("sokulecek_png_1793724543109.jpg", None, "Fabrika & Çelik Konstrüksiyon Sökümü"),
    # 4 derived with distinct framing so each has unique composition
    "sari-hurda-1": ("bronz_png_1793724449425.jpg", (0.08, 0.08, 0.94, 0.92), "MS-58 Çubuk & Musluk Sarı Pirinç"),
    "nikel-hurda": ("paslanmaz_1793724443807.jpg", (0.10, 0.05, 0.92, 0.90), "Saf Nikel Anot & Şablon Hurdası"),
    "hurda-raf-1": ("demir_1793724486061.jpg", (0.06, 0.10, 0.94, 0.92), "Ağır Yük & Market Depo Raf Hurdası"),
    "endustriyel-mutfak": ("paslanmaz_1793724443807.jpg", (0.04, 0.12, 0.88, 0.94), "Endüstriyel Paslanmaz Mutfak Ekipmanı"),
}

def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\bahnschrift.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def process_images():
    logo_orig = Image.open(LOGO_PATH).convert("RGBA")
    
    # Also save clean brand logo assets
    logo_w, logo_h = logo_orig.size
    logo_web = logo_orig.resize((440, int(440 * logo_h / logo_w)), Image.Resampling.LANCZOS)
    logo_web.save(os.path.join(OUT_DIR, "bulgan-logo.webp"), "WEBP", quality=92)
    logo_web.convert("RGB").save(os.path.join(OUT_DIR, "bulgan-logo.png"), "PNG", optimize=True)

    font_label = load_font(18, bold=True)
    font_domain = load_font(16, bold=True)
    font_sub = load_font(13, bold=False)

    TARGET_W, TARGET_H = 960, 640

    for slug, (src_file, crop_box, label_tr) in SOURCE_MAP.items():
        src_path = os.path.join(BRAIN_DIR, src_file)
        img = Image.open(src_path).convert("RGB")
        w, h = img.size

        if crop_box:
            cx1, cy1, cx2, cy2 = int(w * crop_box[0]), int(h * crop_box[1]), int(w * crop_box[2]), int(h * crop_box[3])
            img = img.crop((cx1, cy1, cx2, cy2))
            if slug == "sari-hurda-1":
                img = ImageEnhance.Color(img).enhance(1.18)
                img = ImageEnhance.Brightness(img).enhance(1.06)
            elif slug == "nikel-hurda":
                img = ImageEnhance.Color(img).enhance(0.85)
                img = ImageEnhance.Contrast(img).enhance(1.12)

        # Center crop to 3:2 (960x640)
        iw, ih = img.size
        target_ratio = TARGET_W / TARGET_H
        cur_ratio = iw / ih
        if cur_ratio > target_ratio:
            new_w = int(ih * target_ratio)
            left = (iw - new_w) // 2
            img = img.crop((left, 0, left + new_w, ih))
        else:
            new_h = int(iw / target_ratio)
            top = (ih - new_h) // 2
            img = img.crop((0, top, iw, top + new_h))

        img = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        canvas = img.convert("RGBA")

        # Subtle bottom gradient vignette for natural photographic legibility (no boxy neon overlays!)
        overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        bar_h = 68
        for y in range(TARGET_H - 120, TARGET_H):
            progress = (y - (TARGET_H - 120)) / 120.0
            alpha = int(225 * (progress ** 1.35))
            draw.line([(0, y), (TARGET_W, y)], fill=(12, 16, 22, alpha))

        # Thin gold metallic rule line at the very bottom (3px) matching the BULGAN HURDACILIK gold plate
        draw.rectangle([0, TARGET_H - 3, TARGET_W, TARGET_H], fill=(212, 165, 42, 240))

        # Place Bulgan Hurdacılık logo cleanly on bottom-left
        lh = 44
        lw = int(lh * (logo_w / logo_h))
        logo_small = logo_orig.resize((lw, lh), Image.Resampling.LANCZOS)
        overlay.paste(logo_small, (20, TARGET_H - bar_h + 10), logo_small)

        # Vertical subtle divider next to logo
        div_x = 20 + lw + 16
        draw.line([(div_x, TARGET_H - bar_h + 14), (div_x, TARGET_H - 16)], fill=(255, 255, 255, 55), width=1)

        # Material label & location on left of divider
        draw.text((div_x + 16, TARGET_H - bar_h + 13), label_tr, font=font_label, fill=(248, 250, 252, 250))
        draw.text((div_x + 16, TARGET_H - bar_h + 35), "Mardin & Güneydoğu Anadolu Saha Alımı", font=font_sub, fill=(185, 195, 208, 220))

        # Right side: Domain & Direct Kantar Phone
        domain_txt = "bulgangeridonusum.com.tr"
        phone_txt = "0545 904 38 34"
        dbbox = draw.textbbox((0, 0), domain_txt, font=font_domain)
        pbbox = draw.textbbox((0, 0), phone_txt, font=font_sub)
        dw = dbbox[2] - dbbox[0]
        pw = pbbox[2] - pbbox[0]

        draw.text((TARGET_W - dw - 22, TARGET_H - bar_h + 13), domain_txt, font=font_domain, fill=(234, 188, 62, 255))
        draw.text((TARGET_W - pw - 22, TARGET_H - bar_h + 35), phone_txt, font=font_sub, fill=(226, 232, 240, 235))

        final_rgb = Image.alpha_composite(canvas, overlay).convert("RGB")
        webp_path = os.path.join(OUT_DIR, f"{slug}.webp")
        jpg_path = os.path.join(OUT_DIR, f"{slug}.jpg")
        final_rgb.save(webp_path, "WEBP", quality=88, method=6)
        final_rgb.save(jpg_path, "JPEG", quality=88, optimize=True)
        print(f"Stamped: {slug}.webp ({os.path.getsize(webp_path)//1024} KB)")

if __name__ == "__main__":
    process_images()


def generate_og_and_favicons():
    logo_orig = Image.open(LOGO_PATH).convert("RGBA")
    bg_src = Image.open(os.path.join(BRAIN_DIR, "bakir_1793724442901.jpg")).convert("RGB")
    W, H = 1200, 630
    bg = bg_src.resize((W, int(W * bg_src.size[1] / bg_src.size[0])), Image.Resampling.LANCZOS)
    bg = bg.crop((0, 0, W, H)).convert("RGBA")

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(W):
        alpha = int(245 - (x / W) * 65)
        draw.line([(x, 0), (x, H)], fill=(13, 17, 23, alpha))

    draw.rectangle([0, H - 6, W, H], fill=(212, 165, 42, 255))
    draw.rectangle([0, 0, 8, H], fill=(34, 168, 76, 255))

    lw = 420
    lh = int(lw * logo_orig.size[1] / logo_orig.size[0])
    logo_resized = logo_orig.resize((lw, lh), Image.Resampling.LANCZOS)
    overlay.paste(logo_resized, (60, 56), logo_resized)

    f_h1 = load_font(44, bold=True)
    f_h2 = load_font(26, bold=False)
    f_badge = load_font(22, bold=True)

    draw.text((64, 235), "MARDİN & GÜNEYDOĞU ANADOLU", font=f_badge, fill=(234, 188, 62, 255))
    draw.text((64, 275), "Lisanslı Metal Geri Dönüşüm &\nAdresten Nakit Hurda Alım Merkezi", font=f_h1, fill=(248, 250, 252, 255))
    draw.text((64, 415), "Bakır • Kablo • Demir • Alüminyum • Sarı Pirinç • Krom • Fabrika Sökümü", font=f_h2, fill=(195, 205, 218, 240))

    draw.rounded_rectangle([64, 485, 540, 555], radius=8, fill=(24, 138, 62, 255))
    draw.text((90, 507), "Kantar & WhatsApp: 0545 904 38 34", font=f_badge, fill=(255, 255, 255, 255))
    draw.text((575, 507), "bulgangeridonusum.com.tr", font=f_badge, fill=(234, 188, 62, 255))

    og_final = Image.alpha_composite(bg, overlay).convert("RGB")
    og_final.save(os.path.join(OUT_DIR, "og-cover.webp"), "WEBP", quality=90)
    og_final.save(os.path.join(OUT_DIR, "og-cover.jpg"), "JPEG", quality=90, optimize=True)
    print("Generated og-cover.webp & og-cover.jpg")

if __name__ == "__main__":
    generate_og_and_favicons()
