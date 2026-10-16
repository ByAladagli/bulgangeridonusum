import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
c = open(r'C:\AI-Tools\cloned-sites\bulgangeridonusum\index.html', encoding='utf-8', errors='ignore').read()
pos = c.find('İstanbul’da Hangi İlçelerde Hizmet Veriyoruz?')
container_end = c.find('fusion-fullwidth', pos + 50)
section_content = c[pos:container_end]
links = re.findall(r'href=[\'"]([^\'"]+hurdaci\.html)[\'"]', section_content)
print(f'Total district links in grid: {len(links)}')
print(links[:15])

# Also check header menu
menu_pos = c.find('awb-menu__main-ul')
menu_end = c.find('</nav>', menu_pos)
menu_content = c[menu_pos:menu_end]
menu_links = re.findall(r'href=[\'"]([^\'"]+)[\'"][^>]*><span>([^<]+)</span>', menu_content)
print('\nMain menu links:')
for h, l in menu_links[:20]:
    print(f'  {h} -> {l}')
