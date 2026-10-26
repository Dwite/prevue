// 구조 시안 공용 — 문구 사전 · 아이콘 · 창 틀. 영어 문구는 길이 확인용 임시 문구다(실제 문구는 영어 버전 작업이 쓴다).
const LANG = new URLSearchParams(location.search).get("lang") === "en" ? "en" : "ko";
document.documentElement.lang = LANG;

const ICON = {
  glyph: `<svg viewBox="0 0 240 240" aria-hidden="true"><polygon points="120,40 189.3,80 120,120 50.7,80" fill="currentColor"/><polygon points="189.3,80 189.3,160 120,200 120,120" fill="currentColor" opacity=".62"/><polygon points="50.7,80 120,120 120,200 50.7,160" fill="currentColor" opacity=".34"/><path d="M14 44V14H44M14 196V226H44M226 44V14H196M226 196V226H196" fill="none" stroke="currentColor" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  ok: `<svg class="ic" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m3.5 8.5 3 3 6-7"/></svg>`,
  busy: `<svg class="ic" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M8 2.5a5.5 5.5 0 1 1-5.5 5.5"/></svg>`,
  search: `<svg class="ic" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 3 3"/></svg>`,
  plus: `<svg class="ic" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M8 3.5v9M3.5 8h9"/></svg>`,
  branch: `<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="5" cy="3.5" r="1.5"/><circle cx="5" cy="12.5" r="1.5"/><circle cx="11" cy="5.5" r="1.5"/><path d="M5 5v6M11 7c0 2.5-6 2-6 4"/></svg>`,
  chevron: `<svg class="ic" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="m4.5 6.5 3.5 3.5 3.5-3.5"/></svg>`,
  file: `<svg class="ic" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M4 2h5.5L12 4.5V14H4z"/></svg>`,
};

// 시안이 그리는 대상 — nowinandroid 렌더(img/)와 같은 앱
const APP = { name: "Now in Android", tile: "N", dir: "nowinandroid", branch: "main", rest: "feature:foryou · demoDebug" };
const TABS = [
  { name: "ForYouScreen", sel: true }, { name: "NiaButton" }, { name: "SearchScreen", stale: true },
  { name: "InterestsScreen" }, { name: "SearchScreen", mod: "core:ui" },
];

function tabsHtml() {
  return TABS.map(t => `<span class="tab" role="tab" aria-selected="${!!t.sel}"><span class="name">${t.name}</span>${t.stale ? `<span class="tdot" title="${t_("stale")}"></span>` : ""}</span>`).join("");
}
function subHtml() {
  return `<span class="pj">${APP.dir}</span><span class="pj">${ICON.branch}${APP.branch}</span><span class="rest">· ${APP.rest}</span>`;
}
function pillHtml(state) {
  if (state === "busy") return `<span class="pill busy">${ICON.busy}<span class="pt long">${t_("compiling")} ForYouScreen.kt</span><span class="pt count">3/20</span></span>`;
  return `<span class="pill ok">${ICON.ok}<span class="pt">640ms</span></span>`;
}
// 확정 — 헤더 안 C(파일 레일) + 돋보기 없음(빠른 열기 입구는 레일의 "파일 열기 ⌘K"와 / · ⌘K). 배치 CSS는 draft.css 의 .shell
const XI = `<svg class="ic" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="m5 5 6 6M11 5l-6 6"/></svg>`;
function railHtml() {
  return `<nav class="rail"><h4>${t_("openFiles")}</h4>${TABS.map((t, i) => `<span class="rt${i === 3 ? " hover" : ""}" aria-selected="${!!t.sel}" title="feature/foryou/src/main/kotlin/…/${t.name}.kt">${ICON.file}<span class="name">${t.name}</span>${t.mod ? `<span class="mod">${t.mod}</span>` : ""}${t.stale ? `<span class="tdot" title="${t_("stale")}"></span>` : ""}<span class="x">${XI}</span></span>`).join("")}
    <span class="rt open">${ICON.plus}<span class="name">${t_("openFile")}</span><kbd>⌘K</kbd></span></nav>`;
}
function shellC(state, content) {
  return `<div class="shell"><div class="r1"><span class="brand">${ICON.glyph}<span>Prevue</span></span><span class="sep"></span>
      <div class="lock"><span class="tile">${APP.tile}</span><div class="t"><div class="app-name">${APP.name}</div><div class="sub">${subHtml()}</div></div></div>
      <span class="grow"></span><div class="tools">${pillHtml(state)}<button class="icon-btn">?</button></div></div>
    <div class="body">${railHtml()}<div class="main">${content}</div></div></div>`;
}

// 옛 확정(헤더 안 A) — 비교용으로 남긴다 — 다른 화면 시안이 위에 얹는다. 배치 CSS는 draft.css 의 .hdr
function headerA(state, tabs = true) {
  return `<div class="hdr">
    <div class="r1"><span class="brand">${ICON.glyph}<span>Prevue</span></span><span class="sep"></span>
      <div class="lock"><span class="tile">${APP.tile}</span><div class="t"><div class="app-name">${APP.name}</div><div class="sub">${subHtml()}</div></div></div>
      <span class="grow"></span><div class="tools">${pillHtml(state)}<button class="icon-btn">${ICON.search}</button><button class="icon-btn">?</button></div></div>
    ${tabs ? `<div class="r2">${tabsHtml()}<button class="icon-btn add">${ICON.plus}</button></div>` : ""}</div>`;
}

function boardHtml() {
  return `<div class="board"><div class="ghead"><b>ForYouScreenPopulatedFeed</b><span>${t_("count5")} · 25%</span></div>
    <div class="cards">${["ForYouScreenPopulatedFeed-0", "ForYouScreenPopulatedFeed_2-0", "ForYouScreenPopulatedFeed_1-0", "ForYouScreenPopulatedFeed_3-0"]
      .map(n => `<div class="card"><img src="../img/${n}.png" alt=""></div>`).join("")}</div></div>`;
}

const STR = {
  ko: { compiling: "컴파일 중…", count5: "5장", stale: "그림이 소스보다 옛것", lang: "English", openFiles: "열린 파일", openFile: "파일 열기",
        copyPath: "경로 복사", reveal: "Finder에서 보기", copyBranch: "브랜치 이름 복사", wide: "넓은 창", narrow: "좁은 창 390", light: "라이트", dark: "다크",
        ok: "✓ 끝", busy: "진행 중 · 긴 문구" },
  en: { compiling: "Compiling…", count5: "5 previews", stale: "Image is older than source", lang: "한국어", openFiles: "Open files", openFile: "Open file",
        copyPath: "Copy path", reveal: "Show in Finder", copyBranch: "Copy branch name", wide: "wide", narrow: "narrow 390", light: "light", dark: "dark",
        ok: "✓ done", busy: "busy · long text" },
};
function t_(k) { return STR[LANG][k] ?? k; }

// 한 안의 창 둘 — 넓은 창의 라이트(끝) · 다크(진행 중, 긴 문구). 좁은 창은 시안에서 뺐다(사용자 2026-10-21)
function frames(render) {
  const out = [];
  for (const [size, theme, state] of [["wide", "light", "ok"], ["wide", "dark", "busy"]]) {
    out.push(`<figure><figcaption>${t_(size)} · ${t_(theme)} · ${t_(state)}</figcaption><div class="win ${size}" data-theme="${theme}">${render(state, size)}</div></figure>`);
  }
  return `<div class="frames">${out.join("")}</div>`;
}

function langButton() {
  const a = document.getElementById("lang");
  if (!a) return;
  a.textContent = t_("lang");
  const u = new URL(location.href);
  if (LANG === "en") u.searchParams.delete("lang"); else u.searchParams.set("lang", "en");
  a.href = u.toString();
}
