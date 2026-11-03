/* ==========================================================================
   BULGAN HURDACILIK & GERİ DÖNÜŞÜM — LIVE PRICE ENGINE, CALCULATOR & UI
   ========================================================================== */

(function () {
  "use strict";

  const PHONE_RAW = "905459043834";
  let priceCatalog = [];
  let basket = [];

  function formatTL(num) {
    return new Intl.NumberFormat("tr-TR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(num) + " ₺";
  }

  // 1. Mobile Navigation Drawer
  const mobileBtn = document.getElementById("mobileMenuBtn");
  const mobileDrawer = document.getElementById("mobileDrawer");
  if (mobileBtn && mobileDrawer) {
    mobileBtn.addEventListener("click", function () {
      const isOpen = mobileDrawer.classList.toggle("open");
      mobileBtn.setAttribute("aria-expanded", String(isOpen));
      mobileBtn.innerHTML = isOpen ? "✕" : "☰";
    });
  }

  // 2. Fetch Live Daily Scrap Prices (/api/prices -> fallback /data/prices.json)
  async function loadPrices() {
    let data = null;
    try {
      const res = await fetch("/api/prices", { cache: "no-cache" });
      if (res.ok) {
        data = await res.json();
      }
    } catch (_) {}

    if (!data || !Array.isArray(data.categories)) {
      try {
        const resLocal = await fetch("/data/prices.json", { cache: "no-cache" });
        if (resLocal.ok) {
          data = await resLocal.json();
        }
      } catch (_) {}
    }

    if (!data || !Array.isArray(data.categories)) return;
    priceCatalog = data.categories;

    // Update timestamps & exchange ticker
    document.querySelectorAll("[data-updated-at]").forEach((el) => {
      el.textContent = data.updatedAt || "Bugün";
    });
    if (data.exchange) {
      document.querySelectorAll("[data-usd-try]").forEach((el) => {
        el.textContent = data.exchange.USD_TRY + " ₺";
      });
      document.querySelectorAll("[data-eur-try]").forEach((el) => {
        el.textContent = data.exchange.EUR_TRY + " ₺";
      });
    }

    // Build flat lookup map for table cells
    const itemMap = {};
    priceCatalog.forEach((cat) => {
      cat.items.forEach((item) => {
        itemMap[item.code] = item;
      });
    });

    document.querySelectorAll("[data-price-code]").forEach((el) => {
      const code = el.getAttribute("data-price-code");
      if (itemMap[code]) {
        el.textContent = formatTL(itemMap[code].price) + " / KG";
      }
    });

    document.querySelectorAll("[data-ton-code]").forEach((el) => {
      const code = el.getAttribute("data-ton-code");
      if (itemMap[code]) {
        el.textContent = formatTL(itemMap[code].tonPrice) + " / TON";
      }
    });

    initCalculator();
  }

  // 3. Interactive Digital Kantar & Multi-Item Scrap Calculator
  function initCalculator() {
    const catSelect = document.getElementById("calcCategory");
    const itemSelect = document.getElementById("calcSubItem");
    const weightInput = document.getElementById("calcWeight");
    const unitSelect = document.getElementById("calcUnit");
    const citySelect = document.getElementById("calcCity");
    const lcdRate = document.getElementById("lcdUnitRate");
    const lcdTotal = document.getElementById("lcdTotalAmount");
    const addBasketBtn = document.getElementById("calcAddBasketBtn");
    const basketContainer = document.getElementById("calcBasketList");
    const whatsappSendBtn = document.getElementById("calcWhatsappBtn");

    if (!catSelect || !itemSelect || !weightInput || !lcdTotal) return;

    // Populate categories
    catSelect.innerHTML = "";
    priceCatalog.forEach((cat) => {
      const opt = document.createElement("option");
      opt.value = cat.id;
      opt.textContent = cat.shortName + " (" + cat.items.length + " Kalem)";
      catSelect.appendChild(opt);
    });

    function populateSubItems() {
      const selectedCatId = catSelect.value;
      const catObj = priceCatalog.find((c) => c.id === selectedCatId) || priceCatalog[0];
      itemSelect.innerHTML = "";
      if (!catObj) return;
      catObj.items.forEach((it) => {
        const opt = document.createElement("option");
        opt.value = it.code;
        opt.dataset.price = String(it.price);
        opt.dataset.name = it.name;
        opt.textContent = `${it.name} — ${formatTL(it.price)}/KG`;
        itemSelect.appendChild(opt);
      });
      computeCurrent();
    }

    function getCurrentSelection() {
      const selOpt = itemSelect.options[itemSelect.selectedIndex];
      const unitPrice = selOpt ? parseFloat(selOpt.dataset.price || "0") : 0;
      const itemName = selOpt ? selOpt.dataset.name : "Hurda Metal";
      const rawWeight = parseFloat(weightInput.value) || 0;
      const unit = unitSelect ? unitSelect.value : "KG";
      const kgWeight = unit === "TON" ? rawWeight * 1000 : rawWeight;
      const lineTotal = kgWeight * unitPrice;
      return { itemName, unitPrice, rawWeight, unit, kgWeight, lineTotal };
    }

    function computeCurrent() {
      const cur = getCurrentSelection();
      if (lcdRate) {
        lcdRate.textContent = `Birim: ${formatTL(cur.unitPrice)} / KG (-%20 Borsa Net)`;
      }
      const basketSum = basket.reduce((acc, b) => acc + b.lineTotal, 0);
      const grandTotal = basket.length > 0 ? basketSum : cur.lineTotal;
      lcdTotal.textContent = formatTL(grandTotal);
    }

    function renderBasket() {
      if (!basketContainer) return;
      if (basket.length === 0) {
        basketContainer.style.display = "none";
        computeCurrent();
        return;
      }
      basketContainer.style.display = "block";
      basketContainer.innerHTML = basket
        .map(
          (b, idx) => `
          <div class="calc-basket-item">
            <span><strong>${b.itemName}</strong> (${b.rawWeight} ${b.unit})</span>
            <span>
              <strong>${formatTL(b.lineTotal)}</strong>
              <button type="button" class="calc-basket-remove" data-idx="${idx}" title="Kaldır">✕</button>
            </span>
          </div>`
        )
        .join("");

      basketContainer.querySelectorAll(".calc-basket-remove").forEach((btn) => {
        btn.addEventListener("click", function () {
          const i = parseInt(btn.getAttribute("data-idx"), 10);
          basket.splice(i, 1);
          renderBasket();
        });
      });
      computeCurrent();
    }

    catSelect.addEventListener("change", populateSubItems);
    itemSelect.addEventListener("change", computeCurrent);
    weightInput.addEventListener("input", computeCurrent);
    if (unitSelect) unitSelect.addEventListener("change", computeCurrent);

    if (addBasketBtn) {
      addBasketBtn.addEventListener("click", function () {
        const cur = getCurrentSelection();
        if (cur.kgWeight <= 0) {
          weightInput.focus();
          return;
        }
        basket.push(cur);
        renderBasket();
      });
    }

    if (whatsappSendBtn) {
      whatsappSendBtn.addEventListener("click", function () {
        const loc = citySelect ? citySelect.value : "Mardin / Güneydoğu Anadolu";
        const itemsToSend = basket.length > 0 ? basket : [getCurrentSelection()];
        let total = 0;
        const lines = itemsToSend.map((it, idx) => {
          total += it.lineTotal;
          return `${idx + 1}. ${it.itemName}: ${it.rawWeight} ${it.unit} x ${formatTL(it.unitPrice)} = ${formatTL(it.lineTotal)}`;
        });
        const msg =
          `Merhaba *Bulgan Hurdacılık*, web sitenizdeki Canlı Kantar Hesaplama Aracı ile fiyat hesapladım:\n\n` +
          `📍 *Bölge:* ${loc}\n` +
          lines.join("\n") +
          `\n\n💰 *Tahmini Toplam Nakit Tutar:* ${formatTL(total)}\n` +
          `Yerinde tartım ve nakit alım için dönüş yapabilir misiniz?`;
        trackConversion("calculator_whatsapp_click", { value: total, location: loc });
        window.open(`https://wa.me/${PHONE_RAW}?text=${encodeURIComponent(msg)}`, "_blank");
      });
    }

    populateSubItems();
  }

  // 4. Filterable Price Table Tabs & Search
  const tabs = document.querySelectorAll(".price-tab");
  const blocks = document.querySelectorAll(".price-category-block");
  const searchInput = document.getElementById("priceSearchInput");

  tabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      const filterId = tab.getAttribute("data-filter");
      blocks.forEach((blk) => {
        if (filterId === "all" || blk.getAttribute("data-cat-id") === filterId) {
          blk.style.display = "block";
        } else {
          blk.style.display = "none";
        }
      });
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const q = searchInput.value.trim().toLowerCase();
      blocks.forEach((blk) => {
        const rows = blk.querySelectorAll("tbody tr");
        let visibleCount = 0;
        rows.forEach((r) => {
          const txt = r.textContent.toLowerCase();
          const show = !q || txt.includes(q);
          r.style.display = show ? "" : "none";
          if (show) visibleCount++;
        });
        blk.style.display = visibleCount > 0 ? "block" : "none";
      });
    });
  }

  // 5. Form Validation, Loading States & Thank You Redirect (Checklist #12, #13, #14)
  document.querySelectorAll("form[data-bulgan-form]").forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      let valid = true;

      const nameField = form.querySelector("[name='fullName']");
      const phoneField = form.querySelector("[name='phone']");
      const regionField = form.querySelector("[name='region']");
      const typeField = form.querySelector("[name='scrapType']");
      const weightField = form.querySelector("[name='weight']");
      const notesField = form.querySelector("[name='notes']");

      [nameField, phoneField].forEach((field) => {
        if (!field) return;
        const wrap = field.closest(".calc-form-group");
        const val = field.value.trim();
        if (!val || (field === phoneField && val.replace(/\D/g, "").length < 10)) {
          valid = false;
          if (wrap) wrap.classList.add("has-error");
        } else {
          if (wrap) wrap.classList.remove("has-error");
        }
      });

      if (!valid) return;

      const submitBtn = form.querySelector("button[type='submit']");
      if (submitBtn) {
        submitBtn.classList.add("loading");
        submitBtn.disabled = true;
      }

      const summary = {
        fullName: nameField ? nameField.value.trim() : "",
        phone: phoneField ? phoneField.value.trim() : "",
        region: regionField ? regionField.value : "Mardin",
        scrapType: typeField ? typeField.value : "Genel Hurda",
        weight: weightField ? weightField.value : "Belirtilmedi",
        notes: notesField ? notesField.value.trim() : ""
      };

      try {
        sessionStorage.setItem("bulgan_last_lead", JSON.stringify(summary));
      } catch (_) {}

      trackConversion("lead_form_submit", summary);

      setTimeout(function () {
        window.location.href = "/tesekkurler.html";
      }, 650);
    });
  });

  // 6. Cookie Consent Banner (Checklist #17)
  const cookieBanner = document.getElementById("cookieBanner");
  const acceptAllBtn = document.getElementById("cookieAcceptAll");
  const acceptEssentialBtn = document.getElementById("cookieAcceptEssential");

  try {
    const consent = localStorage.getItem("bulgan_cookie_consent");
    if (!consent && cookieBanner) {
      cookieBanner.classList.add("show");
    }
  } catch (_) {}

  if (acceptAllBtn) {
    acceptAllBtn.addEventListener("click", function () {
      try {
        localStorage.setItem("bulgan_cookie_consent", JSON.stringify({ analytics: true, essential: true, ts: Date.now() }));
      } catch (_) {}
      if (cookieBanner) cookieBanner.classList.remove("show");
    });
  }

  if (acceptEssentialBtn) {
    acceptEssentialBtn.addEventListener("click", function () {
      try {
        localStorage.setItem("bulgan_cookie_consent", JSON.stringify({ analytics: false, essential: true, ts: Date.now() }));
      } catch (_) {}
      if (cookieBanner) cookieBanner.classList.remove("show");
    });
  }

  // 7. Conversion & Analytics Helper (Checklist #18)
  function trackConversion(eventName, params) {
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, params || {});
    }
  }

  document.querySelectorAll("a[href^='tel:'], a[href*='wa.me']").forEach((link) => {
    link.addEventListener("click", function () {
      const isWa = link.href.includes("wa.me");
      trackConversion(isWa ? "whatsapp_click" : "phone_call_click", { href: link.href });
    });
  });

  // Initialize prices & calculator on load
  loadPrices();
})();
