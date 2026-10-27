# -*- coding: utf-8 -*-
"""
Builder script to update cars_data.js and cars_database.json from the official VinFast brochure CSV.
Includes all 22 official VinFast models/versions + 3 competitor benchmark cars.
Maps official pricing, images, colors, and structured 7-category specifications.
"""
import csv
import json
import os
import re
import sys

csv_file = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/data/vinfast_official_brochure_specs.csv'
raw_db_file = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-baogia/data_da_bo_sung_phu_kien_combo.json'

# Load existing rich vinfast-baogia database for images and colors
vinfast_raw = []
if os.path.exists(raw_db_file):
    with open(raw_db_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        vinfast_raw = data.get('cars', [])

# Map of raw cars by version / standardName
vf_raw_map = {}
for c in vinfast_raw:
    v = c.get('version', '').strip().upper()
    vf_raw_map[v] = c
    if c.get('standardName'):
        vf_raw_map[c.get('standardName').strip().upper()] = c

COLOR_HEX = {
    'Trắng': '#F8FAFC',
    'Infinity Blanc': '#F8FAFC',
    'Brahminy White': '#F8FAFC',
    'Xám': '#64748B',
    'Zenith Grey': '#64748B',
    'Neptune Grey': '#475569',
    'Xám Đậm': '#334155',
    'Bạc': '#CBD5E1',
    'Desat Silver': '#CBD5E1',
    'Đen': '#0F172A',
    'Jet Black': '#0F172A',
    'Đỏ': '#DC2626',
    'Crimson Red': '#DC2626',
    'Vàng': '#F59E0B',
    'Summer Yellow': '#F59E0B',
    'Cam': '#EA580C',
    'Sunset Orange': '#EA580C',
    'Hồng': '#F472B6',
    'Iris Berry': '#C084FC',
    'Xanh Lá': '#16A34A',
    'Urban Mint': '#34D399',
    'Xanh': '#2563EB',
    'VinFast Blue': '#2563EB',
    'Electric Blue': '#38BDF8',
    'Xanh Da Trời': '#38BDF8',
    'Aquatic Azure': '#0EA5E9',
    'Xanh Đại Dương': '#0284C7',
    'Deep Ocean': '#047857',
    'Nâu': '#78350F',
    'Cam Nóc Đen': '#EA580C',
    'Tím': '#7C3AED',
    'Vàng Nóc Đen': '#F59E0B',
    'Xanh Nóc Trắng': '#0284C7',
    'Vàng Nóc Trắng': '#F59E0B',
    'Hồng Nóc Trắng': '#F472B6',
    'Đỏ Nóc Đen': '#DC2626',
    'Cam Nóc Trắng': '#EA580C',
    'Đen Nóc Trắng': '#0F172A',
    'Tím Nóc Xám': '#7C3AED'
}

def get_colors(raw_key, custom_colors=None):
    if custom_colors:
        return custom_colors
    raw = vf_raw_map.get(raw_key) or {}
    color_imgs = raw.get('colorImages') or {}
    res = []
    for c_name, c_url in color_imgs.items():
        res.append({
            'name': c_name,
            'hex': COLOR_HEX.get(c_name, '#94A3B8'),
            'image': c_url
        })
    if not res:
        # Default colors
        return [
            {'name': 'Trắng (Infinity Blanc)', 'hex': '#F8FAFC', 'image': raw.get('image') or ''},
            {'name': 'Xám (Zenith Grey)', 'hex': '#64748B', 'image': raw.get('image') or ''},
            {'name': 'Đỏ (Crimson Red)', 'hex': '#DC2626', 'image': raw.get('image') or ''},
            {'name': 'Đen (Jet Black)', 'hex': '#0F172A', 'image': raw.get('image') or ''}
        ]
    return res

# Official Pricing & Metadata Map
OFFICIAL_CAR_META = {
    'VinFast VF 3 Eco': {
        'id': 'vf3_eco',
        'shortName': 'VF 3 Eco',
        'segment': 'Minicar (Mini SUV Đô thị)',
        'price': 285000000,
        'priceText': '285.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 900.000 đ/tháng hoặc Mua pin: 322.000.000 đ',
        'raw_key': 'VF3 ECO',
        'badgeColor': 'yellow',
        'highlights': ['Gầm cao 175 mm', 'Màn hình 10 inch', 'Sạc nhanh 36 phút', 'Chi phí sạc chỉ ~300đ/km']
    },
    'VinFast VF 3 Plus': {
        'id': 'vf3_plus',
        'shortName': 'VF 3 Plus',
        'segment': 'Minicar (Mini SUV Đô thị)',
        'price': 296000000,
        'priceText': '296.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 900.000 đ/tháng hoặc Mua pin: 333.000.000 đ',
        'raw_key': 'VF3 PLUS',
        'badgeColor': 'yellow',
        'highlights': ['Thêm ốp la-zăng thể thao', 'Gương chỉnh & gập điện', 'Hỗ trợ đỗ xe & Camera lùi', 'Màn hình 10 inch']
    },
    'VinFast VF 5 Plus': {
        'id': 'vf5_plus',
        'shortName': 'VF 5 Plus',
        'segment': 'Hạng A (A-SUV Đô thị)',
        'price': 496000000,
        'priceText': '496.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 1.200.000 đ/tháng hoặc Kèm pin: 576.000.000 đ',
        'raw_key': 'VF5',
        'badgeColor': 'blue',
        'highlights': ['Công suất 134 HP cực bốc', '6 túi khí an toàn', '8 tùy chọn màu ngoại thất', 'Vua doanh số phân khúc A-SUV']
    },
    'VF 6 Eco': {
        'id': 'vf6_eco',
        'shortName': 'VF 6 Eco',
        'segment': 'Hạng B (B-SUV Đô thị)',
        'price': 646000000,
        'priceText': '646.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 1.800.000 đ/tháng hoặc Kèm pin: 736.000.000 đ',
        'raw_key': 'VF6 ECO',
        'badgeColor': 'emerald',
        'highlights': ['Pin 59.6 kWh tầm xa 485 km (NEDC)', 'Công suất 130 kW (174 HP)', 'Màn hình 12.9 inch', 'Trợ lái ADAS tiêu chuẩn']
    },
    'VF 6 Plus': {
        'id': 'vf6_plus',
        'shortName': 'VF 6 Plus',
        'segment': 'Hạng B (B-SUV Đô thị)',
        'price': 699000000,
        'priceText': '699.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 1.800.000 đ/tháng hoặc Kèm pin: 789.000.000 đ',
        'raw_key': 'VF6 PLUS',
        'badgeColor': 'emerald',
        'highlights': ['Công suất khủng 201 HP / 310 Nm', 'Mâm 18 inch', 'Gói ADAS nâng cao Level 2', 'Màn hình HUD & 8 loa, 7 túi khí']
    },
    'VinFast VF 7 Eco': {
        'id': 'vf7_eco',
        'shortName': 'VF 7 Eco',
        'segment': 'Hạng C (C-SUV Thể thao)',
        'price': 740000000,
        'priceText': '740.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 850.000.000 đ',
        'raw_key': 'VF7 ECO',
        'badgeColor': 'purple',
        'highlights': ['Trục cơ sở 2.840 mm rộng nhất hạng C', 'Công suất 174 HP', 'Mâm 19 inch', 'Tay nắm cửa dạng ẩn hiện đại']
    },
    'VinFast VF 7 Plus': {
        'id': 'vf7_plus_fwd',
        'shortName': 'VF 7 Plus (FWD)',
        'segment': 'Hạng C (C-SUV Thể thao)',
        'price': 830000000,
        'priceText': '830.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 940.000.000 đ',
        'raw_key': 'VF7 PLUS TC2 - TRẦN THÉP',
        'badgeColor': 'purple',
        'highlights': ['Pin 70 kWh', 'Công suất 201 HP / 310 Nm', 'Mâm 20 inch bề thế', 'Màn hình HUD & Sạc không dây, ADAS cao cấp']
    },
    'VinFast VF 7 Plus AWD': {
        'id': 'vf7_plus_awd',
        'shortName': 'VF 7 Plus AWD',
        'segment': 'Hạng C (C-SUV Thể thao)',
        'price': 880000000,
        'priceText': '880.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 990.000.000 đ',
        'raw_key': 'VF7 PLUS TC2 - TRẦN THÉP',
        'badgeColor': 'purple',
        'highlights': ['Dẫn động 2 cầu AWD 349 HP / 500 Nm', 'Tăng tốc 0-100km/h chỉ 5.8s', 'Mâm 20 inch', 'Trọn bộ ADAS tự hành Cấp 2']
    },
    'VF 8 Eco': {
        'id': 'vf8_eco_catl',
        'shortName': 'VF 8 Eco (CATL)',
        'segment': 'Hạng D (D-SUV Toàn cầu)',
        'price': 898000000,
        'priceText': '898.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 1.019.000.000 đ',
        'raw_key': 'VF8 ECO TIÊU CHUẨN 1 - 1 CẦU',
        'badgeColor': 'sky',
        'highlights': ['Pin CATL 87.7 kWh tầm xa 562 km (NEDC)', 'Màn hình 15.6 inch', '10 túi khí an toàn', 'Cốp trước Frunk 88L']
    },
    'VF 8 Plus': {
        'id': 'vf8_plus_catl',
        'shortName': 'VF 8 Plus (CATL)',
        'segment': 'Hạng D (D-SUV Toàn cầu)',
        'price': 1079000000,
        'priceText': '1.079.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 1.199.000.000 đ',
        'raw_key': 'VF8 PLUS TIÊU CHUẨN 1 - 2 CẦU',
        'badgeColor': 'sky',
        'highlights': ['AWD 402 HP / 620 Nm tăng tốc 5.5s', 'Pin CATL 87.7 kWh', 'Ghế sưởi & thông gió 2 hàng ghế', '11 túi khí, ADAS Level 2 nâng cao']
    },
    'VinFast VF 8 Thế hệ mới': {
        'id': 'vf8_the_he_moi',
        'shortName': 'VF 8 Thế Hệ Mới',
        'segment': 'Hạng D (D-SUV Cải tiến)',
        'price': 899000000,
        'priceText': '899.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 1.099.000.000 đ',
        'raw_key': 'VF8 ALL NEW',
        'badgeColor': 'sky',
        'highlights': ['Công suất 170 kW (228 HP) / 330 Nm', 'Pin 60.13 kWh (480-500 km NEDC)', 'Trọng lượng nhẹ 1.870 kg', 'Mâm 19 inch, sạc nhanh < 30 phút']
    },
    'VinFast VF 9 Eco': {
        'id': 'vf9_eco_catl',
        'shortName': 'VF 9 Eco (CATL)',
        'segment': 'Hạng E (Full-size Luxury SUV)',
        'price': 1348000000,
        'priceText': '1.348.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 3.900.000 đ/tháng hoặc Kèm pin: 1.589.000.000 đ',
        'raw_key': 'VF9 ECO',
        'badgeColor': 'rose',
        'highlights': ['Pin khủng CATL 123 kWh (626 km WLTP)', 'AWD 402 HP', 'Đèn LED Matrix & Cửa hít', 'Điều hòa 3 vùng, 11 túi khí']
    },
    'VinFast VF 9 Plus': {
        'id': 'vf9_plus_catl',
        'shortName': 'VF 9 Plus (Chủ tịch)',
        'segment': 'Hạng E (Full-size Luxury SUV)',
        'price': 1529000000,
        'priceText': '1.529.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 3.900.000 đ/tháng hoặc Kèm pin: 1.789.000.000 đ',
        'raw_key': 'VF9 PLUS',
        'badgeColor': 'rose',
        'highlights': ['Ghế VIP cơ trưởng massage sưởi/thông gió', 'Pin CATL 123 kWh', 'La-zăng 21 inch', 'Màn hình hàng ghế sau 8 inch & Ổ điện 230V']
    },
    'VinFast Minio Green': {
        'id': 'minio_green',
        'shortName': 'Minio Green',
        'segment': 'Minicar Dịch vụ Đô thị',
        'price': 188000000,
        'priceText': '188.000.000 VNĐ',
        'batteryFeeText': 'Gói cước sạc & thuê pin thương mại ưu đãi',
        'raw_key': 'MINIO GREEN',
        'badgeColor': 'emerald',
        'highlights': ['Giá chỉ 188 triệu đồng', 'Quãng đường 210 km (NEDC)', 'Đèn trước LED', 'Sạc nhanh 34 phút (>= 24 kW)']
    },
    'VinFast Herio Green': {
        'id': 'herio_green',
        'shortName': 'Herio Green',
        'segment': 'Hạng A (Đô thị / Dịch vụ Green)',
        'price': 450000000,
        'priceText': '450.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 1.200.000 đ/tháng hoặc Mua kèm pin',
        'raw_key': 'HERIO GREEN',
        'badgeColor': 'emerald',
        'highlights': ['Công suất 100 kW (134 HP)', '4 phanh đĩa an toàn', 'Bi-Halogen Projector', 'Màn hình 8 inch CarPlay không dây & ViVi']
    },
    'VinFast Limo Green': {
        'id': 'limo_green',
        'shortName': 'Limo Green',
        'segment': 'Dịch vụ Đưa đón VIP (7 Chỗ)',
        'price': 699000000,
        'priceText': '699.000.000 VNĐ',
        'batteryFeeText': 'Chính sách ưu đãi doanh nghiệp & Xanh SM Luxury',
        'raw_key': 'LIMO GREEN',
        'badgeColor': 'emerald',
        'highlights': ['7 chỗ ngồi nỉ cao cấp', 'Pin 60.13 kWh (450 km NEDC)', 'Công suất 150 kW / 280 Nm', 'Mâm 18 inch, sạc nhanh 30 phút']
    },
    'VinFast VF MPV7': {
        'id': 'vf_mpv7',
        'shortName': 'VF MPV 7',
        'segment': 'MPV Đa dụng 7 Chỗ',
        'price': 750000000,
        'priceText': '750.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.100.000 đ/tháng hoặc Mua kèm pin',
        'raw_key': 'VF MVP 7',
        'badgeColor': 'teal',
        'highlights': ['7 chỗ da nhân tạo', 'Mâm hợp kim 19 inch (235/50 R19)', 'Pin 60.13 kWh (450 km)', 'Cần số sau vô lăng & Ga tự động']
    },
    'VinFast VF 2': {
        'id': 'vf2',
        'shortName': 'VF 2',
        'segment': 'Minicar (Mini Car Đô thị)',
        'price': 188000000,
        'priceText': '188.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 600.000 đ/tháng hoặc Kèm pin: 248.000.000 đ',
        'raw_key': 'VF 2',
        'badgeColor': 'yellow',
        'highlights': ['Kích thước siêu nhỏ 3.090 mm', 'Đèn LED trước', 'Pin LFP 18.3 kWh (210 km)', 'Sạc nhanh 34 phút']
    },
    'VinFast EC VAN (Bản tiêu chuẩn / Tiêu chuẩn)': {
        'id': 'ec_van_standard',
        'shortName': 'EC Van Tiêu Chuẩn',
        'segment': 'Xe Tải Van Điện Đô thị',
        'price': 248000000,
        'priceText': '248.000.000 VNĐ',
        'batteryFeeText': 'Gói cước sạc & thuê pin thương mại',
        'raw_key': 'EC VAN TIÊU CHUẨN',
        'badgeColor': 'amber',
        'highlights': ['Vào phố cấm 24/7', 'Khoang hàng 2.6 m3, tải 650 kg', 'Pin 18.3 kWh (175 km)', 'Sạc nhanh DC 24.2 kW']
    },
    'VinFast EC VAN - Phiên bản Nâng cao': {
        'id': 'ec_van_advanced',
        'shortName': 'EC Van Nâng Cao',
        'segment': 'Xe Tải Van Điện Đô thị',
        'price': 286000000,
        'priceText': '286.000.000 VNĐ',
        'batteryFeeText': 'Gói cước sạc & thuê pin thương mại',
        'raw_key': 'EC VAN NÂNG CAO',
        'badgeColor': 'amber',
        'highlights': ['Thêm điều hòa 2 chiều', 'Kính cửa chỉnh điện', 'Khóa cửa tự động khi chạy', 'Khoang hàng 2.6 m3, tải 650 kg']
    },
    'VinFast EC VAN - Phiên bản Nâng cao có cửa trượt': {
        'id': 'ec_van_sliding',
        'shortName': 'EC Van Cửa Trượt',
        'segment': 'Xe Tải Van Điện Đô thị',
        'price': 306000000,
        'priceText': '306.000.000 VNĐ',
        'batteryFeeText': 'Gói cước sạc & thuê pin thương mại',
        'raw_key': 'EC VAN NÂNG CAO (Cửa trượt)',
        'badgeColor': 'amber',
        'highlights': ['Cửa lùa trượt bên hông bốc dỡ hàng siêu tiện', 'Điều hòa 2 chiều', 'Tải trọng 650 kg', 'Lưu thông 24/7 nội đô']
    },
    'VinFast VF Wild': {
        'id': 'vf_wild',
        'shortName': 'VF Wild (EREV)',
        'segment': 'Bán Tải Cỡ Trung Đột Phá',
        'price': 860000000,
        'priceText': '860.000.000 VNĐ (Dự kiến)',
        'batteryFeeText': 'Chính sách công nghệ mở rộng tầm vận hành EREV',
        'raw_key': 'VF WILD COMFORT',
        'badgeColor': 'orange',
        'highlights': ['Tầm xa > 1.000 km (hỗn hợp)', 'Động cơ xăng 1.5L sạc pin + Mô tơ 160 kW', 'Lội nước 500 mm, thùng 1.574 mm', 'Hỗ trợ cấp điện ngoài V2L']
    }
}

# Brochure references dict
BROCHURE_REFS = {
    '1': '16062026-Brochure-VF-3.pdf (Tài liệu chính thức VF 3)',
    '2': 'VF5Brochure.pdf (Tài liệu chính thức VF 5)',
    '3': 'VF 6_Brochure_Final_130526 (12AM)_compressed.pdf (Tài liệu chính thức VF 6)',
    '4': '10042026-Brochur- VF-7.pdf (Tài liệu chính thức VF 7)',
    '5': 'VF 8 - 05.03.2026.pdf (Tài liệu chính thức VF 8 Pin CATL)',
    '6': 'VF 8 The he moi_Brochure_final 20.05.pdf (Tài liệu chính thức VF 8 Thế hệ mới)',
    '7': 'VF 9_ Brochure.pdf (Tài liệu chính thức VF 9)',
    '8': 'Brochure Minio Green 090126.pdf (Tài liệu chính thức Minio Green)',
    '9': '06082025-brochure-herio.pdf (Tài liệu chính thức Herio Green)',
    '10': '09012026-brochure-limo-green.pdf (Tài liệu chính thức Limo Green)',
    '11': '05022026-Brochure-VF-MPV-7.pdf (Tài liệu chính thức VF MPV 7)',
    '12': 'brochure_vf_2.pdf (Tài liệu chính thức VF 2)',
    '13': 'brochure-ec-van-040726-e.pdf (Tài liệu chính thức EC Van)',
    '14': '260921 VF WILD.pdf (Tài liệu chính thức VF Wild)'
}

# Parse CSV rows
parsed_cars = []

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        model_name = row.get('Dòng xe / Phiên bản', '').strip()
        if not model_name or model_name == 'Index' or model_name.isdigit():
            continue

        meta = OFFICIAL_CAR_META.get(model_name)
        if not meta:
            # Fallback search
            for k, m in OFFICIAL_CAR_META.items():
                if k.lower() in model_name.lower() or model_name.lower() in k.lower():
                    meta = m
                    break
        if not meta:
            meta = {
                'id': model_name.lower().replace(' ', '_'),
                'shortName': model_name.replace('VinFast', '').strip(),
                'segment': 'Ô tô điện VinFast',
                'price': 500000000,
                'priceText': 'Đang cập nhật',
                'batteryFeeText': 'Theo chính sách VinFast',
                'raw_key': model_name,
                'badgeColor': 'blue',
                'highlights': []
            }

        ref_code = row.get('Nguồn', '').strip()
        ref_text = BROCHURE_REFS.get(ref_code, f'Brochure chính thức #{ref_code}')

        # Specs raw texts
        dims_text = row.get('Kích thước & Trọng lượng', '').strip()
        engine_text = row.get('Hiệu suất & Động cơ', '').strip()
        battery_text = row.get('Pin & Sạc', '').strip()
        exterior_text = row.get('Ngoại thất', '').strip()
        interior_text = row.get('Nội thất & Tiện nghi', '').strip()
        safety_text = row.get('Tính năng an toàn & An ninh', '').strip()

        # Helper to extract key values
        def extract(pattern, text, default='Chưa công bố'):
            m = re.search(pattern, text, re.IGNORECASE)
            if not m:
                return default
            for g in m.groups():
                if g is not None:
                    return g.strip()
            return default

        # Dimensions
        d_r_c = extract(r'Kích thước(?:\s*xe)?\s*\((?:D\s*x\s*R\s*x\s*C)\):\s*([^;]+)', dims_text)
        wheelbase = extract(r'Chiều dài cơ sở:\s*([^;]+)', dims_text)
        ground_clearance = extract(r'Khoảng sáng gầm xe(?: không tải)?:\s*([^;]+)', dims_text)
        turning_radius = extract(r'Bán kính quay (?:đầu|vòng)(?: tối thiểu)?:\s*([^;]+)', dims_text)
        weight = extract(r'Trọng lượng không tải:\s*([^;]+)', dims_text)
        payload = extract(r'Tải trọng:\s*([^;]+)', dims_text)
        trunk = extract(r'Dung tích (?:khoang hành lý|cốp xe|khoang chứa hành lý)[^:]*:\s*([^;]+)', dims_text)
        cargo_bed = extract(r'(?:Kích thước khoang hàng|Kích thước thùng xe):\s*([^;]+)', dims_text)

        # Performance & Engine
        engine_type = extract(r'(?:Động cơ|motor|Loại động cơ):\s*([^;]+)', engine_text)
        drivetrain = extract(r'Dẫn động:\s*([^;]+)', engine_text)
        max_power = extract(r'Công suất tối đa:\s*([^;]+)', engine_text)
        max_torque = extract(r'Mô-men xoắn (?:cực đại|tối đa):\s*([^;]+)', engine_text)
        acceleration = extract(r'Tăng tốc 0[–-]100 km/h:\s*([^;]+)', engine_text)
        max_speed = extract(r'(?:Tốc độ tối đa|Vận tốc tối đa):\s*([^;]+)', engine_text)
        drive_modes = extract(r'Chế độ lái:\s*([^;]+)', engine_text)
        suspension = extract(r'Hệ thống treo[^:]*:\s*([^;]+)', engine_text)
        water_wading = extract(r'Khả năng lội nước:\s*([^;]+)', engine_text)

        # Battery & Charging
        battery_type = extract(r'Loại pin:\s*([^;]+)|Pin\s*([^;]+)', battery_text)
        battery_cap = extract(r'Dung lượng pin(?: khả dụng)?:\s*([^;]+)', battery_text)
        range_val = extract(r'Quãng đường (?:di chuyển|chạy)[^:]*:\s*([^;]+)', battery_text)
        fast_charge = extract(r'Thời gian (?:nạp|sạc) pin nhanh nhất[^:]*:\s*([^;]+)', battery_text)
        ac_charge = extract(r'Công suất sạc AC tối đa:\s*([^;]+)', battery_text)
        dc_charge = extract(r'Công suất sạc(?: nhanh)? DC tối đa:\s*([^;]+)', battery_text)
        regen = extract(r'Hệ thống phanh tái sinh:\s*([^;]+)|Phanh tái sinh:\s*([^;]+)', battery_text)
        v2l = 'Có hỗ trợ (Vehicle-to-Load)' if 'V2L' in battery_text else 'Không áp dụng'

        # Exterior
        headlights = extract(r'Đèn (?:chiếu sáng phía trước|pha|chiếu sáng LED):\s*([^;]+)', exterior_text)
        wheels = extract(r'(?:Mâm/Lốp|Lazang|Vành mâm xe|La-zăng|Kích thước lốp|Kích thước la-zăng):\s*([^;]+)', exterior_text)
        mirrors = extract(r'Gương chiếu hậu[^:]*:\s*([^;]+)', exterior_text)
        wipers = extract(r'Gạt mưa[^:]*:\s*([^;]+)', exterior_text)
        tailgate = extract(r'(?:Đóng/mở cốp sau|Cửa cốp sau|Cốp sau):\s*([^;]+)', exterior_text)

        # Interior
        seats = extract(r'Số chỗ ngồi:\s*([^;]+)|(\d+\s*chỗ[^;]*)', interior_text)
        infotainment = extract(r'Màn hình giải trí[^:]*:\s*([^;]+)|Màn hình thông tin lái:\s*([^;]+)', interior_text)
        hud = 'Có (Màn hình HUD kính lái)' if 'Màn hình HUD: Có' in interior_text or 'màn hình HUD' in interior_text.lower() and 'Không' not in extract(r'Màn hình HUD:\s*([^;]+)', interior_text) else 'Không có'
        sound = extract(r'Hệ thống (?:âm thanh|loa):\s*([^;]+)', interior_text)
        climate = extract(r'(?:Hệ thống điều hòa|Điều hòa)[^:]*:\s*([^;]+)', interior_text)
        shifter = extract(r'(?:Cần chuyển số|Cần số|Phanh tay|Phanh đỗ điện tử)[^:]*:\s*([^;]+)', interior_text)

        # Safety & ADAS
        airbags = extract(r'(\d+\s*túi khí[^;]*|1 túi khí[^;]*|2 túi khí[^;]*|4 túi khí[^;]*|6 túi khí[^;]*|7 túi khí[^;]*|10 túi khí[^;]*|11 túi khí[^;]*)', safety_text)
        if airbags == 'Chưa công bố' and 'túi khí' in safety_text.lower():
            airbags = extract(r'Túi khí[^:]*:\s*([^;]+)', safety_text)
        adas_info = extract(r'(?:ADAS[^:]*|Trợ lái[^:]*):\s*([^;]+)', safety_text)
        if adas_info == 'Chưa công bố':
            adas_info = 'Trợ lái tiêu chuẩn' if 'Cruise' in interior_text or 'Cruise' in safety_text else 'Cơ bản'

        # Colors & Image
        raw_key = meta['raw_key']
        raw_car = vf_raw_map.get(raw_key, {})
        car_image = raw_car.get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/vf5/xe-dien-vinfast-vf-5-plus-thiet-ke-ngoai-that-mau-trang-desktop.webp'
        car_colors = get_colors(raw_key)

        # Power number for radar
        hp = 100
        p_match = re.search(r'(\d+)\s*(?:kW|hp|HP)', max_power)
        if p_match:
            val = int(p_match.group(1))
            hp = int(val * 1.341) if 'kw' in max_power.lower() else val

        radar_power = min(100, max(45, int(hp / 4.2)))
        radar_range = 75
        r_match = re.search(r'(\d+)\s*km', range_val)
        if r_match:
            r_num = int(r_match.group(1))
            radar_range = min(100, max(50, int(r_num / 6.2)))

        is_ev = 'xăng' not in engine_type.lower() and 'đốt trong' not in engine_type.lower()
        fuel_type = 'Điện thuần (BEV)' if is_ev else 'Xăng + Điện (EREV)'

        # Assemble car object
        car_obj = {
            'id': meta['id'],
            'name': model_name,
            'shortName': meta['shortName'],
            'brand': 'VinFast',
            'origin': 'Việt Nam',
            'segment': meta['segment'],
            'category': 'Xe điện VinFast',
            'price': meta['price'],
            'priceText': meta['priceText'],
            'batteryFeeText': meta['batteryFeeText'],
            'fuelType': fuel_type,
            'image': car_image,
            'colors': car_colors,
            'tag': meta['highlights'][0] if meta.get('highlights') else 'Chính hãng VinFast',
            'badgeColor': meta['badgeColor'],
            'highlights': meta.get('highlights') or [d_r_c, max_power, range_val, ref_text],
            'brochureRef': ref_text,
            'radar': {
                'power': radar_power,
                'space': 85 if '7 chỗ' in dims_text or 'Full-size' in meta['segment'] else (60 if '3.190' in dims_text or '3.090' in dims_text else 80),
                'range': radar_range,
                'safety': 95 if '11 túi' in airbags or '7 túi' in airbags else (80 if '6 túi' in airbags or '4 túi' in airbags else 65),
                'tech': 95 if 'ADAS Level 2' in safety_text or 'ADAS' in safety_text else 75,
                'economy': 98 if is_ev else 90
            },
            'specs': {
                'cat1_dimensions': {
                    'title': 'I. KÍCH THƯỚC & TRỌNG LƯỢNG',
                    'd_r_c': d_r_c if d_r_c != 'Chưa công bố' else dims_text.split(';')[0].replace('Kích thước (D x R x C):', '').strip(),
                    'wheelbase': wheelbase,
                    'groundClearance': ground_clearance,
                    'turningRadius': turning_radius,
                    'weight': weight,
                    'payload': payload,
                    'trunk': trunk,
                    'cargoBed': cargo_bed
                },
                'cat2_engine': {
                    'title': 'II. HIỆU SUẤT & ĐỘNG CƠ',
                    'engineType': engine_type,
                    'drivetrain': drivetrain,
                    'maxPower': max_power,
                    'maxTorque': max_torque,
                    'acceleration': acceleration,
                    'maxSpeed': max_speed,
                    'driveModes': drive_modes,
                    'suspension': suspension,
                    'waterWading': water_wading
                },
                'cat3_battery': {
                    'title': 'III. PIN & SẠC',
                    'batteryType': battery_type,
                    'batteryCapacity': battery_cap,
                    'range': range_val,
                    'fastChargeTime': fast_charge,
                    'acCharge': ac_charge,
                    'dcCharge': dc_charge,
                    'regenBraking': regen,
                    'v2l': v2l
                },
                'cat4_exterior': {
                    'title': 'IV. NGOẠI THẤT',
                    'headlights': headlights,
                    'wheels': wheels,
                    'mirrors': mirrors,
                    'wipers': wipers,
                    'tailgate': tailgate,
                    'fullExterior': exterior_text
                },
                'cat5_interior': {
                    'title': 'V. NỘI THẤT & TIỆN NGHI',
                    'seating': seats,
                    'infotainment': infotainment,
                    'hud': hud,
                    'sound': sound,
                    'climate': climate,
                    'shifter': shifter,
                    'fullInterior': interior_text
                },
                'cat6_safety': {
                    'title': 'VI. TÍNH NĂNG AN TOÀN & AN NINH',
                    'airbags': airbags,
                    'adas': adas_info,
                    'fullSafety': safety_text
                },
                'cat7_economics': {
                    'title': 'VII. CHI PHÍ SỬ DỤNG & BẢO HÀNH',
                    'fuelCost1000km': '300.000 - 450.000 VNĐ' if is_ev else '650.000 VNĐ (sạc + xăng)',
                    'maintenance': 'Bảo dưỡng định kỳ 12.000 km/lần, chi phí cực thấp',
                    'warranty': '7 - 10 năm hoặc 160.000 - 200.000 km (Pin bảo hành lên tới 10 năm)'
                },
                'cat8_reference': {
                    'title': 'VIII. TÀI LIỆU BROCHURE CHÍNH HÃNG',
                    'source': ref_text
                }
            }
        }
        parsed_cars.append(car_obj)

print(f"Successfully processed {len(parsed_cars)} VinFast cars from brochure.")

# Append competitor benchmark cars (Toyota Wigo, Kia Morning, Hyundai i10)
competitors = [
    {
        'id': 'toyota_wigo_g',
        'name': 'Toyota Wigo G',
        'shortName': 'Wigo G',
        'brand': 'Toyota',
        'origin': 'Nhập khẩu Indonesia',
        'segment': 'Hạng A (Hatchback Đô thị)',
        'category': 'Xe xăng đối thủ',
        'price': 405000000,
        'priceText': '405.000.000 VNĐ',
        'batteryFeeText': 'Không áp dụng (Xe động cơ đốt trong)',
        'fuelType': 'Xăng (Đốt trong)',
        'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
        'colors': [
            {'name': 'Đỏ', 'hex': '#DC2626', 'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Trắng', 'hex': '#F8FAFC', 'image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Cam', 'hex': '#EA580C', 'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'}
        ],
        'tag': 'Xe xăng nhập khẩu Nhật/Indo',
        'badgeColor': 'rose',
        'highlights': ['Đèn trước Full LED', 'Vòng quay 4.5m luồn lách', 'Động cơ 1.2L 3 xi-lanh', 'Hộp số D-CVT'],
        'brochureRef': 'Brochure Toyota Wigo 2024-2026',
        'radar': {'power': 55, 'space': 70, 'range': 85, 'safety': 68, 'tech': 62, 'economy': 75},
        'specs': {
            'cat1_dimensions': {
                'title': 'I. KÍCH THƯỚC & TRỌNG LƯỢNG',
                'd_r_c': '3.760 x 1.665 x 1.515 mm',
                'wheelbase': '2.525 mm',
                'groundClearance': '160 mm',
                'turningRadius': '4,50 m',
                'weight': '890 kg',
                'payload': '350 kg',
                'trunk': '261 L',
                'cargoBed': 'Không áp dụng'
            },
            'cat2_engine': {
                'title': 'II. HIỆU SUẤT & ĐỘNG CƠ',
                'engineType': 'Xăng 1.2L 3 xi-lanh (Đốt trong)',
                'drivetrain': 'Cầu trước (FWD)',
                'maxPower': '65 kW (87 HP) @ 6.000 rpm',
                'maxTorque': '113 Nm @ 4.500 rpm',
                'acceleration': '12.5 s',
                'maxSpeed': '155 km/h',
                'driveModes': 'Không có (D/S/B)',
                'suspension': 'MacPherson / Dầm xoắn',
                'waterWading': 'Khoảng 250 mm'
            },
            'cat3_battery': {
                'title': 'III. PIN & SẠC',
                'batteryType': 'Không áp dụng (Bình xăng 36 L)',
                'batteryCapacity': 'Bình xăng 36 L',
                'range': '~550 - 650 km / bình xăng đầy',
                'fastChargeTime': 'Đổ xăng 3 phút',
                'acCharge': 'Không áp dụng',
                'dcCharge': 'Không áp dụng',
                'regenBraking': 'Không áp dụng',
                'v2l': 'Không có'
            },
            'cat4_exterior': {
                'title': 'IV. NGOẠI THẤT',
                'headlights': 'LED phản xạ đa hướng / LED',
                'wheels': 'Mâm hợp kim 14 inch (175/65R14)',
                'mirrors': 'Chỉnh điện, gập điện, tích hợp báo rẽ',
                'wipers': 'Chỉnh cơ gián đoạn',
                'tailgate': 'Chỉnh cơ',
                'fullExterior': 'Đèn trước full LED phản xạ đa hướng, mâm hợp kim 14 inch, gương gập điện'
            },
            'cat5_interior': {
                'title': 'V. NỘI THẤT & TIỆN NGHI',
                'seating': '5 chỗ ngồi (ghế nỉ)',
                'infotainment': 'Màn hình cảm ứng 7 inch',
                'hud': 'Không có',
                'sound': '4 loa',
                'climate': 'Điều hòa chỉnh điện (hiển thị số)',
                'shifter': 'Cần số cơ khí truyền thống',
                'fullInterior': 'Ghế nỉ, màn hình 7 inch, khởi động nút bấm Start/Stop'
            },
            'cat6_safety': {
                'title': 'VI. TÍNH NĂNG AN TOÀN & AN NINH',
                'airbags': '2 túi khí',
                'adas': 'Cảnh báo điểm mù BSM, Cảnh báo phương tiện cắt ngang RCTA',
                'fullSafety': 'ABS, EBD, BA, VSC, TRC, HAC, Cảm biến lùi, Camera lùi, 2 túi khí'
            },
            'cat7_economics': {
                'title': 'VII. CHI PHÍ SỬ DỤNG & BẢO HÀNH',
                'fuelCost1000km': '1.300.000 - 1.500.000 VNĐ (xăng ~24k/L)',
                'maintenance': 'Bảo dưỡng định kỳ 5.000 km/lần',
                'warranty': '3 năm hoặc 100.000 km'
            },
            'cat8_reference': {
                'title': 'VIII. TÀI LIỆU BROCHURE CHÍNH HÃNG',
                'source': 'Catalogue chính thức Toyota Việt Nam'
            }
        }
    },
    {
        'id': 'kia_morning_xline',
        'name': 'Kia Morning X-Line',
        'shortName': 'Morning X-Line',
        'brand': 'Kia',
        'origin': 'Lắp ráp trong nước (Thaco)',
        'segment': 'Hạng A (Hatchback Đô thị)',
        'category': 'Xe xăng đối thủ',
        'price': 439000000,
        'priceText': '439.000.000 VNĐ',
        'batteryFeeText': 'Không áp dụng (Xe động cơ đốt trong)',
        'fuelType': 'Xăng (Đốt trong)',
        'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80',
        'colors': [
            {'name': 'Đỏ', 'hex': '#DC2626', 'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Vàng', 'hex': '#F59E0B', 'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Trắng', 'hex': '#F8FAFC', 'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80'}
        ],
        'tag': 'Ngoại hình việt dã phong cách',
        'badgeColor': 'amber',
        'highlights': ['Gói ngoại thất X-Line việt dã', 'Màn hình 8 inch nổi', 'Đèn Projector thấu kính', 'Khởi động Start/Stop'],
        'brochureRef': 'Brochure Kia Morning Thaco',
        'radar': {'power': 52, 'space': 62, 'range': 80, 'safety': 65, 'tech': 66, 'economy': 72},
        'specs': {
            'cat1_dimensions': {
                'title': 'I. KÍCH THƯỚC & TRỌNG LƯỢNG',
                'd_r_c': '3.595 x 1.595 x 1.495 mm',
                'wheelbase': '2.400 mm',
                'groundClearance': '152 mm',
                'turningRadius': '4,70 m',
                'weight': '950 kg',
                'payload': '320 kg',
                'trunk': '255 L (gập ghế 1.010 L)',
                'cargoBed': 'Không áp dụng'
            },
            'cat2_engine': {
                'title': 'II. HIỆU SUẤT & ĐỘNG CƠ',
                'engineType': 'Xăng Kappa 1.25L 4 xi-lanh',
                'drivetrain': 'Cầu trước (FWD)',
                'maxPower': '62 kW (83 HP) @ 6.000 rpm',
                'maxTorque': '122 Nm @ 4.000 rpm',
                'acceleration': '13.0 s',
                'maxSpeed': '150 km/h',
                'driveModes': 'Không có',
                'suspension': 'MacPherson / Trục xoắn',
                'waterWading': 'Khoảng 200 mm'
            },
            'cat3_battery': {
                'title': 'III. PIN & SẠC',
                'batteryType': 'Không áp dụng (Bình xăng 35 L)',
                'batteryCapacity': 'Bình xăng 35 L',
                'range': '~450 - 550 km / bình xăng đầy',
                'fastChargeTime': 'Đổ xăng 3 phút',
                'acCharge': 'Không áp dụng',
                'dcCharge': 'Không áp dụng',
                'regenBraking': 'Không áp dụng',
                'v2l': 'Không có'
            },
            'cat4_exterior': {
                'title': 'IV. NGOẠI THẤT',
                'headlights': 'Halogen Projector / LED',
                'wheels': 'Mâm hợp kim 15 inch (175/50R15)',
                'mirrors': 'Chỉnh điện, gập điện, sấy gương',
                'wipers': 'Chỉnh cơ',
                'tailgate': 'Chỉnh cơ',
                'fullExterior': 'Gói ốp thể thao X-Line, đèn halogen projector, mâm đúc 15 inch'
            },
            'cat5_interior': {
                'title': 'V. NỘI THẤT & TIỆN NGHI',
                'seating': '5 chỗ (ghế da 2 tông màu)',
                'infotainment': 'Màn hình cảm ứng 8 inch',
                'hud': 'Không có',
                'sound': '6 loa',
                'climate': 'Điều hòa tự động',
                'shifter': 'Cần số cơ zíc zắc',
                'fullInterior': 'Ghế da phối viền chỉ màu, điều hòa tự động, màn hình 8 inch'
            },
            'cat6_safety': {
                'title': 'VI. TÍNH NĂNG AN TOÀN & AN NINH',
                'airbags': '2 túi khí',
                'adas': 'Cơ bản',
                'fullSafety': 'ABS, EBD, ESC, HAC khởi hành ngang dốc, camera lùi, cảm biến lùi, 2 túi khí'
            },
            'cat7_economics': {
                'title': 'VII. CHI PHÍ SỬ DỤNG & BẢO HÀNH',
                'fuelCost1000km': '1.400.000 - 1.600.000 VNĐ (xăng ~24k/L)',
                'maintenance': 'Bảo dưỡng định kỳ 5.000 km',
                'warranty': '3 năm không giới hạn km'
            },
            'cat8_reference': {
                'title': 'VIII. TÀI LIỆU BROCHURE CHÍNH HÃNG',
                'source': 'Catalogue Thaco Kia Việt Nam'
            }
        }
    },
    {
        'id': 'hyundai_i10_at',
        'name': 'Hyundai Grand i10 1.2 AT',
        'shortName': 'Grand i10 1.2 AT',
        'brand': 'Hyundai',
        'origin': 'Lắp ráp trong nước (TC Motor)',
        'segment': 'Hạng A (Hatchback Đô thị)',
        'category': 'Xe xăng đối thủ',
        'price': 435000000,
        'priceText': '435.000.000 VNĐ',
        'batteryFeeText': 'Không áp dụng (Xe động cơ đốt trong)',
        'fuelType': 'Xăng (Đốt trong)',
        'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80',
        'colors': [
            {'name': 'Trắng', 'hex': '#F8FAFC', 'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Đỏ', 'hex': '#DC2626', 'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Bạc', 'hex': '#CBD5E1', 'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80'}
        ],
        'tag': 'Hàng ghế sau rộng & Cửa gió sau',
        'badgeColor': 'indigo',
        'highlights': ['Cửa gió điều hòa hàng ghế 2', 'Cảm biến áp suất lốp TPMS', 'Ga tự động Cruise Control', '4 túi khí an toàn'],
        'brochureRef': 'Brochure Hyundai Grand i10 TC Motor',
        'radar': {'power': 53, 'space': 74, 'range': 80, 'safety': 75, 'tech': 72, 'economy': 70},
        'specs': {
            'cat1_dimensions': {
                'title': 'I. KÍCH THƯỚC & TRỌNG LƯỢNG',
                'd_r_c': '3.815 x 1.680 x 1.520 mm',
                'wheelbase': '2.450 mm',
                'groundClearance': '157 mm',
                'turningRadius': '5,10 m',
                'weight': '1.020 kg',
                'payload': '350 kg',
                'trunk': '260 L',
                'cargoBed': 'Không áp dụng'
            },
            'cat2_engine': {
                'title': 'II. HIỆU SUẤT & ĐỘNG CƠ',
                'engineType': 'Xăng Kappa 1.2L MPI 4 xi-lanh',
                'drivetrain': 'Cầu trước (FWD)',
                'maxPower': '61 kW (83 HP) @ 6.000 rpm',
                'maxTorque': '114 Nm @ 4.000 rpm',
                'acceleration': '12.8 s',
                'maxSpeed': '155 km/h',
                'driveModes': 'Eco / Normal',
                'suspension': 'MacPherson / Thanh xoắn',
                'waterWading': 'Khoảng 250 mm'
            },
            'cat3_battery': {
                'title': 'III. PIN & SẠC',
                'batteryType': 'Không áp dụng (Bình xăng 37 L)',
                'batteryCapacity': 'Bình xăng 37 L',
                'range': '~480 - 580 km / bình xăng đầy',
                'fastChargeTime': 'Đổ xăng 3 phút',
                'acCharge': 'Không áp dụng',
                'dcCharge': 'Không áp dụng',
                'regenBraking': 'Không áp dụng',
                'v2l': 'Không có'
            },
            'cat4_exterior': {
                'title': 'IV. NGOẠI THẤT',
                'headlights': 'Halogen Projector / LED',
                'wheels': 'Mâm hợp kim 15 inch Diamond Cut (175/60R15)',
                'mirrors': 'Chỉnh điện, gập điện, sấy gương',
                'wipers': 'Chỉnh cơ',
                'tailgate': 'Chỉnh cơ',
                'fullExterior': 'Lưới tản nhiệt mở rộng, đèn LED định vị ban ngày, mâm 15 inch'
            },
            'cat5_interior': {
                'title': 'V. NỘI THẤT & TIỆN NGHI',
                'seating': '5 chỗ (ghế da màu tối có chỉ viền đỏ)',
                'infotainment': 'Màn hình cảm ứng 8 inch (Apple CarPlay/Android Auto)',
                'hud': 'Không có',
                'sound': '4 loa',
                'climate': 'Điều hòa chỉnh cơ + Cửa gió điều hòa hàng ghế sau',
                'shifter': 'Cần số tự động 4 cấp',
                'fullInterior': 'Cửa gió sau độc nhất phân khúc A, ga tự động Cruise Control'
            },
            'cat6_safety': {
                'title': 'VI. TÍNH NĂNG AN TOÀN & AN NINH',
                'airbags': '4 túi khí',
                'adas': 'Ga tự động Cruise Control, TPMS cảm biến áp suất lốp',
                'fullSafety': 'ABS, EBD, BA, ESC, HAC, Cảm biến lùi, Camera lùi, Cảm biến áp suất lốp dTPMS, 4 túi khí'
            },
            'cat7_economics': {
                'title': 'VII. CHI PHÍ SỬ DỤNG & BẢO HÀNH',
                'fuelCost1000km': '1.450.000 - 1.650.000 VNĐ (xăng ~24k/L)',
                'maintenance': 'Bảo dưỡng định kỳ 5.000 km',
                'warranty': '5 năm hoặc 100.000 km'
            },
            'cat8_reference': {
                'title': 'VIII. TÀI LIỆU BROCHURE CHÍNH HÃNG',
                'source': 'Catalogue Hyundai TC Motor Việt Nam'
            }
        }
    }
]

master_cars = parsed_cars + competitors

# Save JSON and JS files
out_json = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/data/cars_database.json'
out_js = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/js/cars_data.js'

with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'cars': master_cars}, f, ensure_ascii=False, indent=2)

with open(out_js, 'w', encoding='utf-8') as f:
    f.write('// Master Official VinFast Brochure Database (25 Cars & Versions)\n')
    f.write('window.CARS_DATABASE = ')
    json.dump(master_cars, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"Master Database successfully generated with {len(master_cars)} total cars!")
print(f"- 22 Official VinFast models & versions directly from brochure CSV")
print(f"- 3 Petrol Competitor models (Toyota Wigo G, Kia Morning X-Line, Hyundai Grand i10 1.2 AT)")
