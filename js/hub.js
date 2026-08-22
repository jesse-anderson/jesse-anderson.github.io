/* Hub Landing Page JS
   - Static-first: only enrich "Latest writing"
   - Degrades gracefully: if fetch/parse fails, show a single fallback line + link
*/

(function () {
  "use strict";

  const TOOLS_ORIGIN = "https://tools.jesse-anderson.net";
  const TOOLS_HOME = TOOLS_ORIGIN + "/tools.html";
  const BLOG_ORIGIN = "https://blog.jesse-anderson.net";
  const BLOG_HOME = BLOG_ORIGIN + "/";

  const SENSORS_ORIGIN = "https://sensors.jesse-anderson.net";
  // Few-KB extract built for exactly this chart. The full daily-stats artifact is
  // ~256 KB, which is not a sane download for one sparkline.
  const SENSORS_SUMMARY_URL = SENSORS_ORIGIN + "/data/public/summary.json";

  // Quarto homepage contains post listing markup
  const BLOG_LISTING_URL = BLOG_HOME;

  const MAX_POSTS = 3;

  function $(sel, root = document) {
    return root.querySelector(sel);
  }

  function $$(sel, root = document) {
    return root.querySelectorAll(sel);
  }
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function normalizeUrl(href) {
    if (!href) return null;
    try {
      // Handles relative hrefs (e.g., ./posts/foo/index.html)
      return new URL(href, BLOG_ORIGIN).toString();
    } catch {
      return href;
    }
  }

  function uniqueNonEmpty(arr) {
    const out = [];
    const seen = new Set();
    for (const v of arr || []) {
      const s = String(v || "").trim();
      if (!s) continue;
      const key = s.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(s);
    }
    return out;
  }

  function withTimeout(ms) {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), ms);
    return { controller, cancel: () => clearTimeout(id) };
  }

  // ============================================
  // TOOLS STATS FUNCTIONALITY
  // ============================================

  /**
   * Fetches tools.html and extracts tool statistics
   * @param {string} toolsUrl - URL to tools.html
   * @returns {Promise<{totalTools: number, categories: Array<{name: string, count: number}>, error?: string}>}
   */
  async function getToolsStats(toolsUrl = TOOLS_HOME) {
    const { controller, cancel } = withTimeout(4500);

    try {
      const response = await fetch(toolsUrl, {
        method: "GET",
        mode: "cors",
        cache: "no-store",
        signal: controller.signal
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch tools.html: ${response.status}`);
      }

      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");

      const categories = [];
      let totalTools = 0;

      const sections = doc.querySelectorAll(".category-section");

      for (const section of sections) {
        const titleEl = section.querySelector(".category-title");
        const categoryName = titleEl ? titleEl.textContent.trim() : "Unknown";

        const toolCards = section.querySelectorAll(".tools-grid .tool-card");
        const toolCount = toolCards.length;

        if (toolCount > 0) {
          categories.push({
            name: categoryName,
            count: toolCount
          });
          totalTools += toolCount;
        }
      }

      return { totalTools, categories };
    } catch (err) {
      console.error("Error fetching tools stats:", err);
      return { totalTools: 0, categories: [], error: err.message };
    } finally {
      cancel();
    }
  }

  /**
   * Updates the UI with tools statistics
   */
  async function loadToolsStats() {
    const stats = await getToolsStats();

    if (stats.error || stats.totalTools === 0) {
      return; // Silently fail - static content remains as fallback
    }

    // Update the Tools Hub card examples list with dynamic categories
    const toolsCard = $(".destination-card--tools");
    if (toolsCard) {
      const examplesList = toolsCard.querySelector(".card-examples");
      if (examplesList && stats.categories.length > 0) {
        examplesList.innerHTML = "";
        const topCategories = stats.categories
          .sort((a, b) => b.count - a.count)
          .slice(0, 3);

        for (const cat of topCategories) {
          const li = el("li", "", `${cat.name} (${cat.count})`);
          examplesList.appendChild(li);
        }
      }

      // Add badge showing total tools count
      const cardTitle = toolsCard.querySelector(".card-title");
      if (cardTitle && !cardTitle.querySelector(".tools-count-badge")) {
        const badge = el("span", "tools-count-badge", stats.totalTools.toString());
        badge.setAttribute("title", `${stats.totalTools} tools available`);
        cardTitle.appendChild(badge);
      }
    }

    // Update "View all tools →" link with count
    const viewAllLink = $('a.text-link[href*="tools.jesse-anderson.net"]');
    if (viewAllLink && !viewAllLink.dataset.updated) {
      viewAllLink.textContent = `View all ${stats.totalTools} tools →`;
      viewAllLink.dataset.updated = "true";
    }
  }

  function renderFallback(container) {
    container.innerHTML = "";
    container.setAttribute("aria-busy", "false");

    const box = el("div", "writing-item");
    const title = el("h3", "writing-title");
    const a = el("a", "");
    a.href = BLOG_HOME;
    a.textContent = "Browse all posts on the blog →";
    title.appendChild(a);

    const p = el("p", "muted");
    p.textContent = "Latest posts are available on the blog (auto-loading may be blocked by network/CORS settings).";

    box.appendChild(title);
    box.appendChild(p);
    container.appendChild(box);
  }

  function renderPosts(container, posts) {
    container.innerHTML = "";
    container.setAttribute("aria-busy", "false");

    for (const post of posts.slice(0, MAX_POSTS)) {
      const card = el("div", "writing-item");

      const h = el("h3", "writing-title");
      const a = el("a", "");
      a.href = post.url || BLOG_HOME;
      a.textContent = post.title || "Untitled post";
      h.appendChild(a);

      const meta = el("div", "writing-meta");

      const date = el("div", "writing-date", post.dateText || "");
      meta.appendChild(date);

      if (post.tags && post.tags.length) {
        const tagsWrap = el("div", "writing-tags");
        for (const t of post.tags.slice(0, 2)) {
          tagsWrap.appendChild(el("span", "writing-tag", t));
        }
        meta.appendChild(tagsWrap);
      }

      card.appendChild(h);
      card.appendChild(meta);
      container.appendChild(card);
    }
  }

  function parseQuartoListingFromHtml(htmlText) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlText, "text/html");

    const postNodes = Array.from(doc.querySelectorAll(".quarto-post"));
    const posts = [];

    for (const node of postNodes) {
      const titleAnchor =
        node.querySelector(".listing-title a") ||
        node.querySelector("h3.listing-title a") ||
        node.querySelector("a.no-external");

      const title = titleAnchor ? titleAnchor.textContent.trim() : null;
      const url = titleAnchor ? normalizeUrl(titleAnchor.getAttribute("href")) : null;

      const dateEl = node.querySelector(".listing-date");
      const dateText = dateEl ? dateEl.textContent.trim() : "";

      const dateSortRaw = node.getAttribute("data-listing-date-sort") || "";
      const dateSort = Number(dateSortRaw);
      const safeDateSort = Number.isFinite(dateSort) ? dateSort : 0;

      const tags = uniqueNonEmpty(
        Array.from(node.querySelectorAll(".listing-category")).map((t) => t.textContent)
      );

      if (title && url) {
        posts.push({
          title,
          url,
          dateText,
          dateSort: safeDateSort,
          tags
        });
      }
    }

    posts.sort((a, b) => (b.dateSort || 0) - (a.dateSort || 0));
    return posts.slice(0, MAX_POSTS);
  }

  async function loadLatestWriting() {
    const container = $("#latestWriting");
    if (!container) return;

    // Keep the skeleton visible until we either render posts or render fallback.
    container.setAttribute("aria-busy", "true");

    const { controller, cancel } = withTimeout(4500);

    try {
      const resp = await fetch(BLOG_LISTING_URL, {
        method: "GET",
        mode: "cors",
        cache: "no-store",
        redirect: "follow",
        signal: controller.signal
      });

      if (!resp.ok) throw new Error("Fetch failed: " + resp.status);

      const html = await resp.text();
      const posts = parseQuartoListingFromHtml(html);

      if (!posts || !posts.length) {
        renderFallback(container);
        return;
      }

      renderPosts(container, posts);
    } catch (err) {
      // Graceful: show one useful fallback tile; no uncaught console errors.
      renderFallback(container);
    } finally {
      cancel();
    }
  }

  // Mobile menu toggle functionality
  function initMobileMenu() {
    const toggle = $(".mobile-menu-toggle");
    const mobileNav = $(".mobile-nav");
    
    if (!toggle || !mobileNav) return;
    
    toggle.addEventListener("click", () => {
      const isOpen = mobileNav.classList.toggle("active");
      toggle.classList.toggle("active", isOpen);
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
    
    // Close menu when clicking a link
    mobileNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        mobileNav.classList.remove("active");
        toggle.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Theme toggle functionality
  function initThemeToggle() {
    const btn = $(".theme-toggle-btn");
    if (!btn) return;

    // Get saved theme or detect system preference
    function getPreferredTheme() {
      const saved = localStorage.getItem("theme");
      if (saved) return saved;
      return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }

    // Apply theme to document
    function setTheme(theme) {
      document.documentElement.setAttribute("data-theme", theme);
      localStorage.setItem("theme", theme);
    }

    // Initialize
    setTheme(getPreferredTheme());

    // Toggle on click
    btn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      setTheme(current === "dark" ? "light" : "dark");
    });

    // Listen for system preference changes
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
      if (!localStorage.getItem("theme")) {
        setTheme(e.matches ? "dark" : "light");
      }
    });
  }
  /* ---- Sensor sparkline -------------------------------------------------
     Indoor vs outdoor daily mean PM2.5. Plotted together on purpose: indoor PM
     on its own cannot tell a stove from regional smoke, and the pair can.
     The data is published on a 30-day delay, so this shows the depth of the
     record, NOT current liveness — the caption has to say so.
     Static-first like the rest of this file: the block stays hidden unless real
     data arrives, so a failed fetch leaves no empty chart behind.
  */
  const SVGNS = "http://www.w3.org/2000/svg";
  const svgEl = (name, attrs) => {
    const n = document.createElementNS(SVGNS, name);
    Object.keys(attrs).forEach((k) => n.setAttribute(k, attrs[k]));
    return n;
  };

  // "Nice" axis bounds: round the domain out to a readable step so the y labels are
  // numbers a person would actually write down.
  function niceBounds(lo, hi) {
    if (!(hi > lo)) return { lo: 0, hi: Math.max(1, hi || 1), step: 1 };
    const raw = (hi - lo) / 3;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw) || 10 * mag;
    return { lo: Math.floor(lo / step) * step, hi: Math.ceil(hi / step) * step, step };
  }

  function sparkPath(values, geo) {
    const step = values.length > 1 ? (geo.w - geo.l - geo.r) / (values.length - 1) : 0;
    const span = geo.hi - geo.lo || 1;
    let d = "", pen = false;
    values.forEach((v, i) => {
      if (v === null || v === undefined) { pen = false; return; }   // gaps stay gaps
      const x = geo.l + i * step;
      const y = geo.h - geo.b - ((v - geo.lo) / span) * (geo.h - geo.t - geo.b);
      d += (pen ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1) + " ";
      pen = true;
    });
    return d.trim();
  }

  function buildSparkSvg(data, W, H) {
    const t = data.t || [];
    const series = [["outdoor", data.outdoor_pm25 || []], ["indoor", data.indoor_pm25 || []]];
    const present = series.reduce((a, s) => a.concat(s[1]), [])
      .filter((v) => typeof v === "number");
    if (!t.length || !present.length) return null;

    const nb = niceBounds(Math.min.apply(null, present), Math.max.apply(null, present));
    const geo = { w: W, h: H, l: 34, r: 6, t: 8, b: 20, lo: nb.lo, hi: nb.hi };

    const svg = svgEl("svg", {
      viewBox: "0 0 " + W + " " + H, class: "spark-svg", role: "img",
      "aria-label": "Daily mean PM2.5 in micrograms per cubic metre, indoor versus "
        + "outdoor, " + t[0] + " to " + t[t.length - 1]
    });

    // y gridlines + labels
    for (let v = nb.lo; v <= nb.hi + 1e-9; v += nb.step) {
      const y = geo.h - geo.b - ((v - geo.lo) / (geo.hi - geo.lo || 1)) * (geo.h - geo.t - geo.b);
      svg.appendChild(svgEl("line", {
        x1: geo.l, x2: geo.w - geo.r, y1: y.toFixed(1), y2: y.toFixed(1), class: "spark-grid"
      }));
      const lab = svgEl("text", { x: geo.l - 5, y: (y + 3).toFixed(1), class: "spark-axis",
        "text-anchor": "end" });
      lab.textContent = String(Math.round(v * 10) / 10);
      svg.appendChild(lab);
    }

    // y unit, x endpoints
    const unit = svgEl("text", { x: 0, y: 0, class: "spark-axis spark-axis--unit",
      transform: "translate(9," + (geo.h / 2) + ") rotate(-90)", "text-anchor": "middle" });
    unit.textContent = "µg/m³";
    svg.appendChild(unit);

    [[t[0], geo.l, "start"], [t[t.length - 1], geo.w - geo.r, "end"]].forEach((x) => {
      const lab = svgEl("text", { x: x[1], y: geo.h - 6, class: "spark-axis",
        "text-anchor": x[2] });
      lab.textContent = x[0];
      svg.appendChild(lab);
    });

    series.forEach((pair) => {
      const d = sparkPath(pair[1], geo);
      if (d) svg.appendChild(svgEl("path", { d: d, fill: "none",
        class: "spark-line spark-line--" + pair[0] }));
    });
    return svg;
  }

  function renderSparkline(box, data) {
    const host = box.querySelector("[data-spark-chart]");
    const draw = (w, h) => {
      host.textContent = "";
      const svg = buildSparkSvg(data, w, h);
      if (svg) host.appendChild(svg);
      return !!svg;
    };
    if (!draw(560, 150)) return false;

    // One ratio per indoor sensor. They disagree, and that is worth showing rather
    // than averaging away; the charted one is marked.
    const ratios = Object.keys(data.io_ratio || {})
      .filter((k) => typeof data.io_ratio[k].median === "number")
      .sort();
    if (ratios.length) {
      const r = box.querySelector("[data-spark-ratio]");
      r.textContent = "indoor/outdoor median · " + ratios.map(function (k) {
        const s = data.io_ratio[k];
        const mark = k === data.primary_indoor ? " (charted)" : "";
        return k.replace(/-/g, " ") + " " + s.median.toFixed(2) + mark;
      }).join(" · ");
      r.hidden = false;
    }
    box.querySelector("[data-spark-through]").textContent = data.published_through || "";

    // Expand: same chart, more room. Escape or the backdrop closes it.
    const btn = box.querySelector("[data-spark-expand]");
    if (btn) {
      const onKey = (e) => { if (e.key === "Escape") toggle(false); };
      function toggle(open) {
        box.classList.toggle("spark--full", open);
        btn.setAttribute("aria-expanded", String(open));
        document.body.style.overflow = open ? "hidden" : "";
        draw(open ? 1100 : 560, open ? Math.max(320, window.innerHeight - 260) : 150);
        if (open) document.addEventListener("keydown", onKey);
        else document.removeEventListener("keydown", onKey);
      }
      btn.addEventListener("click", () =>
        toggle(!box.classList.contains("spark--full")));
      box.addEventListener("click", (e) => {
        if (e.target === box && box.classList.contains("spark--full")) toggle(false);
      });
    }
    box.hidden = false;
    return true;
  }

  async function loadSensorSparkline() {
    const box = document.querySelector("[data-spark]");
    if (!box) return;
    const { controller, cancel } = withTimeout(4500);
    try {
      const resp = await fetch(SENSORS_SUMMARY_URL, {
        method: "GET", mode: "cors", cache: "no-store",
        redirect: "follow", signal: controller.signal
      });
      if (!resp.ok) throw new Error("Fetch failed: " + resp.status);
      renderSparkline(box, await resp.json());
    } catch (err) {
      console.error("Error fetching sensor summary:", err);   // block stays hidden
    } finally {
      cancel();
    }
  }

  window.addEventListener("DOMContentLoaded", () => {
    loadLatestWriting();
    loadToolsStats();
    loadSensorSparkline();
    initMobileMenu();
    initThemeToggle();
  });
})();
