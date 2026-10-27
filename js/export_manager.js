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
   * Pre-renders clean Infographic DOM for PNG/PDF capture (Pure Light Mode)
   */
  function buildInfographicElement(cars, options = {}) {
    const container = document.createElement('div');
    container.id = 'export-temp-capture';
    container.style.position = 'fixed';
    container.style.left = '-9999px';
    container.style.top = '0';
    container.style.width = cars.length > 2 ? '1440px' : '1140px';
    container.style.backgroundColor = '#ffffff';
    container.style.color = '#0f172a';
    container.style.fontFamily = "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    container.style.padding = '40px';
    container.style.boxSizing = 'border-box';

    const dateStr = new Date().toLocaleDateString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });

    let carsHeaderHtml = '';
    cars.forEach(car => {
      carsHeaderHtml += `
        <div style="flex: 1; background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 20px; padding: 20px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.06);">
          <div>
            <div style="display: inline-block; font-size: 11px; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em; color: #1d4ed8; background: #eff6ff; border: 1px solid #bfdbfe; padding: 3px 12px; border-radius: 9999px; margin-bottom: 8px;">${car.segment.split('(')[0].trim()}</div>
            <h2 style="font-size: 20px; font-weight: 900; color: #0f172a; margin: 0 0 4px 0; line-height: 1.2;">${car.name}</h2>
            <div style="font-size: 18px; font-weight: 900; color: #059669; margin-bottom: 4px;">${car.priceText}</div>
            <div style="font-size: 11px; color: #64748b; font-weight: 600; margin-bottom: 14px;">${car.batteryFeeText || car.fuelType}</div>
          </div>
          <div style="position: relative; width: 100%; height: 160px; margin-bottom: 14px; display: flex; align-items: center; justify-content: center; overflow: hidden; background: radial-gradient(circle, #f8fafc 0%, #f1f5f9 100%); border-radius: 14px; padding: 10px; border: 1px solid #f1f5f9;">
            <img src="${car.image}" crossorigin="anonymous" style="max-height: 100%; max-width: 100%; object-fit: contain; filter: drop-shadow(0 8px 12px rgba(15, 23, 42, 0.12));" />
          </div>
          <div style="background: #f8fafc; border-radius: 14px; padding: 12px 14px; text-align: left; border: 1px solid #e2e8f0;">
            <div style="font-size: 10px; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">Ưu điểm nổi bật</div>
            <ul style="font-size: 12px; line-height: 1.5; color: #334155; margin: 0; padding: 0; list-style: none;">
              ${(car.highlights || []).slice(0, 3).map(h => `<li style="display: flex; align-items: flex-start; gap: 6px; margin-bottom: 3px;"><span style="color: #2563eb; font-weight: 900; line-height: 1;">•</span><span>${h}</span></li>`).join('')}
            </ul>
            ${car.brochureRef ? `
              <div style="margin-top: 8px; padding-top: 6px; border-top: 1px solid #e2e8f0; font-size: 10px; color: #0284c7; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                Catalogue: ${car.brochureRef.split('(')[0]}
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
            <div style="flex: 1; padding: 12px 14px; font-size: 12px; text-align: left; border-left: 1px solid #e2e8f0; display: flex; align-items: flex-start; ${isWinner ? 'background: #ecfdf5; color: #065f46; font-weight: 700;' : 'color: #1e293b;'}">
              <div style="width: 100%; line-height: 1.45;">${formattedVal}</div>
            </div>
          `;
        });

        rowsHtml += `
          <div style="display: flex; align-items: stretch; border-bottom: 1px solid #e2e8f0; ${diffInfo.isDifferent ? 'background: #f0f9ff;' : 'background: #ffffff;'}">
            <div style="width: 280px; min-width: 280px; padding: 12px 14px; font-size: 12px; font-weight: 700; color: #334155; background: #f8fafc; border-right: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; gap: 8px;">
              <span>${spec.label}</span>
              ${diffInfo.isDifferent ? '<span style="font-size: 9px; text-transform: uppercase; padding: 2px 6px; border-radius: 4px; background: #dbeafe; color: #1e40af; font-weight: 800; border: 1px solid #bfdbfe; white-space: nowrap;">Khác biệt</span>' : ''}
            </div>
            ${colsHtml}
          </div>
        `;
      });

      categoriesHtml += `
        <div style="margin-bottom: 24px; border-radius: 16px; overflow: hidden; border: 1.5px solid #cbd5e1; background: #ffffff; box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);">
          <div style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); padding: 10px 18px; border-bottom: 1.5px solid #cbd5e1; display: flex; align-items: center; gap: 8px;">
            <span style="width: 8px; height: 8px; border-radius: 9999px; background: #2563eb; display: inline-block;"></span>
            <h3 style="font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.06em; color: #0f172a; margin: 0;">${cat.title}</h3>
          </div>
          ${rowsHtml}
        </div>
      `;
    });

    container.innerHTML = `
      <div style="width: 100%; background: #ffffff;">
        <!-- Header Banner -->
        <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px; margin-bottom: 24px; border-bottom: 2px solid #e2e8f0;">
          <div style="display: flex; align-items: center; gap: 16px;">
            <div style="width: 52px; height: 52px; border-radius: 16px; background: linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 16px -4px rgba(29, 78, 216, 0.3);">
              <svg style="width: 30px; height: 30px; color: #ffffff;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.5 2.8C2.1 10.7 2 10.8 2 11v5c0 .6.4 1 1 1h2"></path>
                <circle cx="7" cy="17" r="2"></circle>
                <path d="M9 17h6"></path>
                <circle cx="17" cy="17" r="2"></circle>
              </svg>
            </div>
            <div>
              <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.12em; color: #2563eb; margin-bottom: 2px;">VINFAST SMART COMPARISON PLATFORM • CHÍNH HÃNG 100%</div>
              <h1 style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 0; line-height: 1.2;">BẢNG SO SÁNH THÔNG SỐ XE VINFAST CHUẨN XÁC</h1>
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 12px; color: #64748b;">Ngày lập: <strong style="color: #0f172a;">${dateStr}</strong></div>
            <div style="font-size: 12px; color: #64748b;">Nguồn dữ liệu: <strong style="color: #059669;">Catalogue Chính Thức VinFast 2026</strong></div>
          </div>
        </div>

        <!-- Vehicle Cards Row -->
        <div style="display: flex; gap: 16px; margin-bottom: 24px;">
          ${carsHeaderHtml}
        </div>

        <!-- Specifications Table -->
        <div style="margin-bottom: 24px;">
          ${categoriesHtml}
        </div>

        <!-- Footer -->
        <div style="padding-top: 16px; border-top: 1.5px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: #64748b;">
          <div>* Dữ liệu được trích xuất và đối chiếu chuẩn xác 100% từ hồ sơ kỹ thuật và Catalogue chính thức VinFast (vinfastauto.com/vn_vi).</div>
          <div style="color: #2563eb; font-weight: 800;">vinfastauto.com/vn_vi • VinFast Smart Compare</div>
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

      // Render with html2canvas (Clean Crisp Light Mode)
      const canvas = await window.html2canvas(container, {
        scale: 2, // 2x high resolution
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
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
        backgroundColor: '#ffffff',
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
    buildInfographicElement,
    showToast
  };
})();
