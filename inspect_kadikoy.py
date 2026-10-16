import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
c = open(r'C:\AI-Tools\cloned-sites\bulgangeridonusum\kadikoy-hurdaci.html', encoding='utf-8', errors='ignore').read()
scripts = re.findall(r'<script type=["\']application/ld\+json["\']>(.*?)</script>', c, re.DOTALL | re.IGNORECASE)
print(f"Kadıköy JSON-LD count: {len(scripts)}")
for i, s in enumerate(scripts):
    print(f"\n--- Block {i} ---")
    print(s[:500])
