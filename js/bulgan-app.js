/* ==========================================================================
   BULGAN HURDACILIK & GERİ DÖNÜŞÜM — İSTEMCİ UYGULAMA MOTORU
   Canlı Borsa Veri Eşitleme , Hesaplama Aracı & Form Doğrulama
   ========================================================================== */

(function () {
  "use strict";

  let priceCatalog = null;
  let basket = [];

  function formatTL(num) {
    return Number(num || 0).toLocaleString("tr-TR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }) + " TL";
  }

  // 1. Mobil Menü Kontrolü
  function initMobileNav() {
    const btn = document.getElementById("mobileMenuBtn");
    const nav = document.getElementById("mainNav");
    if (!btn || !nav) return;

    btn.addEventListener("click", function () {
      const expanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!expanded));
      nav.classList.toggle("open");
    });
  }

  // 2. Canlı Fiyat Verisini Çek (/api/prices -> /data/prices.json)
  async function loadPrices() {
    try {
      const res = await fetch("/api/prices", { headers: { Accept: "application/json" } });
      if (res.ok) {
        priceCatalog = await res.json();
        applyPricesToDOM(priceCatalog);
        return;
      }
    } catch (_) {}

    try {
      const fallback = await fetch("/data/prices.json");
      if (fallback.ok) {
        priceCatalog = await fallback.json();
        applyPricesToDOM(priceCatalog);
      }
    } catch (err) {
      console.error("Fiyat verisi yüklenemedi:", err);
    }
  }

  function applyPricesToDOM(data) {
    if (!data || !Array.isArray(data.categories)) return;

    // Güncelleme tarihi ve kurlar
    document.querySelectorAll("[data-live-updated]").forEach(function (el) {
      el.textContent = data.updatedAt || "Bugün";
    });
    if (data.exchange) {
      document.querySelectorAll("[data-live-usd]").forEach(function (el) {
        el.textContent = Number(data.exchange.USD_TRY).toFixed(2) + " TL";
      });
      document.querySelectorAll("[data-live-eur]").forEach(function (el) {
        el.textContent = Number(data.exchange.EUR_TRY).toFixed(2) + " TL";
      });
    }

    // Tablo hücrelerini kod bazlı güncelle
    const codeMap = {};
    data.categories.forEach(function (cat) {
      (cat.items || []).forEach(function (item) {
        codeMap[item.code] = item;
      });
    });

    document.querySelectorAll("[data-item-code]").forEach(function (row) {
      const code = row.getAttribute("data-item-code");
      const info = codeMap[code];
      if (!info) return;
      const mCell = row.querySelector("[data-col-market]");
      const nCell = row.querySelector("[data-col-net]");
      if (mCell) mCell.textContent = formatTL(info.marketPrice);
      if (nCell) nCell.textContent = formatTL(info.price) + " / " + info.unit;
    });

    initCalculator(data);
  }

  // 3. Canlı Hurda Hesaplama Aracı
  function initCalculator(data) {
    const catSelect = document.getElementById("calcCategory");
    const itemSelect = document.getElementById("calcItem");
    const weightInput = document.getElementById("calcWeight");
    const unitSelect = document.getElementById("calcUnit");
    const citySelect = document.getElementById("calcCity");

    const unitMarketEl = document.getElementById("calcMarketUnit");
    const unitNetEl = document.getElementById("calcNetUnit");
    const totalEl = document.getElementById("calcTotalAmount");
    const addBasketBtn = document.getElementById("calcAddBasketBtn");
    const basketWrap = document.getElementById("calcBasketList");
    const waQuoteBtn = document.getElementById("calcWaBtn");

    if (!catSelect || !itemSelect || !weightInput) return;

    // Kategorileri doldur
    catSelect.innerHTML = "";
    data.categories.forEach(function (cat, idx) {
      const opt = document.createElement("option");
      opt.value = String(idx);
      opt.textContent = cat.shortName + " (" + cat.items.length + " Kalem)";
      catSelect.appendChild(opt);
    });

    function populateItems() {
      const cIdx = parseInt(catSelect.value, 10) || 0;
      const cat = data.categories[cIdx] || data.categories[0];
      itemSelect.innerHTML = "";
      (cat.items || []).forEach(function (it, iIdx) {
        const opt = document.createElement("option");
        opt.value = String(iIdx);
        opt.textContent = it.name + " — " + formatTL(it.price) + "/KG";
        itemSelect.appendChild(opt);
      });
      recalc();
    }

    function getCurrentSelection() {
      const cIdx = parseInt(catSelect.value, 10) || 0;
      const iIdx = parseInt(itemSelect.value, 10) || 0;
      const cat = data.categories[cIdx] || data.categories[0];
      const item = (cat && cat.items[iIdx]) || (cat && cat.items[0]);
      const rawWeight = parseFloat(weightInput.value);
      const weight = isNaN(rawWeight) || rawWeight < 0 ? 0 : rawWeight;
      const isTon = unitSelect && unitSelect.value === "TON";
      const kg = isTon ? weight * 1000 : weight;
      const city = citySelect ? citySelect.value : "Mardin (Kızıltepe)";
      return { cat: cat, item: item, weight: weight, isTon: isTon, kg: kg, city: city };
    }

    function recalc() {
      const sel = getCurrentSelection();
      if (!sel.item) return;

      if (unitMarketEl) unitMarketEl.textContent = formatTL(sel.item.marketPrice) + " / KG";
      if (unitNetEl) unitNetEl.textContent = formatTL(sel.item.price) + " / KG";

      const currentLineTotal = sel.kg * sel.item.price;
      const basketTotal = basket.reduce(function (acc, b) {
        return acc + b.total;
      }, 0);

      const grandTotal = basket.length > 0 ? basketTotal : currentLineTotal;
      if (totalEl) totalEl.textContent = formatTL(grandTotal);

      if (waQuoteBtn) {
        let lines = [];
        if (basket.length > 0) {
          basket.forEach(function (b, i) {
            lines.push(
              (i + 1) + ". " + b.name + " (" + b.kg + " KG x " + b.unitPrice.toFixed(2) + " TL = " + formatTL(b.total) + ")"
            );
          });
        } else {
          lines.push("- " + sel.item.name + ": " + sel.kg + " KG (" + formatTL(currentLineTotal) + ")");
        }
        const msg =
          "Merhaba Bulgan Hurdacılık, web sitenizdeki canlı kantar hesaplama aracından yazıyorum.\n" +
          "Konum: " + sel.city + "\n" +
          "Hurda Listesi:\n" +
          lines.join("\n") +
          "\nTahmini Net Kantar Tutarı: " + formatTL(grandTotal) +
          "\nYerinde tartım ve nakit alım için dönüş rica ederim.";
        waQuoteBtn.href = "https://wa.me/905459043834?text=" + encodeURIComponent(msg);
      }
    }

    function renderBasket() {
      if (!basketWrap) return;
      if (basket.length === 0) {
        basketWrap.innerHTML = "";
        recalc();
        return;
      }
      basketWrap.innerHTML = basket
        .map(function (b, idx) {
          return (
            '<div class="calc-basket-item">' +
            "<span>" + b.name + " (" + b.kg + " KG)</span>" +
            '<span><strong>' + formatTL(b.total) + '</strong> <button type="button" class="calc-basket-remove" data-rm="' + idx + '" aria-label="Kalemi Sil">&times;</button></span>' +
            "</div>"
          );
        })
        .join("");

      basketWrap.querySelectorAll("[data-rm]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          const rmIdx = parseInt(btn.getAttribute("data-rm"), 10);
          basket.splice(rmIdx, 1);
          renderBasket();
        });
      });
      recalc();
    }

    if (addBasketBtn) {
      addBasketBtn.addEventListener("click", function () {
        const sel = getCurrentSelection();
        if (!sel.item || sel.kg <= 0) return;
        basket.push({
          name: sel.item.name,
          kg: sel.kg,
          unitPrice: sel.item.price,
          total: sel.kg * sel.item.price
        });
        renderBasket();
      });
    }

    catSelect.addEventListener("change", populateItems);
    itemSelect.addEventListener("change", recalc);
    weightInput.addEventListener("input", recalc);
    if (unitSelect) unitSelect.addEventListener("change", recalc);
    if (citySelect) citySelect.addEventListener("change", recalc);

    populateItems();
  }

  // 4. İletişim ve Kantar Çağrı Formu Doğrulama + Sunucu Gönderimi
  function initContactForms() {
    const forms = document.querySelectorAll(".js-bulgan-form");
    forms.forEach(function (form) {
      form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const nameInput = form.querySelector('[name="name"]');
        const phoneInput = form.querySelector('[name="phone"]');
        const cityInput = form.querySelector('[name="city"]');
        const matInput = form.querySelector('[name="material"]');
        const weightInput = form.querySelector('[name="weight"]');
        const noteInput = form.querySelector('[name="note"]');
        const submitBtn = form.querySelector('button[type="submit"]');

        let valid = true;

        function setErr(input, msgId, show) {
          if (!input) return;
          input.classList.toggle("input-error", show);
          const errEl = form.querySelector("#" + msgId);
          if (errEl) errEl.classList.toggle("visible", show);
          if (show) valid = false;
        }

        const nameVal = nameInput ? nameInput.value.trim() : "";
        const phoneVal = phoneInput ? phoneInput.value.replace(/\D/g, "") : "";

        setErr(nameInput, "errName", nameVal.length < 2);
        setErr(phoneInput, "errPhone", phoneVal.length < 10);

        if (!valid) return;

        const origText = submitBtn ? submitBtn.textContent : "Gönder";
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = "Kantar Merkezine İletiliyor...";
        }

        const payload = {
          name: nameVal,
          phone: phoneInput ? phoneInput.value.trim() : "",
          city: cityInput ? cityInput.value : "Mardin",
          material: matInput ? matInput.value : "Genel Hurda",
          weight: weightInput ? weightInput.value.trim() : "",
          note: noteInput ? noteInput.value.trim() : ""
        };

        try {
          await fetch("/api/contact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
        } catch (_) {}

        window.location.href =
          "/tesekkurler.html?name=" +
          encodeURIComponent(payload.name) +
          "&city=" +
          encodeURIComponent(payload.city) +
          "&material=" +
          encodeURIComponent(payload.material);
      });
    });
  }

  // 5. KVKK Çerez Tercih Yönetimi
  function initCookieBanner() {
    const bar = document.getElementById("cookieBanner");
    if (!bar) return;
    try {
      if (!localStorage.getItem("bulgan_cookie_consent")) {
        bar.classList.add("visible");
      }
    } catch (_) {}

    const acceptBtn = document.getElementById("cookieAcceptBtn");
    const essentialBtn = document.getElementById("cookieEssentialBtn");

    function saveChoice(val) {
      try {
        localStorage.setItem("bulgan_cookie_consent", val);
      } catch (_) {}
      bar.classList.remove("visible");
    }

    if (acceptBtn) {
      acceptBtn.addEventListener("click", function () {
        saveChoice("all");
      });
    }
    if (essentialBtn) {
      essentialBtn.addEventListener("click", function () {
        saveChoice("essential");
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    loadPrices();
    initContactForms();
    initCookieBanner();
  });
})();


// ==========================================================================
// 6. GOOGLE ADS DÖNÜŞÜM TAKİBİ & ADSENSE REKLAM YERLEŞİM ALTYAPISI
// (mehmethilmiozkan@gmail.com / bulganorhan19@gmail.com)
// ==========================================================================
(function () {
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = window.gtag || gtag;

  document.addEventListener("click", function (e) {
    const link = e.target && e.target.closest ? e.target.closest("a") : null;
    if (!link) return;
    const href = link.getAttribute("href") || "";

    if (href.startsWith("tel:")) {
      window.dataLayer.push({
        event: "phone_call_click",
        phone_number: href.replace("tel:", ""),
        page_path: window.location.pathname
      });
    } else if (href.includes("wa.me/")) {
      window.dataLayer.push({
        event: "whatsapp_click",
        whatsapp_url: href,
        page_path: window.location.pathname
      });
    }
  });
})();
