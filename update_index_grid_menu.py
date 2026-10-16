import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
filepath = r'C:\AI-Tools\cloned-sites\bulgangeridonusum\index.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Replace the district section title
c = c.replace('İstanbul’da Hangi İlçelerde Hizmet Veriyoruz?', 'Mardin’de Hangi İlçelerde Hizmet Veriyoruz?')
c = c.replace("İstanbul'da Hangi İlçelerde Hizmet Veriyoruz?", 'Mardin’de Hangi İlçelerde Hizmet Veriyoruz?')

# Mardin Districts to feature
mardin_districts = [
    ("kiziltepe-hurdaci.html", "Kızıltepe Hurdacı"),
    ("mardin-hurdaci.html", "Mardin Merkez / Artuklu"),
    ("midyat-hurdaci.html", "Midyat Hurdacı"),
    ("nusaybin-hurdaci.html", "Nusaybin Hurdacı"),
    ("derik-hurdaci.html", "Derik Hurdacı"),
    ("mazidagi-hurdaci.html", "Mazıdağı Hurdacı"),
    ("dargecit-hurdaci.html", "Dargeçit Hurdacı"),
    ("savur-hurdaci.html", "Savur Hurdacı"),
    ("yesilli-hurdaci.html", "Yeşilli Hurdacı"),
    ("omerli-hurdaci.html", "Ömerli Hurdacı"),
]

# Find the district grid block
heading_pos = c.find('Mardin’de Hangi İlçelerde Hizmet Veriyoruz?')
if heading_pos != -1:
    grid_start = c.find('<div class="fusion-layout-column fusion_builder_column fusion-builder-column-34', heading_pos)
    grid_end = c.find('<input id="daextam-post-id"', grid_start)
    if grid_start != -1 and grid_end != -1:
        # Build Mardin district columns
        new_cols = []
        for i, (href, name) in enumerate(mardin_districts):
            col_html = f'''<div class="fusion-layout-column fusion_builder_column fusion-builder-column-{34+i} fusion-flex-column" style="--awb-bg-size:cover;--awb-width-large:20%;--awb-margin-top-large:0px;--awb-spacing-right-large:0%;--awb-margin-bottom-large:15px;--awb-spacing-left-large:0%;--awb-width-medium:33.3%;--awb-order-medium:0;--awb-width-small:100%;"><div class="fusion-column-wrapper fusion-column-has-shadow fusion-flex-justify-content-center fusion-content-layout-row"><i class="fb-icon-element-{12+i} fb-icon-element fontawesome-icon fa-map-marker-alt fas circle-no fusion-text-flow" style="--awb-iconcolor:#06a829;--awb-iconcolor-hover:#06a829;--awb-font-size:25px;--awb-margin-right:12.5px;"></i><div class="fusion-text"><p><span style="color: #333333;"><a style="color: #333333; font-weight: 600;" href="{href}">{name}</a></span></p></div></div></div>'''
            new_cols.append(col_html)
        
        c = c[:grid_start] + "".join(new_cols) + c[grid_end:]
        print("Updated District Grid to Mardin districts successfully.")
    else:
        print(f"Could not locate grid boundaries: start={grid_start}, end={grid_end}")
else:
    print("Could not find district heading.")

# Update the top province list:
c = c.replace('Hangi İllerde Hizmet Veriyoruz?</h3>', 'Güneydoğu & Mardin Bölgesi Hizmet Noktalarımız</h3>')
# Replace province links
c = c.replace('<a style="color: #333333;" href="istanbul-hurdaci.html">İstanbul Hurdacı</a>',
              '<a style="color: #333333; font-weight: 600;" href="mardin-hurdaci.html">Mardin Hurdacı</a>')
c = c.replace('<a style="color: #333333;" href="edirne-hurdaci.html">Edirne Hurdacı</a>',
              '<a style="color: #333333; font-weight: 600;" href="kiziltepe-hurdaci.html">Kızıltepe Hurdacı</a>')
c = c.replace('<a style="color: #333333;" href="kirklareli-hurdaci.html">Kırklareli Hurdacı</a>',
              '<a style="color: #333333;" href="midyat-hurdaci.html">Midyat Hurdacı</a>')
c = c.replace('<a style="color: #333333;" href="tekirdag-hurdaci.html">Tekirdağ Hurdacı</a>',
              '<a style="color: #333333;" href="nusaybin-hurdaci.html">Nusaybin Hurdacı</a>')

# Update Header Nav Menu: Add Mardin & Kızıltepe Hurdacı at the very top of the Hurdacı dropdown
old_menu_first_item = '<li id="menu-item-2064" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-2064 awb-menu__li awb-menu__sub-li"><a href="istanbul-hurdaci.html" class="awb-menu__sub-a" tabindex="-1"><span>İstanbul Hurdacı</span></a></li>'
mardin_menu_items = '''<li id="menu-item-mardin" class="menu-item menu-item-type-custom menu-item-object-custom awb-menu__li awb-menu__sub-li" style="background: #e8f5e9;"><a href="mardin-hurdaci.html" class="awb-menu__sub-a" tabindex="-1"><span style="color:#06a829; font-weight:bold;">📍 Mardin Hurdacı</span></a></li>
<li id="menu-item-kiziltepe" class="menu-item menu-item-type-custom menu-item-object-custom awb-menu__li awb-menu__sub-li" style="background: #e8f5e9;"><a href="kiziltepe-hurdaci.html" class="awb-menu__sub-a" tabindex="-1"><span style="color:#06a829; font-weight:bold;">📍 Kızıltepe Hurdacı</span></a></li>
<li id="menu-item-midyat" class="menu-item menu-item-type-custom menu-item-object-custom awb-menu__li awb-menu__sub-li"><a href="midyat-hurdaci.html" class="awb-menu__sub-a" tabindex="-1"><span>Midyat Hurdacı</span></a></li>
<li id="menu-item-nusaybin" class="menu-item menu-item-type-custom menu-item-object-custom awb-menu__li awb-menu__sub-li"><a href="nusaybin-hurdaci.html" class="awb-menu__sub-a" tabindex="-1"><span>Nusaybin Hurdacı</span></a></li>'''

if old_menu_first_item in c:
    c = c.replace(old_menu_first_item, mardin_menu_items + '\n' + old_menu_first_item, 1)
    print("Injected Mardin into Main Header Nav Menu successfully.")
else:
    print("Could not find old_menu_first_item in header.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(c)

print("index.html grid and menu updated successfully.")
