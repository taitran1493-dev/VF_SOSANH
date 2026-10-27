import urllib.request
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = [
    'https://vinfastauto.com/vn_vi/dat-coc-xe-dien-vf3',
    'https://shop.vinfastauto.com/vn_vi/dat-coc-o-to-dien-vinfast.html?modelId=Products-Car-VF7',
    'https://shop.vinfastauto.com/vn_vi/dat-coc-o-to-dien-vinfast.html?modelId=Products-Car-VF8',
    'https://shop.vinfastauto.com/vn_vi/dat-coc-o-to-dien-vinfast.html?modelId=Products-Car-VF9'
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'https://[^\s"\'<>]+\.(?:png|webp|jpg)', html)
        print(f"=== {url} ===")
        found = set()
        for m in matches:
            m_low = m.lower()
            if any(k in m_low for k in ['vf', 'car', 'product', 'exterior', '360', 'color']):
                found.add(m)
        for f in list(found)[:10]:
            print("  ", f)
    except Exception as e:
        print(f"Error {url}:", e)
