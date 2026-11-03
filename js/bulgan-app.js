/* ==========================================================================
   BULGAN HURDACILIK - CLIENT APPLICATION ENGINE (100% UTF-8)
   Mobile Navigation, Instant Price Search, Live Calculator & Form Validation
   ========================================================================== */

(function () {
  "use strict";

  // 1. Mobile Drawer Navigation
  function initMobileDrawer() {
    const btn = document.getElementById("mobileMenuBtn");
    const drawer = document.getElementById("mobileDrawer");
    const closeBtn = document.getElementById("mobileDrawerClose");
    const backdrop = document.getElementById("mobileDrawerBackdrop");

    if (!btn || !drawer) return;

    function openDrawer() {
      drawer.classList.add("open");
      if (backdrop) backdrop.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    }

    function closeDrawer() {
      drawer.classList.remove("open");
      if (backdrop) backdrop.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      openDrawer();
    });

    if (closeBtn) closeBtn.addEventListener("click", closeDrawer);
    if (backdrop) backdrop.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("open")) {
        closeDrawer();
      }
    });
  }

  // 2. Interactive Calculator on Landing Page
  function initCalculator() {
    const metalSelect = document.getElementById("calcMetalSelect");
    const amountInput = document.getElementById("calcAmountInput");
    const locSelect = document.getElementById("calcLocationSelect");
    const unitDisplay = document.getElementById("calcUnitDisplay");
    const totalDisplay = document.getElementById("calcTotalDisplay");
    const waBtn = document.getElementById("calcWaBtn");

    if (!metalSelect || !amountInput || !totalDisplay) return;

    function updateCalc() {
      const price = parseFloat(metalSelect.value) || 0;
      const amount = parseFloat(amountInput.value) || 0;
      const total = price * amount;

      const selectedOptText = metalSelect.options[metalSelect.selectedIndex].text.split("(")[0].trim();
      const selectedLoc = locSelect ? locSelect.value : "Mardin";

      if (unitDisplay) {
        unitDisplay.textContent = price.toLocaleString("tr-TR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " TL / KG";
      }

      totalDisplay.textContent = total.toLocaleString("tr-TR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " TL";

      if (waBtn) {
        const msg = encodeURIComponent(
          "Merhaba, " + amount + " KG " + selectedOptText + " hurdası satmak istiyorum. " +
          "Konum: " + selectedLoc + ". Tahmini kantar tutarı: " +
          total.toLocaleString("tr-TR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " TL. " +
          "Adrese araç ve kantar talep ediyorum."
        );
        waBtn.href = "https://wa.me/905459043834?text=" + msg;
      }
    }

    metalSelect.addEventListener("change", updateCalc);
    amountInput.addEventListener("input", updateCalc);
    if (locSelect) locSelect.addEventListener("change", updateCalc);
    updateCalc();
  }

  // 3. Instant Live Price Search on hurda-fiyatlari.html
  function initPriceSearch() {
    const input = document.getElementById("priceSearchBar");
    if (!input) return;

    input.addEventListener("input", function () {
      const q = this.value.toLocaleLowerCase("tr-TR").trim();
      const rows = document.querySelectorAll(".price-row");
      const tables = document.querySelectorAll(".data-table-card");

      rows.forEach(function (row) {
        const term = (row.getAttribute("data-search-term") || "").toLocaleLowerCase("tr-TR");
        const text = row.textContent.toLocaleLowerCase("tr-TR");
        if (!q || term.includes(q) || text.includes(q)) {
          row.style.display = "";
        } else {
          row.style.display = "none";
        }
      });

      tables.forEach(function (table) {
        const visibleRows = table.querySelectorAll(".price-row:not([style*='display: none'])");
        if (visibleRows.length === 0 && q) {
          table.style.display = "none";
        } else {
          table.style.display = "";
        }
      });
    });
  }

  // 4. Smooth Anchor Scrolling for Category Jump Bar
  function initJumpBar() {
    const pills = document.querySelectorAll(".jump-pill-btn");
    pills.forEach(function (pill) {
      pill.addEventListener("click", function (e) {
        const targetId = this.getAttribute("href");
        if (targetId && targetId.startsWith("#")) {
          const target = document.querySelector(targetId);
          if (target) {
            e.preventDefault();
            const yOffset = -120;
            const y = target.getBoundingClientRect().top + window.pageYOffset + yOffset;
            window.scrollTo({ top: y, behavior: "smooth" });

            pills.forEach(p => p.classList.remove("active"));
            this.classList.add("active");
          }
        }
      });
    });
  }

  // DOM Content Loaded Initializer
  document.addEventListener("DOMContentLoaded", function () {
    initMobileDrawer();
    initCalculator();
    initPriceSearch();
    initJumpBar();
  });
})();
