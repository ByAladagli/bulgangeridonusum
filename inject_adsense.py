import os
import re

ROOT = r"C:\AI-Tools\cloned-sites\bulgangeridonusum"
PUB_ID = "pub-3325199916968482"
CA_PUB = "ca-pub-3325199916968482"

# 1. Update ads.txt
ads_txt_content = (
    f"# Bulgan Hurdacılık (bulgangeridonusum.com.tr) - Authorized Digital Sellers (ads.txt)\n"
    f"# Google AdSense Publisher: {CA_PUB} ({PUB_ID})\n"
    f"# Account: mehmethilmiozkan@gmail.com\n"
    f"google.com, {PUB_ID}, DIRECT, f08c47fec0942fa0\n"
)
with open(os.path.join(ROOT, "ads.txt"), "w", encoding="utf-8") as f:
    f.write(ads_txt_content)

# 2. Update Cloudflare function
fn_content = f"""export async function onRequestGet(context) {{
  const body = "google.com, {PUB_ID}, DIRECT, f08c47fec0942fa0\\n";
  return new Response(body, {{
    status: 200,
    headers: {{
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600"
    }}
  }});
}}
"""
with open(os.path.join(ROOT, "functions", "ads.txt.js"), "w", encoding="utf-8") as f:
    f.write(fn_content)

# 3. Inject Google AdSense Auto Ads tag into all 65 HTML pages
ads_tag = f"""  <!-- Google AdSense Auto Ads ({CA_PUB}) -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={CA_PUB}" crossorigin="anonymous"></script>"""

htmls = [f for f in os.listdir(ROOT) if f.endswith(".html")]
injected = 0
for fname in htmls:
    p = os.path.join(ROOT, fname)
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    if "pagead2.googlesyndication.com" not in html:
        html = html.replace("</head>", f"{ads_tag}\n</head>")
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        injected += 1

print(f"Successfully configured ads.txt and injected AdSense ({CA_PUB}) into {injected} HTML pages.")
