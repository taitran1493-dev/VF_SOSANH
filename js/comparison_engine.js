/**
 * Comparison Engine for VinFast Smart Car Comparison Platform
 * Highly structured 9 categories with atomic specs, smart difference detection,
 * and intelligent multi-line formatting that breaks long grouped specs into clean,
 * readable bullet points and interactive tags.
 */

window.ComparisonEngine = (function () {
  'use strict';

  const SPEC_CATEGORIES = [
    {
      id: 'cat1_dimensions',
      title: 'I. KÍCH THƯỚC & TRỌNG LƯỢNG',
      icon: 'maximize-2',
      specs: [
        { key: 'd_r_c', label: 'Dài x Rộng x Cao (mm)', type: 'dimension' },
        { key: 'wheelbase', label: 'Chiều dài cơ sở (mm)', type: 'number_higher_better' },
        { key: 'groundClearance', label: 'Khoảng sáng gầm xe không tải (mm)', type: 'number_higher_better' },
        { key: 'turningRadius', label: 'Bán kính quay đầu tối thiểu (m)', type: 'number_lower_better' },
        { key: 'weight', label: 'Trọng lượng không tải (kg)', type: 'split_lines' },
        { key: 'payload', label: 'Tải trọng chở hàng / người (kg)', type: 'split_lines' },
        { key: 'trunk', label: 'Dung tích khoang hành lý / cốp xe', type: 'trunk_breakdown' },
        { key: 'cargoBed', label: 'Kích thước thùng hàng / khoang chứa', type: 'split_lines' }
      ]
    },
    {
      id: 'cat2_engine',
      title: 'II. HIỆU SUẤT & ĐỘNG CƠ',
      icon: 'zap',
      specs: [
        { key: 'engineType', label: 'Loại động cơ / Số motor', type: 'text' },
        { key: 'drivetrain', label: 'Hệ dẫn động', type: 'badge' },
        { key: 'maxPower', label: 'Công suất tối đa', type: 'power_compare' },
        { key: 'maxTorque', label: 'Mô-men xoắn cực đại (Nm)', type: 'text' },
        { key: 'acceleration', label: 'Tăng tốc 0–100 km/h (s)', type: 'accel_compare' },
        { key: 'maxSpeed', label: 'Tốc độ tối đa (km/h)', type: 'split_lines' },
        { key: 'driveModes', label: 'Chế độ lái', type: 'badge_list' },
        { key: 'suspension', label: 'Hệ thống treo trước / sau', type: 'split_lines' },
        { key: 'waterWading', label: 'Khả năng lội nước', type: 'text' }
      ]
    },
    {
      id: 'cat3_battery',
      title: 'III. PIN & SẠC ĐIỆN',
      icon: 'battery-charging',
      specs: [
        { key: 'batteryType', label: 'Loại pin công nghệ', type: 'split_lines' },
        { key: 'batteryCapacity', label: 'Dung lượng pin khả dụng', type: 'text' },
        { key: 'range', label: 'Quãng đường di chuyển / 1 lần sạc', type: 'range_compare' },
        { key: 'fastChargeTime', label: 'Thời gian sạc nhanh nhất (10% - 70%)', type: 'split_lines' },
        { key: 'acCharge', label: 'Công suất sạc AC', type: 'text' },
        { key: 'dcCharge', label: 'Công suất sạc DC tối đa', type: 'text' },
        { key: 'regenBraking', label: 'Hệ thống phanh tái sinh', type: 'badge' },
        { key: 'v2l', label: 'Cấp điện ngoài V2L (Vehicle-to-Load)', type: 'badge' }
      ]
    },
    {
      id: 'cat4_exterior',
      title: 'IV. NGOẠI THẤT & TRANG BỊ NGOÀI',
      icon: 'sparkles',
      specs: [
        { key: 'headlights', label: 'Đèn chiếu sáng phía trước', type: 'split_lines' },
        { key: 'wheels', label: 'Mâm & Lốp (La-zăng)', type: 'split_lines' },
        { key: 'mirrors', label: 'Gương chiếu hậu ngoài', type: 'split_lines' },
        { key: 'wipers', label: 'Gạt mưa trước', type: 'text' },
        { key: 'tailgate', label: 'Cốp sau (Đóng / mở)', type: 'badge' },
        { key: 'exteriorList', label: 'Trang bị ngoại thất chi tiết', type: 'bullet_list' }
      ]
    },
    {
      id: 'cat5_interior',
      title: 'V. NỘI THẤT & TIỆN NGHI CABIN',
      icon: 'layout',
      specs: [
        { key: 'seating', label: 'Số chỗ ngồi & Chất liệu ghế', type: 'split_lines' },
        { key: 'frontSeats', label: 'Ghế lái & Ghế phụ', type: 'split_lines' },
        { key: 'rearSeats', label: 'Hàng ghế sau / Ghế VIP', type: 'split_lines' },
        { key: 'infotainment', label: 'Màn hình giải trí cảm ứng', type: 'text' },
        { key: 'hud', label: 'Màn hình HUD kính lái', type: 'badge' },
        { key: 'sound', label: 'Hệ thống âm thanh / Loa', type: 'split_lines' },
        { key: 'climate', label: 'Điều hòa & Lọc bụi Combi 1.0', type: 'split_lines' },
        { key: 'shifter', label: 'Cần số & Phanh đỗ điện tử', type: 'split_lines' },
        { key: 'interiorList', label: 'Tiện nghi cabin chi tiết', type: 'bullet_list' }
      ]
    },
    {
      id: 'cat6_safety',
      title: 'VI. AN TOÀN TIÊU CHUẨN',
      icon: 'shield-check',
      specs: [
        { key: 'airbags', label: 'Số túi khí an toàn', type: 'airbag_compare' },
        { key: 'standardSafety', label: 'Hệ thống phanh & Cân bằng điện tử', type: 'safety_acronym_badges' },
        { key: 'safetyList', label: 'Danh mục an toàn tiêu chuẩn', type: 'bullet_list' }
      ]
    },
    {
      id: 'cat7_adas',
      title: 'VII. HỆ THỐNG TRỢ LÁI NÂNG CAO (ADAS)',
      icon: 'cpu',
      specs: [
        { key: 'adasSummary', label: 'Tổng quan gói trợ lái', type: 'badge' },
        { key: 'adasList', label: 'Chi tiết các tính năng ADAS', type: 'adas_badges' }
      ]
    },
    {
      id: 'cat8_economics',
      title: 'VIII. CHI PHÍ VẬN HÀNH & BẢO HÀNH',
      icon: 'trending-up',
      specs: [
        { key: 'fuelCost1000km', label: 'Chi phí nhiên liệu / 1.000 km', type: 'text' },
        { key: 'maintenance', label: 'Chi phí bảo dưỡng định kỳ', type: 'split_lines' },
        { key: 'warranty', label: 'Chính sách bảo hành chính hãng', type: 'split_lines' }
      ]
    },
    {
      id: 'cat9_reference',
      title: 'IX. HỒ SƠ BROCHURE KIỂM CHỨNG',
      icon: 'file-check',
      specs: [
        { key: 'source', label: 'Tài liệu Catalogue / Brochure', type: 'text' }
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

    // Winner detection
    let bestIndex = -1;

    // Power
    if (specKey === 'maxPower') {
      let maxHp = -1;
      cars.forEach((c, idx) => {
        const val = String(values[idx]);
        const hpMatch = val.match(/(\d+)\s*hp/i);
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
    // Acceleration (lower is better)
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
    // Airbags
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
    // Range
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
    // Wheelbase / Ground clearance
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
    // ADAS Count
    else if (specKey === 'adasList') {
      let maxCount = 0;
      cars.forEach((c, idx) => {
        const list = Array.isArray(values[idx]) ? values[idx] : [];
        if (list.length > maxCount) {
          maxCount = list.length;
          bestIndex = idx;
        }
      });
    }

    return { isDifferent, values, bestIndex };
  }

  /**
   * Helper: Split string avoiding cutting inside parentheses
   */
  function splitRespectingParens(text) {
    if (!text || text === '—') return [];
    // Split by semicolons, or commas outside parens, or slashes outside parens
    const parts = text.split(/[,;\n]+(?![^\(]*\))/).map(p => p.trim()).filter(Boolean);
    return parts;
  }

  /**
   * 1. Render Safety Acronyms (ABS, EBD, BA, ESC, TCS, HSA, ROM, ESS, dTPMS, AutoHold)
   */
  function renderSafetyAcronyms(val) {
    const str = String(val);
    if (!str || str === '—') return `<span class="text-subtle font-medium text-xs">—</span>`;

    // Extract any descriptive header before parenthesis
    let headerText = '';
    const headerMatch = str.match(/^([^\(]+)\s*\((.+)\)$/);
    let acronymsStr = str;

    if (headerMatch) {
      headerText = headerMatch[1].trim();
      acronymsStr = headerMatch[2].trim();
    }

    // Known acronym list or extract capitalized tokens
    const tokens = acronymsStr.split(/[,;\/\s]+/).map(t => t.trim()).filter(Boolean);
    const validAcronyms = tokens.filter(t => /^[A-Z0-9\+\-]+$/i.test(t) && t.length >= 2);

    if (validAcronyms.length === 0) {
      return renderSplitLines(str);
    }

    return `
      <div class="flex flex-col gap-2 w-full text-left">
        ${headerText ? `
          <div class="text-xs font-bold text-primary flex items-center gap-1.5 leading-snug">
            <svg class="w-3.5 h-3.5 text-blue-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            <span>${headerText}</span>
          </div>
        ` : ''}
        <div class="flex flex-wrap gap-1.5 pt-0.5">
          ${validAcronyms.map(ac => `<span class="spec-tag">${ac}</span>`).join('')}
        </div>
      </div>
    `;
  }

  /**
   * 2. Render Trunk Breakdown
   */
  function renderTrunkBreakdown(val) {
    const str = String(val);
    if (!str || str === '—') return `<span class="text-subtle font-medium text-xs">—</span>`;

    // Case 1: "36 L / 285 L"
    if (str.includes('/')) {
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

    // Case 2: "376 L (tăng lên 1.373 L khi gập hàng ghế thứ 2)"
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
          // If part has colon like "Ghế lái: Chỉnh điện 12 hướng"
          const colonIdx = part.indexOf(':');
          if (colonIdx > 0 && colonIdx < 30) {
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

    // Check for label prefix with colon (e.g. "Đèn pha: Halogen")
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

    // Dimension: 4.545 x 1.890 x 1.635 mm
    if (specType === 'dimension') {
      return `
        <div class="font-extrabold text-sm text-primary text-left tracking-tight">
          ${str}
        </div>
      `;
    }

    // Power: "150 kW / 201 hp" or "300 kW (402 hp)"
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
            ${str.toLowerCase().includes('2 motor') ? '<div class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">2 Motor điện AWD</div>' : ''}
          </div>
        `;
      }
      return `<div class="font-extrabold text-sm text-primary text-left">${str}</div>`;
    }

    // Range: "215 km (NEDC)" or "450 km"
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

    // Airbags
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

    // Default
    return `
      <div class="font-semibold text-xs text-primary text-left leading-relaxed">
        ${str}
      </div>
    `;
  }

  /**
   * Master Value Formatter: breaks long multi-item specs into clean bullet lines & badges
   */
  function formatSpecValue(val, specType = 'text', isWinner = false) {
    if (!val || val === '—' || val === 'Chưa công bố' || (Array.isArray(val) && val.length === 0)) {
      return `<span class="text-subtle font-medium text-xs tracking-wide">—</span>`;
    }

    // 1. Safety Acronym Badges
    if (specType === 'safety_acronym_badges') {
      return renderSafetyAcronyms(val);
    }

    // 2. ADAS Badges grid
    if (specType === 'adas_badges' || (Array.isArray(val) && specType === 'adas')) {
      const items = Array.isArray(val) ? val : String(val).split(/[,;]+/);
      const cleanItems = items.map(i => i.trim()).filter(Boolean);
      if (cleanItems.length === 0) return `<span class="text-subtle text-xs">—</span>`;

      return `
        <div class="flex flex-col gap-1.5 text-left w-full">
          ${cleanItems.map(item => `
            <div class="flex items-start gap-2 p-2 rounded-xl bg-blue-500/10 dark:bg-blue-500/15 border border-blue-500/20 text-xs font-semibold text-blue-700 dark:text-blue-300 leading-snug">
              <svg class="w-3.5 h-3.5 text-blue-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
              <span>${item}</span>
            </div>
          `).join('')}
        </div>
      `;
    }

    // 3. Trunk Breakdown
    if (specType === 'trunk_breakdown' || (typeof val === 'string' && (val.includes('/') || val.toLowerCase().includes('khi gập') || val.toLowerCase().includes('cốp xe')))) {
      return renderTrunkBreakdown(val);
    }

    // 4. Multiline List (Array or semicolon separated)
    if (specType === 'bullet_list' || Array.isArray(val)) {
      const items = Array.isArray(val) ? val : String(val).split(';').map(p => p.trim()).filter(Boolean);
      // Filter out redundant giant ADAS blocks from safety list
      const filtered = items.filter(it => !it.toLowerCase().startsWith('adas') && !it.toLowerCase().startsWith('trợ lái'));
      const renderItems = filtered.length > 0 ? filtered : items;
      if (renderItems.length === 0) return `<span class="text-subtle text-xs">—</span>`;

      return `
        <div class="spec-bullet-list">
          ${renderItems.map(item => renderBulletItem(item)).join('')}
        </div>
      `;
    }

    // 5. Split Lines
    if (specType === 'split_lines') {
      return renderSplitLines(val);
    }

    // 6. Badge style
    if (specType === 'badge') {
      const str = String(val);
      const isPositive = str.toLowerCase().includes('có') || str.toLowerCase().includes('awd') || str.toLowerCase().includes('rwd') || str.toLowerCase().includes('điện');
      return `
        <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold ${
          isPositive 
            ? 'bg-emerald-500/15 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400' 
            : 'bg-slate-200 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300'
        }">
          ${isPositive ? '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>' : ''}
          <span>${str}</span>
        </span>
      `;
    }

    // 7. Drive modes (badge list)
    if (specType === 'badge_list') {
      const str = String(val);
      if (str.includes('/')) {
        const modes = str.split('/').map(m => m.trim()).filter(Boolean);
        return `
          <div class="flex flex-wrap gap-1.5 text-left">
            ${modes.map(m => `<span class="spec-tag">${m}</span>`).join('')}
          </div>
        `;
      }
      return `<div class="font-semibold text-xs text-primary text-left">${str}</div>`;
    }

    // 8. Auto-detect if string has multiple comma-separated clauses outside parens
    if (typeof val === 'string' && (val.includes(';') || (val.match(/,/g) || []).length >= 2)) {
      return renderSplitLines(val);
    }

    // 9. Default single metric
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
      const pStr = c.specs?.cat2_engine?.maxPower || '';
      const kw = pStr.match(/(\d+)\s*kW/i);
      const hp = pStr.match(/(\d+)\s*hp/i);
      let num = 0;
      if (hp) num = parseInt(hp[1], 10);
      else if (kw) num = Math.round(parseInt(kw[1], 10) * 1.341);
      return { car: c, hp: num, text: pStr };
    }).sort((a, b) => b.hp - a.hp);

    if (powerList[0].hp > powerList[powerList.length - 1].hp) {
      takeaways.push({
        icon: 'zap',
        color: 'emerald',
        title: 'Sức Mạnh & Khả Năng Tăng Tốc',
        content: `<strong>${powerList[0].car.shortName}</strong> dẫn đầu về công suất với <strong>${powerList[0].text}</strong>. ${
          powerList[0].car.fuelType.includes('Điện') 
            ? 'Động cơ điện cho mô-men xoắn tức thời cực đại, giúp xe bốc và vượt dốc cực kỳ thoát xe.' 
            : 'Động cơ đốt trong truyền thống.'
        }`
      });
    }

    // Range
    const rangeList = cars.map(c => {
      const rStr = c.specs?.cat3_battery?.range || '';
      const m = rStr.match(/(\d+)\s*km/i);
      return { car: c, km: m ? parseInt(m[1], 10) : 0, text: rStr };
    }).sort((a, b) => b.km - a.km);

    if (rangeList[0].km > 0) {
      takeaways.push({
        icon: 'battery-charging',
        color: 'blue',
        title: 'Tầm Vận Hành & Tốc Độ Sạc',
        content: `<strong>${rangeList[0].car.shortName}</strong> có tầm di chuyển lên tới <strong>${rangeList[0].text}</strong> sau 1 lần sạc đầy. Sạc siêu nhanh DC từ 10% đến 70% chỉ trong 25 - 36 phút tại hơn 150.000 cổng sạc V-GREEN phủ khắp toàn quốc.`
      });
    }

    // Space
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
        content: `<strong>${wbList[0].car.shortName}</strong> sở hữu chiều dài cơ sở ấn tượng nhất (<strong>${wbList[0].text}</strong>), tạo nên khoang để chân hàng ghế sau rộng rãi nhất trong phân khúc so sánh.`
      });
    }

    // Cost & Fuel Efficiency
    const hasEV = cars.some(c => c.fuelType.includes('Điện'));
    const hasICE = cars.some(c => c.fuelType.includes('Xăng'));

    if (hasEV && hasICE) {
      takeaways.push({
        icon: 'trending-up',
        color: 'emerald',
        title: 'Chi Phí Vận Hành (Điện vs Xăng)',
        content: `Xe điện VinFast chỉ tốn khoảng <strong>300 - 450 đ/km</strong> chi phí sạc pin, trong khi xe xăng cùng cỡ tiêu tốn từ <strong>1.300 - 1.650 đ/km</strong>. Trung bình mỗi năm chạy 18.000 km, xe điện giúp tiết kiệm từ <strong>18 - 25 triệu VNĐ</strong>.`
      });
    }

    return {
      title: `Phân tích so sánh giữa ${cars.map(c => c.shortName).join(' vs ')}`,
      conclusion: hasEV && hasICE
        ? 'Dòng xe thuần điện VinFast vượt trội hoàn toàn về công suất tức thời, chi phí nhiên liệu rẻ hơn gấp 3 lần và bảo hành tới 10 năm.'
        : 'Mỗi phiên bản đều có ưu thế riêng về trang bị công nghệ, tầm hoạt động và mức giá tương ứng với nhu cầu sử dụng.',
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
