/*
 * Costa's Meat Market — language helper for the EN / ES / PT pages.
 *  - Remembers the language a visitor picks (same "cmm-lang" key the socials page uses).
 *  - If someone's phone is set to Spanish or Portuguese and they land on a page in
 *    another language, it offers a one-tap link to their version. It never redirects,
 *    so Google can still crawl every language.
 */
(function () {
  var d = document;
  var KEY = "cmm-lang";
  var OFFER = {
    es: "¿Prefieres español? <a hreflang=\"es\" href=\"{href}\">Ver esta página en español</a>",
    pt: "Prefere português? <a hreflang=\"pt\" href=\"{href}\">Ver esta página em português</a>",
    en: "Prefer English? <a hreflang=\"en\" href=\"{href}\">View this page in English</a>"
  };

  function store(value) { try { window.localStorage.setItem(KEY, value); } catch (e) {} }
  function recall() { try { return window.localStorage.getItem(KEY); } catch (e) { return null; } }

  var pageLang = (d.documentElement.lang || "en").slice(0, 2).toLowerCase();

  d.addEventListener("click", function (event) {
    var link = event.target.closest ? event.target.closest("a[hreflang]") : null;
    if (link) store(link.getAttribute("hreflang").slice(0, 2));
  });

  var saved = recall();
  if (saved) return;

  var wanted = null;
  var list = navigator.languages || [navigator.language || "en"];
  for (var i = 0; i < list.length; i++) {
    var code = String(list[i]).slice(0, 2).toLowerCase();
    if (code === "es" || code === "pt" || code === "en") { wanted = code; break; }
  }
  if (!wanted || wanted === pageLang) return;

  var alt = d.querySelector('link[rel="alternate"][hreflang="' + wanted + '"]');
  var slot = d.getElementById("lang-suggest");
  if (!alt || !slot) return;
  slot.innerHTML = OFFER[wanted].replace("{href}", alt.getAttribute("href"));
  slot.hidden = false;
})();
