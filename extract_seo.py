import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI-Tools\cloned-sites\bulgangeridonusum\index.html'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

pattern = re.compile(r'<script type=["\']application/ld\+json["\']>(.*?)</script>', re.DOTALL | re.IGNORECASE)
matches = pattern.findall(c)
print(f"Total JSON-LD scripts found: {len(matches)}")
for i, m in enumerate(matches):
    print(f"\n--- BLOCK {i} (len: {len(m)}) ---")
    print(m.strip()[:600])
