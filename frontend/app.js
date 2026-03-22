/* ═══════════════════════════════════════════════════════
   PriceRadar — App Logic (Phase 2)
   Handles both Price Intelligence tab and Market Trends tab
   ═══════════════════════════════════════════════════════ */

const API = "http://localhost:8000";

let currentProduct = null;
let currentMarket  = null;
let priceChart     = null;
let gtChart        = null;
let invForecastChart = null;
let invCoverageChart = null;
let searchTimer    = null;

const i18n = {
  en: {
    nav_analytics: "Analytics", title_intel: "Price Intelligence", title_trends: "Market Trends",
    kpi_avg: "Market Average", kpi_avg_sub: "5 competitors",
    kpi_low: "Lowest Price", kpi_low_sub: "Best deal",
    kpi_high: "Highest Price", kpi_high_sub: "Premium tier",
    kpi_spread: "Price Spread", kpi_spread_sub: "Opportunity gap",
    card_your_price: "💰 Your Price & Cost", card_your_price_hint: "Compare and protect margin",
    btn_analyze: "Analyze →"
  },
  gu: {
    nav_analytics: "વિશ્લેષણ", title_intel: "ભાવ વિશ્લેષણ", title_trends: "બજારના વલણો",
    kpi_avg: "સરેરાશ બજાર ભાવ", kpi_avg_sub: "૫ સ્પર્ધકો",
    kpi_low: "સૌથી ઓછો ભાવ", kpi_low_sub: "શ્રેષ્ઠ ડીલ",
    kpi_high: "સૌથી વધુ ભાવ", kpi_high_sub: "પ્રીમિયમ",
    kpi_spread: "ભાવ તફાવત", kpi_spread_sub: "તક",
    card_your_price: "💰 તમારી કિંમત અને પડતર", card_your_price_hint: "સરખામણી કરો અને માર્જિન બચાવો",
    btn_analyze: "વિશ્લેષણ કરો →"
  },
  hi: {
    nav_analytics: "विश्लेषण", title_intel: "मूल्य विश्लेषण", title_trends: "बाज़ार के रुझान",
    kpi_avg: "औसत बाज़ार मूल्य", kpi_avg_sub: "5 प्रतिस्पर्धी",
    kpi_low: "सबसे कम कीमत", kpi_low_sub: "सर्वोत्तम डील",
    kpi_high: "सबसे अधिक कीमत", kpi_high_sub: "प्रीमियम",
    kpi_spread: "मूल्य अंतर", kpi_spread_sub: "अवसर",
    card_your_price: "💰 आपकी कीमत और लागत", card_your_price_hint: "तुलना करें एवं मार्जिन बचाएं",
    btn_analyze: "विश्लेषण करें →"
  },
  fr: {
    nav_analytics: "Analytique", title_intel: "Intelligence de Prix", title_trends: "Tendances",
    kpi_avg: "Moyenne Marché", kpi_avg_sub: "5 concurrents",
    kpi_low: "Prix le Plus Bas", kpi_low_sub: "Top offre",
    kpi_high: "Prix le Plus Élevé", kpi_high_sub: "Premium",
    kpi_spread: "Écart de Prix", kpi_spread_sub: "Opportunité",
    card_your_price: "💰 Votre Prix & Coût", card_your_price_hint: "Comparez & Protégez la marge",
    btn_analyze: "Analyser →"
  },
  zh: {
    nav_analytics: "分析", title_intel: "价格智能", title_trends: "市场趋势",
    kpi_avg: "市场平均价", kpi_avg_sub: "5个竞争对手",
    kpi_low: "最低价", kpi_low_sub: "最优惠价格",
    kpi_high: "最高价", kpi_high_sub: "高级",
    kpi_spread: "价格差", kpi_spread_sub: "机会差距",
    card_your_price: "💰 您的价格与成本", card_your_price_hint: "比较并保护利润5%",
    btn_analyze: "分析 →"
  }
};

let currentLang = "en";

function setLanguage(lang) {
  currentLang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (i18n[lang] && i18n[lang][key]) {
      el.textContent = i18n[lang][key];
    }
  });
}

// ─── Init ─────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  checkApi();
  setupSearch();
  setupKeydownAnalyze();
  renderGtDefaultChips();
  startRealtimeClock();
  
  // Pre-load trends overview and catalog after a short delay
  setTimeout(() => {
    fetchProductsCatalog();
    fetchBestsellers("amazon");
    fetchSocialSignals();
    fetchInventoryStores();
  }, 800);
});

// ─── API Health ────────────────────────────────────────
async function checkApi() {
  try {
    const r = await fetch(`${API}/health`);
    setStatus(r.ok ? "ok" : "err", r.ok ? "API Connected" : "API Error");
  } catch {
    setStatus("err", "Start backend first");
  }
}

function setStatus(state, msg) {
  document.getElementById("statusDot").className  = "status-dot " + state;
  document.getElementById("statusText").textContent = msg;
}

// ─── Clock ──────────────────────────────────────────────
function startRealtimeClock() {
  const clockEl = document.getElementById("realtimeClock");
  if (!clockEl) return;
  const update = () => {
    clockEl.textContent = new Date().toLocaleTimeString("en-US", { hour12: false });
  };
  update(); // Initial call
  setInterval(update, 1000);
}

// ─── Tab Switching ─────────────────────────────────────
function switchTab(tab) {
  currentTab = tab;
  document.getElementById("tabPrices").style.display  = tab === "prices"  ? "block" : "none";
  document.getElementById("tabTrends").style.display  = tab === "trends"  ? "block" : "none";
  document.getElementById("tabInventory").style.display = tab === "inventory" ? "block" : "none";

  document.getElementById("navPrices").className = "nav-item" + (tab === "prices" ? " active" : "");
  document.getElementById("navTrends").className = "nav-item" + (tab === "trends" ? " active" : "");
  document.getElementById("navInventory").className = "nav-item" + (tab === "inventory" ? " active" : "");

  const titles = { prices: "Price Intelligence", trends: "Market Trends", inventory: "Inventory Intelligence" };
  document.getElementById("pageTitle").textContent = titles[tab] || tab;
}

function loadDemoAndSwitch(productId, tab) {
  switchTab(tab);
  selectProduct(productId);
}

// ─── Search ─────────────────────────────────────────────
function setupSearch() {
  const input = document.getElementById("searchInput");
  const drop  = document.getElementById("autocompleteDrop");
  input.addEventListener("input", () => {
    const q = input.value.trim();
    clearTimeout(searchTimer);
    if (!q) { hideDrop(); return; }
    searchTimer = setTimeout(() => fetchSuggestions(q), 280);
  });
  input.addEventListener("focus", () => {
    if (input.value.trim()) fetchSuggestions(input.value.trim());
  });
  document.addEventListener("click", e => {
    if (!e.target.closest(".topbar-search")) hideDrop();
  });
}

function setupKeydownAnalyze() {
  document.getElementById("yourPriceInput").addEventListener("keydown", e => {
    if (e.key === "Enter") analyzePrice();
  });
}

async function fetchSuggestions(q) {
  try {
    const r = await fetch(`${API}/api/products/search?q=${encodeURIComponent(q)}`);
    const data = await r.json();
    renderDropdown(data.products || []);
  } catch { hideDrop(); }
}

function renderDropdown(products) {
  const drop = document.getElementById("autocompleteDrop");
  if (!products.length) { hideDrop(); return; }
  drop.innerHTML = products.slice(0, 7).map(p => `
    <div class="auto-item" onclick="selectProduct('${p.id}')">
      <span class="auto-cat">${p.category}</span>
      <span class="auto-name">${esc(p.name)}</span>
      <span class="auto-price">₹${fmt(p.base_price)}</span>
    </div>`).join("");
  drop.style.display = "block";
}
function hideDrop() { document.getElementById("autocompleteDrop").style.display = "none"; }

// ─── Catalog Grid ───────────────────────────────────────
async function fetchProductsCatalog() {
  try {
    const r = await fetch(`${API}/api/products/search?q=`);
    const data = await r.json();
    renderCatalog(data.products || []);
  } catch (e) {
    document.getElementById("catalogGrid").innerHTML = "<p>Error loading catalog.</p>";
  }
}

function renderCatalog(products) {
  const grid = document.getElementById("catalogGrid");
  if (!products.length) return;
  grid.innerHTML = products.map(p => `
    <div class="cat-card" onclick="loadDemoAndSwitch('${p.id}', 'prices')">
      <div class="cat-category">${esc(p.category)}</div>
      <div class="cat-name">${esc(p.name)}</div>
      <div class="cat-price">₹${fmt(p.base_price)} / ${esc(p.unit)}</div>
    </div>
  `).join("");
}

// ─── Select Product ─────────────────────────────────────
async function selectProduct(productId) {
  hideDrop();
  document.getElementById("searchInput").value       = "";
  document.getElementById("emptyState").style.display    = "none";
  document.getElementById("priceDashboard").style.display = "block";
  document.getElementById("recCard").style.display        = "none";
  document.getElementById("signalsCard").style.display    = "none";
  document.getElementById("yourPriceInput").value         = "";
  document.getElementById("bannerTitle").textContent      = "Loading…";
  document.getElementById("compTable").innerHTML = '<div class="shimmer" style="height:260px;border-radius:8px"></div>';

  switchTab("prices");
  try {
    const [prod, market, history] = await Promise.all([
      fetch(`${API}/api/products/${productId}`).then(r => r.json()),
      fetch(`${API}/api/prices/${productId}`).then(r => r.json()),
      fetch(`${API}/api/history/${productId}?days=7`).then(r => r.json()),
    ]);
    currentProduct = prod;
    currentMarket  = market;

    renderBanner(prod, market);
    renderKPIs(market);
    renderCompTable(market);
    renderChart(history);
    document.getElementById("yourPriceInput").value = prod.base_price;
    document.getElementById("costPriceInput").value = Math.round(prod.base_price * 0.85); // Default 15% margin
  } catch {
    document.getElementById("bannerTitle").textContent = "Error — is the backend running?";
  }
}

// ─── Banner ─────────────────────────────────────────────
function renderBanner(prod, market) {
  document.getElementById("bannerCat").textContent   = prod.category;
  document.getElementById("bannerTitle").textContent = prod.name;
  document.getElementById("bannerBrand").textContent = "by " + prod.brand;

  const s = market.demand_signals;
  let chips = "";
  if (s.festival) {
    chips += `<span class="demand-chip festival">🎉 ${s.festival} Season (+${s.festival_boost_pct}%)</span>`;
  }
  chips += s.is_high_demand
    ? '<span class="demand-chip high">📈 High Demand</span>'
    : `<span class="demand-chip normal">📅 ${s.day_of_week}</span>`;
  document.getElementById("bannerChips").innerHTML = chips;
}

// ─── KPIs ───────────────────────────────────────────────
function renderKPIs(market) {
  const s = market.market_stats;
  animCount("kpiAvg",    s.average);
  animCount("kpiLow",    s.lowest);
  animCount("kpiHigh",   s.highest);
  document.getElementById("kpiSpread").textContent = s.spread_pct + "%";
}

// ─── Competitor Table ────────────────────────────────────
function renderCompTable(market) {
  const comps = market.competitors;
  const yourPrice = parseFloat(document.getElementById("yourPriceInput").value) || null;
  let html = "";

  if (yourPrice) {
    const belowCount = comps.filter(c => c.price < yourPrice).length;
    html += `<div class="comp-row" style="border-color:#3b82f6;background:#eff6ff">
      <span class="comp-logo">🏬</span>
      <div><div class="comp-name">Your Store</div><div class="comp-meta">Your current listing</div></div>
      <span class="comp-price price-mid" style="color:#2563eb;margin-left:auto">₹${fmt(yourPrice)}</span>
      <span class="comp-badge badge-you">${belowCount} cheaper</span>
    </div>`;
  }

  comps.forEach((c, i) => {
    const priceClass = c.tag === "cheapest" ? "price-low" : c.tag === "priciest" ? "price-high" : "price-mid";
    const badgeClass = c.tag === "cheapest" ? "badge-lowest" : c.tag === "priciest" ? "badge-highest" : "badge-mid";
    const badgeLabel = c.tag === "cheapest" ? "Lowest 🏆" : c.tag === "priciest" ? "Highest" : "Mid";
    html += `<div class="comp-row" style="animation-delay:${i*50}ms">
      <span class="comp-logo">${c.logo}</span>
      <div>
        <div class="comp-name">${esc(c.competitor_name)}</div>
        <div class="comp-meta">${c.in_stock
          ? `🚚 ${c.delivery_days}-day delivery · ⭐ ${c.rating}`
          : '<span class="oos-tag">Out of Stock</span>'}</div>
      </div>
      <span class="comp-price ${priceClass}">₹${fmt(c.price)}</span>
      <span class="comp-badge ${badgeClass}">${badgeLabel}</span>
    </div>`;
  });
  document.getElementById("compTable").innerHTML = html;
}

// ─── Chart ──────────────────────────────────────────────
function renderChart(historyData) {
  const history = historyData.history;
  const labels  = history.map(d => d.label);
  const COMP_COLORS = {
    amazon: "#2563eb", flipkart: "#7c3aed", croma: "#16a34a",
    reliance: "#dc2626", vijay: "#d97706",
  };
  const COMP_NAMES = {
    amazon: "Amazon", flipkart: "Flipkart", croma: "Croma",
    reliance: "Reliance", vijay: "Vijay Sales",
  };

  const datasets = Object.entries(COMP_COLORS).map(([cid, color]) => ({
    label: COMP_NAMES[cid],
    data: history.map(d => d.prices[cid]),
    borderColor: color, backgroundColor: color + "18",
    borderWidth: 2, pointRadius: 3, pointHoverRadius: 5, tension: 0.4, fill: false,
  }));
  datasets.push({
    label: "Market Avg", data: history.map(d => d.market_avg),
    borderColor: "#94a3b8", backgroundColor: "transparent",
    borderWidth: 1.5, borderDash: [5,4], pointRadius: 0, tension: 0.4, fill: false,
  });

  if (priceChart) priceChart.destroy();
  priceChart = new Chart(document.getElementById("priceChart").getContext("2d"), {
    type: "line", data: { labels, datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#fff", borderColor: "#e2e8f0", borderWidth: 1,
          titleColor: "#0f172a", bodyColor: "#475569",
          titleFont: { family: "Inter", weight: "700", size: 12 },
          bodyFont:  { family: "JetBrains Mono", size: 12 },
          callbacks: { label: c => ` ${c.dataset.label}: ₹${fmt(c.raw)}` },
        },
      },
      scales: {
        x: { grid: { color: "#f1f5f9" }, ticks: { color: "#94a3b8", font: { size: 11 } } },
        y: {
          grid: { color: "#f1f5f9" },
          ticks: { color: "#94a3b8", font: { family: "JetBrains Mono", size: 11 }, callback: v => "₹" + fmt(v) },
        },
      },
    },
  });

  document.getElementById("chartLegend").innerHTML = Object.entries(COMP_COLORS).map(([id, color]) =>
    `<div class="leg-item"><div class="leg-dot" style="background:${color}"></div>${COMP_NAMES[id]}</div>`
  ).join("") + `<div class="leg-item"><div class="leg-dot" style="background:#94a3b8;opacity:0.5"></div>Avg</div>`;
}

// ─── Analyze Price ───────────────────────────────────────
async function analyzePrice() {
  if (!currentProduct) return;
  const yourPrice = parseFloat(document.getElementById("yourPriceInput").value);
  const costPrice = parseFloat(document.getElementById("costPriceInput").value);
  
  if (!yourPrice || yourPrice <= 0 || !costPrice || costPrice <= 0) {
    if (!yourPrice) document.getElementById("yourPriceInput").style.borderColor = "#dc2626";
    if (!costPrice) document.getElementById("costPriceInput").style.borderColor = "#dc2626";
    setTimeout(() => {
      document.getElementById("yourPriceInput").style.borderColor = "";
      document.getElementById("costPriceInput").style.borderColor = "";
    }, 1500);
    return;
  }
  
  const btn = document.getElementById("analyzeBtn");
  btn.textContent = "Analyzing…"; btn.disabled = true;
  try {
    const r = await fetch(`${API}/api/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: currentProduct.id, your_price: yourPrice, cost_price: costPrice }),
    });
    const data = await r.json();
    renderRec(data);
    renderSignals(data.demand_signals);
    renderCompTable(currentMarket);
  } catch (e) { console.error(e); }
  finally { 
    btn.textContent = i18n[currentLang]["btn_analyze"] || "Analyze →"; 
    btn.disabled = false; 
  }
}

function renderRec(data) {
  const rec = data.recommendation;
  const badge = document.getElementById("recActionBadge");
  badge.className = `rec-action-badge ${rec.action}`;
  badge.textContent = rec.action === "reduce" ? "↓ Reduce" : rec.action === "increase" ? "↑ Raise" : "✓ Hold";

  document.getElementById("recPriceDisplay").textContent = "₹" + fmt(rec.optimal_price);

  const demClr = rec.expected_demand_chg >= 0 ? "pos" : "neg";
  const demArrow = rec.expected_demand_chg >= 0 ? "▲" : "▼";
  document.getElementById("recChips").innerHTML = `
    <span class="rec-chip ${demClr}">${demArrow} ${Math.abs(rec.expected_demand_chg)}% demand</span>
    <span class="rec-chip">${rec.gap_from_current_pct >= 0 ? "+" : ""}${rec.gap_from_current_pct}% from current</span>
    <span class="rec-chip">${rec.margin_impact_pct >= 0 ? "+" : ""}${rec.margin_impact_pct}% margin</span>`;
  document.getElementById("recReasonBox").textContent = rec.reason;
  document.getElementById("recCard").style.display = "block";
  setTimeout(() => {
    document.getElementById("confBar").style.width = rec.confidence_score + "%";
    document.getElementById("confVal").textContent = rec.confidence_score + "%";
  }, 100);
}

function renderSignals(signals) {
  const demPct = Math.round((signals.overall_demand - 1) * 100);
  document.getElementById("signalsGrid").innerHTML = `
    <div class="sig-item"><div class="sig-icon">📅</div><div class="sig-label">Day</div><div class="sig-value">${signals.day_of_week}</div></div>
    <div class="sig-item"><div class="sig-icon">📈</div><div class="sig-label">Demand</div><div class="sig-value" style="color:${demPct>5?"var(--green)":"inherit"}">${demPct>0?"+":""}${demPct}%</div></div>
    <div class="sig-item"><div class="sig-icon">🎉</div><div class="sig-label">Festival</div><div class="sig-value">${signals.festival||"None near"}</div></div>
    <div class="sig-item"><div class="sig-icon">📊</div><div class="sig-label">Market</div><div class="sig-value" style="color:${signals.is_high_demand?"var(--green)":"inherit"}">${signals.is_high_demand?"🔥 High":"Normal"}</div></div>`;
  document.getElementById("signalsCard").style.display = "block";
}

// ══════════ TRENDS TAB ══════════════════════════════════

// ─── Google Trends Default Chips ────────────────────────
function renderGtDefaultChips() {
  const chips = ["Samsung Galaxy S24", "iPhone 15 Price India", "Nike Running Shoes", "Air Fryer India", "Wireless Earbuds"];
  document.getElementById("gtDefaultChips").innerHTML = chips.map(c =>
    `<span class="gt-chip" onclick="quickGtSearch('${c}')">${c}</span>`
  ).join("");
}

function quickGtSearch(kw) {
  document.getElementById("gtKeyword").value = kw;
  fetchGoogleTrends();
}

async function fetchGoogleTrends() {
  const kw = document.getElementById("gtKeyword").value.trim();
  if (!kw) return;
  document.getElementById("gtResult").style.display = "none";

  try {
    const r = await fetch(`${API}/api/trends/google?keyword=${encodeURIComponent(kw)}`);
    const data = await r.json();
    renderGoogleTrends(data);
  } catch (e) { console.error(e); }
}

function renderGoogleTrends(data) {
  document.getElementById("gtResult").style.display = "block";
  document.getElementById("gtMeta").innerHTML = `
    <span class="gt-status">${data.status}</span>
    <span class="gt-peak">Current: <strong>${data.current_interest}</strong> · Peak: <strong>${data.peak_interest}</strong> · Region: 🇮🇳 India</span>
    ${data.source === "synthetic" ? '<span style="font-size:0.7rem;color:var(--text3)">(Demo data — pytrends throttled)</span>' : ""}`;

  const labels = data.dates
    ? data.dates
    : Array.from({length: data.interest_over_time.length}, (_, i) => {
        const d = new Date(); d.setDate(d.getDate() - (data.interest_over_time.length - 1 - i));
        return d.toLocaleDateString("en-IN", {month:"short", day:"numeric"});
      });

  if (gtChart) gtChart.destroy();
  gtChart = new Chart(document.getElementById("gtChart").getContext("2d"), {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: data.keyword,
        data: data.interest_over_time,
        borderColor: "#2563eb",
        backgroundColor: "rgba(37,99,235,0.08)",
        borderWidth: 2.5, fill: true, tension: 0.4,
        pointRadius: 4, pointBackgroundColor: "#2563eb",
      }],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#fff", borderColor: "#e2e8f0", borderWidth: 1,
          bodyColor: "#0f172a", bodyFont: { family: "Inter", size: 12 },
          callbacks: { label: c => ` Interest: ${c.raw} / 100` },
        },
      },
      scales: {
        x: { grid: { color: "#f1f5f9" }, ticks: { color: "#94a3b8" } },
        y: { min: 0, max: 100, grid: { color: "#f1f5f9" }, ticks: { color: "#94a3b8", callback: v => v } },
      },
    },
  });

  if (data.related_queries?.length) {
    document.getElementById("relatedQueries").innerHTML = `
      <div class="related-title">Related Searches</div>
      <div class="rq-chips">${data.related_queries.map(q => `<span class="rq-chip" onclick="quickGtSearch('${q}')">${q}</span>`).join("")}</div>`;
  }
}

// ─── Bestsellers ─────────────────────────────────────────
function switchPlatform(platform) {
  currentPlatform = platform;
  ["amazon","etsy","ebay"].forEach(p => {
    document.getElementById(`ptab${p.charAt(0).toUpperCase()+p.slice(1)}`).className = "ptab" + (p === platform ? " active" : "");
  });
  document.getElementById("amazonCatFilter").style.display = platform === "amazon" ? "inline-block" : "none";
  fetchBestsellers(platform);
}

async function fetchBestsellers(platform) {
  platform = platform || currentPlatform;
  const cat = document.getElementById("amazonCatFilter")?.value || "Electronics";
  const panel = document.getElementById("bestsellersPanel");
  panel.innerHTML = '<div class="shimmer" style="height:300px;border-radius:12px"></div>';

  try {
    const url = platform === "amazon"
      ? `${API}/api/trends/bestsellers?platform=amazon&category=${cat}`
      : `${API}/api/trends/bestsellers?platform=${platform}`;
    const r = await fetch(url);
    const data = await r.json();
    renderBestsellers(data, platform);
  } catch (e) {
    panel.innerHTML = `<div class="card"><p style="color:var(--text3)">Could not load data.</p></div>`;
  }
}

function renderBestsellers(data, platform) {
  let html = `<div class="card" style="padding:0;overflow:hidden">`;
  html += `<table class="bs-table"><thead><tr>`;

  if (platform === "amazon") {
    html += `<th>#</th><th>Product</th><th>Price</th><th>Change</th><th>Rating</th><th>Badge</th></tr></thead><tbody>`;
    data.items.forEach(item => {
      html += `<tr class="bs-row">
        <td class="bs-rank">${item.rank}</td>
        <td><div class="bs-title">${esc(item.title)}</div><div class="bs-brand">${esc(item.brand)}</div></td>
        <td class="bs-price">₹${fmt(item.price)}</td>
        <td><span class="rank-change">${esc(item.rank_change)}</span></td>
        <td>⭐ ${item.rating} <span style="color:var(--text3);font-size:0.7rem">(${fmt(item.reviews)})</span></td>
        <td><span class="bs-badge">${esc(item.badge)}</span></td>
      </tr>`;
    });
  } else if (platform === "etsy") {
    html += `<th>Product</th><th>Category</th><th>Price (USD)</th><th>Sales</th><th>Score</th><th>Tag</th></tr></thead><tbody>`;
    data.items.forEach(item => {
      html += `<tr class="bs-row">
        <td class="bs-title">${esc(item.title)}</td>
        <td style="color:var(--text3)">${esc(item.category)}</td>
        <td class="bs-price">$${item.price_usd}</td>
        <td class="watch-count">${fmt(item.sales)}</td>
        <td><div style="display:flex;align-items:center;gap:6px">
          <div style="width:50px;height:6px;background:var(--bg2);border-radius:99px;overflow:hidden">
            <div style="height:100%;width:${item.trending_score}%;background:#7c3aed;border-radius:99px"></div>
          </div>
          <span style="font-size:0.72rem;color:var(--text3)">${item.trending_score}</span>
        </div></td>
        <td><span class="bs-badge" style="background:var(--violet-light);color:var(--violet)">${esc(item.tag)}</span></td>
      </tr>`;
    });
  } else {
    html += `<th>Item</th><th>Category</th><th>Asking Price</th><th>Watched</th><th>Bids</th><th>Price Trend</th></tr></thead><tbody>`;
    data.items.forEach(item => {
      const upDown = item.price_trend.startsWith("+") ? "ebay-trend-up" : "ebay-trend-down";
      html += `<tr class="bs-row">
        <td><div class="bs-title">${esc(item.title)}</div><div class="bs-brand">${esc(item.condition)}</div></td>
        <td style="color:var(--text3)">${esc(item.category)}</td>
        <td class="bs-price">₹${fmt(item.price)}</td>
        <td class="watch-count">👁 ${fmt(item.watch_count)}</td>
        <td>${item.bids}</td>
        <td><span class="${upDown}">${item.price_trend}</span></td>
      </tr>`;
    });
  }

  html += `</tbody></table></div>`;
  document.getElementById("bestsellersPanel").innerHTML = html;
}

// ─── Social Signals ─────────────────────────────────────
async function fetchSocialSignals() {
  try {
    const [tiktokR, igR, pinterestR] = await Promise.all([
      fetch(`${API}/api/trends/tiktok`).then(r => r.json()),
      fetch(`${API}/api/trends/instagram`).then(r => r.json()),
      fetch(`${API}/api/trends/pinterest`).then(r => r.json()),
    ]);
    renderTikTok(tiktokR.items || []);
    renderInstagram(igR.hashtags || []);
    renderPinterest(pinterestR.trends || []);
  } catch (e) { console.error(e); }
}

function renderTikTok(items) {
  document.getElementById("tiktokList").innerHTML = items.slice(0, 6).map(item => `
    <div class="tk-item">
      <div class="tk-title">${esc(item.title)}</div>
      <div class="tk-hashtag">${esc(item.hashtag)}</div>
      <div class="tk-meta">
        <span class="tk-stat">▶ ${item.views_m}M views</span>
        <span class="tk-stat">❤️ ${item.like_rate}% like rate</span>
        <span class="tk-velocity">${item.trend_velocity}</span>
      </div>
    </div>`).join("");
}

function renderPinterest(items) {
  document.getElementById("pinterestList").innerHTML = items.slice(0, 7).map(item => `
    <div class="pin-item">
      <div class="pin-searches">${item.monthly_searches_k}k</div>
      <div class="pin-keyword">${esc(item.keyword)}</div>
      <div class="pin-growth">${esc(item.yoy_growth)}</div>
    </div>`).join("");
}

function renderInstagram(items) {
  document.getElementById("instagramList").innerHTML = items.slice(0, 7).map(item => {
    const engClass = item.engagement === "Very High" ? "eng-vh" : item.engagement === "High" ? "eng-h" : "eng-m";
    return `<div class="ig-item">
      <div class="ig-tag">${esc(item.hashtag)}</div>
      <div class="ig-posts">${item.posts_m}M posts</div>
      <span class="ig-eng ${engClass}">${item.engagement}</span>
    </div>`;
  }).join("");
}

// ─── Helpers ─────────────────────────────────────────────
function fmt(n) {
  if (n === undefined || n === null) return "—";
  return Math.round(n).toLocaleString("en-IN");
}

function animCount(id, target) {
  const el = document.getElementById(id);
  const start = performance.now(), dur = 650;
  const tick = now => {
    const p = Math.min((now - start) / dur, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    el.textContent = "₹" + fmt(Math.round(target * ease));
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

// ══════════ INVENTORY TAB ══════════════════════════════════
async function fetchInventoryStores() {
  try {
    const r = await fetch(`${API}/api/inventory/stores`);
    const data = await r.json();
    const sel = document.getElementById("invStoreSelect");
    const sumSel = document.getElementById("invSummaryFilter");
    
    let html = "";
    let sumHtml = '<option value="ALL">All Stores</option>';
    data.stores.forEach(s => {
      html += `<option value="${s.id}">${s.name}</option>`;
      sumHtml += `<option value="${s.id}">${s.name}</option>`;
    });
    sel.innerHTML = html;
    sumSel.innerHTML = sumHtml;
    
    if (data.stores.length > 0) onStoreChange();
    fetchInventorySummary();
  } catch (e) { console.error(e); }
}

async function onStoreChange() {
  try {
    const storeId = document.getElementById("invStoreSelect").value;
    const r = await fetch(`${API}/api/inventory/skus?store_id=${storeId}`);
    const data = await r.json();
    const sel = document.getElementById("invSkuSelect");
    sel.innerHTML = data.skus.map(s => `<option value="${s.id}">${s.name}</option>`).join("");
    if (data.skus.length > 0) onSkuChange();
  } catch (e) { console.error(e); }
}

function onSkuChange() {
  fetchForecast();
}

async function fetchForecast() {
  const storeId = document.getElementById("invStoreSelect").value;
  const skuId = document.getElementById("invSkuSelect").value;
  if (!storeId || !skuId) return;
  
  try {
    const r = await fetch(`${API}/api/inventory/forecast?store_id=${storeId}&sku_id=${skuId}`);
    const data = await r.json();
    renderForecastChart(data.charts.forecast_demand, data.charts.running_stock);
    renderInventoryKPIs(data.metrics);
  } catch (e) { console.error(e); }
}

function renderForecastChart(demand, stock) {
  const labels = [];
  const d = new Date();
  for (let i = 0; i < 7; i++) {
    labels.push(d.toLocaleDateString("en-US", {weekday:"short", month:"short", day:"numeric"}));
    d.setDate(d.getDate() + 1);
  }

  // Draw daily boxes
  const daysShort = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
  let boxHtml = "";
  const d2 = new Date();
  for (let i = 0; i < 7; i++) {
    boxHtml += `<div class="inv-daily-box">
      <div class="idb-day">${daysShort[d2.getDay()]}</div>
      <div class="idb-val">${demand[i]}</div>
      <div class="idb-sub">units</div>
    </div>`;
    d2.setDate(d2.getDate() + 1);
  }
  document.getElementById("invDailyBoxes").innerHTML = boxHtml;

  if (invForecastChart) invForecastChart.destroy();
  invForecastChart = new Chart(document.getElementById("forecastChart").getContext("2d"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          type: "line", label: "Running Stock", data: stock,
          borderColor: "#10b981", backgroundColor: "#10b981",
          borderWidth: 2, tension: 0.1, fill: false, yAxisID: "y1",
          pointRadius: 4, pointBackgroundColor: "#10b981", order: 1
        },
        {
          type: "bar", label: "Forecasted Demand", data: demand,
          backgroundColor: "#3b82f6", borderRadius: 4, yAxisID: "y", order: 2
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: { position: "left", title: { display: true, text: "Units/Day" }, grid: { color: "#f1f5f9" } },
        y1: { position: "right", title: { display: true, text: "Stock Left" }, grid: { display: false } }
      }
    }
  });
}

function renderInventoryKPIs(metrics) {
  document.getElementById("ikpiStock").textContent = fmt(metrics.current_stock);
  document.getElementById("ikpiNeed").textContent = fmt(metrics.total_7_day_demand);
  document.getElementById("ikpiAvg").textContent = metrics.avg_daily_demand;
  document.getElementById("ikpiReorder").textContent = fmt(metrics.reorder_qty);
  
  const box = document.getElementById("ikpiReorderBox");
  if (metrics.reorder_qty > 0) {
    box.style.borderColor = "#f59e0b";
    document.getElementById("ikpiReorder").style.color = "#f59e0b";
  } else {
    box.style.borderColor = "var(--border)";
    document.getElementById("ikpiReorder").style.color = "var(--text3)";
  }

  // Doughnut
  let cov = metrics.coverage_pct;
  document.getElementById("covCenterText").innerHTML = `${cov}%<div style="font-size:0.7rem;font-weight:500;color:var(--text3)">coverage</div>`;
  
  const color = cov >= 100 ? "#10b981" : cov >= 70 ? "#f59e0b" : "#dc2626";
  const dataArr = [Math.min(cov, 100), Math.max(0, 100 - cov)];

  if (invCoverageChart) invCoverageChart.destroy();
  invCoverageChart = new Chart(document.getElementById("coverageChart").getContext("2d"), {
    type: "doughnut",
    data: {
      datasets: [{ data: dataArr, backgroundColor: [color, "#e2e8f0"], borderWidth: 0, hoverOffset: 0 }]
    },
    options: {
      cutout: "75%", responsive: true, maintainAspectRatio: false,
      plugins: { tooltip: { enabled: false } },
      animation: { animateScale: true }
    }
  });
}

async function fetchInventorySummary() {
  const storeId = document.getElementById("invSummaryFilter").value;
  const url = storeId === "ALL" ? `${API}/api/inventory/summary` : `${API}/api/inventory/summary?store_id=${storeId}`;
  try {
    const r = await fetch(url);
    const data = await r.json();
    
    let html = "";
    data.items.forEach(item => {
      html += `<tr class="bs-row">
        <td style="font-weight:600;font-size:0.8rem">${esc(item.store_name)}</td>
        <td><div class="bs-title">${esc(item.sku_name)}</div><div class="bs-brand" style="font-family:monospace">${item.sku_id}</div></td>
        <td><span class="auto-cat" style="background:var(--bg2);color:var(--text2)">${esc(item.category)}</span></td>
        <td><span class="inv-stock-lbl">${fmt(item.current_stock)}</span><span class="stock-${item.stock_level}">${item.stock_level}</span></td>
        <td style="font-family:monospace;font-weight:600;color:#3b82f6">${fmt(item.total_demand)}</td>
        <td style="font-family:monospace">${item.avg_daily}</td>
        <td><span class="badge-risk-${item.risk}">${item.risk}</span></td>
      </tr>`;
    });
    document.getElementById("invSummaryBody").innerHTML = html || '<tr><td colspan="7" style="padding:20px;text-align:center">No data available.</td></tr>';
  } catch (e) {
    document.getElementById("invSummaryBody").innerHTML = '<tr><td colspan="7" style="padding:20px;text-align:center;color:red">Error loading summary.</td></tr>';
  }
}
