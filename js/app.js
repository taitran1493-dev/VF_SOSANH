/**
 * Main Application Controller for VinFast Smart Car Comparison Platform
 * Pure 100% Official VinFast Portfolio (15 Models, 19 Variants)
 * Apple Design UI/UX • Tactile Feedback • High-Contrast Readability
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // State (Default: Pure Light Mode, Focus on VF 3 & VF 8 Lineup)
  const state = {
    selectedCarIds: ['vf3_eco', 'vf3_plus', 'vf8_eco', 'vf8_plus'],
    showDiffOnly: false,
    highlightAdvantages: true,
    searchQuery: '',
    selectedCategory: 'all',
    isDarkMode: false,
    carColorOverrides: {},
    modalTargetIndex: -1 // Index of car slot to replace or -1 for append
  };

  // DOM Elements
  const els = {
    carsHeaderRow: document.getElementById('cars-header-row'),
    specsContainer: document.getElementById('specs-container'),
    diffOnlyToggle: document.getElementById('toggle-diff-only'),
    highlightToggle: document.getElementById('toggle-highlight'),
    specSearchInput: document.getElementById('spec-search-input'),
    btnExportPng: document.getElementById('btn-export-png'),
    btnExportPdf: document.getElementById('btn-export-pdf'),
    btnShare: document.getElementById('btn-share-link'),
    btnThemeToggle: document.getElementById('btn-theme-toggle'),
    presetPills: document.getElementById('preset-pills'),
    smartSummaryContainer: document.getElementById('smart-summary-container'),
    vehicleSelectorModal: document.getElementById('vehicle-selector-modal'),
    closeVehicleModal: document.getElementById('btn-close-vehicle-modal'),
    modalCarList: document.getElementById('modal-car-list'),
    modalSearchInput: document.getElementById('modal-search-input'),
    modalSegmentTabs: document.getElementById('modal-segment-tabs')
  };

  // Parse URL params
  function parseUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const carsParam = params.get('cars');
    if (carsParam) {
      const ids = carsParam.split(',').filter(id => window.CARS_DATABASE.some(c => c.id === id));
      if (ids.length >= 1) {
        state.selectedCarIds = ids.slice(0, 5);
      }
    }
  }

  function updateUrlParams() {
    const url = new URL(window.location);
    url.searchParams.set('cars', state.selectedCarIds.join(','));
    window.history.replaceState({}, '', url);
  }

  function getSelectedCars() {
    return state.selectedCarIds.map(id => {
      const car = window.CARS_DATABASE.find(c => c.id === id);
      if (!car) return null;
      const clone = JSON.parse(JSON.stringify(car));
      if (state.carColorOverrides[car.id]) {
        clone.image = state.carColorOverrides[car.id];
      }
      return clone;
    }).filter(Boolean);
  }

  /**
   * Render Top Car Header Cards with Apple Frosted Acrylic & Micro-Interactions
   */
  function renderCarHeaders() {
    const cars = getSelectedCars();
    const canAddMore = cars.length < 5;

    let html = '';
    cars.forEach((car, index) => {
      const colors = car.colors || [];
      const currentColorImg = car.image;

      let colorChipsHtml = '';
      if (colors.length > 0) {
        colorChipsHtml = `
          <div class="mt-2.5 flex items-center justify-center gap-1.5 flex-wrap">
            <span class="text-[10px] text-[var(--text-muted)] font-bold mr-1">Màu sơn:</span>
            ${colors.map(col => `
              <button 
                class="color-chip w-4 h-4 rounded-full border border-slate-400/60 shadow-sm ${col.image === currentColorImg ? 'active' : ''}" 
                style="background-color: ${col.hex};" 
                title="${col.name}" 
                data-car-id="${car.id}" 
                data-color-img="${col.image}">
              </button>
            `).join('')}
          </div>
        `;
      }

      html += `
        <div class="flex-1 min-w-[260px] max-w-[360px] theme-card rounded-3xl p-5 relative group transition-all duration-300 flex flex-col justify-between">
          <!-- Top controls -->
          <div class="flex items-center justify-between mb-2">
            <span class="text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full bg-blue-500/15 text-blue-600 dark:text-blue-400 border border-blue-500/25">${car.segment.split('(')[0].trim()}</span>
            <div class="flex items-center gap-1">
              <button class="btn-change-car p-1.5 rounded-xl text-[var(--text-muted)] hover:text-blue-500 hover:bg-[var(--row-hover)] transition" title="Đổi xe khác" data-slot-index="${index}">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
              </button>
              ${cars.length > 1 ? `
                <button class="btn-remove-car p-1.5 rounded-xl text-[var(--text-muted)] hover:text-rose-500 hover:bg-[var(--row-hover)] transition" title="Bỏ xe này" data-car-id="${car.id}">
                  <i data-lucide="x" class="w-3.5 h-3.5"></i>
                </button>
              ` : ''}
            </div>
          </div>

          <!-- Name & Price -->
          <div class="text-center mb-2">
            <h3 class="text-lg font-black text-[var(--text-primary)] tracking-tight leading-snug">${car.name}</h3>
            <div class="text-base font-extrabold text-emerald-600 dark:text-emerald-400 mt-0.5">${car.priceText}</div>
            <div class="text-[11px] font-medium text-[var(--text-muted)]">${car.batteryFeeText || car.fuelType}</div>
          </div>

          <!-- Car Image -->
          <div class="relative w-full h-36 flex items-center justify-center my-2 p-1 overflow-hidden group-hover:scale-105 transition-transform duration-300">
            <img src="${car.image}" alt="${car.name}" class="max-h-full max-w-full object-contain filter drop-shadow-xl" loading="lazy" />
          </div>

          <!-- Color Selector -->
          ${colorChipsHtml}

          <!-- Highlights & Official Link -->
          <div class="mt-4 pt-3 border-t border-[var(--border-subtle)]">
            <div class="text-[11px] font-bold text-[var(--text-muted)] uppercase tracking-wider mb-1.5 flex items-center gap-1">
              <i data-lucide="sparkles" class="w-3 h-3 text-amber-500"></i>
              <span>Điểm nhấn nổi bật</span>
            </div>
            <ul class="text-xs space-y-1 text-[var(--text-secondary)]">
              ${(car.highlights || []).slice(0, 2).map(h => `
                <li class="flex items-start gap-1.5 leading-snug">
                  <span class="text-blue-500 font-bold">•</span>
                  <span>${h}</span>
                </li>
              `).join('')}
            </ul>
            ${car.officialLink ? `
              <div class="mt-2.5 pt-2 border-t border-[var(--border-subtle)] flex items-center justify-between text-[11px]">
                <a href="${car.officialLink}" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-cyan-400 font-semibold hover:underline flex items-center gap-1">
                  <i data-lucide="external-link" class="w-3 h-3"></i>
                  <span>Trang chủ VinFast</span>
                </a>
                <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">100% Thuần Điện</span>
              </div>
            ` : ''}
          </div>
        </div>
      `;
    });

    // Add Vehicle Button
    if (canAddMore) {
      html += `
        <button id="btn-open-add-car" class="min-w-[200px] flex-1 max-w-[260px] border-2 border-dashed border-[var(--border-medium)] rounded-3xl p-6 flex flex-col items-center justify-center text-[var(--text-muted)] hover:text-blue-500 hover:border-blue-500 hover:bg-blue-500/5 transition-all duration-300 group">
          <div class="w-12 h-12 rounded-2xl bg-[var(--surface-card)] group-hover:bg-blue-500/15 text-[var(--text-muted)] group-hover:text-blue-500 flex items-center justify-center transition-all duration-300 mb-3 shadow-md border border-[var(--border-subtle)]">
            <i data-lucide="plus" class="w-6 h-6"></i>
          </div>
          <span class="text-sm font-bold text-[var(--text-primary)] group-hover:text-blue-500">Thêm xe so sánh</span>
          <span class="text-xs text-[var(--text-muted)] mt-1">So sánh tối đa 5 xe</span>
        </button>
      `;
    }

    els.carsHeaderRow.innerHTML = html;

    // Attach color chip listeners
    els.carsHeaderRow.querySelectorAll('.color-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const carId = chip.dataset.carId;
        const colorImg = chip.dataset.colorImg;
        if (carId && colorImg) {
          state.carColorOverrides[carId] = colorImg;
          renderAll();
        }
      });
    });

    // Attach remove car listeners
    els.carsHeaderRow.querySelectorAll('.btn-remove-car').forEach(btn => {
      btn.addEventListener('click', () => {
        const carId = btn.dataset.carId;
        state.selectedCarIds = state.selectedCarIds.filter(id => id !== carId);
        updateUrlParams();
        renderAll();
      });
    });

    // Attach change car listeners
    els.carsHeaderRow.querySelectorAll('.btn-change-car').forEach(btn => {
      btn.addEventListener('click', () => {
        const slotIdx = parseInt(btn.dataset.slotIndex, 10);
        openVehicleModal(slotIdx);
      });
    });

    // Attach add car button
    const addBtn = document.getElementById('btn-open-add-car');
    if (addBtn) {
      addBtn.addEventListener('click', () => openVehicleModal(-1));
    }
  }

  /**
   * Render Floating Sticky Compare Bar
   */
  function renderStickyCompareBar() {
    const cars = getSelectedCars();
    const container = document.getElementById('sticky-cars-row');
    const diffCounter = document.getElementById('sticky-diff-counter');
    if (!container) return;

    if (diffCounter) {
      diffCounter.textContent = `${cars.length} XE ĐANG SO SÁNH`;
    }

    container.innerHTML = cars.map(car => `
      <div class="flex items-center gap-2.5 px-3 py-1.5 rounded-2xl bg-[var(--surface-card)] border border-[var(--border-subtle)] min-w-[200px] flex-shrink-0 shadow-sm">
        <div class="w-8 h-8 rounded-lg bg-[var(--bg-subtle)] p-0.5 flex items-center justify-center flex-shrink-0">
          <img src="${car.image}" alt="${car.name}" class="max-h-full max-w-full object-contain" />
        </div>
        <div class="truncate">
          <div class="text-xs font-bold text-[var(--text-primary)] truncate">${car.shortName}</div>
          <div class="text-[10px] font-extrabold text-emerald-600 dark:text-emerald-400">${car.priceText.replace(' VNĐ', '')}</div>
        </div>
      </div>
    `).join('');
  }

  function handleScroll() {
    const stickyBar = document.getElementById('sticky-compare-bar');
    const targetSection = document.getElementById('car-selection-section');
    if (!stickyBar || !targetSection) return;

    const rect = targetSection.getBoundingClientRect();
    if (rect.bottom < 80) {
      stickyBar.classList.remove('is-hidden');
      stickyBar.classList.add('is-visible');
    } else {
      stickyBar.classList.remove('is-visible');
      stickyBar.classList.add('is-hidden');
    }
  }

  /**
   * Render Main Specs Table with 7 Official Categories
   */
  function renderSpecsTable() {
    const cars = getSelectedCars();
    const categories = window.ComparisonEngine.SPEC_CATEGORIES;
    const query = state.searchQuery.toLowerCase().trim();

    let html = '';

    categories.forEach(cat => {
      // Filter specs if searching
      const filteredSpecs = cat.specs.filter(spec => {
        if (!query) return true;
        if (spec.label.toLowerCase().includes(query)) return true;
        return cars.some(car => {
          const val = car.specs?.[cat.id]?.[spec.key];
          if (!val) return false;
          if (Array.isArray(val)) return val.some(v => String(v).toLowerCase().includes(query));
          return String(val).toLowerCase().includes(query);
        });
      });

      if (filteredSpecs.length === 0) return;

      let rowsHtml = '';
      let visibleRowCount = 0;

      filteredSpecs.forEach(spec => {
        const diffInfo = window.ComparisonEngine.analyzeDifferences(cars, cat.id, spec.key);

        if (state.showDiffOnly && !diffInfo.isDifferent) {
          return;
        }

        visibleRowCount++;
        const rowBgClass = (visibleRowCount % 2 === 0) ? 'table-row-even' : 'table-row-odd';

        let colsHtml = '';
        cars.forEach((car, idx) => {
          const rawVal = diffInfo.values[idx];
          const isWinner = state.highlightAdvantages && diffInfo.bestIndex === idx;

          const formattedHtml = window.ComparisonEngine.formatSpecValue(rawVal, spec.type, isWinner);

          colsHtml += `
            <div class="flex-1 min-w-[240px] md:min-w-[280px] p-4 text-left flex flex-col items-start justify-start border-l border-[var(--border-subtle)] ${
              isWinner ? 'bg-emerald-500/10' : ''
            }">
              <div class="w-full flex flex-col items-start gap-1.5">
                ${formattedHtml}
                ${isWinner ? `
                  <span class="winner-badge mt-2">
                    <i data-lucide="check" class="w-3 h-3"></i>
                    <span>Tối ưu nhất</span>
                  </span>
                ` : ''}
              </div>
            </div>
          `;
        });

        rowsHtml += `
          <div class="diff-row ${rowBgClass} flex items-stretch border-b border-[var(--border-subtle)] transition-colors ${diffInfo.isDifferent ? 'is-diff' : ''}">
            <div class="w-72 md:w-80 p-4 text-xs font-black flex items-center justify-between gap-2 sticky-col z-10">
              <span class="tracking-tight text-[var(--text-primary)] font-bold">${spec.label}</span>
              ${diffInfo.isDifferent ? `
                <span class="diff-badge flex-shrink-0" title="Có sự chênh lệch giữa các xe">
                  Khác biệt
                </span>
              ` : ''}
            </div>
            ${colsHtml}
          </div>
        `;
      });

      if (visibleRowCount > 0) {
        html += `
          <div class="mb-8 rounded-3xl overflow-hidden border border-[var(--border-subtle)] bg-[var(--surface-card)] shadow-xl">
            <!-- Category Header -->
            <div class="bg-[var(--surface-table-header)] px-6 py-3.5 border-b border-[var(--border-subtle)] flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-xl bg-blue-500/15 text-blue-500 flex items-center justify-center shadow-sm">
                  <i data-lucide="${cat.icon}" class="w-4 h-4"></i>
                </div>
                <h3 class="text-xs font-black uppercase tracking-wider text-[var(--text-primary)]">${cat.title}</h3>
              </div>
              <span class="text-[11px] font-bold text-[var(--text-muted)]">${visibleRowCount} mục thông số</span>
            </div>
            <!-- Rows -->
            <div class="overflow-x-auto">
              ${rowsHtml}
            </div>
          </div>
        `;
      }
    });

    if (!html) {
      html = `
        <div class="p-12 text-center text-[var(--text-muted)] bg-[var(--surface-card)] rounded-3xl border border-[var(--border-subtle)]">
          <i data-lucide="search-x" class="w-12 h-12 mx-auto text-[var(--text-subtle)] mb-3"></i>
          <p class="text-base font-semibold text-[var(--text-primary)]">Không tìm thấy thông số nào phù hợp</p>
          <p class="text-xs text-[var(--text-muted)] mt-1">Hãy thử xóa bộ lọc tìm kiếm hoặc tắt chế độ "Chỉ hiện điểm khác biệt".</p>
        </div>
      `;
    }

    els.specsContainer.innerHTML = html;
  }

  /**
   * Render Smart AI Summary
   */
  function renderSmartSummary() {
    const cars = getSelectedCars();
    const summary = window.ComparisonEngine.generateSmartSummary(cars);

    let html = `
      <div class="theme-card rounded-3xl p-6 lg:p-8 mb-8 relative overflow-hidden">
        <!-- Top Title -->
        <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-6 border-b border-[var(--border-subtle)] gap-4">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <i data-lucide="cpu" class="w-5 h-5 text-white"></i>
            </div>
            <div>
              <div class="text-[10px] font-extrabold uppercase tracking-widest text-blue-500">SMART ANALYSIS ENGINE • MASTER PORTFOLIO</div>
              <h2 class="text-xl font-black text-[var(--text-primary)]">${summary.title}</h2>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="flex h-2.5 w-2.5 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span class="text-xs font-semibold text-emerald-600 dark:text-emerald-400">100% Thuần Điện VinFast</span>
          </div>
        </div>

        <!-- Takeaway Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          ${summary.takeaways.map(t => `
            <div class="p-4 rounded-2xl bg-[var(--bg-subtle)] border border-[var(--border-subtle)]">
              <div class="flex items-center gap-2.5 mb-2">
                <div class="w-6 h-6 rounded-lg bg-${t.color}-500/20 text-${t.color}-500 flex items-center justify-center">
                  <i data-lucide="${t.icon}" class="w-3.5 h-3.5"></i>
                </div>
                <h4 class="text-xs font-bold text-[var(--text-primary)] uppercase tracking-wide">${t.title}</h4>
              </div>
              <p class="text-xs text-[var(--text-secondary)] leading-relaxed">${t.content}</p>
            </div>
          `).join('')}
        </div>

        <!-- Conclusion -->
        <div class="p-4 rounded-2xl bg-blue-500/10 border border-blue-500/25 flex items-start gap-3">
          <i data-lucide="lightbulb" class="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5"></i>
          <div class="text-xs text-[var(--text-primary)] leading-relaxed">
            ${summary.conclusion}
          </div>
        </div>
      </div>
    `;

    els.smartSummaryContainer.innerHTML = html;
  }

  /**
   * Render Preset Quick Comparison Scenarios (Curated for the 15 official VinFast models & variants)
   */
  function renderPresets() {
    const presets = [
      {
        label: '⚡ VF 3: Eco vs Plus',
        desc: 'Mâm thép đen vs Mâm ốp khí động học, camera lùi, gương chỉnh điện',
        carIds: ['vf3_eco', 'vf3_plus']
      },
      {
        label: '👑 VF 8: Eco vs Plus vs All-New 2026',
        desc: 'Mâm 19" (349 hp) vs Mâm 20" (402 hp) vs Thế Hệ Mới 2026',
        carIds: ['vf8_eco', 'vf8_plus', 'vf8_all_new']
      },
      {
        label: '🏰 VF 9: Eco vs Plus 7 chỗ vs Plus 6 chỗ VIP',
        desc: 'Ghế băng liền vs Trần kính Panorama vs Ghế Cơ Trưởng hạng thương gia',
        carIds: ['vf9_eco', 'vf9_plus_7seat', 'vf9_plus_6seat']
      },
      {
        label: '🚀 VF 7: Base vs Plus Thép vs Plus Panorama',
        desc: '174 hp FWD vs 349 hp AWD Trần Thép vs Trần Kính Toàn Cảnh',
        carIds: ['vf7_s', 'vf7_plus_steel', 'vf7_plus_panorama']
      },
      {
        label: '🔋 Bộ Đôi Crossover Đô Thị',
        desc: 'VF 5 Plus vs VF 6 Plus (Bán chạy nhất phân khúc A & B)',
        carIds: ['vf5_plus', 'vf6_plus']
      },
      {
        label: '🚖 Đội Xe Dịch Vụ Vận Tải Green',
        desc: 'Herio Green vs Nerio Green vs Limo Green (7 chỗ)',
        carIds: ['herio_green', 'nerio_green', 'limo_green']
      },
      {
        label: '🏕️ Bán Tải & Chuyên Dụng',
        desc: 'Bán tải VF WILD vs VF MPV 7 vs Tải van ECVAN',
        carIds: ['vf_wild', 'vf_mpv7', 'ecvan']
      }
    ];

    els.presetPills.innerHTML = presets.map((p, idx) => `
      <button class="btn-preset-pill px-4 py-2.5 rounded-2xl theme-card text-left hover:border-blue-500 transition-all duration-200 group flex-shrink-0" data-preset-idx="${idx}">
        <div class="text-xs font-bold text-[var(--text-primary)] group-hover:text-blue-500">${p.label}</div>
        <div class="text-[11px] text-[var(--text-muted)] truncate max-w-[240px] mt-0.5">${p.desc}</div>
      </button>
    `).join('');

    els.presetPills.querySelectorAll('.btn-preset-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.presetIdx, 10);
        const preset = presets[idx];
        if (preset) {
          state.selectedCarIds = [...preset.carIds];
          updateUrlParams();
          renderAll();
          if (window.confetti) {
            window.confetti({ particleCount: 35, spread: 60, origin: { y: 0.85 } });
          }
        }
      });
    });
  }

  /**
   * Vehicle Selector Modal
   */
  function openVehicleModal(targetSlotIndex = -1) {
    state.modalTargetIndex = targetSlotIndex;
    renderModalCarList();
    els.vehicleSelectorModal.style.display = 'flex';
    if (window.lucide) window.lucide.createIcons();
  }

  function closeVehicleModal() {
    els.vehicleSelectorModal.style.display = 'none';
  }

  function renderModalCarList(filterSegment = 'all', searchQuery = '') {
    let cars = window.CARS_DATABASE;

    if (filterSegment !== 'all') {
      if (filterSegment === 'urban') {
        cars = cars.filter(c => c.category === 'Đô thị & Minicar' || c.id.startsWith('vf3') || c.id === 'vf2' || c.id === 'vf5_plus' || c.id === 'minio_green');
      } else if (filterSegment === 'suv') {
        cars = cars.filter(c => c.category === 'SUV Cỡ Lớn & Thể Thao' || c.segment.toLowerCase().includes('suv') || c.id.startsWith('vf6') || c.id.startsWith('vf7') || c.id.startsWith('vf8') || c.id.startsWith('vf9'));
      } else if (filterSegment === 'green') {
        cars = cars.filter(c => c.category === 'Dịch Vụ Green Series' || c.id.includes('green'));
      } else if (filterSegment === 'utility') {
        cars = cars.filter(c => c.category === 'Bán Tải & Chuyên Dụng' || c.id === 'vf_wild' || c.id === 'vf_mpv7' || c.id === 'ecvan');
      }
    }

    if (searchQuery) {
      const q = searchQuery.toLowerCase().trim();
      cars = cars.filter(c => c.name.toLowerCase().includes(q) || c.segment.toLowerCase().includes(q) || c.shortName.toLowerCase().includes(q));
    }

    els.modalCarList.innerHTML = cars.map(car => {
      const isSelected = state.selectedCarIds.includes(car.id);
      return `
        <div class="p-3.5 rounded-2xl border ${isSelected ? 'border-blue-500 bg-blue-500/10' : 'border-[var(--border-subtle)] bg-[var(--surface-card)] hover:border-blue-400'} flex items-center justify-between gap-4 transition shadow-sm">
          <div class="flex items-center gap-3.5 flex-1">
            <div class="w-18 h-12 bg-[var(--bg-subtle)] rounded-xl p-1 flex items-center justify-center flex-shrink-0 border border-[var(--border-subtle)]">
              <img src="${car.image}" alt="${car.name}" class="max-h-full max-w-full object-contain" />
            </div>
            <div>
              <div class="text-[10px] font-extrabold uppercase text-blue-500">${car.segment}</div>
              <h4 class="text-sm font-bold text-[var(--text-primary)]">${car.name}</h4>
              <div class="text-xs font-semibold text-emerald-600 dark:text-emerald-400">${car.priceText}</div>
            </div>
          </div>
          <div>
            ${isSelected ? `
              <span class="text-xs font-bold text-blue-600 dark:text-blue-400 px-3 py-1.5 rounded-xl bg-blue-500/15 border border-blue-500/30">Đang chọn</span>
            ` : `
              <button class="btn-select-car px-3.5 py-1.5 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white transition shadow-md" data-car-id="${car.id}">
                Chọn xe
              </button>
            `}
          </div>
        </div>
      `;
    }).join('');

    els.modalCarList.querySelectorAll('.btn-select-car').forEach(btn => {
      btn.addEventListener('click', () => {
        const carId = btn.dataset.carId;
        if (state.modalTargetIndex >= 0 && state.modalTargetIndex < state.selectedCarIds.length) {
          state.selectedCarIds[state.modalTargetIndex] = carId;
        } else {
          if (!state.selectedCarIds.includes(carId) && state.selectedCarIds.length < 5) {
            state.selectedCarIds.push(carId);
          }
        }
        closeVehicleModal();
        updateUrlParams();
        renderAll();
      });
    });
  }

  /**
   * Theme Switcher
   */
  function initTheme() {
    const params = new URLSearchParams(window.location.search);
    const themeParam = params.get('theme');
    if (themeParam === 'dark') {
      state.isDarkMode = true;
      localStorage.setItem('theme', 'dark');
    } else if (themeParam === 'light') {
      state.isDarkMode = false;
      localStorage.setItem('theme', 'light');
    } else {
      const stored = localStorage.getItem('theme');
      // Default to Light mode per user instruction
      state.isDarkMode = stored === 'dark';
    }
    applyTheme();
  }

  function applyTheme() {
    const icon = document.getElementById('theme-toggle-icon');
    if (state.isDarkMode) {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
      if (icon) {
        icon.setAttribute('data-lucide', 'sun');
      }
    } else {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark');
      if (icon) {
        icon.setAttribute('data-lucide', 'moon');
      }
    }
    if (window.lucide) window.lucide.createIcons();
  }

  function toggleTheme() {
    state.isDarkMode = !state.isDarkMode;
    localStorage.setItem('theme', state.isDarkMode ? 'dark' : 'light');
    applyTheme();
    renderAll();
  }

  /**
   * Share Link
   */
  function shareLink() {
    const url = window.location.href;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => {
        window.ExportManager.showToast('Đã sao chép liên kết so sánh vào Clipboard! Bạn có thể gửi cho bạn bè hoặc khách hàng.');
      });
    } else {
      prompt('Sao chép đường dẫn so sánh này:', url);
    }
  }

  /**
   * Interactive Fuel & Operating Cost Calculator
   */
  function initCostCalculator() {
    const slider = document.getElementById('calc-km-slider');
    const label = document.getElementById('slider-km-val');
    const evMonth = document.getElementById('cost-ev-month');
    const evYear = document.getElementById('cost-ev-year');
    const iceMonth = document.getElementById('cost-ice-month');
    const iceYear = document.getElementById('cost-ice-year');
    const savingsYear = document.getElementById('cost-savings-year');

    if (!slider) return;

    function update() {
      const km = parseInt(slider.value, 10);
      label.textContent = `${km.toLocaleString('vi-VN')} km`;

      const evMonthly = km * 380;
      const evYearly = evMonthly * 12;

      const iceMonthly = km * 1550;
      const iceYearly = iceMonthly * 12;

      const diffYearly = iceYearly - evYearly;

      evMonth.textContent = `${Math.round(evMonthly).toLocaleString('vi-VN')} đ`;
      evYear.textContent = `~${(evYearly / 1000000).toFixed(1)} triệu / năm`;

      iceMonth.textContent = `${Math.round(iceMonthly).toLocaleString('vi-VN')} đ`;
      iceYear.textContent = `~${(iceYearly / 1000000).toFixed(1)} triệu / năm`;

      savingsYear.textContent = `+${(diffYearly / 1000000).toFixed(1)} triệu`;
    }

    slider.addEventListener('input', update);
    update();
  }

  /**
   * Master Render
   */
  function renderAll() {
    renderCarHeaders();
    renderStickyCompareBar();
    renderSmartSummary();
    renderSpecsTable();
    window.ComparisonEngine.renderRadarChart('radar-canvas', getSelectedCars(), state.isDarkMode);

    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  /**
   * Event Listeners
   */
  function bindEvents() {
    window.addEventListener('scroll', handleScroll, { passive: true });

    els.diffOnlyToggle.addEventListener('change', (e) => {
      state.showDiffOnly = e.target.checked;
      renderSpecsTable();
      if (window.lucide) window.lucide.createIcons();
    });

    els.highlightToggle.addEventListener('change', (e) => {
      state.highlightAdvantages = e.target.checked;
      renderSpecsTable();
      if (window.lucide) window.lucide.createIcons();
    });

    els.specSearchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      renderSpecsTable();
      if (window.lucide) window.lucide.createIcons();
    });

    els.btnExportPng.addEventListener('click', () => {
      window.ExportManager.exportToImage(getSelectedCars());
    });

    els.btnExportPdf.addEventListener('click', () => {
      window.ExportManager.exportToPDF(getSelectedCars());
    });

    els.btnShare.addEventListener('click', shareLink);
    els.btnThemeToggle.addEventListener('click', toggleTheme);

    els.closeVehicleModal.addEventListener('click', closeVehicleModal);
    els.vehicleSelectorModal.addEventListener('click', (e) => {
      if (e.target === els.vehicleSelectorModal) closeVehicleModal();
    });

    // Close Lineup Modal
    const btnLineup = document.getElementById('btn-view-lineup');
    const lineupModal = document.getElementById('lineup-modal');
    const btnCloseLineup = document.getElementById('btn-close-lineup-modal');
    if (btnLineup && lineupModal) {
      btnLineup.addEventListener('click', () => {
        lineupModal.style.display = 'flex';
      });
      btnCloseLineup?.addEventListener('click', () => {
        lineupModal.style.display = 'none';
      });
      lineupModal.addEventListener('click', (e) => {
        if (e.target === lineupModal) lineupModal.style.display = 'none';
      });
    }

    els.modalSearchInput.addEventListener('input', (e) => {
      const activeTab = els.modalSegmentTabs.querySelector('.active-tab')?.dataset.segment || 'all';
      renderModalCarList(activeTab, e.target.value);
    });

    els.modalSegmentTabs.querySelectorAll('button').forEach(tab => {
      tab.addEventListener('click', () => {
        els.modalSegmentTabs.querySelectorAll('button').forEach(t => t.classList.remove('active-tab', 'bg-blue-600', 'text-white'));
        tab.classList.add('active-tab', 'bg-blue-600', 'text-white');
        renderModalCarList(tab.dataset.segment, els.modalSearchInput.value);
      });
    });
  }

  // Initialize
  initTheme();
  parseUrlParams();
  renderPresets();
  initCostCalculator();
  bindEvents();
  renderAll();
});
