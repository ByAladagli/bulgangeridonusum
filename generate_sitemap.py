import os
import glob
from datetime import datetime

base_dir = r'C:\AI-Tools\cloned-sites\bulgangeridonusum'
domain = "https://bulgangeridonusum.com.tr"

html_files = [os.path.basename(f) for f in glob.glob(os.path.join(base_dir, '*.html'))]

# Priority order
priority_map = {
    "index.html": ("1.0", "daily"),
    "mardin-hurdaci.html": ("0.95", "daily"),
    "kiziltepe-hurdaci.html": ("0.95", "daily"),
    "midyat-hurdaci.html": ("0.90", "daily"),
    "nusaybin-hurdaci.html": ("0.90", "daily"),
    "hurda-fiyatlari.html": ("0.90", "daily"),
    "bakir-hurda-fiyatlari.html": ("0.85", "weekly"),
    "demir-hurda-fiyatlari.html": ("0.85", "weekly"),
    "aluminyum-hurda-fiyatlari.html": ("0.85", "weekly"),
    "kablo-hurda-fiyatlari.html": ("0.85", "weekly"),
    "iletisim.html": ("0.80", "monthly"),
}

today = datetime.now().strftime('%Y-%m-%d')

urls = []
for f in html_files:
    if f in priority_map:
        prio, freq = priority_map[f]
    else:
        prio, freq = "0.7", "monthly"
    
    url = f"{domain}/{f}" if f != "index.html" else f"{domain}/"
    urls.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""

sitemap_path = os.path.join(base_dir, 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap_content)
print(f"Generated sitemap.xml with {len(urls)} URLs at {sitemap_path}")

robots_content = f"""User-agent: *
Allow: /
Disallow: /admin.html

Sitemap: {domain}/sitemap.xml
"""

robots_path = os.path.join(base_dir, 'robots.txt')
with open(robots_path, 'w', encoding='utf-8') as f:
    f.write(robots_content)
print(f"Generated robots.txt at {robots_path}")
