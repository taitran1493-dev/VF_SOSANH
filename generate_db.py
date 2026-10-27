# -*- coding: utf-8 -*-
"""
Script to generate cars_data.js and database.json for VinFast Smart Comparison App.
Includes comprehensive specifications, color variations, pricing, pros/cons, radar scores,
and category breakdowns.
"""
import json
import os
import shutil

src_json_path = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-baogia/data_da_bo_sung_phu_kien_combo.json'
uploaded_img_path = r'C:/Users/PC/.gemini/antigravity/brain/1e80d419-e01f-4ebc-8a77-b069525ba658/.user_uploaded/media_1793091166775_7da96cda.jpg'
dest_assets_dir = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/assets'
os.makedirs(dest_assets_dir, exist_ok=True)

# Copy uploaded strip
dest_uploaded_img = os.path.join(dest_assets_dir, 'vinfast_lineup_strip.jpg')
if os.path.exists(uploaded_img_path):
    shutil.copy2(uploaded_img_path, dest_uploaded_img)

# Load existing rich vinfast-baogia database
vinfast_raw = []
if os.path.exists(src_json_path):
    with open(src_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        vinfast_raw = data.get('cars', [])

# Map of raw cars by version/standardName
vf_map = {}
for c in vinfast_raw:
    key = c.get('version', '').strip().upper()
    vf_map[key] = c
    if c.get('standardName'):
        vf_map[c.get('standardName').strip().upper()] = c

print(f"Loaded {len(vinfast_raw)} cars from raw vinfast dataset.")

# Colors hex map for UI color badges
COLOR_HEX = {
    'Trắng': '#F8FAFC',
    'Xám': '#64748B',
    'Xám Đậm': '#334155',
    'Bạc': '#CBD5E1',
    'Đen': '#0F172A',
    'Đỏ': '#DC2626',
    'Vàng': '#F59E0B',
    'Cam': '#EA580C',
    'Hồng': '#F472B6',
    'Xanh Lá': '#16A34A',
    'Xanh': '#2563EB',
    'Xanh Da Trời': '#38BDF8',
    'Xanh Đại Dương': '#0284C7',
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

def get_color_list(c_dict):
    color_imgs = c_dict.get('colorImages') or {}
    res = []
    for c_name, c_url in color_imgs.items():
        res.append({
            'name': c_name,
            'hex': COLOR_HEX.get(c_name, '#94A3B8'),
            'image': c_url
        })
    return res

# Build Master Comparison Database
cars_list = [
    # 1. VINFAST HERIO GREEN (From user prompt)
    {
        'id': 'vinfast_herio_green',
        'name': 'VinFast Herio Green',
        'shortName': 'Herio Green',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Hạng A (Đô thị / Dịch vụ Green)',
        'category': 'Xe điện',
        'price': 450000000,
        'priceText': '450.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 1.200.000 đ/tháng hoặc Mua kèm pin',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('HERIO GREEN', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/herio-green/hinh-anh-xe-vinfast-herio-green-mau-trang.webp',
        'colors': get_color_list(vf_map.get('HERIO GREEN', {})),
        'tag': 'Tối ưu kinh doanh & Dịch vụ Xanh',
        'badgeColor': 'emerald',
        'highlights': [
            'Động cơ điện 134 HP cực bốc, gấp rưỡi xe xăng hạng A',
            '4 phanh đĩa trước/sau vượt trội chuẩn an toàn phân khúc',
            'Chi phí sạc điện siêu tiết kiệm chỉ ~400đ/km',
            'Bản tối ưu chi phí đầu tư cho gia đình trẻ và taxi công nghệ'
        ],
        'pros': [
            'Công suất mạnh mẽ 100 kW (134 HP) tăng tốc tức thì',
            'Chiều dài cơ sở 2.514 mm cho không gian ngồi rộng rãi',
            'Hệ thống phanh 4 đĩa an toàn hơn phanh tang trống',
            'Tiết kiệm chi phí bảo trì bảo dưỡng vượt trội'
        ],
        'cons': [
            'Mâm thép 16 inch (chưa phải mâm hợp kim thể thao)',
            'Chưa trang bị Cruise Control và Camera lùi nguyên bản',
            'Đèn pha halogen truyền thống'
        ],
        'radar': {
            'power': 85,
            'space': 80,
            'range': 75,
            'safety': 76,
            'tech': 70,
            'economy': 98
        },
        'specs': {
            'dimensions': {
                'd_r_c': '3.967 x 1.723 x 1.579 mm',
                'wheelbase': '2.514 mm',
                'groundClearance': '160 mm',
                'turningRadius': '5,25 m',
                'trunk': '260 L (gập ghế 900 L) - 331/1.015 L',
                'weight': '1.340 kg'
            },
            'powertrain': {
                'engineType': '1 Động cơ điện (Permanent Magnet)',
                'maxPower': '100 kW (134 HP)',
                'maxTorque': '135 Nm',
                'maxSpeed': '130 km/h',
                'batteryCapacity': 'LFP 37,23 kWh',
                'range': '326 km (chuẩn NEDC)',
                'acCharge': '6,6 kW (AC tại nhà)',
                'dcCharge': '~ 50 kW (Trạm sạc nhanh)',
                'fastChargeTime': '33 phút (0 - 70%)',
                'driveModes': '2 chế độ: Eco / Sport',
                'regenBraking': '2 chế độ: Cao / Thấp',
                'cooling': 'Làm mát pin bằng dung dịch nước'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Dầm xoắn',
                'brakes': 'Đĩa thông gió / Đĩa',
                'wheels': 'Mâm thép 16 inch (195/60R16)',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Dạng cơ',
                'shifter': 'Điện tử dạng núm xoay hiện đại'
            },
            'exteriorSafety': {
                'lighting': 'Halogen / Halogen',
                'lightFeatures': 'Đèn định vị Halogen',
                'mirrors': 'Chỉnh điện, tích hợp đèn báo rẽ',
                'windows': 'Chỉnh điện, lên/xuống 1 chạm cửa tài xế',
                'tailgate': 'Chỉnh cơ',
                'wipers': 'Chỉnh cơ gián đoạn',
                'cruiseControl': 'Không có',
                'parkingSensors': 'Không có',
                'rearCamera': 'Không có',
                'airbags': '2 túi khí an toàn',
                'adas': 'ABS, EBD, BA, ESC, TCS, HSA khởi hành ngang dốc'
            },
            'economics': {
                'fuelCost1000km': '400.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Cực thấp (không bugi, nhớt máy, lọc dầu)',
                'warranty': '7 năm hoặc 160.000 km'
            }
        }
    },

    # 2. VINFAST VF 5 PLUS (From user prompt)
    {
        'id': 'vinfast_vf5_plus',
        'name': 'VinFast VF 5 Plus',
        'shortName': 'VF 5 Plus',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Hạng A (A-SUV Đô thị)',
        'category': 'Xe điện',
        'price': 496000000,
        'priceText': '496.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 1.200.000 đ/tháng hoặc Kèm pin: 576.000.000 đ',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF5', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/vf5/xe-dien-vinfast-vf-5-plus-thiet-ke-ngoai-that-mau-trang-desktop.webp',
        'colors': get_color_list(vf_map.get('VF5', {})),
        'tag': 'Vua doanh số phân khúc A-SUV',
        'badgeColor': 'blue',
        'highlights': [
            'Trang bị đầy đủ Ga tự động Cruise Control & Cảm biến + Camera lùi',
            'Mâm hợp kim đúc thể thao 17 inch lớn nhất phân khúc',
            'Đèn pha tự động bật/tắt và đèn chờ dẫn đường thông minh',
            '6 túi khí an toàn vượt trội, phanh đĩa 4 bánh'
        ],
        'pros': [
            'Công suất 134 HP mạnh mẽ vượt xa các mẫu xe xăng cùng tầm giá',
            'Trang bị Cruise Control giúp đi cao tốc cực kỳ nhàn nhã',
            'Mâm đúc 17 inch tạo dáng xe SUV cơ bắp, tôn gầm cao 168mm',
            'Chi phí nuôi xe siêu hạt dẻ, sạc nhanh 33 phút'
        ],
        'cons': [
            'Đèn chiếu sáng chính vẫn là bóng Halogen (có thể nâng cấp LED)',
            'Cần làm quen với văn hóa sạc pin xe điện'
        ],
        'radar': {
            'power': 85,
            'space': 80,
            'range': 75,
            'safety': 88,
            'tech': 82,
            'economy': 96
        },
        'specs': {
            'dimensions': {
                'd_r_c': '3.967 x 1.723 x 1.579 mm',
                'wheelbase': '2.514 mm',
                'groundClearance': '160 - 168 mm',
                'turningRadius': '5,25 m',
                'trunk': '260 L (mở rộng 900 L) - 331/1.015 L',
                'weight': '1.340 kg'
            },
            'powertrain': {
                'engineType': '1 Động cơ điện (Permanent Magnet)',
                'maxPower': '100 kW (134 HP)',
                'maxTorque': '135 Nm',
                'maxSpeed': '130 km/h',
                'batteryCapacity': 'LFP 37,23 kWh',
                'range': '326 km (chuẩn NEDC)',
                'acCharge': '6,6 kW (AC)',
                'dcCharge': '~ 50 kW (DC Siêu nhanh)',
                'fastChargeTime': '33 phút (0 - 70%)',
                'driveModes': '2 chế độ: Eco / Sport',
                'regenBraking': '2 chế độ: Cao / Thấp',
                'cooling': 'Làm mát pin bằng dung dịch nước'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Dầm xoắn',
                'brakes': 'Đĩa thông gió / Đĩa',
                'wheels': 'Mâm hợp kim 17 inch (205/55R17)',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Dạng cơ',
                'shifter': 'Điện tử dạng núm xoay hiện đại'
            },
            'exteriorSafety': {
                'lighting': 'Halogen / Halogen',
                'lightFeatures': 'Tự động bật/tắt, đèn chờ dẫn đường, đèn định vị Halogen',
                'mirrors': 'Chỉnh điện, tích hợp đèn báo rẽ',
                'windows': 'Chỉnh điện, lên/xuống 1 chạm cửa tài xế',
                'tailgate': 'Chỉnh cơ',
                'wipers': 'Tự động / Chỉnh cơ',
                'cruiseControl': 'Có (Cruise Control tích hợp vô lăng)',
                'parkingSensors': 'Có (Cảm biến đỗ xe phía sau)',
                'rearCamera': 'Có (Camera lùi hiển thị màn hình 8 inch)',
                'airbags': '6 túi khí an toàn bảo vệ toàn diện',
                'adas': 'ABS, EBD, BA, ESC, TCS, HSA, Giám sát áp suất lốp'
            },
            'economics': {
                'fuelCost1000km': '400.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Rất thấp (bảo dưỡng 12.000 km/lần)',
                'warranty': '7 năm hoặc 160.000 km (Pin 8 năm không giới hạn km)'
            }
        }
    },

    # 3. TOYOTA WIGO G (From user prompt)
    {
        'id': 'toyota_wigo_g',
        'name': 'Toyota Wigo G',
        'shortName': 'Wigo G',
        'brand': 'Toyota',
        'origin': 'Nhập khẩu Indonesia',
        'segment': 'Hạng A (Hatchback Đô thị)',
        'category': 'Xe xăng',
        'price': 405000000,
        'priceText': '405.000.000 VNĐ',
        'batteryFeeText': 'Không áp dụng (Xe động cơ đốt trong)',
        'fuelType': 'Xăng (Đốt trong)',
        'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80',
        'colors': [
            {'name': 'Đỏ', 'hex': '#DC2626', 'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Trắng', 'hex': '#F8FAFC', 'image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Cam', 'hex': '#EA580C', 'image': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'},
            {'name': 'Bạc', 'hex': '#CBD5E1', 'image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80'}
        ],
        'tag': 'Hatchback nhập khẩu tiết kiệm xăng',
        'badgeColor': 'rose',
        'highlights': [
            'Hệ thống đèn trước full LED phản xạ đa hướng hiện đại',
            'Bán kính quay đầu cực nhỏ chỉ 4.5m xoay trở linh hoạt ngõ hẻm',
            'Động cơ 1.2L 3 xi-lanh tiết kiệm nhiên liệu ~5.2L/100km',
            'Hộp số D-CVT chuyển số êm ái'
        ],
        'pros': [
            'Đèn LED hiện đại hơn bóng Halogen của xe điện hạng A',
            'Bán kính vòng quay 4.5m luồn lách cực nhanh',
            'Thương hiệu Toyota giữ giá và hệ thống đại lý rộng khắp',
            'Trọng lượng xe nhẹ 890 kg giúp tiết kiệm xăng'
        ],
        'cons': [
            'Công suất chỉ 87 HP (yếu hơn nhiều so với 134 HP của VF5)',
            'Phanh sau tang trống (chưa được 4 phanh đĩa)',
            'Mâm lốp nhỏ chỉ 14 inch',
            'Không có Ga tự động Cruise Control'
        ],
        'radar': {
            'power': 55,
            'space': 70,
            'range': 85,
            'safety': 68,
            'tech': 62,
            'economy': 75
        },
        'specs': {
            'dimensions': {
                'd_r_c': '3.760 x 1.665 x 1.515 mm',
                'wheelbase': '2.525 mm',
                'groundClearance': '160 mm',
                'turningRadius': '4,50 m (rất linh hoạt)',
                'trunk': '261 L',
                'weight': '890 kg'
            },
            'powertrain': {
                'engineType': 'Động cơ xăng 1.2L 3 xi-lanh (Đốt trong)',
                'maxPower': '65 kW (87 HP) @ 6.000 rpm',
                'maxTorque': '113 Nm @ 4.500 rpm',
                'maxSpeed': '155 km/h',
                'batteryCapacity': 'Không áp dụng (Bình xăng 36 L)',
                'range': '~550 - 650 km / bình xăng đầy',
                'acCharge': 'Không áp dụng (Đổ xăng 3 phút)',
                'dcCharge': 'Không áp dụng',
                'fastChargeTime': 'Không áp dụng',
                'driveModes': 'Không có (D/S/B)',
                'regenBraking': 'Không áp dụng',
                'cooling': 'Két nước làm mát động cơ đốt trong'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Dầm xoắn',
                'brakes': 'Đĩa tản nhiệt / Tang trống',
                'wheels': 'Mâm hợp kim 14 inch (175/65R14)',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Dạng cơ cần kéo',
                'shifter': 'Cần số cơ khí truyền thống'
            },
            'exteriorSafety': {
                'lighting': 'LED phản xạ đa hướng / LED',
                'lightFeatures': 'Tự động bật/tắt',
                'mirrors': 'Chỉnh điện, gập điện, tích hợp đèn báo rẽ',
                'windows': 'Chỉnh điện, 1 chạm bên lái',
                'tailgate': 'Chỉnh cơ',
                'wipers': 'Chỉnh cơ gián đoạn',
                'cruiseControl': 'Không có',
                'parkingSensors': 'Có (Cảm biến lùi)',
                'rearCamera': 'Có (Camera lùi)',
                'airbags': '2 túi khí',
                'adas': 'ABS, EBD, BA, VSC, TRC, HAC, Cảnh báo điểm mù BSM'
            },
            'economics': {
                'fuelCost1000km': '1.300.000 - 1.500.000 VNĐ (xăng ~24k/L)',
                'maintenanceCost': 'Định kỳ 5.000 km (thay nhớt, lọc)',
                'warranty': '3 năm hoặc 100.000 km'
            }
        }
    },

    # 4. KIA MORNING X-LINE (From user prompt)
    {
        'id': 'kia_morning_xline',
        'name': 'Kia Morning X-Line',
        'shortName': 'Morning X-Line',
        'brand': 'Kia',
        'origin': 'Lắp ráp trong nước (Thaco)',
        'segment': 'Hạng A (Hatchback Đô thị)',
        'category': 'Xe xăng',
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
        'tag': 'Kiểu dáng cá tính, năng động cho phái đẹp',
        'badgeColor': 'amber',
        'highlights': [
            'Thiết kế gói ngoại thất X-Line phong cách việt dã cá tính',
            'Đèn pha Halogen Projector có thấu kính gom sáng tốt',
            'Nội thất ghế da phối màu thời trang, màn hình 8 inch',
            'Khởi động nút bấm Start/Stop và chìa khóa thông minh'
        ],
        'pros': [
            'Kích thước nhỏ gọn 3.595 mm cực dễ đỗ xe trong phố chật',
            'Thiết kế trẻ trung, màu sắc bắt mắt',
            'Trang bị điều hòa tự động và ghế da 2 tông màu',
            'Phụ tùng thay thế phong phú, dễ sửa chữa'
        ],
        'cons': [
            'Công suất chỉ 83 HP yếu nhất trong nhóm so sánh',
            'Không gian hàng ghế sau và cốp xe 255L khá khiêm tốn',
            'Phanh sau tang trống',
            'Không có Cruise Control'
        ],
        'radar': {
            'power': 52,
            'space': 62,
            'range': 80,
            'safety': 65,
            'tech': 66,
            'economy': 72
        },
        'specs': {
            'dimensions': {
                'd_r_c': '3.595 x 1.595 x 1.495 mm',
                'wheelbase': '2.400 mm',
                'groundClearance': '152 mm',
                'turningRadius': '4,70 m',
                'trunk': '255 L (mở rộng 1.010 L)',
                'weight': '950 kg'
            },
            'powertrain': {
                'engineType': 'Động cơ xăng Kappa 1.25L 4 xi-lanh',
                'maxPower': '62 kW (83 HP) @ 6.000 rpm',
                'maxTorque': '122 Nm @ 4.000 rpm',
                'maxSpeed': '150 km/h',
                'batteryCapacity': 'Không áp dụng (Bình xăng 35 L)',
                'range': '~450 - 550 km / bình xăng đầy',
                'acCharge': 'Không áp dụng',
                'dcCharge': 'Không áp dụng',
                'fastChargeTime': 'Không áp dụng',
                'driveModes': 'Không có',
                'regenBraking': 'Không áp dụng',
                'cooling': 'Két nước làm mát động cơ đốt trong'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Trục xoắn lò xo trụ',
                'brakes': 'Đĩa / Tang trống',
                'wheels': 'Mâm hợp kim 15 inch (175/50R15)',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Dạng cơ tay kéo',
                'shifter': 'Cần số cơ zíc zắc'
            },
            'exteriorSafety': {
                'lighting': 'Halogen Projector / LED',
                'lightFeatures': 'Tự động bật/tắt, LED ban ngày',
                'mirrors': 'Chỉnh điện, gập điện, sấy gương, báo rẽ',
                'windows': 'Chỉnh điện',
                'tailgate': 'Chỉnh cơ',
                'wipers': 'Chỉnh cơ',
                'cruiseControl': 'Không có',
                'parkingSensors': 'Có (Cảm biến lùi)',
                'rearCamera': 'Có (Camera lùi)',
                'airbags': '2 túi khí',
                'adas': 'ABS, EBD, ESC, HAC khởi hành ngang dốc'
            },
            'economics': {
                'fuelCost1000km': '1.400.000 - 1.600.000 VNĐ (xăng ~24k/L)',
                'maintenanceCost': 'Định kỳ 5.000 km',
                'warranty': '3 năm không giới hạn km'
            }
        }
    },

    # 5. HYUNDAI GRAND I10 1.2 AT (From user prompt)
    {
        'id': 'hyundai_i10_at',
        'name': 'Hyundai Grand i10 1.2 AT',
        'shortName': 'Grand i10 1.2 AT',
        'brand': 'Hyundai',
        'origin': 'Lắp ráp trong nước (TC Motor)',
        'segment': 'Hạng A (Hatchback Đô thị)',
        'category': 'Xe xăng',
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
        'tag': 'Khoang lái rộng rãi & Cảm biến áp suất lốp',
        'badgeColor': 'indigo',
        'highlights': [
            'Trang bị Ga tự động Cruise Control và Cảm biến áp suất lốp TPMS',
            'Hàng ghế sau có cửa gió điều hòa riêng biệt độc nhất phân khúc',
            'Đèn Projector thấu kính sắc nét kết hợp dải LED ban ngày',
            '4 túi khí an toàn bảo vệ hành khách'
        ],
        'pros': [
            'Hàng ghế 2 rộng rãi và có cửa gió sau thoải mái trong mùa hè',
            'Trang bị Cruise Control tiện lợi khi đi xa',
            'Có cảm biến áp suất lốp tiêu chuẩn',
            'Bản đồ dẫn đường offline tích hợp sẵn'
        ],
        'cons': [
            'Công suất 83 HP chỉ đủ dùng cho đô thị, vượt xe tải cần đà',
            'Phanh sau tang trống',
            'Mức tiêu hao xăng trong phố khá tốn (~7 - 8L/100km)'
        ],
        'radar': {
            'power': 53,
            'space': 74,
            'range': 80,
            'safety': 75,
            'tech': 72,
            'economy': 70
        },
        'specs': {
            'dimensions': {
                'd_r_c': '3.815 x 1.680 x 1.520 mm',
                'wheelbase': '2.450 mm',
                'groundClearance': '157 mm',
                'turningRadius': '5,10 m',
                'trunk': '260 L',
                'weight': '1.020 kg'
            },
            'powertrain': {
                'engineType': 'Động cơ xăng Kappa 1.2L MPI 4 xi-lanh',
                'maxPower': '61 kW (83 HP) @ 6.000 rpm',
                'maxTorque': '114 Nm @ 4.000 rpm',
                'maxSpeed': '155 km/h',
                'batteryCapacity': 'Không áp dụng (Bình xăng 37 L)',
                'range': '~480 - 580 km / bình xăng đầy',
                'acCharge': 'Không áp dụng',
                'dcCharge': 'Không áp dụng',
                'fastChargeTime': 'Không áp dụng',
                'driveModes': 'Eco / Normal',
                'regenBraking': 'Không áp dụng',
                'cooling': 'Két nước làm mát động cơ đốt trong'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Thanh xoắn',
                'brakes': 'Đĩa / Tang trống',
                'wheels': 'Mâm hợp kim 15 inch (175/60R15)',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Dạng cơ tay kéo',
                'shifter': 'Cần số tự động 4 cấp'
            },
            'exteriorSafety': {
                'lighting': 'Halogen Projector / LED',
                'lightFeatures': 'Tự động bật/tắt, LED ban ngày',
                'mirrors': 'Chỉnh điện, gập điện, sấy gương, tích hợp báo rẽ',
                'windows': 'Chỉnh điện',
                'tailgate': 'Chỉnh cơ',
                'wipers': 'Chỉnh cơ',
                'cruiseControl': 'Có (Cruise Control tích hợp vô lăng)',
                'parkingSensors': 'Có (Cảm biến lùi)',
                'rearCamera': 'Có (Camera lùi hiển thị trên gương/màn hình)',
                'airbags': '4 túi khí an toàn',
                'adas': 'ABS, EBD, BA, ESC, HAC, Cảm biến áp suất lốp TPMS'
            },
            'economics': {
                'fuelCost1000km': '1.450.000 - 1.650.000 VNĐ (xăng ~24k/L)',
                'maintenanceCost': 'Định kỳ 5.000 km',
                'warranty': '5 năm hoặc 100.000 km'
            }
        }
    },

    # 6. VINFAST VF 3 (Mini SUV)
    {
        'id': 'vinfast_vf3_plus',
        'name': 'VinFast VF 3 Plus',
        'shortName': 'VF 3 Plus',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Minicar (Mini SUV Đô thị)',
        'category': 'Xe điện',
        'price': 296000000,
        'priceText': '296.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 900.000 đ/tháng hoặc Mua pin: 388.000.000 đ',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF3 PLUS', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/vf3/hinh-anh-vinfast-vf3-mau-vang-desktop.webp',
        'colors': get_color_list(vf_map.get('VF3 PLUS', {})),
        'tag': 'Cơn sốt Mini SUV quốc dân',
        'badgeColor': 'yellow',
        'highlights': [
            'Khoảng sáng gầm cực khủng 191 mm leo vỉa hè, lội nước đỉnh cao',
            'Mâm 16 inch hầm hố, kiểu dáng việt dã khối hộp cá tính',
            'Màn hình cảm ứng trung tâm siêu to 10 inch',
            'Dẫn động cầu sau (RWD) cho cảm giác lái cực kỳ lanh lẹ'
        ],
        'pros': [
            'Gầm cao 191 mm bất chấp mọi ổ gà và đường ngập nước mùa mưa',
            'Kích thước nhỏ gọn luồn lách siêu đỉnh, đỗ xe đâu cũng vừa',
            'Chi phí sạc điện siêu rẻ ~300đ/km, rẻ hơn cả xe máy tay ga',
            'Màn hình giải trí 10 inch sắc nét, hỗ trợ kết nối thông minh'
        ],
        'cons': [
            'Cấu hình 3 cửa (4 chỗ ngồi, người ngồi sau phải gập ghế phụ)',
            'Dung tích cốp sau khi dựng cả 2 hàng ghế khá nhỏ (36 L)',
            'Chỉ có 1 túi khí người lái'
        ],
        'radar': {
            'power': 48,
            'space': 55,
            'range': 68,
            'safety': 60,
            'tech': 78,
            'economy': 100
        },
        'specs': {
            'dimensions': {
                'd_r_c': '3.190 x 1.679 x 1.652 mm',
                'wheelbase': '2.075 mm',
                'groundClearance': '191 mm (cao nhất phân khúc)',
                'turningRadius': '4,50 m',
                'trunk': '36 L (mở rộng 285 L khi gập ghế)',
                'weight': '860 kg'
            },
            'powertrain': {
                'engineType': '1 Động cơ điện (cầu sau)',
                'maxPower': '32 kW (43 HP)',
                'maxTorque': '110 Nm',
                'maxSpeed': '100 km/h',
                'batteryCapacity': 'LFP 18,64 kWh',
                'range': '215 km (chuẩn NEDC)',
                'acCharge': '3,3 kW (Sạc tại nhà 220V)',
                'dcCharge': '15 - 20 kW (Sạc nhanh)',
                'fastChargeTime': '36 phút (10 - 70%)',
                'driveModes': '2 chế độ: Eco / Normal',
                'regenBraking': 'Tích hợp tự động',
                'cooling': 'Làm mát tự nhiên & quản lý nhiệt thông minh'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Dầm xoắn',
                'brakes': 'Đĩa trước / Tang trống sau',
                'wheels': 'Mâm thép 16 inch hoặc ốp mâm thể thao (175/75R16)',
                'drivetrain': 'Cầu sau (RWD)',
                'parkingBrake': 'Dạng cơ',
                'shifter': 'Cần gạt chuyển số sau vô lăng kiểu xe sang'
            },
            'exteriorSafety': {
                'lighting': 'Halogen Projector / Halogen',
                'lightFeatures': 'Thanh nan trang trí chữ V biểu tượng',
                'mirrors': 'Chỉnh cơ',
                'windows': 'Chỉnh điện',
                'tailgate': 'Chỉnh cơ mở hất lên',
                'wipers': 'Chỉnh cơ',
                'cruiseControl': 'Không có',
                'parkingSensors': 'Cảm biến lùi phía sau',
                'rearCamera': 'Tùy chọn phụ kiện chính hãng',
                'airbags': '1 túi khí người lái',
                'adas': 'ABS, EBD, BA, Kiểm soát lực kéo TCS'
            },
            'economics': {
                'fuelCost1000km': '250.000 - 300.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Siêu rẻ',
                'warranty': '7 năm hoặc 160.000 km'
            }
        }
    },

    # 7. VINFAST VF 6 PLUS (SUV Hạng B)
    {
        'id': 'vinfast_vf6_plus',
        'name': 'VinFast VF 6 Plus',
        'shortName': 'VF 6 Plus',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Hạng B (B-SUV Đô thị)',
        'category': 'Xe điện',
        'price': 699000000,
        'priceText': '699.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 1.800.000 đ/tháng hoặc Kèm pin: 789.000.000 đ',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF6 PLUS', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/vf6/hinh-anh-xe-vinfast-vf6-mau-xanh-reu-desktop.webp',
        'colors': get_color_list(vf_map.get('VF6 PLUS', {})),
        'tag': 'SUV Hạng B hiệu năng khủng 201 HP',
        'badgeColor': 'emerald',
        'highlights': [
            'Công suất khủng 201 HP / 310 Nm áp đảo mọi xe xăng Hạng B (Seltos, Creta)',
            'Gói trợ lái ADAS Cấp độ 2 với giữ làn, bám đuôi, phanh tự động khẩn cấp',
            'Mâm đúc thể thao hợp kim 19 inch Diamond Cut cực chất',
            'Màn hình cảm ứng 12.9 inch hướng về người lái, 8 túi khí'
        ],
        'pros': [
            'Gia tốc mạnh mẽ vượt xe cực kỳ dứt khoát trên cao tốc',
            'Trục cơ sở 2.730 mm rộng ngang xe hạng C',
            'Hệ thống an toàn ADAS Cấp 2 bảo vệ toàn diện',
            'Ghế da chỉnh điện 8 hướng, tích hợp thông gió'
        ],
        'cons': [
            'Không có màn hình sau vô lăng (hiển thị toàn bộ trên màn 12.9 inch và HUD)',
            'Hệ thống sạc cần làm quen nếu hay đi tỉnh'
        ],
        'radar': {
            'power': 92,
            'space': 88,
            'range': 82,
            'safety': 95,
            'tech': 94,
            'economy': 92
        },
        'specs': {
            'dimensions': {
                'd_r_c': '4.238 x 1.820 x 1.594 mm',
                'wheelbase': '2.730 mm (rộng nhất phân khúc B)',
                'groundClearance': '170 mm',
                'turningRadius': '5,30 m',
                'trunk': '423 L (mở rộng 1.576 L)',
                'weight': '1.750 kg'
            },
            'powertrain': {
                'engineType': '1 Động cơ điện (Permanent Magnet)',
                'maxPower': '150 kW (201 HP)',
                'maxTorque': '310 Nm',
                'maxSpeed': '175 km/h',
                'batteryCapacity': 'LFP 59,6 kWh',
                'range': '381 km (chuẩn WLTP) / ~430 km (NEDC)',
                'acCharge': '11 kW',
                'dcCharge': '~ 80 kW',
                'fastChargeTime': '25 phút (10 - 70%)',
                'driveModes': '3 chế độ: Eco / Normal / Sport',
                'regenBraking': '3 mức tái sinh',
                'cooling': 'Làm mát dung dịch chất lỏng'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Đa điểm liên kết',
                'brakes': 'Đĩa thông gió trước / Đĩa sau',
                'wheels': 'Mâm hợp kim 19 inch (235/45R19)',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Phanh tay điện tử tích hợp Auto Hold',
                'shifter': 'Nút bấm điện tử dạng đàn piano tinh tế'
            },
            'exteriorSafety': {
                'lighting': 'Full LED Projector trước & LED cánh chim VinFast',
                'lightFeatures': 'Tự động bật/tắt, thích ứng thông minh',
                'mirrors': 'Chỉnh điện, gập điện, sấy gương, cảnh báo điểm mù',
                'windows': 'Chỉnh điện 1 chạm 4 cửa chống kẹt',
                'tailgate': 'Chỉnh cơ (có thể lên cốp điện chính hãng)',
                'wipers': 'Gạt mưa tự động theo cảm biến',
                'cruiseControl': 'Ga tự động thích ứng thông minh (Adaptive Cruise Control)',
                'parkingSensors': 'Cảm biến trước và sau',
                'rearCamera': 'Camera 360 độ siêu nét',
                'airbags': '8 túi khí',
                'adas': 'Cấp độ 2: Hỗ trợ giữ làn LKA, Phanh AEB, Cảnh báo lệch làn LDW'
            },
            'economics': {
                'fuelCost1000km': '500.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Rất tiết kiệm',
                'warranty': '7 năm hoặc 160.000 km'
            }
        }
    },

    # 8. VINFAST VF 7 PLUS TC2 (SUV Hạng C)
    {
        'id': 'vinfast_vf7_plus',
        'name': 'VinFast VF 7 Plus (Trần Thép)',
        'shortName': 'VF 7 Plus',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Hạng C (C-SUV Thể thao)',
        'category': 'Xe điện',
        'price': 830000000,
        'priceText': '830.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 1.030.000.000 đ',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF7 PLUS TC2 - TRẦN THÉP', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/vf7/hinh-anh-vinfast-vf7-mau-trang-desktop.webp',
        'colors': get_color_list(vf_map.get('VF7 PLUS TC2 - TRẦN THÉP', {})),
        'tag': 'Quái vật tốc độ 349 HP & Dẫn động 2 cầu AWD',
        'badgeColor': 'purple',
        'highlights': [
            '2 Động cơ điện AWD sản sinh 349 HP / 500 Nm, tăng tốc 0-100km/h chỉ 5.8s',
            'Thiết kế tương lai chắp bút bởi Torino Design danh tiếng Italy',
            'Màn hình cảm ứng 12.9 inch kết hợp HUD hiển thị kính lái',
            'Mâm hợp kim thể thao 20 inch bề thế nhất phân khúc C'
        ],
        'pros': [
            'Gia tốc tương đương các mẫu xe thể thao Porsche Macan hay BMW M',
            'Dẫn động 4 bánh toàn thời gian bám đường xuất sắc mọi thời tiết',
            'Gói trợ lái ADAS Level 2 cao cấp với hỗ trợ lái trên cao tốc',
            'Trần thép cách nhiệt tốt phù hợp khí hậu nhiệt đới nắng nóng'
        ],
        'cons': [
            'Gia tốc rất nhạy đòi hỏi người lái làm quen chân ga',
            'Trọng lượng xe đầm chắc nên tiêu hao điện nhiều hơn VF5/VF6'
        ],
        'radar': {
            'power': 99,
            'space': 90,
            'range': 86,
            'safety': 96,
            'tech': 96,
            'economy': 88
        },
        'specs': {
            'dimensions': {
                'd_r_c': '4.545 x 1.890 x 1.635 mm',
                'wheelbase': '2.840 mm (dài nhất phân khúc C)',
                'groundClearance': '190 mm',
                'turningRadius': '5,60 m',
                'trunk': '520 L (mở rộng 1.680 L)',
                'weight': '2.100 kg'
            },
            'powertrain': {
                'engineType': '2 Động cơ điện trước & sau (AWD)',
                'maxPower': '260 kW (349 HP)',
                'maxTorque': '500 Nm',
                'maxSpeed': '175 km/h (0-100 km/h: 5.8s)',
                'batteryCapacity': 'NMC 75,3 kWh',
                'range': '431 km (chuẩn WLTP) / ~490 km (NEDC)',
                'acCharge': '11 kW',
                'dcCharge': '~ 150 kW (Siêu sạc DC)',
                'fastChargeTime': '24 phút (10 - 70%)',
                'driveModes': '3 chế độ: Eco / Normal / Sport',
                'regenBraking': 'Tái sinh năng lượng thông minh',
                'cooling': 'Làm mát pin & động cơ bằng chất lỏng'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Đa điểm độc lập',
                'brakes': 'Đĩa tản nhiệt 4 bánh hiệu năng cao',
                'wheels': 'Mâm hợp kim 20 inch thể thao',
                'drivetrain': 'Hai cầu toàn thời gian (AWD)',
                'parkingBrake': 'Phanh tay điện tử & Auto Hold',
                'shifter': 'Nút bấm chuyển số phong cách phi thuyền'
            },
            'exteriorSafety': {
                'lighting': 'Full LED Matrix thích ứng thông minh',
                'lightFeatures': 'Tự động pha/cốt, nhận diện biển báo, mở rộng góc chiếu',
                'mirrors': 'Chỉnh điện, gập điện tự động, sấy, tự nghiêng khi lùi',
                'windows': 'Chỉnh điện 1 chạm 4 cửa kính chống kẹt 2 lớp',
                'tailgate': 'Cốp điện thông minh rảnh tay (đá cốp)',
                'wipers': 'Tự động cảm biến mưa',
                'cruiseControl': 'Full Adaptive Cruise Control + Stop & Go',
                'parkingSensors': 'Cảm biến trước, sau và bên sườn',
                'rearCamera': 'Camera 360 độ 3D Surround View',
                'airbags': '8 túi khí',
                'adas': 'Trọn bộ ADAS Cấp 2: Giữ làn, Chuyển làn tự động, Phanh tự động'
            },
            'economics': {
                'fuelCost1000km': '650.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Tiết kiệm 50% so với xe xăng cùng phân khúc',
                'warranty': '10 năm hoặc 200.000 km'
            }
        }
    },

    # 9. VINFAST VF 8 ALL NEW (SUV Hạng D)
    {
        'id': 'vinfast_vf8_all_new',
        'name': 'VinFast VF 8 All New',
        'shortName': 'VF 8 All New',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Hạng D (D-SUV Cao cấp Toàn cầu)',
        'category': 'Xe điện',
        'price': 899000000,
        'priceText': '899.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.900.000 đ/tháng hoặc Kèm pin: 1.099.000.000 đ',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF8 ALL NEW', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/vf8-all-new/hinh-anh-xe-vinfast-vf-8-all-new-mau-trang-desktop.webp',
        'colors': get_color_list(vf_map.get('VF8 ALL NEW', {})),
        'tag': 'SUV thông minh toàn cầu - Đỉnh cao công nghệ',
        'badgeColor': 'sky',
        'highlights': [
            'Hệ thống truyền động điện 2 cầu AWD công suất lên tới 402 HP',
            'Pin CATL thế hệ mới dung lượng 87,7 kWh cho tầm di chuyển 471 km',
            'Màn hình trung tâm 15.6 inch 4K điều khiển bằng giọng nói tiếng Việt Vivi',
            '11 túi khí an toàn và chứng nhận an toàn 5 sao NHTSA / Euro NCAP'
        ],
        'pros': [
            'Sức mạnh 402 HP vượt trội mọi mẫu xe xăng hạng D (SantaFe, Sorento, Fortuner)',
            'Gói dịch vụ Smart Services thông minh, tự động cập nhật phần mềm OTA',
            'Hệ thống âm thanh vòm 10 loa sống động',
            'Bảo hành chính hãng 10 năm dài nhất thị trường'
        ],
        'cons': [
            'Kích thước lớn 4.75m cần không gian đỗ xe thoải mái',
            'Trọng lượng xe 2.5 tấn'
        ],
        'radar': {
            'power': 98,
            'space': 94,
            'range': 90,
            'safety': 99,
            'tech': 98,
            'economy': 86
        },
        'specs': {
            'dimensions': {
                'd_r_c': '4.750 x 1.934 x 1.667 mm',
                'wheelbase': '2.950 mm',
                'groundClearance': '179 mm',
                'turningRadius': '5,80 m',
                'trunk': '576 L (mở rộng 1.373 L) + Cốp trước Frunk 77 L',
                'weight': '2.540 kg'
            },
            'powertrain': {
                'engineType': '2 Động cơ điện (AWD 2 cầu độc lập)',
                'maxPower': '300 kW (402 HP)',
                'maxTorque': '620 Nm',
                'maxSpeed': '200 km/h (0-100 km/h: 5.5s)',
                'batteryCapacity': 'CATL 87,7 kWh',
                'range': '471 km (chuẩn WLTP) / ~530 km (NEDC)',
                'acCharge': '11 kW 3 pha',
                'dcCharge': '~ 250 kW (Siêu sạc cực nhanh)',
                'fastChargeTime': '24 phút (10 - 70%)',
                'driveModes': 'Eco / Normal / Sport',
                'regenBraking': 'Cao / Tiêu chuẩn',
                'cooling': 'Hệ thống quản lý nhiệt pin chủ động'
            },
            'chassis': {
                'suspension': 'Độc lập tay đòn kép trước / Đa liên kết sau',
                'brakes': 'Đĩa thông gió 4 bánh đục lỗ thể thao',
                'wheels': 'Mâm hợp kim 20 inch (245/45R20)',
                'drivetrain': 'Hai cầu toàn thời gian thông minh (AWD)',
                'parkingBrake': 'Điện tử tự động',
                'shifter': 'Nút bấm sang số mạ chrome cao cấp'
            },
            'exteriorSafety': {
                'lighting': 'Full LED thông minh ma trận',
                'lightFeatures': 'Tự động điều chỉnh góc chiếu thích ứng, đèn dẫn đường',
                'mirrors': 'Chỉnh điện, gập điện, nhớ vị trí, sấy gương, chống chói',
                'windows': 'Kính 2 lớp cách âm cách nhiệt toàn xe',
                'tailgate': 'Cốp điện chống kẹt thông minh',
                'wipers': 'Gạt mưa tự động',
                'cruiseControl': 'Full Speed Range Adaptive Cruise Control + Traffic Jam Assist',
                'parkingSensors': '12 cảm biến siêu âm xung quanh xe',
                'rearCamera': 'Camera 360 độ giả lập 3D',
                'airbags': '11 túi khí (bao gồm túi khí rèm và túi khí trung tâm)',
                'adas': 'Đầy đủ tính năng ADAS tự hành cấp độ 2+'
            },
            'economics': {
                'fuelCost1000km': '750.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Tiết kiệm 60% so với SUV xăng 7 chỗ',
                'warranty': '10 năm hoặc 200.000 km'
            }
        }
    },

    # 10. VINFAST VF 9 PLUS (Flagship Full-size)
    {
        'id': 'vinfast_vf9_plus',
        'name': 'VinFast VF 9 Plus (Ghế Cơ Trưởng)',
        'shortName': 'VF 9 Plus',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Hạng E (Full-size Luxury SUV)',
        'category': 'Xe điện',
        'price': 1529000000,
        'priceText': '1.529.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 3.900.000 đ/tháng hoặc Kèm pin: 2.119.000.000 đ',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF9 PLUS', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/vf9/hinh-anh-vinfast-vf9-mau-trang-desktop.webp',
        'colors': get_color_list(vf_map.get('VF9 PLUS', {})),
        'tag': 'Biệt thự di động - Đẳng cấp Chủ tịch',
        'badgeColor': 'rose',
        'highlights': [
            'Cấu hình 6 chỗ ngồi với hàng ghế thương gia độc lập massage sưởi/làm mát',
            'Pin CATL khủng 123 kWh cho quãng đường di chuyển lên tới 602 km',
            'Hệ thống treo khí nén điện tử thích ứng nâng hạ gầm êm ái như bay',
            'Trần kính toàn cảnh Panorama tích hợp chống tia UV 99%'
        ],
        'pros': [
            'Kích thước khổng lồ trên 5.1m mang lại không gian nội thất cực kỳ xa hoa',
            'Hàng ghế VIP thương gia có bệ tỳ tay riêng, sạc không dây và màn hình phụ',
            'Khả năng cách âm siêu tĩnh lặng hàng đầu phân khúc xe sang',
            'Trang bị hệ thống âm thanh 13 loa cao cấp'
        ],
        'cons': [
            'Kích thước Full-size đòi hỏi lái xe cần cẩn thận ở ngõ nhỏ',
            'Mức đầu tư ban đầu cao nhất trong dải sản phẩm VinFast'
        ],
        'radar': {
            'power': 98,
            'space': 100,
            'range': 98,
            'safety': 100,
            'tech': 100,
            'economy': 84
        },
        'specs': {
            'dimensions': {
                'd_r_c': '5.118 x 2.254 x 1.696 mm',
                'wheelbase': '3.150 mm (khoang hành khách siêu rộng)',
                'groundClearance': '189 mm (nâng hạ khí nén)',
                'turningRadius': '6,20 m',
                'trunk': '800 L (mở rộng 2.200 L)',
                'weight': '2.830 kg'
            },
            'powertrain': {
                'engineType': '2 Động cơ điện (AWD thông minh)',
                'maxPower': '300 kW (402 HP)',
                'maxTorque': '620 Nm',
                'maxSpeed': '200 km/h (0-100 km/h: 6.5s)',
                'batteryCapacity': 'CATL 123 kWh',
                'range': '602 km (chuẩn WLTP) / ~680 km (NEDC)',
                'acCharge': '11 kW',
                'dcCharge': '~ 250 kW',
                'fastChargeTime': '26 phút (10 - 70%)',
                'driveModes': 'Eco / Normal / Sport',
                'regenBraking': 'Tái sinh năng lượng 2 cấp độ',
                'cooling': 'Làm mát dung dịch tuần hoàn cưỡng bức'
            },
            'chassis': {
                'suspension': 'Khí nén thích ứng độc lập 4 bánh nâng hạ gầm',
                'brakes': 'Đĩa thông gió đục lỗ 4 bánh',
                'wheels': 'Mâm hợp kim 21 inch phong cách phi thuyền',
                'drivetrain': 'Hai cầu toàn thời gian (AWD)',
                'parkingBrake': 'Phanh tay điện tử & Auto Hold',
                'shifter': 'Nút bấm sang số cảm ứng sang trọng'
            },
            'exteriorSafety': {
                'lighting': 'Full LED Matrix thích ứng thông minh nhất',
                'lightFeatures': 'Tự động mở rộng luồng sáng, chống chói xe đối diện',
                'mirrors': 'Chỉnh điện, gập điện tự động, sấy, nhớ vị trí, tự cụp khi lùi',
                'windows': 'Kính cách âm 2 lớp toàn bộ, rèm che nắng hàng 2',
                'tailgate': 'Cốp điện mở rảnh tay thông minh',
                'wipers': 'Gạt mưa tự động thông minh',
                'cruiseControl': 'Full Level 2+ Highway Assist & Tự động đổi làn',
                'parkingSensors': 'Hệ thống cảm biến đỗ xe tự động Surround',
                'rearCamera': 'Camera 360 độ 3D Panorama + HUD kính lái',
                'airbags': '11 túi khí an toàn tối đa',
                'adas': 'Đầy đủ bộ công nghệ ADAS cao cấp nhất'
            },
            'economics': {
                'fuelCost1000km': '850.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Rẻ hơn 70% so với Lexus LX600, Mercedes GLS',
                'warranty': '10 năm hoặc 200.000 km'
            }
        }
    },

    # 11. VINFAST VF MPV 7 (MPV 7 Chỗ)
    {
        'id': 'vinfast_vf_mpv7',
        'name': 'VinFast VF MPV 7',
        'shortName': 'VF MPV 7',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'MPV Đa dụng 7 Chỗ',
        'category': 'Xe điện',
        'price': 750000000,
        'priceText': '750.000.000 VNĐ',
        'batteryFeeText': 'Thuê pin: 2.100.000 đ/tháng hoặc Mua kèm pin',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF MVP 7', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/mpv7/hinh-anh-xe-vinfast-mpv7-mau-nau-desktop.webp',
        'colors': get_color_list(vf_map.get('VF MVP 7', {})),
        'tag': 'MPV 7 chỗ điện thực dụng & Tiện nghi gia đình',
        'badgeColor': 'teal',
        'highlights': [
            'Cấu hình 7 chỗ ngồi thực thụ với không gian trần cao thoáng đãng',
            'Sàn phẳng hoàn toàn tối ưu hóa diện tích để chân cho 3 hàng ghế',
            'Chi phí vận hành tiết kiệm gấp 3 lần xe MPV xăng (Xpander, Veloz)',
            'Màn hình giải trí cỡ lớn, cửa gió điều hòa độc lập cho từng hàng ghế'
        ],
        'pros': [
            'Không gian 7 chỗ rộng rãi, hàng ghế 3 ngồi thoải mái cho người lớn',
            'Động cơ điện êm ái, không mùi xăng dầu say xe',
            'Chi phí sạc điện siêu kinh tế cho gia đình đông người và dịch vụ du lịch',
            'Trang bị an toàn đầy đủ camera 360 và túi khí bảo vệ 3 hàng ghế'
        ],
        'cons': [
            'Bán kính quay đầu lớn hơn hatchback',
            'Cần kế hoạch sạc khi đi tour du lịch dài ngày'
        ],
        'radar': {
            'power': 80,
            'space': 96,
            'range': 82,
            'safety': 85,
            'tech': 86,
            'economy': 94
        },
        'specs': {
            'dimensions': {
                'd_r_c': '4.720 x 1.860 x 1.730 mm',
                'wheelbase': '2.880 mm (không gian 3 hàng ghế cực rộng)',
                'groundClearance': '175 mm',
                'turningRadius': '5,50 m',
                'trunk': '350 L (gập hàng 3: 1.100 L)',
                'weight': '1.920 kg'
            },
            'powertrain': {
                'engineType': '1 Động cơ điện công suất cao',
                'maxPower': '150 kW (201 HP)',
                'maxTorque': '310 Nm',
                'maxSpeed': '160 km/h',
                'batteryCapacity': 'LFP 68 kWh',
                'range': '410 km (chuẩn NEDC)',
                'acCharge': '11 kW',
                'dcCharge': '~ 100 kW',
                'fastChargeTime': '28 phút (10 - 70%)',
                'driveModes': 'Eco / Normal / Sport',
                'regenBraking': '2 chế độ',
                'cooling': 'Làm mát dung dịch lỏng'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Đa liên kết',
                'brakes': 'Đĩa thông gió 4 bánh',
                'wheels': 'Mâm hợp kim 18 inch (225/55R18)',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Phanh tay điện tử & Auto Hold',
                'shifter': 'Núm xoay điện tử hiện đại'
            },
            'exteriorSafety': {
                'lighting': 'Full LED trước sau',
                'lightFeatures': 'Tự động bật/tắt, dải LED nhận diện thương hiệu',
                'mirrors': 'Chỉnh điện, gập điện, sấy gương',
                'windows': 'Chỉnh điện 1 chạm',
                'tailgate': 'Cốp điện mở rảnh tay',
                'wipers': 'Tự động',
                'cruiseControl': 'Có (Adaptive Cruise Control)',
                'parkingSensors': 'Cảm biến trước và sau',
                'rearCamera': 'Camera 360 độ',
                'airbags': '6 túi khí',
                'adas': 'Cảnh báo điểm mù, Giữ làn đường, Phanh tự động khẩn cấp'
            },
            'economics': {
                'fuelCost1000km': '550.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Tiết kiệm 65% so với MPV xăng',
                'warranty': '7 năm hoặc 160.000 km'
            }
        }
    },

    # 12. VINFAST LIMO GREEN (MPV Dịch vụ Cao cấp)
    {
        'id': 'vinfast_limo_green',
        'name': 'VinFast Limo Green',
        'shortName': 'Limo Green',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Dịch vụ Đưa đón Cao cấp (Green SM Luxury)',
        'category': 'Xe điện',
        'price': 699000000,
        'priceText': '699.000.000 VNĐ',
        'batteryFeeText': 'Chính sách ưu đãi doanh nghiệp & đối tác Xanh SM',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('LIMO GREEN', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/limo-green/hinh-anh-xe-vinfast-limo-green-mau-trang-desktop.webp',
        'colors': get_color_list(vf_map.get('LIMO GREEN', {})),
        'tag': 'Chuyên cơ mặt đất dịch vụ đưa đón VIP',
        'badgeColor': 'emerald',
        'highlights': [
            'Thiết kế tối ưu cho trải nghiệm ngồi của hành khách phía sau',
            'Không gian duỗi chân rộng thênh thang, điều hòa mát lạnh sâu',
            'Khung gầm chắc chắn, vận hành êm ru không tiếng ồn động cơ',
            'Chi phí năng lượng tối ưu mang lại lợi nhuận cao nhất cho chủ xe'
        ],
        'pros': [
            'Được khách hàng đón nhận và đánh giá 5 sao về độ êm ái',
            'Độ bền bỉ cao, vật liệu nội thất da cao cấp dễ lau chùi',
            'Được hỗ trợ hệ sinh thái trạm sạc ưu tiên của V-GREEN',
            'Giá đầu tư hợp lý, hoàn vốn siêu nhanh'
        ],
        'cons': [
            'Hướng tới mục đích phục vụ hành khách hơn là trải nghiệm lái cá nhân',
            'Trang bị vừa đủ cho mục đích vận hành chuyên nghiệp'
        ],
        'radar': {
            'power': 78,
            'space': 95,
            'range': 80,
            'safety': 82,
            'tech': 78,
            'economy': 99
        },
        'specs': {
            'dimensions': {
                'd_r_c': '4.680 x 1.840 x 1.700 mm',
                'wheelbase': '2.840 mm',
                'groundClearance': '170 mm',
                'turningRadius': '5,40 m',
                'trunk': '480 L (đựng vừa 4 vali cỡ lớn)',
                'weight': '1.850 kg'
            },
            'powertrain': {
                'engineType': '1 Động cơ điện hiệu suất cao',
                'maxPower': '130 kW (174 HP)',
                'maxTorque': '280 Nm',
                'maxSpeed': '150 km/h',
                'batteryCapacity': 'LFP 60 kWh',
                'range': '390 km (chuẩn NEDC)',
                'acCharge': '7,4 kW',
                'dcCharge': '~ 80 kW',
                'fastChargeTime': '30 phút (10 - 70%)',
                'driveModes': 'Eco / Normal',
                'regenBraking': '2 chế độ',
                'cooling': 'Làm mát pin bằng dung dịch'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Dầm xoắn gia cường',
                'brakes': 'Đĩa thông gió trước / Đĩa sau',
                'wheels': 'Mâm hợp kim 17 inch',
                'drivetrain': 'Cầu trước (FWD)',
                'parkingBrake': 'Phanh tay điện tử',
                'shifter': 'Núm xoay điện tử'
            },
            'exteriorSafety': {
                'lighting': 'LED / LED',
                'lightFeatures': 'Tự động bật tắt',
                'mirrors': 'Chỉnh điện, gập điện',
                'windows': 'Chỉnh điện',
                'tailgate': 'Chỉnh cơ trợ lực',
                'wipers': 'Chỉnh cơ gián đoạn',
                'cruiseControl': 'Có (Cruise Control)',
                'parkingSensors': 'Cảm biến lùi',
                'rearCamera': 'Camera lùi góc rộng',
                'airbags': '4 túi khí',
                'adas': 'ABS, EBD, ESC, Kiểm soát chống trượt TCS'
            },
            'economics': {
                'fuelCost1000km': '480.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Rất thấp',
                'warranty': '7 năm hoặc 200.000 km'
            }
        }
    },

    # 13. VINFAST EC VAN (Xe Tải Van Chở Hàng Đô Thị)
    {
        'id': 'vinfast_ec_van',
        'name': 'VinFast EC Van (Cửa trượt)',
        'shortName': 'EC Van',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Xe Tải Van Điện Đô Thị (Vận tải Logictics)',
        'category': 'Xe tải điện',
        'price': 306000000,
        'priceText': '306.000.000 VNĐ',
        'batteryFeeText': 'Gói cước sạc & thuê pin thương mại ưu đãi',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('EC VAN NÂNG CAO (Cửa trượt)', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/car/ec-van/hinh-anh-xe-vinfast-ec-van-mau-do-desktop.webp',
        'colors': get_color_list(vf_map.get('EC VAN NÂNG CAO (Cửa trượt)', {})),
        'tag': 'Lưu thông 24/24 nội đô không cấm giờ',
        'badgeColor': 'amber',
        'highlights': [
            'Được phép lưu thông vào phố cấm 24/7 theo quy định xe điện sạch',
            'Thể tích khoang chở hàng rộng rãi ~2.6 m3, tải trọng lên tới 650 kg',
            'Cửa lùa trượt hông tiện lợi bốc dỡ hàng hóa trong ngõ nhỏ',
            'Tiết kiệm đến 70% chi phí vận chuyển so với xe tải xăng/dầu'
        ],
        'pros': [
            'Chạy vào trung tâm thành phố giờ cao điểm không lo bị phạt cấm giờ',
            'Sạc nhanh chỉ 35 phút quay vòng chuyến liên tục',
            'Kết cấu sàn phẳng chống trượt, khung vỏ thép chịu lực dày dặn',
            'Chi phí lăn bánh siêu rẻ, miễn 100% lệ phí trước bạ'
        ],
        'cons': [
            'Cấu hình 2 chỗ ngồi phía trước (ưu tiên tối đa khoang chở hàng)',
            'Trang bị nội thất tập trung vào tính thực dụng'
        ],
        'radar': {
            'power': 65,
            'space': 98,
            'range': 70,
            'safety': 72,
            'tech': 68,
            'economy': 100
        },
        'specs': {
            'dimensions': {
                'd_r_c': '3.700 x 1.550 x 1.850 mm',
                'wheelbase': '2.400 mm',
                'groundClearance': '165 mm',
                'turningRadius': '4,80 m (linh hoạt luồn hẻm)',
                'trunk': 'Khoang hàng 2.600 L (Tải trọng 650 kg)',
                'weight': '1.150 kg'
            },
            'powertrain': {
                'engineType': '1 Động cơ điện mô-men xoắn cao',
                'maxPower': '45 kW (60 HP)',
                'maxTorque': '150 Nm',
                'maxSpeed': '90 km/h',
                'batteryCapacity': 'LFP 28 kWh',
                'range': '210 km (chuẩn NEDC chở đủ tải)',
                'acCharge': '3,3 - 6,6 kW',
                'dcCharge': '~ 30 kW',
                'fastChargeTime': '35 phút (10 - 70%)',
                'driveModes': 'Eco / Normal',
                'regenBraking': 'Tích hợp sẵn',
                'cooling': 'Làm mát dung dịch'
            },
            'chassis': {
                'suspension': 'Độc lập MacPherson / Nhíp lá chịu tải cao',
                'brakes': 'Đĩa trước / Tang trống sau',
                'wheels': 'Mâm thép chịu tải 14 inch (165/70R14 LT)',
                'drivetrain': 'Cầu sau (RWD chở nặng leo dốc khỏe)',
                'parkingBrake': 'Phanh cơ tay kéo',
                'shifter': 'Núm xoay điện tử'
            },
            'exteriorSafety': {
                'lighting': 'Halogen độ bền cao',
                'lightFeatures': 'Đèn định vị Halogen',
                'mirrors': 'Chỉnh cơ góc quan sát lớn',
                'windows': 'Chỉnh điện',
                'tailgate': 'Cửa sau mở 2 cánh 180 độ + Cửa trượt hông',
                'wipers': 'Chỉnh cơ',
                'cruiseControl': 'Không có',
                'parkingSensors': 'Cảm biến lùi',
                'rearCamera': 'Tùy chọn gắn thêm',
                'airbags': '1 túi khí người lái',
                'adas': 'ABS, EBD phân bổ lực phanh theo tải trọng'
            },
            'economics': {
                'fuelCost1000km': '320.000 VNĐ (sạc điện)',
                'maintenanceCost': 'Cực thấp',
                'warranty': '5 năm hoặc 150.000 km'
            }
        }
    },

    # 14. VINFAST VF WILD (Bán Tải Điện Khủng)
    {
        'id': 'vinfast_vf_wild',
        'name': 'VinFast VF Wild Comfort',
        'shortName': 'VF Wild',
        'brand': 'VinFast',
        'origin': 'Việt Nam',
        'segment': 'Bán Tải Điện Cỡ Trung (Mid-size Pickup)',
        'category': 'Xe bán tải điện',
        'price': 860000000,
        'priceText': '860.000.000 VNĐ (Dự kiến)',
        'batteryFeeText': 'Chính sách pin thế hệ mới',
        'fuelType': 'Điện thuần (BEV)',
        'image': vf_map.get('VF WILD COMFORT', {}).get('image') or 'https://static-cms-prod.vinfastauto.com/statics/wild-2026/vh-wild-desktop.webp',
        'colors': get_color_list(vf_map.get('VF WILD COMFORT', {})),
        'tag': 'Bán tải điện dũng mãnh đột phá công nghệ',
        'badgeColor': 'orange',
        'highlights': [
            'Thiết kế kính chắn gió sau và vách cabin mở gập thông vào thùng xe độc nhất',
            'Chiều dài thùng xe mở rộng linh hoạt từ 1.58m lên tới 2.44m',
            'Khung gầm sắt xi rời chuyên dụng off-road, hệ dẫn động 2 cầu điện tử',
            'Kính lái toàn cảnh Panorama và cửa sổ trời thời thượng'
        ],
        'pros': [
            'Sức kéo vượt trội tức thì của động cơ điện, không bị trễ tua như máy dầu',
            'Tính năng mở thông cabin độc đáo biến thùng xe thành giường nằm camping',
            'Không gian cabin rộng rãi như một chiếc SUV hạng sang',
            'Miễn phí 100% lệ phí trước bạ xe điện'
        ],
        'cons': [
            'Kích thước bán tải 5.3m khá cồng kềnh trong phố nhỏ',
            'Mẫu xe đang trong lộ trình thương mại hóa bàn giao'
        ],
        'radar': {
            'power': 96,
            'space': 99,
            'range': 88,
            'safety': 95,
            'tech': 95,
            'economy': 90
        },
        'specs': {
            'dimensions': {
                'd_r_c': '5.324 x 1.997 x 1.760 mm',
                'wheelbase': '3.250 mm',
                'groundClearance': '220 mm (lội nước đỉnh cao)',
                'turningRadius': '6,30 m',
                'trunk': 'Thùng hàng 1.580 mm - mở rộng thông cabin 2.440 mm',
                'weight': '2.450 kg'
            },
            'powertrain': {
                'engineType': '2 Động cơ điện trước & sau (AWD)',
                'maxPower': '300 kW (402 HP)',
                'maxTorque': '640 Nm',
                'maxSpeed': '180 km/h',
                'batteryCapacity': 'NMC 85 kWh',
                'range': '450 km (chuẩn EPA)',
                'acCharge': '11 kW',
                'dcCharge': '~ 200 kW',
                'fastChargeTime': '25 phút (10 - 70%)',
                'driveModes': 'Eco / Normal / Sport / Off-road / Towing (Kéo rơ-mooc)',
                'regenBraking': 'Tái sinh đa cấp độ',
                'cooling': 'Làm mát dung dịch chuyên dụng địa hình'
            },
            'chassis': {
                'suspension': 'Độc lập tay đòn kép trước / Đa liên kết sau',
                'brakes': 'Đĩa thông gió 4 bánh hiệu năng cao',
                'wheels': 'Mâm hợp kim 20 inch kèm lốp địa hình All-Terrain',
                'drivetrain': 'Hai cầu điện tử thông minh (Dual Motor AWD)',
                'parkingBrake': 'Phanh tay điện tử & Auto Hold',
                'shifter': 'Cần số điện tử thể thao'
            },
            'exteriorSafety': {
                'lighting': 'Full LED Cyber Matrix tương lai',
                'lightFeatures': 'Thanh đèn LED vắt ngang trước sau',
                'mirrors': 'Gương chiếu hậu kỹ thuật số camera hiện đại',
                'windows': 'Kính cabin sau mở gập điện độc quyền',
                'tailgate': 'Cửa thùng sau trợ lực điện thông minh',
                'wipers': 'Tự động cảm biến',
                'cruiseControl': 'Full Adaptive Cruise Control',
                'parkingSensors': 'Cảm biến 360 độ xung quanh',
                'rearCamera': 'Camera 360 độ kèm camera gầm xe vượt địa hình',
                'airbags': '8 túi khí',
                'adas': 'Hỗ trợ lái bán tự động trên cao tốc và vượt địa hình'
            },
            'economics': {
                'fuelCost1000km': '680.000 VNĐ (sạc điện so với 2.200.000 VNĐ tiền dầu bán tải)',
                'maintenanceCost': 'Rất tiết kiệm',
                'warranty': '10 năm hoặc 200.000 km'
            }
        }
    }
]

# Write database.json
json_out_path = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/data/cars_database.json'
os.makedirs(os.path.dirname(json_out_path), exist_ok=True)
with open(json_out_path, 'w', encoding='utf-8') as f:
    json.dump({'cars': cars_list}, f, ensure_ascii=False, indent=2)

# Write cars_data.js
js_out_path = r'C:/Users/PC/.gemini/antigravity/scratch/vinfast-compare/js/cars_data.js'
os.makedirs(os.path.dirname(js_out_path), exist_ok=True)
with open(js_out_path, 'w', encoding='utf-8') as f:
    f.write('// Auto-generated VinFast Smart Comparison Database\n')
    f.write('window.CARS_DATABASE = ')
    json.dump(cars_list, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"Generated {len(cars_list)} cars in database successfully!")
print(f"- JSON: {json_out_path}")
print(f"- JS: {js_out_path}")
