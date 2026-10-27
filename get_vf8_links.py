import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = 'https://shop.vinfastauto.com/vn_vi/dat-coc-o-to-dien-vinfast.html?modelId=Products-Car-VF8'
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')

matches = set(re.findall(r'https://shop\.vinfastauto\.com/on/demandware\.static/[^\s"\'<>]+\.(?:png|webp|jpg)', html))
print(f"Total CDN links found: {len(matches)}")
for m in sorted(matches):
    if 'vf8' in m.lower():
        print('VF8:', m)
