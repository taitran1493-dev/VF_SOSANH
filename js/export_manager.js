/**
 * Export Manager for VinFast Smart Car Comparison Platform
 * Supports high-resolution Infographic PNG export and professional PDF document export.
 * Includes verified brochure citations and references.
 */

window.ExportManager = (function () {
  'use strict';

  function showLoading(msg = 'Đang khởi tạo tài liệu so sánh...') {
    let loader = document.getElementById('export-loading-overlay');
    if (!loader) {
      loader = document.createElement('div');
      loader.id = 'export-loading-overlay';
      loader.className = 'fixed inset-0 z-50 flex flex-col items-center justify-center bg-black/80 backdrop-blur-md text-white transition-opacity duration-300';
      loader.innerHTML = `
        <div class="relative w-16 h-16 mb-4">
          <div class="absolute inset-0 rounded-full border-4 border-blue-500/20"></div>
          <div class="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin"></div>
        </div>
        <p id="export-loading-text" class="text-lg font-semibold text-slate-100 tracking-wide"></p>
        <p class="text-xs text-slate-400 mt-1">Vui lòng chờ trong giây lát...</p>
      `;
      document.body.appendChild(loader);
    }
    document.getElementById('export-loading-text').textContent = msg;
    loader.style.display = 'flex';
  }

  function hideLoading() {
    const loader = document.getElementById('export-loading-overlay');
    if (loader) {
      loader.style.display = 'none';
    }
  }

  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-6 right-6 z-50 flex items-center gap-3 px-5 py-3.5 rounded-xl shadow-2xl text-sm font-semibold text-white transition-all transform duration-300 translate-y-2 opacity-0 ${
      type === 'success' ? 'bg-emerald-600' : 'bg-blue-600'
    }`;
    toast.innerHTML = `
      <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      <span>${message}</span>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.classList.remove('translate-y-2', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
    }, 50);

    setTimeout(() => {
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  /**
   * Pre-renders clean Infographic DOM for PNG/PDF capture
   */
  function buildInfographicElement(cars, options = {}) {
    const container = document.createElement('div');
    container.id = 'export-temp-capture';
    container.style.position = 'fixed';
    container.style.left = '-9999px';
    container.style.top = '0';
    container.style.width = cars.length > 2 ? '1420px' : '1100px';
    container.style.backgroundColor = '#0b0f19';
    container.style.color = '#f8fafc';
    container.style.fontFamily = "'Plus Jakarta Sans', sans-serif";
    container.style.padding = '40px';
    container.style.borderRadius = '0px';

    const dateStr = new Date().toLocaleDateString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });

    let carsHeaderHtml = '';
    cars.forEach(car => {
      carsHeaderHtml += `
        <div class="flex-1 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 text-center flex flex-col justify-between">
          <div>
            <div class="text-[11px] uppercase font-bold tracking-wider text-blue-400 mb-1">${car.segment}</div>
            <h2 class="text-xl font-extrabold text-white mb-1">${car.name}</h2>
            <div class="text-lg font-bold text-emerald-400 mb-1">${car.priceText}</div>
            <div class="text-[10px] text-slate-400 mb-3">${car.batteryFeeText || car.fuelType}</div>
          </div>
          <div class="relative w-full h-40 mb-3 flex items-center justify-center overflow-hidden">
            <img src="${car.image}" crossorigin="anonymous" class="max-h-full max-w-full object-contain filter drop-shadow-xl" />
          </div>
          <div class="bg-slate-950/80 rounded-xl p-3 text-left border border-slate-800/80">
            <div class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">Ưu điểm nổi bật</div>
            <ul class="text-xs space-y-1 text-slate-200">
              ${(car.highlights || []).slice(0, 3).map(h => `<li class="flex items-start gap-1.5"><span class="text-blue-400 font-bold">•</span><span>${h}</span></li>`).join('')}
            </ul>
            ${car.brochureRef ? `
              <div class="mt-2 pt-2 border-t border-slate-800 text-[10px] text-cyan-400 font-medium truncate">
                Tài liệu: ${car.brochureRef.split('(')[0]}
              </div>
            ` : ''}
          </div>
        </div>
      `;
    });

    // Build categories
    let categoriesHtml = '';
    window.ComparisonEngine.SPEC_CATEGORIES.forEach(cat => {
      let rowsHtml = '';
      cat.specs.forEach(spec => {
        const diffInfo = window.ComparisonEngine.analyzeDifferences(cars, cat.id, spec.key);
        
        let colsHtml = '';
        cars.forEach((car, idx) => {
          const rawVal = diffInfo.values[idx];
          const isWinner = diffInfo.bestIndex === idx;
          const formattedVal = window.ComparisonEngine.formatSpecValue(rawVal, spec.type, isWinner);
          colsHtml += `
            <div class="flex-1 p-3 text-xs text-left flex items-start justify-start border-l border-slate-800/60 ${isWinner ? 'bg-emerald-950/20 text-emerald-300 font-bold' : 'text-slate-200'}">
              <div class="w-full">${formattedVal}</div>
            </div>
          `;
        });

        rowsHtml += `
          <div class="flex items-stretch border-b border-slate-800/50 ${diffInfo.isDifferent ? 'bg-blue-950/15' : ''}">
            <div class="w-80 p-3 text-xs font-semibold text-slate-300 flex items-center gap-2">
              <span>${spec.label}</span>
              ${diffInfo.isDifferent ? '<span class="text-[9px] uppercase px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 font-bold">Khác biệt</span>' : ''}
            </div>
            ${colsHtml}
          </div>
        `;
      });

      categoriesHtml += `
        <div class="mb-5 rounded-2xl overflow-hidden border border-slate-800 bg-slate-900/60">
          <div class="bg-gradient-to-r from-blue-900/50 to-slate-900 px-4 py-2 border-b border-slate-800 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            <h3 class="text-xs font-bold uppercase tracking-wider text-white">${cat.title}</h3>
          </div>
          ${rowsHtml}
        </div>
      `;
    });

    container.innerHTML = `
      <div style="width: 100%;">
        <!-- Header Banner -->
        <div class="flex items-center justify-between pb-5 mb-5 border-b border-slate-800">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <svg class="w-7 h-7 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.5 2.8C2.1 10.7 2 10.8 2 11v5c0 .6.4 1 1 1h2"></path>
                <circle cx="7" cy="17" r="2"></circle>
                <path d="M9 17h6"></path>
                <circle cx="17" cy="17" r="2"></circle>
              </svg>
            </div>
            <div>
              <div class="text-[10px] font-extrabold uppercase tracking-widest text-blue-400">VINFAST SMART COMPARISON PLATFORM • BROCHURE VERIFIED</div>
              <h1 class="text-2xl font-black text-white">BẢNG SO SÁNH THÔNG SỐ XE CHUẨN XÁC CHÍNH HÃNG</h1>
            </div>
          </div>
          <div class="text-right">
            <div class="text-xs text-slate-400">Ngày lập báo cáo: <strong class="text-slate-200">${dateStr}</strong></div>
            <div class="text-xs text-slate-400">Nguồn kiểm chứng: <strong class="text-emerald-400">Brochure VinFast 2026</strong></div>
          </div>
        </div>

        <!-- Vehicle Cards Row -->
        <div class="flex gap-4 mb-5">
          ${carsHeaderHtml}
        </div>

        <!-- Specifications Table -->
        <div class="mb-5">
          ${categoriesHtml}
        </div>

        <!-- Footer -->
        <div class="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div>* Dữ liệu được trích xuất và đối chiếu chuẩn xác 100% từ hồ sơ kỹ thuật và Catalogue chính thức VinFast (vinfastauto.com/vn_vi).</div>
          <div class="text-blue-400 font-semibold">vinfastauto.com/vn_vi • VinFast Smart Compare</div>
        </div>
      </div>
    `;

    document.body.appendChild(container);
    return container;
  }

  /**
   * Export Image as PNG
   */
  async function exportToImage(cars) {
    if (!cars || cars.length === 0) {
      alert('Vui lòng chọn ít nhất 1 xe để xuất hình ảnh.');
      return;
    }

    showLoading('Đang vẽ và kết xuất hình ảnh so sánh chuẩn HD...');

    try {
      const container = buildInfographicElement(cars);

      // Wait for any images to complete loading
      const imgs = container.querySelectorAll('img');
      await Promise.all(Array.from(imgs).map(img => {
        if (img.complete) return Promise.resolve();
        return new Promise(resolve => {
          img.onload = resolve;
          img.onerror = resolve;
        });
      }));

      // Render with html2canvas
      const canvas = await window.html2canvas(container, {
        scale: 2, // 2x high resolution
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#0b0f19',
        logging: false
      });

      // Cleanup temp DOM
      container.remove();

      // Convert to downloadable PNG
      const imageURL = canvas.toDataURL('image/png');
      const filename = `So_Sanh_Xe_${cars.map(c => c.shortName.replace(/[\s()]/g, '_')).join('_vs_')}_${Date.now()}.png`;

      const link = document.createElement('a');
      link.href = imageURL;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();

      hideLoading();
      showToast('Đã xuất hình ảnh so sánh thành công!');

      // Offer quick preview modal with clipboard copy
      showImagePreviewModal(imageURL, canvas);

    } catch (err) {
      console.error('Export image error:', err);
      hideLoading();
      alert('Có lỗi xảy ra khi tạo hình ảnh: ' + err.message);
    }
  }

  /**
   * Export PDF Document
   */
  async function exportToPDF(cars) {
    if (!cars || cars.length === 0) {
      alert('Vui lòng chọn ít nhất 1 xe để xuất PDF.');
      return;
    }

    if (!window.jspdf || !window.jspdf.jsPDF) {
      alert('Thư viện tạo PDF đang được tải, vui lòng thử lại sau 2 giây.');
      return;
    }

    showLoading('Đang tạo file PDF báo cáo so sánh...');

    try {
      const container = buildInfographicElement(cars);

      // Wait for images
      const imgs = container.querySelectorAll('img');
      await Promise.all(Array.from(imgs).map(img => {
        if (img.complete) return Promise.resolve();
        return new Promise(resolve => {
          img.onload = resolve;
          img.onerror = resolve;
        });
      }));

      const canvas = await window.html2canvas(container, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#0b0f19',
        logging: false
      });

      container.remove();

      const imgData = canvas.toDataURL('image/jpeg', 0.95);
      const isLandscape = cars.length > 2;
      const pdf = new window.jspdf.jsPDF({
        orientation: isLandscape ? 'landscape' : 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();

      const imgWidth = pageWidth;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      let heightLeft = imgHeight;
      let position = 0;

      // First page
      pdf.addImage(imgData, 'JPEG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      // Handle multi-page if height exceeds single A4
      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'JPEG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      const filename = `Bang_So_Sanh_VinFast_${Date.now()}.pdf`;
      pdf.save(filename);

      hideLoading();
      showToast('Đã xuất file PDF so sánh thành công!');

    } catch (err) {
      console.error('Export PDF error:', err);
      hideLoading();
      alert('Có lỗi xảy ra khi tạo PDF: ' + err.message);
    }
  }

  /**
   * Preview Modal with Copy to Clipboard support
   */
  function showImagePreviewModal(imageURL, canvas) {
    let modal = document.getElementById('image-export-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'image-export-modal';
      modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm';
      modal.innerHTML = `
        <div class="relative max-w-4xl w-full bg-slate-900 border border-slate-700 rounded-3xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
          <div class="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/90">
            <div class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
              <h3 class="font-bold text-white text-base">Xem Trước Hình Ảnh So Sánh</h3>
            </div>
            <div class="flex items-center gap-3">
              <button id="btn-copy-clipboard" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                <span>Sao chép ảnh (Gửi Zalo)</span>
              </button>
              <button id="btn-close-modal" class="text-slate-400 hover:text-white p-1 rounded-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>
          </div>
          <div class="p-6 overflow-y-auto flex-1 flex items-center justify-center bg-slate-950">
            <img id="export-preview-img" src="" class="max-w-full rounded-xl shadow-lg border border-slate-800" />
          </div>
        </div>
      `;
      document.body.appendChild(modal);

      modal.querySelector('#btn-close-modal').addEventListener('click', () => {
        modal.style.display = 'none';
      });

      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
      });
    }

    const previewImg = modal.querySelector('#export-preview-img');
    previewImg.src = imageURL;
    modal.style.display = 'flex';

    const copyBtn = modal.querySelector('#btn-copy-clipboard');
    copyBtn.onclick = async () => {
      try {
        canvas.toBlob(async blob => {
          if (navigator.clipboard && window.ClipboardItem) {
            await navigator.clipboard.write([
              new window.ClipboardItem({ 'image/png': blob })
            ]);
            showToast('Đã sao chép ảnh vào Clipboard! Bạn có thể nhấn Ctrl+V để gửi ngay vào Zalo/Facebook.');
          } else {
            alert('Trình duyệt không hỗ trợ sao chép ảnh trực tiếp. Vui lòng tải file ảnh xuống máy.');
          }
        }, 'image/png');
      } catch (err) {
        console.error('Clipboard copy error:', err);
        alert('Không thể sao chép ảnh: ' + err.message);
      }
    };
  }

  return {
    exportToImage,
    exportToPDF,
    showToast
  };
})();
