import os
import json
import urllib.request
import re

site_dir = r"C:\AI-Tools\cloned-sites\bulgangeridonusum"
key = "c4b12d8a9e7f41a2b3c4d5e6f7a8b9c0"
key_file = os.path.join(site_dir, f"{key}.txt")

# 1. Create key file
with open(key_file, "w", encoding="utf-8") as f:
    f.write(key)
print(f"Created {key}.txt")

# 2. Extract all URLs from sitemap.xml
sitemap_path = os.path.join(site_dir, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap_content = f.read()

urls = re.findall(r'<loc>(https://[^<]+)</loc>', sitemap_content)
print(f"Found {len(urls)} URLs in sitemap.xml")

# 3. Submit to IndexNow API
payload = {
    "host": "bulgangeridonusum.com.tr",
    "key": key,
    "keyLocation": f"https://bulgangeridonusum.com.tr/{key}.txt",
    "urlList": urls
}

print("Submitting to IndexNow...")
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"}
)

try:
    with urllib.request.urlopen(req) as resp:
        print(f"IndexNow Response: {resp.status} {resp.reason}")
except urllib.error.HTTPError as e:
    print(f"IndexNow HTTP Response: {e.code} {e.reason}")
    print(e.read().decode("utf-8", errors="ignore"))
except Exception as e:
    print("Error submitting to IndexNow:", e)
