/* Hub Landing Page JS
   - Static-first: only enrich "Latest writing"
   - Degrades gracefully: if fetch/parse fails, show a single fallback line + link
*/

(function () {
  "use strict";

  const BLOG_ORIGIN = "https://blog.jesse-anderson.net";
  const BLOG_HOME = BLOG_ORIGIN + "/";

  // Quarto homepage contains post listing markup
  const BLOG_LISTING_URL = BLOG_HOME;

  const MAX_POSTS = 3;

  function $(sel, root = document) {
    return root.querySelector(sel);
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

  window.addEventListener("DOMContentLoaded", () => {
    loadLatestWriting();
    initMobileMenu();
  });
})();
