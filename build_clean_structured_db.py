# -*- coding: utf-8 -*-
"""
Intelligent Parser & Cleaner for VinFast Official Brochure Data.
Breaks down conglomerate text fields into atomic, structured specifications.
Splits multi-item features into clean, readable lists.
"""
import csv
import json
import os
import re
import sys

csv_file = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/data/vinfast_official_brochure_specs.csv'
raw_db_file = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-baogia/data_da_bo_sung_phu_kien_combo.json'

vinfast_raw = []
if os.path.exists(raw_db_file):
    with open(raw_db_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        vinfast_raw = data.get('cars', [])

vf_raw_map = {}
for c in vinfast_raw:
    v = c.get('version', '').strip().upper()
    vf_raw_map[v] = c
    if c.get('standardName'):
        vf_raw_map[c.get('standardName').strip().upper()] = c

COLOR_HEX = {
    'Trắng': '#F8FAFC', 'Infinity Blanc': '#F8FAFC', 'Brahminy White': '#F8FAFC',
    'Xám': '#64748B', 'Zenith Grey': '#64748B', 'Neptune Grey': '#475569', 'Xám Đậm': '#334155',
    'Bạc': '#CBD5E1', 'Desat Silver': '#CBD5E1',
    'Đen': '#0F172A', 'Jet Black': '#0F172A',
    'Đỏ': '#DC2626', 'Crimson Red': '#DC2626',
    'Vàng': '#F59E0B', 'Summer Yellow': '#F59E0B',
    'Cam': '#EA580C', 'Sunset Orange': '#EA580C',
    'Hồng': '#F472B6', 'Iris Berry': '#C084FC',
    'Xanh Lá': '#16A34A', 'Urban Mint': '#34D399',
    'Xanh': '#2563EB', 'VinFast Blue': '#2563EB', 'Electric Blue': '#38BDF8',
    'Aquatic Azure': '#0EA5E9', 'Deep Ocean': '#047857', 'Nâu': '#78350F',
    'Cam Nóc Đen': '#EA580C', 'Tím': '#7C3AED', 'Vàng Nóc Đen': '#F59E0B',
    'Xanh Nóc Trắng': '#0284C7', 'Vàng Nóc Trắng': '#F59E0B', 'Hồng Nóc Trắng': '#F472B6',
    'Đỏ Nóc Đen': '#DC2626', 'Cam Nóc Trắng': '#EA580C', 'Đen Nóc Trắng': '#0F172A'
}

def get_colors(raw_key):
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
        img = raw.get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/vf5/xe-dien-vinfast-vf-5-plus-thiet-ke-ngoai-that-mau-trang-desktop.webp'
        return [
            {'name': 'Trắng (Infinity Blanc)', 'hex': '#F8FAFC', 'image': img},
            {'name': 'Xám (Zenith Grey)', 'hex': '#64748B', 'image': img},
            {'name': 'Đỏ (Crimson Red)', 'hex': '#DC2626', 'image': img},
            {'name': 'Đen (Jet Black)', 'hex': '#0F172A', 'image': img}
        ]
    return res

OFFICIAL_CAR_META = {
    'VinFast VF 3 Eco': {'id': 'vf3_eco', 'shortName': 'VF 3 Eco', 'segment': 'Minicar (Mini SUV Đô thị)', 'price': 285000000, 'priceText': '285.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 900.000 đ/tháng | Kèm pin: 322 tr', 'raw_key': 'VF3 ECO', 'badgeColor': 'yellow'},
    'VinFast VF 3 Plus': {'id': 'vf3_plus', 'shortName': 'VF 3 Plus', 'segment': 'Minicar (Mini SUV Đô thị)', 'price': 296000000, 'priceText': '296.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 900.000 đ/tháng | Kèm pin: 333 tr', 'raw_key': 'VF3 PLUS', 'badgeColor': 'yellow'},
    'VinFast VF 5 Plus': {'id': 'vf5_plus', 'shortName': 'VF 5 Plus', 'segment': 'Hạng A (A-SUV Đô thị)', 'price': 496000000, 'priceText': '496.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 1.200.000 đ/tháng | Kèm pin: 576 tr', 'raw_key': 'VF5', 'badgeColor': 'blue'},
    'VF 6 Eco': {'id': 'vf6_eco', 'shortName': 'VF 6 Eco', 'segment': 'Hạng B (B-SUV Đô thị)', 'price': 646000000, 'priceText': '646.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 1.800.000 đ/tháng | Kèm pin: 736 tr', 'raw_key': 'VF6 ECO', 'badgeColor': 'emerald'},
    'VF 6 Plus': {'id': 'vf6_plus', 'shortName': 'VF 6 Plus', 'segment': 'Hạng B (B-SUV Đô thị)', 'price': 699000000, 'priceText': '699.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 1.800.000 đ/tháng | Kèm pin: 789 tr', 'raw_key': 'VF6 PLUS', 'badgeColor': 'emerald'},
    'VinFast VF 7 Eco': {'id': 'vf7_eco', 'shortName': 'VF 7 Eco', 'segment': 'Hạng C (C-SUV Thể thao)', 'price': 740000000, 'priceText': '740.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng | Kèm pin: 850 tr', 'raw_key': 'VF7 ECO', 'badgeColor': 'purple'},
    'VinFast VF 7 Plus': {'id': 'vf7_plus_fwd', 'shortName': 'VF 7 Plus (FWD)', 'segment': 'Hạng C (C-SUV Thể thao)', 'price': 830000000, 'priceText': '830.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng | Kèm pin: 940 tr', 'raw_key': 'VF7 PLUS TC2 - TRẦN THÉP', 'badgeColor': 'purple'},
    'VinFast VF 7 Plus AWD': {'id': 'vf7_plus_awd', 'shortName': 'VF 7 Plus AWD', 'segment': 'Hạng C (C-SUV Thể thao)', 'price': 880000000, 'priceText': '880.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng | Kèm pin: 990 tr', 'raw_key': 'VF7 PLUS TC2 - TRẦN THÉP', 'badgeColor': 'purple'},
    'VF 8 Eco': {'id': 'vf8_eco_catl', 'shortName': 'VF 8 Eco (CATL)', 'segment': 'Hạng D (D-SUV Toàn cầu)', 'price': 898000000, 'priceText': '898.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng | Kèm pin: 1.019 tr', 'raw_key': 'VF8 ECO TIÊU CHUẨN 1 - 1 CẦU', 'badgeColor': 'sky'},
    'VF 8 Plus': {'id': 'vf8_plus_catl', 'shortName': 'VF 8 Plus (CATL)', 'segment': 'Hạng D (D-SUV Toàn cầu)', 'price': 1079000000, 'priceText': '1.079.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng | Kèm pin: 1.199 tr', 'raw_key': 'VF8 PLUS TIÊU CHUẨN 1 - 2 CẦU', 'badgeColor': 'sky'},
    'VinFast VF 8 Thế hệ mới': {'id': 'vf8_the_he_moi', 'shortName': 'VF 8 Thế Hệ Mới', 'segment': 'Hạng D (D-SUV Cải tiến)', 'price': 899000000, 'priceText': '899.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng | Kèm pin: 1.099 tr', 'raw_key': 'VF8 ALL NEW', 'badgeColor': 'sky'},
    'VinFast VF 9 Eco': {'id': 'vf9_eco_catl', 'shortName': 'VF 9 Eco (CATL)', 'segment': 'Hạng E (Full-size Luxury)', 'price': 1348000000, 'priceText': '1.348.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 3.900.000 đ/tháng | Kèm pin: 1.589 tr', 'raw_key': 'VF9 ECO', 'badgeColor': 'rose'},
    'VinFast VF 9 Plus': {'id': 'vf9_plus_catl', 'shortName': 'VF 9 Plus (Chủ tịch)', 'segment': 'Hạng E (Full-size Luxury)', 'price': 1529000000, 'priceText': '1.529.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 3.900.000 đ/tháng | Kèm pin: 1.789 tr', 'raw_key': 'VF9 PLUS', 'badgeColor': 'rose'},
    'VinFast Minio Green': {'id': 'minio_green', 'shortName': 'Minio Green', 'segment': 'Minicar Dịch vụ Đô thị', 'price': 188000000, 'priceText': '188.000.000 VNĐ', 'batteryFeeText': 'Chính sách xe điện thương mại Green', 'raw_key': 'MINIO GREEN', 'badgeColor': 'emerald'},
    'VinFast Herio Green': {'id': 'herio_green', 'shortName': 'Herio Green', 'segment': 'Hạng A (Đô thị / Dịch vụ)', 'price': 450000000, 'priceText': '450.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 1.200.000 đ/tháng', 'raw_key': 'HERIO GREEN', 'badgeColor': 'emerald'},
    'VinFast Limo Green': {'id': 'limo_green', 'shortName': 'Limo Green', 'segment': 'Dịch vụ VIP 7 Chỗ', 'price': 699000000, 'priceText': '699.000.000 VNĐ', 'batteryFeeText': 'Chính sách Xanh SM Luxury', 'raw_key': 'LIMO GREEN', 'badgeColor': 'emerald'},
    'VinFast VF MPV7': {'id': 'vf_mpv7', 'shortName': 'VF MPV 7', 'segment': 'MPV Đa dụng 7 Chỗ', 'price': 750000000, 'priceText': '750.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 2.100.000 đ/tháng', 'raw_key': 'VF MVP 7', 'badgeColor': 'teal'},
    'VinFast VF 2': {'id': 'vf2', 'shortName': 'VF 2', 'segment': 'Minicar Đô thị', 'price': 188000000, 'priceText': '188.000.000 VNĐ', 'batteryFeeText': 'Thuê pin: 600.000 đ/tháng | Kèm pin: 248 tr', 'raw_key': 'VF 2', 'badgeColor': 'yellow'},
    'VinFast EC VAN (Bản tiêu chuẩn / Tiêu chuẩn)': {'id': 'ec_van_standard', 'shortName': 'EC Van Tiêu Chuẩn', 'segment': 'Xe Tải Van Đô thị', 'price': 248000000, 'priceText': '248.000.000 VNĐ', 'batteryFeeText': 'Chính sách sạc & thuê pin thương mại', 'raw_key': 'EC VAN TIÊU CHUẨN', 'badgeColor': 'amber'},
    'VinFast EC VAN - Phiên bản Nâng cao': {'id': 'ec_van_advanced', 'shortName': 'EC Van Nâng Cao', 'segment': 'Xe Tải Van Đô thị', 'price': 286000000, 'priceText': '286.000.000 VNĐ', 'batteryFeeText': 'Chính sách sạc & thuê pin thương mại', 'raw_key': 'EC VAN NÂNG CAO', 'badgeColor': 'amber'},
    'VinFast EC VAN - Phiên bản Nâng cao có cửa trượt': {'id': 'ec_van_sliding', 'shortName': 'EC Van Cửa Trượt', 'segment': 'Xe Tải Van Đô thị', 'price': 306000000, 'priceText': '306.000.000 VNĐ', 'batteryFeeText': 'Chính sách sạc & thuê pin thương mại', 'raw_key': 'EC VAN NÂNG CAO (Cửa trượt)', 'badgeColor': 'amber'},
    'VinFast VF Wild': {'id': 'vf_wild', 'shortName': 'VF Wild (EREV)', 'segment': 'Bán Tải Cỡ Trung Đột Phá', 'price': 860000000, 'priceText': '860.000.000 VNĐ (Dự kiến)', 'batteryFeeText': 'Công nghệ mở rộng tầm vận hành EREV', 'raw_key': 'VF WILD COMFORT', 'badgeColor': 'orange'}
}

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

def clean_extract(pattern, text, default='—'):
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        return default
    for g in m.groups():
        if g is not None:
            return g.strip()
    return default

# Clean smart line-split: avoids splitting inside parentheses
def smart_split(text):
    if not text or text == '—' or text == 'Chưa công bố':
        return []
    return [p.strip() for p in re.split(r';(?![^\(]*\))', text) if p.strip()]

parsed_cars = []

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        model_name = row.get('Dòng xe / Phiên bản', '').strip()
        if not model_name or model_name == 'Index' or model_name.isdigit():
            continue

        meta = OFFICIAL_CAR_META.get(model_name)
        if not meta:
            for k, m in OFFICIAL_CAR_META.items():
                if k.lower() in model_name.lower():
                    meta = m
                    break
        if not meta:
            continue

        ref_code = row.get('Nguồn', '').strip()
        ref_text = BROCHURE_REFS.get(ref_code, f'Brochure #{ref_code}')

        dims_text = row.get('Kích thước & Trọng lượng', '').strip()
        engine_text = row.get('Hiệu suất & Động cơ', '').strip()
        battery_text = row.get('Pin & Sạc', '').strip()
        exterior_text = row.get('Ngoại thất', '').strip()
        interior_text = row.get('Nội thất & Tiện nghi', '').strip()
        safety_text = row.get('Tính năng an toàn & An ninh', '').strip()

        # 1. Dimensions
        d_r_c = clean_extract(r'Kích thước(?:\s*xe)?\s*\((?:D\s*x\s*R\s*x\s*C)\):\s*([^;]+)', dims_text)
        if d_r_c == '—' and dims_text.startswith('Kích thước'):
            d_r_c = dims_text.split(';')[0].replace('Kích thước (D x R x C):', '').strip()
        wheelbase = clean_extract(r'Chiều dài cơ sở:\s*([^;]+)', dims_text)
        ground_clearance = clean_extract(r'Khoảng sáng gầm xe(?: không tải)?:\s*([^;]+)', dims_text)
        turning_radius = clean_extract(r'Bán kính quay (?:đầu|vòng)(?: tối thiểu)?:\s*([^;]+)', dims_text)
        weight = clean_extract(r'Trọng lượng không tải:\s*([^;]+)', dims_text)
        payload = clean_extract(r'Tải trọng:\s*([^;]+)', dims_text)
        trunk = clean_extract(r'Dung tích (?:khoang hành lý|cốp xe|khoang chứa hành lý)[^:]*:\s*([^;]+)', dims_text)
        cargo_bed = clean_extract(r'(?:Kích thước khoang hàng|Kích thước thùng xe):\s*([^;]+)', dims_text)

        # 2. Performance & Engine
        engine_type = clean_extract(r'(?:Động cơ|motor|Loại động cơ):\s*([^;]+)', engine_text)
        drivetrain = clean_extract(r'Dẫn động:\s*([^;]+)', engine_text)
        max_power = clean_extract(r'Công suất tối đa:\s*([^;]+)', engine_text)
        max_torque = clean_extract(r'Mô-men xoắn (?:cực đại|tối đa):\s*([^;]+)', engine_text)
        acceleration = clean_extract(r'Tăng tốc 0[–-]100 km/h:\s*([^;]+)', engine_text)
        max_speed = clean_extract(r'(?:Tốc độ tối đa|Vận tốc tối đa):\s*([^;]+)', engine_text)
        drive_modes = clean_extract(r'Chế độ lái:\s*([^;]+)', engine_text)
        suspension = clean_extract(r'Hệ thống treo[^:]*:\s*([^;]+)', engine_text)
        water_wading = clean_extract(r'Khả năng lội nước:\s*([^;]+)', engine_text)

        # 3. Battery & Charging
        battery_type = clean_extract(r'Loại pin:\s*([^;]+)|Pin\s*([^;]+)', battery_text)
        battery_cap = clean_extract(r'Dung lượng pin(?: khả dụng)?:\s*([^;]+)', battery_text)
        range_val = clean_extract(r'Quãng đường (?:di chuyển|chạy)[^:]*:\s*([^;]+)', battery_text)
        fast_charge = clean_extract(r'Thời gian (?:nạp|sạc) pin nhanh nhất[^:]*:\s*([^;]+)', battery_text)
        ac_charge = clean_extract(r'Công suất sạc AC tối đa:\s*([^;]+)', battery_text)
        dc_charge = clean_extract(r'Công suất sạc(?: nhanh)? DC tối đa:\s*([^;]+)', battery_text)
        regen = clean_extract(r'Hệ thống phanh tái sinh:\s*([^;]+)|Phanh tái sinh:\s*([^;]+)', battery_text)
        v2l = 'Có hỗ trợ (Vehicle-to-Load)' if 'V2L' in battery_text else 'Không áp dụng'

        # 4. Exterior breakdown with smart split
        exterior_items = smart_split(exterior_text)
        headlights = '—'
        wheels = '—'
        mirrors = '—'
        wipers = '—'
        tailgate = '—'

        for p in exterior_items:
            p_low = p.lower()
            if any(k in p_low for k in ['đèn pha', 'đèn chiếu sáng', 'đèn trước', 'cụm đèn']):
                if headlights == '—':
                    headlights = re.sub(r'^(?:Cụm đèn trước|Đèn chiếu sáng phía trước|Đèn chiếu sáng|Đèn pha|Đèn trước)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            elif any(k in p_low for k in ['mâm', 'lốp', 'lazang', 'la-zăng', 'vành']):
                if wheels == '—':
                    wheels = re.sub(r'^(?:Mâm/Lốp|Mâm & Lốp|Lazang|Vành mâm xe|La-zăng|Kích thước lốp|Kích thước la-zăng|Mâm xe|Bánh xe)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            elif 'gương chiếu hậu' in p_low or 'gương ngoài' in p_low:
                if mirrors == '—':
                    mirrors = re.sub(r'^(?:Gương chiếu hậu ngoài|Gương chiếu hậu|Gương ngoài)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            elif 'gạt mưa' in p_low:
                if wipers == '—':
                    wipers = re.sub(r'^(?:Gạt mưa trước|Gạt mưa kính trước|Gạt mưa)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            elif any(k in p_low for k in ['cốp sau', 'cửa cốp', 'đóng/mở cốp']):
                if tailgate == '—':
                    tailgate = re.sub(r'^(?:Đóng/mở cốp sau|Cửa cốp sau|Cốp sau|Cốp điện)[:\s-]*', '', p, flags=re.IGNORECASE).strip()

        # Fallbacks for exterior if not caught by loop
        if headlights == '—':
            headlights = clean_extract(r'Đèn (?:chiếu sáng phía trước|pha|chiếu sáng LED):\s*([^;]+)', exterior_text)
        if wheels == '—':
            wheels = clean_extract(r'(?:Mâm/Lốp|Lazang|Vành mâm xe|La-zăng|Kích thước lốp|Kích thước la-zăng):\s*([^;]+)', exterior_text)
        if mirrors == '—':
            mirrors = clean_extract(r'Gương chiếu hậu[^:]*:\s*([^;]+)', exterior_text)

        # 5. Interior breakdown with smart split
        interior_items = smart_split(interior_text)
        seating = '—'
        front_seats = '—'
        rear_seats = '—'
        infotainment = '—'
        sound = '—'
        climate = '—'
        shifter = '—'

        for p in interior_items:
            p_low = p.lower()
            if 'số chỗ ngồi' in p_low or re.search(r'\d+\s*chỗ', p_low):
                if seating == '—':
                    seating = re.sub(r'^(?:Số chỗ ngồi|Số chỗ)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            if 'ghế lái' in p_low:
                if front_seats == '—':
                    front_seats = p
            if any(k in p_low for k in ['hàng ghế 2', 'hàng ghế thứ 2', 'hàng ghế sau', 'ghế vip']):
                if rear_seats == '—':
                    rear_seats = p
            if any(k in p_low for k in ['màn hình giải trí', 'màn hình cảm ứng', 'màn hình thông tin']):
                if infotainment == '—':
                    infotainment = re.sub(r'^(?:Màn hình giải trí cảm ứng|Màn hình giải trí|Màn hình cảm ứng|Màn hình trung tâm)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            if any(k in p_low for k in ['hệ thống âm thanh', 'loa']):
                if sound == '—':
                    sound = re.sub(r'^(?:Hệ thống âm thanh|Hệ thống loa|Âm thanh|Loa)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            if 'điều hòa' in p_low:
                if climate == '—':
                    climate = re.sub(r'^(?:Hệ thống điều hòa không khí|Hệ thống điều hòa|Điều hòa không khí|Điều hòa)[:\s-]*', '', p, flags=re.IGNORECASE).strip()
            if any(k in p_low for k in ['cần chuyển số', 'cần số', 'phanh đỗ điện tử', 'phanh tay']):
                if shifter == '—':
                    shifter = p

        # Fallbacks for interior
        if seating == '—':
            seating = clean_extract(r'Số chỗ ngồi:\s*([^;]+)|(\d+\s*chỗ[^;]*)', interior_text)
        if front_seats == '—':
            front_seats = clean_extract(r'(Ghế lái[^;]+)', interior_text)
        if rear_seats == '—':
            rear_seats = clean_extract(r'(Hàng ghế [23][^;]+|Ghế VIP[^;]+)', interior_text)
        if climate == '—':
            climate = clean_extract(r'(?:Hệ thống điều hòa|Điều hòa)[^:]*:\s*([^;]+)', interior_text)

        hud = 'Có (Màn hình HUD kính lái)' if ('Màn hình HUD: Có' in interior_text or 'màn hình HUD' in interior_text.lower()) and 'Không' not in clean_extract(r'Màn hình HUD:\s*([^;]+)', interior_text) else 'Không có'

        # 6. Safety & Security
        airbags = clean_extract(r'(\d+\s*túi khí[^;]*|1 túi khí[^;]*|2 túi khí[^;]*|4 túi khí[^;]*|6 túi khí[^;]*|7 túi khí[^;]*|10 túi khí[^;]*|11 túi khí[^;]*)', safety_text)
        if airbags == '—' and 'túi khí' in safety_text.lower():
            airbags = clean_extract(r'Túi khí[^:]*:\s*([^;]+)', safety_text)
        
        raw_safety_parts = smart_split(safety_text)
        standard_safety = '—'
        safety_parts = []
        adas_raw = clean_extract(r'(?:ADAS[^:]*|Trợ lái[^:]*):\s*([^;]+)', safety_text)

        for p in raw_safety_parts:
            p_low = p.lower()
            if any(k in p for k in ['ABS', 'EBD', 'ESC', 'TCS', 'HSA', 'phanh đĩa']):
                if standard_safety == '—':
                    standard_safety = p
            # Exclude redundant mega-ADAS strings from general safety list
            if not p_low.startswith('adas') and not p_low.startswith('trợ lái'):
                safety_parts.append(p)

        adas_items = []
        if adas_raw != '—':
            adas_items = [a.strip() for a in adas_raw.split(',') if a.strip()]
        elif 'Cruise Control' in interior_text or 'Ga tự động' in interior_text or 'Cruise Control' in safety_text:
            adas_items = ['Ga tự động (Cruise Control)']

        # Image & colors
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

        # Highlights
        highlights = [
            f"Công suất: {max_power}" if max_power != '—' else "Hiệu suất mạnh mẽ",
            f"Tầm sạc: {range_val}" if range_val != '—' else "Sạc nhanh tiện lợi",
            f"Kích thước: {d_r_c}" if d_r_c != '—' else "Không gian tối ưu"
        ]

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
            'badgeColor': meta['badgeColor'],
            'highlights': highlights,
            'brochureRef': ref_text,
            'radar': {
                'power': radar_power,
                'space': 88 if '7 chỗ' in dims_text or 'Full-size' in meta['segment'] else (60 if '3.190' in dims_text or '3.090' in dims_text else 80),
                'range': radar_range,
                'safety': 95 if ('11 túi' in airbags or '7 túi' in airbags) else (80 if ('6 túi' in airbags or '4 túi' in airbags) else 65),
                'tech': 95 if adas_items and len(adas_items) > 3 else 75,
                'economy': 98 if is_ev else 90
            },
            'specs': {
                'cat1_dimensions': {
                    'title': 'I. KÍCH THƯỚC & TRỌNG LƯỢNG',
                    'd_r_c': d_r_c,
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
                    'title': 'III. PIN & SẠC ĐIỆN',
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
                    'exteriorList': exterior_items
                },
                'cat5_interior': {
                    'title': 'V. NỘI THẤT & TIỆN NGHI',
                    'seating': seating,
                    'frontSeats': front_seats,
                    'rearSeats': rear_seats,
                    'infotainment': infotainment,
                    'hud': hud,
                    'sound': sound,
                    'climate': climate,
                    'shifter': shifter,
                    'interiorList': interior_items
                },
                'cat6_safety': {
                    'title': 'VI. AN TOÀN TIÊU CHUẨN',
                    'airbags': airbags,
                    'standardSafety': standard_safety,
                    'safetyList': safety_parts
                },
                'cat7_adas': {
                    'title': 'VII. HỆ THỐNG TRỢ LÁI NÂNG CAO (ADAS)',
                    'adasSummary': f"{len(adas_items)} tính năng trợ lái" if adas_items else 'Cơ bản',
                    'adasList': adas_items
                },
                'cat8_economics': {
                    'title': 'VIII. CHI PHÍ VẬN HÀNH & BẢO HÀNH',
                    'fuelCost1000km': '300.000 - 450.000 VNĐ' if is_ev else '650.000 VNĐ (sạc + xăng)',
                    'maintenance': 'Bảo dưỡng định kỳ 12.000 km/lần, chi phí cực thấp',
                    'warranty': '7 - 10 năm hoặc 160.000 - 200.000 km (Bảo hành pin tới 10 năm)'
                },
                'cat9_reference': {
                    'title': 'IX. TÀI LIỆU BROCHURE CHÍNH HÃNG',
                    'source': ref_text
                }
            }
        }
        parsed_cars.append(car_obj)

# Competitor benchmark cars
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
        'batteryFeeText': 'Không áp dụng (Xe xăng đốt trong)',
        'fuelType': 'Xăng (Đốt trong)',
        'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
        'colors': [
            {'name': 'Đỏ', 'hex': '#DC2626', 'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Trắng', 'hex': '#F8FAFC', 'image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Cam', 'hex': '#EA580C', 'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'}
        ],
        'badgeColor': 'rose',
        'highlights': ['Đèn trước Full LED', 'Vòng quay 4.5m luồn lách', 'Động cơ 1.2L 3 xi-lanh', 'Hộp số D-CVT'],
        'brochureRef': 'Catalogue Toyota Wigo 2024-2026',
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
                'title': 'III. PIN & SẠC ĐIỆN',
                'batteryType': 'Không áp dụng (Bình xăng 36 L)',
                'batteryCapacity': 'Bình xăng 36 L',
                'range': '~550 - 650 km / bình xăng',
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
                'exteriorList': ['Đèn trước full LED phản xạ đa hướng', 'Mâm hợp kim 14 inch', 'Gương gập điện tự động', 'Đèn hậu LED']
            },
            'cat5_interior': {
                'title': 'V. NỘI THẤT & TIỆN NGHI',
                'seating': '5 chỗ ngồi (ghế nỉ)',
                'frontSeats': 'Ghế lái chỉnh cơ 4 hướng',
                'rearSeats': 'Gập nguyên băng ghế',
                'infotainment': 'Màn hình cảm ứng 7 inch',
                'hud': 'Không có',
                'sound': '4 loa',
                'climate': 'Điều hòa chỉnh điện (màn hình LCD)',
                'shifter': 'Cần số cơ khí D-CVT',
                'interiorList': ['Màn hình 7 inch', 'Khởi động nút bấm Start/Stop', 'Điều hòa hiển thị số', 'Ghế nỉ thể thao']
            },
            'cat6_safety': {
                'title': 'VI. AN TOÀN TIÊU CHUẨN',
                'airbags': '2 túi khí',
                'standardSafety': 'ABS, EBD, BA, VSC cân bằng điện tử, TRC',
                'safetyList': ['2 túi khí phía trước', 'Hệ thống phanh ABS / EBD / BA', 'Cân bằng điện tử VSC', 'Hỗ trợ khởi hành ngang dốc HAC', 'Camera lùi & Cảm biến lùi']
            },
            'cat7_adas': {
                'title': 'VII. HỆ THỐNG TRỢ LÁI NÂNG CAO (ADAS)',
                'adasSummary': '2 tính năng hỗ trợ',
                'adasList': ['Cảnh báo điểm mù (BSM)', 'Cảnh báo phương tiện cắt ngang khi lùi (RCTA)']
            },
            'cat8_economics': {
                'title': 'VIII. CHI PHÍ VẬN HÀNH & BẢO HÀNH',
                'fuelCost1000km': '1.300.000 - 1.500.000 VNĐ (xăng ~24k/L)',
                'maintenance': 'Bảo dưỡng định kỳ 5.000 km/lần',
                'warranty': '3 năm hoặc 100.000 km'
            },
            'cat9_reference': {
                'title': 'IX. TÀI LIỆU BROCHURE CHÍNH HÃNG',
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
        'batteryFeeText': 'Không áp dụng (Xe xăng đốt trong)',
        'fuelType': 'Xăng (Đốt trong)',
        'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80',
        'colors': [
            {'name': 'Đỏ', 'hex': '#DC2626', 'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Vàng', 'hex': '#F59E0B', 'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Trắng', 'hex': '#F8FAFC', 'image': 'https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80'}
        ],
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
                'title': 'III. PIN & SẠC ĐIỆN',
                'batteryType': 'Không áp dụng (Bình xăng 35 L)',
                'batteryCapacity': 'Bình xăng 35 L',
                'range': '~450 - 550 km / bình xăng',
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
                'exteriorList': ['Gói ốp việt dã X-Line', 'Đèn Halogen Projector thấu kính', 'Mâm đúc hợp kim 15 inch', 'Đèn sương mù']
            },
            'cat5_interior': {
                'title': 'V. NỘI THẤT & TIỆN NGHI',
                'seating': '5 chỗ (ghế da 2 tông màu)',
                'frontSeats': 'Ghế lái chỉnh cơ 6 hướng',
                'rearSeats': 'Gập 60:40',
                'infotainment': 'Màn hình cảm ứng 8 inch',
                'hud': 'Không có',
                'sound': '6 loa',
                'climate': 'Điều hòa tự động',
                'shifter': 'Cần số cơ zíc zắc',
                'interiorList': ['Ghế da phối viền chỉ màu', 'Điều hòa tự động', 'Màn hình nổi 8 inch', 'Chìa khóa thông minh']
            },
            'cat6_safety': {
                'title': 'VI. AN TOÀN TIÊU CHUẨN',
                'airbags': '2 túi khí',
                'standardSafety': 'ABS, EBD, ESC, HAC khởi hành ngang dốc',
                'safetyList': ['2 túi khí phía trước', 'Chống bó cứng phanh ABS', 'Phân phối lực phanh điện tử EBD', 'Cân bằng điện tử ESC', 'Hỗ trợ khởi hành ngang dốc HAC', 'Camera lùi & Cảm biến lùi']
            },
            'cat7_adas': {
                'title': 'VII. HỆ THỐNG TRỢ LÁI NÂNG CAO (ADAS)',
                'adasSummary': 'Cơ bản',
                'adasList': []
            },
            'cat8_economics': {
                'title': 'VIII. CHI PHÍ VẬN HÀNH & BẢO HÀNH',
                'fuelCost1000km': '1.400.000 - 1.600.000 VNĐ (xăng ~24k/L)',
                'maintenance': 'Bảo dưỡng định kỳ 5.000 km/lần',
                'warranty': '3 năm không giới hạn km'
            },
            'cat9_reference': {
                'title': 'IX. TÀI LIỆU BROCHURE CHÍNH HÃNG',
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
        'batteryFeeText': 'Không áp dụng (Xe xăng đốt trong)',
        'fuelType': 'Xăng (Đốt trong)',
        'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80',
        'colors': [
            {'name': 'Trắng', 'hex': '#F8FAFC', 'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Đỏ', 'hex': '#DC2626', 'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Bạc', 'hex': '#CBD5E1', 'image': 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80'}
        ],
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
                'title': 'III. PIN & SẠC ĐIỆN',
                'batteryType': 'Không áp dụng (Bình xăng 37 L)',
                'batteryCapacity': 'Bình xăng 37 L',
                'range': '~480 - 580 km / bình xăng',
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
                'exteriorList': ['Đèn LED định vị ban ngày dạng Boomerang', 'Mâm phay xước thể thao 15 inch', 'Gương gập điện tích hợp báo rẽ']
            },
            'cat5_interior': {
                'title': 'V. NỘI THẤT & TIỆN NGHI',
                'seating': '5 chỗ (ghế nỉ viền chỉ đỏ)',
                'frontSeats': 'Ghế lái chỉnh cơ 6 hướng',
                'rearSeats': 'Gập 60:40, có cửa gió điều hòa riêng',
                'infotainment': 'Màn hình cảm ứng 8 inch (Apple CarPlay/Android Auto)',
                'hud': 'Không có',
                'sound': '4 loa',
                'climate': 'Điều hòa chỉnh cơ + Cửa gió điều hòa hàng ghế sau',
                'shifter': 'Cần số tự động 4 cấp',
                'interiorList': ['Cửa gió điều hòa hàng ghế 2 độc nhất phân khúc A', 'Màn hình 8 inch hỗ trợ Apple CarPlay', 'Ga tự động Cruise Control tích hợp vô lăng']
            },
            'cat6_safety': {
                'title': 'VI. AN TOÀN TIÊU CHUẨN',
                'airbags': '4 túi khí',
                'standardSafety': 'ABS, EBD, BA, ESC, HAC, TPMS cảm biến áp suất lốp',
                'safetyList': ['4 túi khí an toàn', 'Cảm biến áp suất lốp dTPMS', 'Phanh ABS, EBD, BA', 'Cân bằng điện tử ESC', 'Hỗ trợ khởi hành ngang dốc HAC', 'Camera lùi & Cảm biến lùi']
            },
            'cat7_adas': {
                'title': 'VII. HỆ THỐNG TRỢ LÁI NÂNG CAO (ADAS)',
                'adasSummary': 'Ga tự động Cruise Control',
                'adasList': ['Ga tự động (Cruise Control)']
            },
            'cat8_economics': {
                'title': 'VIII. CHI PHÍ VẬN HÀNH & BẢO HÀNH',
                'fuelCost1000km': '1.450.000 - 1.650.000 VNĐ (xăng ~24k/L)',
                'maintenance': 'Bảo dưỡng định kỳ 5.000 km/lần',
                'warranty': '5 năm hoặc 100.000 km'
            },
            'cat9_reference': {
                'title': 'IX. TÀI LIỆU BROCHURE CHÍNH HÃNG',
                'source': 'Catalogue Hyundai TC Motor Việt Nam'
            }
        }
    }
]

master_cars = parsed_cars + competitors

out_json = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/data/cars_database.json'
out_js = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/js/cars_data.js'

with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({'cars': master_cars}, f, ensure_ascii=False, indent=2)

with open(out_js, 'w', encoding='utf-8') as f:
    f.write('// Master Official VinFast Brochure Database (Structured & Clean)\n')
    f.write('window.CARS_DATABASE = ')
    json.dump(master_cars, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"Clean database successfully written with {len(master_cars)} cars!")
