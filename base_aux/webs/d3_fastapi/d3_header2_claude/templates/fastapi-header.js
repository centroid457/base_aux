/**
 * FastAPI Universal Header Widget
 * Drop-in script — auto-reads /openapi.json and renders a service header.
 *
 * USAGE:
 *   <script src="fastapi-header.js"></script>
 *   <!-- OR with options: -->
 *   <script src="fastapi-header.js"
 *           data-env="production"
 *           data-position="top"
 *           data-theme="dark">
 *   </script>
 *
 * OPTIONS (via data- attributes on the script tag):
 *   data-env        — "development" | "staging" | "production" (default: auto-detect)
 *   data-position   — "top" | "bottom" (default: "top")
 *   data-theme      — "dark" | "light" (default: "dark")
 *   data-openapi    — custom OpenAPI JSON path (default: "/openapi.json")
 *   data-collapsed  — "true" to start collapsed (default: "false")
 */

(function () {
  "use strict";

  // ── Config ──────────────────────────────────────────────────────────────────
  const scriptTag =
    document.currentScript ||
    document.querySelector('script[src*="fastapi-header"]');

  const cfg = {
    env: scriptTag?.dataset.env || autoDetectEnv(),
    position: scriptTag?.dataset.position || "top",
    theme: scriptTag?.dataset.theme || "dark",
    openapiPath: scriptTag?.dataset.openapi || "/openapi.json",
    collapsed: scriptTag?.dataset.collapsed === "true",
  };

  function autoDetectEnv() {
    const h = location.hostname;
    if (h === "localhost" || h === "127.0.0.1" || h.startsWith("192.168"))
      return "development";
    if (h.includes("staging") || h.includes("stage") || h.includes("dev"))
      return "staging";
    return "production";
  }

  // ── Styles ───────────────────────────────────────────────────────────────────
  const THEMES = {
    dark: {
      bg: "#0d0d0f",
      bgSecondary: "#17171b",
      border: "#2a2a32",
      text: "#e8e8f0",
      textMuted: "#6b6b80",
      textDim: "#9494aa",
      accent: "#00d4aa",
      accentBg: "rgba(0,212,170,0.08)",
      tagBg: "#1e1e26",
      shadow: "0 4px 32px rgba(0,0,0,0.6)",
      envColors: {
        development: { bg: "#1a2a1a", text: "#4ade80", dot: "#22c55e" },
        staging: { bg: "#2a2210", text: "#fbbf24", dot: "#f59e0b" },
        production: { bg: "#1a1020", text: "#c084fc", dot: "#a855f7" },
      },
    },
    light: {
      bg: "#f8f8fc",
      bgSecondary: "#ffffff",
      border: "#dddde8",
      text: "#18181f",
      textMuted: "#8888a0",
      textDim: "#55556a",
      accent: "#0096cc",
      accentBg: "rgba(0,150,204,0.07)",
      tagBg: "#ebebf5",
      shadow: "0 4px 32px rgba(0,0,0,0.10)",
      envColors: {
        development: { bg: "#edfff0", text: "#16a34a", dot: "#22c55e" },
        staging: { bg: "#fffbeb", text: "#d97706", dot: "#f59e0b" },
        production: { bg: "#faf5ff", text: "#9333ea", dot: "#a855f7" },
      },
    },
  };

  const t = THEMES[cfg.theme] || THEMES.dark;
  const envStyle = t.envColors[cfg.env] || t.envColors.development;

  const css = `
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap');

  #__fapi-header__ {
    all: initial;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    background: ${t.bg};
    color: ${t.text};
    border-bottom: 1px solid ${t.border};
    box-shadow: ${t.shadow};
    position: fixed;
    ${cfg.position === "bottom" ? "bottom: 0;" : "top: 0;"}
    left: 0;
    right: 0;
    z-index: 99999;
    transition: transform 0.25s cubic-bezier(.4,0,.2,1);
    line-height: 1;
    user-select: none;
  }

  #__fapi-header__.fapi-hidden {
    transform: translateY(${cfg.position === "bottom" ? "100%" : "-100%"});
  }

  #__fapi-header__ * { box-sizing: border-box; }

  .fapi-bar {
    display: flex;
    align-items: center;
    gap: 0;
    height: 40px;
    padding: 0 16px;
    overflow: hidden;
  }

  .fapi-logo {
    display: flex;
    align-items: center;
    gap: 7px;
    margin-right: 18px;
    flex-shrink: 0;
  }

  .fapi-logo-icon {
    width: 20px;
    height: 20px;
    background: ${t.accent};
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .fapi-logo-icon svg {
    width: 12px;
    height: 12px;
    fill: #000;
  }

  .fapi-service-name {
    font-size: 13px;
    font-weight: 600;
    color: ${t.text};
    letter-spacing: -0.3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 220px;
  }

  .fapi-divider {
    width: 1px;
    height: 20px;
    background: ${t.border};
    margin: 0 14px;
    flex-shrink: 0;
  }

  .fapi-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    height: 22px;
    padding: 0 9px;
    border-radius: 4px;
    background: ${t.tagBg};
    border: 1px solid ${t.border};
    color: ${t.textDim};
    font-size: 11px;
    white-space: nowrap;
    flex-shrink: 0;
    margin-right: 6px;
    letter-spacing: 0.2px;
  }

  .fapi-pill.accent {
    background: ${t.accentBg};
    border-color: ${t.accent}44;
    color: ${t.accent};
  }

  .fapi-env-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    height: 22px;
    padding: 0 9px;
    border-radius: 4px;
    background: ${envStyle.bg};
    color: ${envStyle.text};
    font-size: 11px;
    font-weight: 500;
    white-space: nowrap;
    flex-shrink: 0;
    margin-right: 6px;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    border: 1px solid ${envStyle.dot}44;
  }

  .fapi-env-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: ${envStyle.dot};
    animation: fapi-pulse 2s infinite;
    flex-shrink: 0;
  }

  .fapi-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #888;
    flex-shrink: 0;
  }

  .fapi-status-dot.ok { background: #22c55e; animation: fapi-pulse 2.5s infinite; }
  .fapi-status-dot.err { background: #ef4444; }
  .fapi-status-dot.loading { background: #f59e0b; animation: fapi-blink 1s infinite; }

  @keyframes fapi-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  @keyframes fapi-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
  }

  .fapi-spacer { flex: 1; }

  .fapi-label {
    color: ${t.textMuted};
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-right: 4px;
  }

  .fapi-link {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    height: 26px;
    padding: 0 10px;
    border-radius: 4px;
    background: ${t.accentBg};
    border: 1px solid ${t.accent}55;
    color: ${t.accent};
    font-size: 11px;
    font-weight: 500;
    text-decoration: none !important;
    cursor: pointer;
    margin-left: 6px;
    letter-spacing: 0.2px;
    transition: background 0.15s, border-color 0.15s;
    flex-shrink: 0;
    font-family: 'IBM Plex Mono', monospace;
  }

  .fapi-link:hover {
    background: ${t.accent}22;
    border-color: ${t.accent};
  }

  .fapi-link svg { width: 10px; height: 10px; fill: currentColor; }

  .fapi-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 4px;
    border: 1px solid ${t.border};
    background: ${t.tagBg};
    color: ${t.textMuted};
    cursor: pointer;
    margin-left: 8px;
    transition: background 0.15s;
    flex-shrink: 0;
  }

  .fapi-toggle:hover { background: ${t.bgSecondary}; color: ${t.text}; }

  .fapi-routes-panel {
    background: ${t.bgSecondary};
    border-top: 1px solid ${t.border};
    padding: 12px 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    max-height: 120px;
    overflow-y: auto;
  }

  .fapi-route-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    height: 20px;
    padding: 0 8px;
    border-radius: 3px;
    font-size: 10.5px;
    background: ${t.tagBg};
    border: 1px solid ${t.border};
    color: ${t.textDim};
    letter-spacing: 0.2px;
  }

  .fapi-method {
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding: 1px 4px;
    border-radius: 2px;
  }

  .fapi-method.GET    { background: #0d3321; color: #4ade80; }
  .fapi-method.POST   { background: #1e2a3a; color: #60a5fa; }
  .fapi-method.PUT    { background: #2a1e0d; color: #fbbf24; }
  .fapi-method.DELETE { background: #2a0d0d; color: #f87171; }
  .fapi-method.PATCH  { background: #1e1a2a; color: #c084fc; }
  .fapi-method.HEAD   { background: #1a2a2a; color: #67e8f9; }

  .fapi-uptime-bar {
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .fapi-uptime-blocks {
    display: flex;
    gap: 2px;
  }

  .fapi-uptime-block {
    width: 5px;
    height: 14px;
    border-radius: 1.5px;
    background: #22c55e;
    opacity: 0.9;
  }

  .fapi-uptime-block.miss { background: #ef4444; opacity: 0.7; }
  `;

  // ── DOM ───────────────────────────────────────────────────────────────────────
  function injectCSS(css) {
    const s = document.createElement("style");
    s.textContent = css;
    document.head.appendChild(s);
  }

  function svg(path, viewBox = "0 0 16 16") {
    return `<svg viewBox="${viewBox}" xmlns="http://www.w3.org/2000/svg"><path d="${path}"/></svg>`;
  }

  const ICONS = {
    bolt: svg("M9.5 2L4 9h5l-1 5 5.5-7H9l.5-5z"),
    docs: svg("M3 2h7l3 3v9H3V2zm7 0v3h3M6 8h4M6 11h4"),
    redoc: svg("M2 2h12v12H2z"),
    external: svg("M10 2h4v4M7 9l7-7M4 4H2v10h10v-2"),
    routes: svg("M2 4h12M2 8h8M2 12h5"),
    collapse: svg("M4 10l4-4 4 4"),
    expand: svg("M4 6l4 4 4-4"),
    copy: svg("M4 4h7v9H4zM7 2h5v7"),
    check: svg("M3 8l3 3 7-7"),
  };

  function buildHeader(info) {
    const { title, version, description, routes, routeCount, healthy } = info;

    const uptimeBlocks = Array.from({ length: 12 }, (_, i) =>
      `<div class="fapi-uptime-block${i === 3 || i === 7 ? " miss" : ""}"></div>`
    ).join("");

    return `
      <div class="fapi-bar">
        <div class="fapi-logo">
          <div class="fapi-logo-icon">${ICONS.bolt}</div>
          <span class="fapi-service-name" title="${title}">${title}</span>
        </div>

        <div class="fapi-divider"></div>

        <div class="fapi-pill accent">
          v${version}
        </div>

        <div class="fapi-env-pill">
          <span class="fapi-env-dot"></span>
          ${cfg.env}
        </div>

        <div class="fapi-divider"></div>

        <div class="fapi-pill" id="fapi-status-pill">
          <span class="fapi-status-dot loading" id="fapi-status-dot"></span>
          <span id="fapi-status-text">checking</span>
        </div>

        <div class="fapi-pill" id="fapi-routes-pill" style="cursor:pointer" title="Show routes">
          ${ICONS.routes}
          <span id="fapi-route-count">${routeCount}</span> routes
        </div>

        <div class="fapi-uptime-bar fapi-pill" title="Uptime (last 12 checks, simulated)">
          <div class="fapi-uptime-blocks">${uptimeBlocks}</div>
        </div>

        <div class="fapi-spacer"></div>

        ${description ? `<span class="fapi-label" style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${description}">${description}</span>` : ""}

        <a class="fapi-link" href="/docs" target="_blank" title="Swagger UI">
          ${ICONS.docs} docs
        </a>
        <a class="fapi-link" href="/redoc" target="_blank" title="ReDoc">
          ${ICONS.redoc} redoc
        </a>

        <div class="fapi-toggle" id="fapi-collapse-btn" title="Toggle header">
          ${cfg.collapsed ? ICONS.expand : ICONS.collapse}
        </div>
      </div>
      <div id="fapi-routes-panel" class="fapi-routes-panel" style="display:none;"></div>
    `;
  }

  // ── API Fetch ────────────────────────────────────────────────────────────────
  async function fetchOpenAPI() {
    try {
      const res = await fetch(cfg.openapiPath);
      if (!res.ok) throw new Error("not ok");
      const data = await res.json();

      const title = data.info?.title || "FastAPI Service";
      const version = data.info?.version || "0.0.0";
      const description = data.info?.description || "";

      const routes = [];
      for (const [path, methods] of Object.entries(data.paths || {})) {
        for (const method of Object.keys(methods)) {
          if (["get", "post", "put", "delete", "patch", "head"].includes(method)) {
            routes.push({ method: method.toUpperCase(), path });
          }
        }
      }

      return { title, version, description, routes, routeCount: routes.length, healthy: true };
    } catch {
      return {
        title: "FastAPI Service",
        version: "—",
        description: "",
        routes: [],
        routeCount: 0,
        healthy: false,
      };
    }
  }

  async function checkHealth() {
    try {
      const res = await fetch("/health", { method: "GET", signal: AbortSignal.timeout(3000) });
      return res.ok;
    } catch {
      try {
        // fallback: ping openapi endpoint
        const res2 = await fetch(cfg.openapiPath, { method: "HEAD", signal: AbortSignal.timeout(3000) });
        return res2.ok;
      } catch { return false; }
    }
  }

  // ── Init ─────────────────────────────────────────────────────────────────────
  async function init() {
    injectCSS(css);

    const root = document.createElement("div");
    root.id = "__fapi-header__";
    if (cfg.collapsed) root.classList.add("fapi-hidden");
    document.body.insertBefore(root, document.body.firstChild);

    // push page content down
    const spacer = document.createElement("div");
    spacer.id = "__fapi-spacer__";
    spacer.style.cssText = `height:40px;${cfg.position === "bottom" ? "display:none" : ""}`;
    document.body.insertBefore(spacer, root.nextSibling);

    const info = await fetchOpenAPI();
    root.innerHTML = buildHeader(info);

    // health check
    const dot = root.querySelector("#fapi-status-dot");
    const txt = root.querySelector("#fapi-status-text");
    const healthy = await checkHealth();
    if (dot && txt) {
      dot.className = "fapi-status-dot " + (healthy ? "ok" : "err");
      txt.textContent = healthy ? "healthy" : "unreachable";
    }

    // routes panel toggle
    const routesPill = root.querySelector("#fapi-routes-pill");
    const panel = root.querySelector("#fapi-routes-panel");
    if (routesPill && panel && info.routes.length) {
      panel.innerHTML = info.routes
        .map(
          (r) =>
            `<div class="fapi-route-tag">
              <span class="fapi-method ${r.method}">${r.method}</span>
              ${r.path}
            </div>`
        )
        .join("");

      routesPill.addEventListener("click", () => {
        const open = panel.style.display !== "none";
        panel.style.display = open ? "none" : "flex";
        spacer.style.height = open ? "40px" : `${root.offsetHeight}px`;
      });
    }

    // collapse toggle
    const collapseBtn = root.querySelector("#fapi-collapse-btn");
    let collapsed = cfg.collapsed;
    if (collapseBtn) {
      collapseBtn.addEventListener("click", () => {
        collapsed = !collapsed;
        root.classList.toggle("fapi-hidden", collapsed);
        spacer.style.height = collapsed ? "0px" : `${root.offsetHeight}px`;
        collapseBtn.innerHTML = collapsed ? ICONS.expand : ICONS.collapse;
      });
    }

    // keyboard shortcut: Alt+H to toggle
    document.addEventListener("keydown", (e) => {
      if (e.altKey && e.key === "h") collapseBtn?.click();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
