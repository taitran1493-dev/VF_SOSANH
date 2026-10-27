/**
 * Comparison Engine for VinFast Smart Car Comparison Platform
 * 7 Official Categories aligned with VinFast Master Specifications
 * Features:
 *  - Atomic spec definitions across 7 official categories
 *  - Smart difference detection (isDifferent) and advantage winner highlight (bestIndex)
 *  - Apple-grade clean multiline formatting (no squeezed long strings)
 *  - Safety acronym badges (ABS, EBD, ESC, TCS, HSA...)
 *  - Structured trunk breakdown (Standard, Folded, Frunk)
 *  - Responsive radar chart with dynamic Dark/Light theming
 *  - Intelligent AI summary highlighting key metrics
 */

window.ComparisonEngine = (function () {
  'use strict';

  const SPEC_CATEGORIES = [
    {
      id: 'cat1_dimensions',
      title: 'I. KÍCH THƯỚC, TRỌNG LƯỢNG & KHÍ ĐỘNG HỌC',
      icon: 'maximize-2',
      specs: [
        { key: 'd_r_c', label: 'Dài x Rộng x Cao (mm)', type: 'dimension' },
        { key: 'segment', label: 'Phân khúc & Cấu hình chỗ', type: 'badge' },
        { key: 'wheelbase', label: 'Chiều dài cơ sở (mm)', type: 'number_higher_better' },
        { key: 'groundClearance', label: 'Khoảng sáng gầm xe không tải (mm)', type: 'number_higher_better' },
        { key: 'turningRadius', label: 'Bán kính quay vòng tối thiểu (m)', type: 'number_lower_better' },
        { key: 'weight', label: 'Khối lượng bản thân không tải (kg)', type: 'split_lines' },
        { key: 'grossWeight', label: 'Khối lượng toàn tải cho phép (kg)', type: 'split_lines' },
        { key: 'dragCoeff', label: 'Hệ số cản khí động học (Cd)', type: 'text' },
        { key: 'offroadAngles', label: 'Góc vượt địa hình & Lội nước', type: 'split_lines' }
      ]
    },
    {
      id: 'cat2_storage',
      title: 'II. KHÔNG GIAN CHỨA ĐỒ & CỐP XE',
      icon: 'package',
      specs: [
        { key: 'trunkStandard', label: 'Thể tích cốp tiêu chuẩn (Lít)', type: 'trunk_breakdown' },
        { key: 'trunkMax', label: 'Thể tích khi gập hàng ghế sau (Lít)', type: 'trunk_breakdown' },
        { key: 'frunk', label: 'Cốp trước Frunk (Lít)', type: 'badge' },
        { key: 'cargoBed', label: 'Thùng hàng / Khoang chứa tải', type: 'split_lines' },
        { key: 'trunkUtility', label: 'Tiện ích cốp sau (Đóng mở điện/Đá cốp)', type: 'badge' }
      ]
    },
    {
      id: 'cat3_powertrain',
      title: 'III. VẬN HÀNH, ĐỘNG CƠ & PIN ĐIỆN',
      icon: 'zap',
      specs: [
        { key: 'motorDrivetrain', label: 'Động cơ & Hệ dẫn động', type: 'split_lines' },
        { key: 'maxPower', label: 'Công suất tối đa (kW / hp)', type: 'power_compare' },
        { key: 'maxTorque', label: 'Mô-men xoắn cực đại (Nm)', type: 'text' },
        { key: 'acceleration', label: 'Tăng tốc 0–100 km/h (s)', type: 'accel_compare' },
        { key: 'batteryType', label: 'Loại pin & Công nghệ pack pin', type: 'split_lines' },
        { key: 'batteryCapacity', label: 'Dung lượng pin khả dụng (kWh)', type: 'text' },
        { key: 'range', label: 'Quãng đường di chuyển 1 lần sạc', type: 'range_compare' },
        { key: 'fastCharge', label: 'Sạc siêu nhanh DC (10% - 70%)', type: 'split_lines' },
        { key: 'acCharge', label: 'Sạc chậm AC gia đình', type: 'split_lines' },
        { key: 'suspension', label: 'Hệ thống treo trước / sau', type: 'split_lines' },
        { key: 'brakes', label: 'Hệ thống phanh trước / sau', type: 'split_lines' },
        { key: 'wheels', label: 'Kích thước mâm & lốp', type: 'split_lines' }
      ]
    },
    {
      id: 'cat4_equipment',
      title: 'IV. TIỆN ÍCH & TRANG BỊ NỘI / NGOẠI THẤT',
      icon: 'sparkles',
      specs: [
        { key: 'headlights', label: 'Đèn chiếu sáng phía trước', type: 'split_lines' },
        { key: 'brandLighting', label: 'Dải LED cánh chim VinFast & Đèn hậu', type: 'split_lines' },
        { key: 'mirrors', label: 'Gương chiếu hậu ngoài', type: 'split_lines' },
        { key: 'seating', label: 'Chất liệu ghế & Cấu hình ghế', type: 'split_lines' },
        { key: 'seatAdjustment', label: 'Chức năng ghế (Chỉnh điện/Thông gió/Massage)', type: 'split_lines' },
        { key: 'gearShifter', label: 'Cần số điều khiển & Phanh đỗ điện tử', type: 'split_lines' },
        { key: 'climate', label: 'Hệ thống điều hòa & Màng lọc Combi 1.0', type: 'split_lines' },
        { key: 'sunroof', label: 'Cửa sổ trời toàn cảnh Panoramic', type: 'badge' },
        { key: 'doors', label: 'Cửa xe & Kính cách âm', type: 'split_lines' }
      ]
    },
    {
      id: 'cat5_tech',
      title: 'V. CÔNG NGHỆ THÔNG MINH & TIỆN ÍCH VF CONNECT',
      icon: 'cpu',
      specs: [
        { key: 'driverDisplay', label: 'Màn hình thông tin lái (Dashboard)', type: 'split_lines' },
        { key: 'infotainment', label: 'Màn hình cảm ứng giải trí trung tâm', type: 'text' },
        { key: 'hud', label: 'Màn hình hiển thị trên kính lái (HUD)', type: 'badge' },
        { key: 'sound', label: 'Hệ thống âm thanh & Loa giải trí', type: 'split_lines' },
        { key: 'viviAI', label: 'Trợ lý ảo ViVi điều khiển giọng nói AI', type: 'badge' },
        { key: 'connectivity', label: 'Kết nối không dây & Cổng sạc điện thoại', type: 'split_lines' },
        { key: 'smartFeatures', label: 'Tính năng thông minh & Cập nhật OTA', type: 'bullet_list' },
        { key: 'appControl', label: 'Ứng dụng quản lý xe trên Smartphone', type: 'bullet_list' }
      ]
    },
    {
      id: 'cat6_safety',
      title: 'VI. AN TOÀN TIÊU CHUẨN & GÓI TRỢ LÁI ADAS',
      icon: 'shield-check',
      specs: [
        { key: 'airbags', label: 'Số túi khí an toàn', type: 'airbag_compare' },
        { key: 'activeSafety', label: 'Hệ thống an toàn chủ động (ABS, ESC, TCS...)', type: 'safety_acronym_badges' },
        { key: 'adasPackage', label: 'Cấp độ trợ lái thông minh ADAS', type: 'badge' },
        { key: 'highwayAssist', label: 'Hỗ trợ di chuyển ùn tắc & Cao tốc', type: 'badge' },
        { key: 'laneKeep', label: 'Cảnh báo chệch làn & Giữ làn khẩn cấp', type: 'badge' },
        { key: 'cruiseControl', label: 'Kiểm soát hành trình thích ứng (ACC)', type: 'badge' },
        { key: 'autoBrake', label: 'Phanh tự động khẩn cấp trước/sau (AEB)', type: 'badge' },
        { key: 'blindSpot', label: 'Cảnh báo điểm mù & Cắt ngang khi lùi', type: 'badge' },
        { key: 'cameraSensors', label: 'Camera quan sát & Cảm biến hỗ trợ đỗ xe', type: 'split_lines' },
        { key: 'smartParking', label: 'Hỗ trợ đỗ xe tự động thông minh', type: 'badge' },
        { key: 'batterySafety', label: 'Tiêu chuẩn an toàn pin & Kháng nước IP67', type: 'split_lines' }
      ]
    },
    {
      id: 'cat7_economics',
      title: 'VII. CHI PHÍ, BẢO HÀNH & HẬU MÃI CHÍNH HÃNG',
      icon: 'trending-up',
      specs: [
        { key: 'price', label: 'Giá niêm yết chính hãng (VNĐ)', type: 'split_lines' },
        { key: 'energyCost', label: 'Chi phí sạc điện ước tính / 1.000 km', type: 'text' },
        { key: 'warrantyCar', label: 'Chính sách bảo hành xe mới', type: 'split_lines' },
        { key: 'warrantyBattery', label: 'Chính sách bảo hành bộ pin cao áp', type: 'split_lines' },
        { key: 'maintenance', label: 'Bảo dưỡng định kỳ & Chi phí phụ tùng', type: 'split_lines' },
        { key: 'chargingNetwork', label: 'Hệ thống trạm sạc V-GREEN toàn quốc', type: 'split_lines' },
        { key: 'officialLink', label: 'Website chính thức VinFast', type: 'official_link' }
      ]
    }
  ];

  /**
   * Check differences across vehicles for a specific spec key
   */
  function analyzeDifferences(cars, categoryId, specKey) {
    if (!cars || cars.length < 2) {
      return { isDifferent: false, values: [], bestIndex: -1 };
    }

    const values = cars.map(car => {
      const cat = car.specs ? car.specs[categoryId] : null;
      let val = cat && cat[specKey] !== undefined ? cat[specKey] : '';
      if (!val || val === 'Chưa công bố') val = '—';
      return val;
    });

    // Normalized comparison string
    const stringReps = values.map(v => {
      if (Array.isArray(v)) return v.join('|').toLowerCase();
      return String(v).trim().toLowerCase().replace(/[\s\-_]/g, '');
    });

    const first = stringReps[0];
    const isDifferent = stringReps.some(v => v !== first && v !== '—' && v !== '');

    let bestIndex = -1;

    // Power (higher hp is better)
    if (specKey === 'maxPower') {
      let maxHp = -1;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const hpMatch = val.match(/(\d+)\s*(?:hp|HP)/i);
        const kwMatch = val.match(/(\d+)\s*kW/i);
        let hp = 0;
        if (hpMatch) hp = parseInt(hpMatch[1], 10);
        else if (kwMatch) hp = Math.round(parseInt(kwMatch[1], 10) * 1.341);
        if (hp > maxHp) {
          maxHp = hp;
          bestIndex = idx;
        }
      });
    }
    // Acceleration (lower seconds is better)
    else if (specKey === 'acceleration') {
      let minSec = 999;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const m = val.match(/(\d+[\.,]?\d*)\s*s/i);
        if (m) {
          const sec = parseFloat(m[1].replace(',', '.'));
          if (sec > 0 && sec < minSec) {
            minSec = sec;
            bestIndex = idx;
          }
        }
      });
    }
    // Range (higher km is better)
    else if (specKey === 'range') {
      let maxR = -1;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const m = val.match(/(\d+)\s*km/i);
        if (m) {
          const num = parseInt(m[1], 10);
          if (num > maxR) {
            maxR = num;
            bestIndex = idx;
          }
        }
      });
    }
    // Airbags (higher count is better)
    else if (specKey === 'airbags') {
      let maxAir = -1;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const m = val.match(/(\d+)\s*túi/i);
        if (m) {
          const num = parseInt(m[1], 10);
          if (num > maxAir) {
            maxAir = num;
            bestIndex = idx;
          }
        }
      });
    }
    // Wheelbase or Ground clearance (higher is better)
    else if (specKey === 'wheelbase' || specKey === 'groundClearance') {
      let maxNum = -1;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const num = parseInt(val.replace(/\D/g, ''), 10);
        if (!isNaN(num) && num > maxNum) {
          maxNum = num;
          bestIndex = idx;
        }
      });
    }
    // Turning Radius (lower is better)
    else if (specKey === 'turningRadius') {
      let minRad = 999;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const m = val.match(/(\d+[\.,]?\d*)\s*m/i);
        if (m) {
          const rad = parseFloat(m[1].replace(',', '.'));
          if (rad > 0 && rad < minRad) {
            minRad = rad;
            bestIndex = idx;
          }
        }
      });
    }
    // Standard Trunk (higher is better)
    else if (specKey === 'trunkStandard' || specKey === 'trunkMax') {
      let maxL = -1;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const m = val.match(/(\d+[\.,]?\d*)\s*L/i);
        if (m) {
          const num = parseInt(m[1].replace(/\D/g, ''), 10);
          if (num > maxL) {
            maxL = num;
            bestIndex = idx;
          }
        }
      });
    }

    return { isDifferent, values, bestIndex };
  }

  /**
   * Helper: Split string avoiding cutting inside parentheses.
   * Splits by semicolons, pipes, or newlines outside parens.
   */
  function splitRespectingParens(text) {
    if (!text || text === '—') return [];
    const parts = text.split(/[;\n|]+(?![^\(]*\))/).map(p => p.trim()).filter(Boolean);
    return parts;
  }

  /**
   * 1. Render Safety Acronyms (ABS, EBD, BA, ESC, TCS, HSA, ROM, ESS, dTPMS, AutoHold)
   */
  function renderSafetyAcronyms(val) {
    const str = String(val);
    if (!str || str === '—') return `<span class="text-subtle font-medium text-xs">—</span>`;

    const recognized = ['ABS', 'EBD', 'BA', 'ESC', 'TCS', 'HSA', 'ROM', 'ESS', 'dTPMS', 'TPMS', 'AutoHold', 'HBA', 'LKA', 'LDW', 'FCW', 'AEB', 'ACC', 'BSW', 'BSM', 'RCTA', 'DOW'];
    
    const parts = str.split(/[;\n]+/).map(p => p.trim()).filter(Boolean);
    let descParts = [];
    let foundAcronyms = [];

    parts.forEach(p => {
      const tokens = p.split(/[,;\/\s\(\)]+/).map(t => t.trim()).filter(Boolean);
      const acronymMatches = tokens.filter(t => 
        recognized.includes(t) || 
        (/^[A-Z0-9\+\-]{2,6}$/.test(t) && t !== 'FULL' && t !== 'LED' && t !== 'SUV' && t !== 'AWD' && t !== 'FWD' && t !== 'RWD')
      );

      if (acronymMatches.length >= 2 || (tokens.length <= 4 && acronymMatches.length >= 1)) {
        acronymMatches.forEach(ac => {
          if (!foundAcronyms.includes(ac)) foundAcronyms.push(ac);
        });
        const remaining = tokens.filter(t => !acronymMatches.includes(t) && !recognized.includes(t)).join(' ');
        if (remaining && remaining.length > 3) descParts.push(remaining);
      } else {
        descParts.push(p);
      }
    });

    if (foundAcronyms.length === 0) {
      return renderSplitLines(str);
    }

    return `
      <div class="flex flex-col gap-2 w-full text-left">
        ${descParts.length > 0 ? `
          <div class="text-xs font-bold text-primary flex items-start gap-1.5 leading-snug">
            <svg class="w-3.5 h-3.5 text-blue-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            <span>${descParts.join('; ')}</span>
          </div>
        ` : ''}
        <div class="flex flex-wrap gap-1.5 pt-0.5">
          ${foundAcronyms.map(ac => `<span class="spec-tag">${ac}</span>`).join('')}
        </div>
      </div>
    `;
  }

  /**
   * 2. Render Trunk Breakdown (Only for trunk specs)
   */
  function renderTrunkBreakdown(val) {
    const str = String(val);
    if (!str || str === '—') return `<span class="text-subtle font-medium text-xs">—</span>`;

    // Only split if it contains / between liter numbers like "36 L / 285 L"
    if (str.includes('/') && /\d+\s*L/i.test(str)) {
      const parts = str.split('/').map(p => p.trim()).filter(Boolean);
      return `
        <div class="flex flex-col gap-1.5 w-full text-left">
          ${parts.map((p, i) => `
            <div class="flex items-center justify-between text-xs py-1 border-b border-dashed border-[var(--border-subtle)] last:border-b-0">
              <span class="text-muted text-[11px] font-semibold">${i === 0 ? 'Tiêu chuẩn:' : (i === 1 ? 'Gập ghế sau:' : 'Cốp trước:')}</span>
              <span class="font-bold text-primary">${p}</span>
            </div>
          `).join('')}
        </div>
      `;
    }

    const match = str.match(/^(\d+[\.,]?\d*\s*L?)\s*\((.+)\)$/i);
    if (match) {
      return `
        <div class="flex flex-col gap-1.5 w-full text-left">
          <div class="flex items-center justify-between text-xs py-1 border-b border-dashed border-[var(--border-subtle)]">
            <span class="text-muted text-[11px] font-semibold">Tiêu chuẩn:</span>
            <span class="font-bold text-primary">${match[1]}</span>
          </div>
          <div class="flex items-start gap-1.5 text-xs py-0.5 text-emerald-600 dark:text-emerald-400 font-semibold leading-tight">
            <svg class="w-3.5 h-3.5 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
            <span>${match[2]}</span>
          </div>
        </div>
      `;
    }

    return `
      <div class="font-bold text-sm text-primary text-left">
        ${str}
      </div>
    `;
  }

  /**
   * 3. Render Split Lines: Breaks down multi-item comma/semicolon/slash strings into lines
   */
  function renderSplitLines(val) {
    const str = String(val);
    if (!str || str === '—') return `<span class="text-subtle font-medium text-xs">—</span>`;

    const parts = splitRespectingParens(str);
    if (parts.length <= 1) {
      return `
        <div class="font-semibold text-xs text-secondary text-left leading-relaxed">
          ${str}
        </div>
      `;
    }

    return `
      <div class="spec-bullet-list">
        ${parts.map(part => {
          const colonIdx = part.indexOf(':');
          if (colonIdx > 0 && colonIdx < 35) {
            const label = part.substring(0, colonIdx).trim();
            const rest = part.substring(colonIdx + 1).trim();
            return `
              <div class="spec-bullet-item">
                <span class="spec-bullet-dot"></span>
                <span class="flex-1">
                  <strong class="text-primary font-bold">${label}:</strong>
                  <span class="text-secondary font-medium ml-1">${rest}</span>
                </span>
              </div>
            `;
          }
          return `
            <div class="spec-bullet-item">
              <span class="spec-bullet-dot"></span>
              <span class="text-secondary font-medium leading-relaxed">${part}</span>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  /**
   * 4. Render Bullet Item for lists
   */
  function renderBulletItem(item) {
    const str = String(item).trim();
    if (!str) return '';

    const colonIdx = str.indexOf(':');
    if (colonIdx > 0 && colonIdx < 35) {
      const label = str.substring(0, colonIdx).trim();
      const rest = str.substring(colonIdx + 1).trim();
      return `
        <div class="spec-bullet-item">
          <span class="spec-bullet-dot"></span>
          <span class="flex-1">
            <strong class="text-primary font-bold">${label}:</strong>
            <span class="text-secondary font-medium ml-1">${rest}</span>
          </span>
        </div>
      `;
    }

    return `
      <div class="spec-bullet-item">
        <span class="spec-bullet-dot"></span>
        <span class="text-secondary font-medium leading-relaxed">${str}</span>
      </div>
    `;
  }

  /**
   * 5. Render Metric Value (Power, Range, Dimensions, Numbers)
   */
  function renderMetricValue(val, specType) {
    const str = String(val);

    if (specType === 'dimension') {
      return `
        <div class="font-extrabold text-sm text-primary text-left tracking-tight">
          ${str}
        </div>
      `;
    }

    if (specType === 'power_compare') {
      const hpMatch = str.match(/(\d+)\s*(?:hp|HP)/i);
      const kwMatch = str.match(/(\d+)\s*kW/i);
      let hpVal = hpMatch ? hpMatch[1] : '';
      let kwVal = kwMatch ? kwMatch[1] : '';

      if (hpVal && kwVal) {
        return `
          <div class="text-left w-full">
            <div class="flex items-baseline gap-1.5">
              <span class="text-base font-black text-primary">${hpVal}</span>
              <span class="text-xs font-bold text-muted uppercase">hp</span>
              <span class="text-xs font-semibold text-subtle">(${kwVal} kW)</span>
            </div>
            ${str.toLowerCase().includes('2 motor') || str.toLowerCase().includes('awd') ? '<div class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">2 Motor điện AWD</div>' : ''}
          </div>
        `;
      }
      return `<div class="font-extrabold text-sm text-primary text-left">${str}</div>`;
    }

    if (specType === 'range_compare') {
      const kmMatch = str.match(/(\d+[\.,]?\d*)\s*km/i);
      const noteMatch = str.match(/\((.+)\)/);
      if (kmMatch) {
        return `
          <div class="text-left w-full">
            <div class="flex items-baseline gap-1.5">
              <span class="text-base font-black text-primary">${kmMatch[1]}</span>
              <span class="text-xs font-bold text-muted uppercase">km</span>
            </div>
            ${noteMatch ? `<div class="text-[10px] font-semibold text-subtle mt-0.5">${noteMatch[1]}</div>` : ''}
          </div>
        `;
      }
    }

    if (specType === 'airbag_compare') {
      const match = str.match(/(\d+)\s*túi/i);
      const extra = str.includes('(') ? str.replace(/^[^\(]+/, '').replace(/[\(\)]/g, '') : '';
      if (match) {
        return `
          <div class="text-left w-full">
            <div class="flex items-baseline gap-1.5">
              <span class="text-base font-black text-primary">${match[1]}</span>
              <span class="text-xs font-bold text-muted">túi khí</span>
            </div>
            ${extra ? `<div class="text-[10px] font-semibold text-subtle mt-0.5 leading-snug">${extra}</div>` : ''}
          </div>
        `;
      }
    }

    return `
      <div class="font-semibold text-xs text-primary text-left leading-relaxed">
        ${str}
      </div>
    `;
  }

  /**
   * Master Value Formatter
   */
  function formatSpecValue(val, specType = 'text', isWinner = false) {
    if (!val || val === '—' || val === 'Chưa công bố' || (Array.isArray(val) && val.length === 0)) {
      return `<span class="text-subtle font-medium text-xs tracking-wide">—</span>`;
    }

    // Official Link
    if (specType === 'official_link') {
      const link = String(val).trim();
      return `
        <a href="${link}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-blue-500/10 hover:bg-blue-500/20 text-blue-600 dark:text-blue-400 text-xs font-bold border border-blue-500/30 transition-all active:scale-95">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
          <span>Xem tại VinFast</span>
        </a>
      `;
    }

    // Safety Acronym Badges
    if (specType === 'safety_acronym_badges') {
      return renderSafetyAcronyms(val);
    }

    // Trunk Breakdown
    if (specType === 'trunk_breakdown') {
      return renderTrunkBreakdown(val);
    }

    // Multiline List
    if (specType === 'bullet_list' || Array.isArray(val)) {
      const items = Array.isArray(val) ? val : String(val).split(';').map(p => p.trim()).filter(Boolean);
      if (items.length === 0) return `<span class="text-subtle text-xs">—</span>`;

      return `
        <div class="spec-bullet-list">
          ${items.map(item => renderBulletItem(item)).join('')}
        </div>
      `;
    }

    // Split Lines
    if (specType === 'split_lines') {
      return renderSplitLines(val);
    }

    // Badge style
    if (specType === 'badge') {
      const str = String(val);
      const isPositive = str.toLowerCase().includes('có') || str.toLowerCase().includes('awd') || str.toLowerCase().includes('rwd') || str.toLowerCase().includes('điện') || str.toLowerCase().includes('level') || str.toLowerCase().includes('chuẩn');
      const isNegative = str.toLowerCase().includes('không') || str.toLowerCase() === '—';
      
      return `
        <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold ${
          isNegative
            ? 'bg-slate-200 dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-300 dark:border-slate-700'
            : isPositive 
              ? 'bg-emerald-500/15 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400' 
              : 'bg-blue-500/15 border border-blue-500/30 text-blue-600 dark:text-blue-400'
        }">
          ${isPositive ? '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>' : ''}
          <span>${str}</span>
        </span>
      `;
    }

    // Auto-detect if string has multiple semicolon clauses
    if (typeof val === 'string' && (val.includes(';') || (val.match(/,/g) || []).length >= 2)) {
      return renderSplitLines(val);
    }

    // Default single metric
    return renderMetricValue(val, specType);
  }

  /**
   * Smart AI Summary Generator
   */
  function generateSmartSummary(cars) {
    if (!cars || cars.length < 2) {
      return {
        title: 'Chưa đủ dữ liệu so sánh',
        conclusion: 'Vui lòng chọn từ 2 xe trở lên để hệ thống phân tích chi tiết.',
        takeaways: []
      };
    }

    const takeaways = [];

    // Power
    const powerList = cars.map(c => {
      const pStr = c.specs?.cat3_powertrain?.maxPower || '';
      const kw = pStr.match(/(\d+)\s*kW/i);
      const hp = pStr.match(/(\d+)\s*hp/i);
      let num = 0;
      if (hp) num = parseInt(hp[1], 10);
      else if (kw) num = Math.round(parseInt(kw[1], 10) * 1.341);
      return { car: c, hp: num, text: pStr };
    }).sort((a, b) => b.hp - a.hp);

    if (powerList[0].hp > 0) {
      takeaways.push({
        icon: 'zap',
        color: 'emerald',
        title: 'Sức Mạnh & Khả Năng Tăng Tốc',
        content: `<strong>${powerList[0].car.shortName}</strong> dẫn đầu về công suất với <strong>${powerList[0].text}</strong>. Động cơ điện đạt mô-men xoắn tức thời cực đại, giúp bứt tốc êm ái, đầm chắc và vượt dốc thoát xe vượt trội.`
      });
    }

    // Range
    const rangeList = cars.map(c => {
      const rStr = c.specs?.cat3_powertrain?.range || '';
      const m = rStr.match(/(\d+)\s*km/i);
      return { car: c, km: m ? parseInt(m[1], 10) : 0, text: rStr };
    }).sort((a, b) => b.km - a.km);

    if (rangeList[0].km > 0) {
      takeaways.push({
        icon: 'battery-charging',
        color: 'blue',
        title: 'Tầm Vận Hành & Tốc Độ Sạc',
        content: `<strong>${rangeList[0].car.shortName}</strong> có cự ly di chuyển ấn tượng lên tới <strong>${rangeList[0].text}</strong> sau 1 lần sạc đầy. Công nghệ sạc siêu nhanh DC đạt 10% - 70% chỉ từ 24 - 36 phút tại 150.000+ cổng sạc V-GREEN phủ kín 63 tỉnh thành.`
      });
    }

    // Space / Wheelbase
    const wbList = cars.map(c => {
      const wbStr = c.specs?.cat1_dimensions?.wheelbase || '';
      const num = parseInt(wbStr.replace(/\D/g, ''), 10) || 0;
      return { car: c, num, text: wbStr };
    }).sort((a, b) => b.num - a.num);

    if (wbList[0].num > wbList[wbList.length - 1].num) {
      takeaways.push({
        icon: 'maximize-2',
        color: 'purple',
        title: 'Kích Thước & Trục Cơ Sở',
        content: `<strong>${wbList[0].car.shortName}</strong> sở hữu trục cơ sở dài nhất (<strong>${wbList[0].text} mm</strong>), mang lại không gian để chân rộng rãi tối ưu cho cả 2 hàng ghế.`
      });
    }

    // Economics & Cost
    takeaways.push({
      icon: 'trending-up',
      color: 'amber',
      title: 'Chi Phí Vận Hành & Bảo Hành',
      content: `Xe điện VinFast chỉ tốn khoảng <strong>300 - 450 đ/km</strong> tiền điện (rẻ hơn 3 - 4 lần xe xăng), miễn 100% lệ phí trước bạ và chính sách bảo hành chính hãng từ <strong>7 đến 10 năm</strong> vượt xa tiêu chuẩn ngành.`
    });

    return {
      title: `Phân tích so sánh giữa ${cars.map(c => c.shortName).join(' vs ')}`,
      conclusion: '100% dải sản phẩm thuần điện VinFast đều được trang bị khung gầm cứng vững tiêu chuẩn quốc tế, công nghệ trợ lái thông minh và hưởng hệ sinh thái trạm sạc lớn nhất Việt Nam.',
      takeaways
    };
  }

  let radarChartInstance = null;

  /**
   * Render Radar Chart matching active theme (Dark / Light)
   */
  function renderRadarChart(canvasId, cars, isDarkMode = true) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !window.Chart) return;

    if (radarChartInstance) {
      radarChartInstance.destroy();
      radarChartInstance = null;
    }

    if (!cars || cars.length === 0) return;

    const labels = [
      'Công Suất (HP)',
      'Không Gian & Cốp',
      'Tầm Di Chuyển',
      'An Toàn Tiêu Chuẩn',
      'Công Nghệ ADAS',
      'Hiệu Quả Kinh Tế'
    ];

    const colorPalette = [
      { border: '#3b82f6', bg: 'rgba(59, 130, 246, 0.25)' },
      { border: '#10b981', bg: 'rgba(16, 185, 129, 0.25)' },
      { border: '#f59e0b', bg: 'rgba(245, 158, 11, 0.25)' },
      { border: '#ec4899', bg: 'rgba(236, 72, 153, 0.25)' },
      { border: '#8b5cf6', bg: 'rgba(139, 92, 246, 0.25)' }
    ];

    const datasets = cars.map((car, idx) => {
      const palette = colorPalette[idx % colorPalette.length];
      const r = car.radar || { power: 70, space: 70, range: 70, safety: 70, tech: 70, economy: 80 };
      return {
        label: car.shortName,
        data: [r.power, r.space, r.range, r.safety, r.tech, r.economy],
        borderColor: palette.border,
        backgroundColor: palette.bg,
        borderWidth: 2.5,
        pointBackgroundColor: palette.border,
        pointBorderColor: '#ffffff',
        pointRadius: 4,
        pointHoverRadius: 6
      };
    });

    const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.08)';
    const textColor = isDarkMode ? '#cbd5e1' : '#334155';
    const pointLabelColor = isDarkMode ? '#f8fafc' : '#0f172a';

    const ctx = canvas.getContext('2d');
    radarChartInstance = new window.Chart(ctx, {
      type: 'radar',
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: textColor,
              boxWidth: 12,
              font: { size: 11, weight: 'bold', family: "'Plus Jakarta Sans', sans-serif" },
              padding: 12
            }
          },
          tooltip: {
            backgroundColor: isDarkMode ? '#1e293b' : '#ffffff',
            titleColor: isDarkMode ? '#ffffff' : '#0f172a',
            bodyColor: isDarkMode ? '#cbd5e1' : '#334155',
            borderColor: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : '#cbd5e1',
            borderWidth: 1,
            padding: 10,
            cornerRadius: 10
          }
        },
        scales: {
          r: {
            min: 30,
            max: 100,
            ticks: {
              stepSize: 20,
              display: false
            },
            grid: {
              color: gridColor
            },
            angleLines: {
              color: gridColor
            },
            pointLabels: {
              color: pointLabelColor,
              font: {
                size: 11,
                weight: '700',
                family: "'Plus Jakarta Sans', sans-serif"
              }
            }
          }
        }
      }
    });
  }

  return {
    SPEC_CATEGORIES,
    analyzeDifferences,
    formatSpecValue,
    generateSmartSummary,
    renderRadarChart
  };

})();
