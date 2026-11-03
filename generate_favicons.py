import os
import sys
from PIL import Image, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

BRAIN_DIR = r"C:\Users\mehme\.gemini\antigravity\brain\c9a180af-f2c1-440d-bf0d-2c3b8dfb3e4d"
FAVICON_SRC = os.path.join(BRAIN_DIR, ".user_uploaded", "media_1793726831429_c6205da1.jpg")
ROOT = r"C:\AI-Tools\cloned-sites\bulgangeridonusum"
IMG_DIR = os.path.join(ROOT, "images")
os.makedirs(IMG_DIR, exist_ok=True)

def build_favicons_from_uploaded():
    src = Image.open(FAVICON_SRC).convert("RGBA")
    w, h = src.size
    # Ensure exact 1:1 square
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    sq = src.crop((left, top, left + side, top + side))

    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-48x48.png": 48,
        "favicon.png": 64,
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
        "icon-512.png": 512,
    }
    for fname, sz in sizes.items():
        resized = sq.resize((sz, sz), Image.Resampling.LANCZOS)
        if sz <= 48:
            resized = ImageEnhance.Sharpness(resized).enhance(1.25)
        resized.save(os.path.join(IMG_DIR, fname), "PNG", optimize=True)
        resized.save(os.path.join(ROOT, fname), "PNG", optimize=True)

    # Also save WebP version for fast modern use
    sq.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(IMG_DIR, "favicon.webp"), "WEBP", quality=92)

    # Multi-size favicon.ico at both root and images/
    ico_imgs = [sq.resize((s, s), Image.Resampling.LANCZOS) for s in (16, 32, 48, 64)]
    for target_ico in (os.path.join(ROOT, "favicon.ico"), os.path.join(IMG_DIR, "favicon.ico")):
        ico_imgs[1].save(
            target_ico,
            format="ICO",
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
            append_images=[ico_imgs[0], ico_imgs[2], ico_imgs[3]]
        )
    print(f"Favicon suite generated from uploaded {w}x{h} icon across all sizes.")

if __name__ == "__main__":
    build_favicons_from_uploaded()
