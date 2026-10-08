/*
 * Costa's Meat Market — click, share and traffic-source tracking.
 *
 * Every page loads Google Analytics 4 (G-S4GM8NREGG) and Microsoft Clarity in <head>. This file adds:
 *   - Events in both tools for the actions that matter: call, directions, order online, WhatsApp,
 *     socials, Google review, language switch, blog clicks and article shares.
 *   - Clarity tags for where the visit came from (UTM tags, short links, social apps, AI assistants,
 *     search engines) and the page language. GA4 reads UTM tags and referrers on its own.
 */
(function () {
  var GA4_ID = "G-S4GM8NREGG";

  var w = window;
  var d = document;

  function clarity() {
    if (typeof w.clarity === "function") w.clarity.apply(null, arguments);
  }

  // Pages load the Google tag in <head>; only inject it here if a page is missing it.
  if (typeof w.gtag !== "function" && /^G-[A-Z0-9]+$/.test(GA4_ID)) {
    var tag = d.createElement("script");
    tag.async = true;
    tag.src = "https://www.googletagmanager.com/gtag/js?id=" + GA4_ID;
    d.head.appendChild(tag);
    w.dataLayer = w.dataLayer || [];
    w.gtag = function () { w.dataLayer.push(arguments); };
    w.gtag("js", new Date());
    w.gtag("config", GA4_ID, { page_language: lang() });
  }

  function lang() {
    return (d.documentElement.lang || "en").slice(0, 2).toLowerCase();
  }

  function store(area, key, value) {
    try { w[area].setItem(key, value); } catch (e) {}
  }
  function recall(area, key) {
    try { return w[area].getItem(key); } catch (e) { return null; }
  }

  // ---------- where did this visit come from? ----------
  var SOCIAL_HOSTS = {
    "l.instagram.com": "instagram", "instagram.com": "instagram", "www.instagram.com": "instagram",
    "l.facebook.com": "facebook", "lm.facebook.com": "facebook", "m.facebook.com": "facebook",
    "www.facebook.com": "facebook", "facebook.com": "facebook",
    "l.wl.co": "whatsapp", "wa.me": "whatsapp", "web.whatsapp.com": "whatsapp",
    "www.tiktok.com": "tiktok", "tiktok.com": "tiktok", "t.co": "x", "x.com": "x",
    "www.youtube.com": "youtube", "m.youtube.com": "youtube", "nextdoor.com": "nextdoor"
  };
  var AI_HOSTS = {
    "chatgpt.com": "chatgpt", "chat.openai.com": "chatgpt",
    "perplexity.ai": "perplexity", "www.perplexity.ai": "perplexity",
    "gemini.google.com": "gemini", "copilot.microsoft.com": "copilot",
    "claude.ai": "claude", "meta.ai": "meta_ai", "www.meta.ai": "meta_ai"
  };

  function detectSource() {
    var query = new URLSearchParams(w.location.search);
    var source = {};
    ["utm_source", "utm_medium", "utm_campaign", "utm_content"].forEach(function (key) {
      var value = query.get(key);
      if (value) source[key] = value.slice(0, 60);
    });
    var host = "";
    try { host = d.referrer ? new URL(d.referrer).hostname : ""; } catch (e) {}
    if (host && host !== w.location.hostname) {
      source.referrer = host;
      if (AI_HOSTS[host]) {
        source.ai_assistant = AI_HOSTS[host];
        if (!source.utm_source) { source.utm_source = AI_HOSTS[host]; source.utm_medium = "ai_assistant"; }
      } else if (!source.utm_source && SOCIAL_HOSTS[host]) {
        source.utm_source = SOCIAL_HOSTS[host]; source.utm_medium = "social";
      } else if (!source.utm_source && /(^|\.)google\./.test(host)) {
        source.utm_source = "google"; source.utm_medium = "organic";
      } else if (!source.utm_source && /(^|\.)(bing\.com|duckduckgo\.com|search\.yahoo\.com)$/.test(host)) {
        source.utm_source = host.split(".").slice(-2, -1)[0]; source.utm_medium = "organic";
      }
    }
    return source;
  }

  var current = detectSource();
  var hasSource = Object.keys(current).length > 0;
  if (hasSource) {
    store("sessionStorage", "cmm-src", JSON.stringify(current));
    if (!recall("localStorage", "cmm-first-src")) {
      store("localStorage", "cmm-first-src", JSON.stringify(current));
    }
  }
  var session = current;
  if (!hasSource) {
    try { session = JSON.parse(recall("sessionStorage", "cmm-src") || "{}"); } catch (e) { session = {}; }
  }

  clarity("set", "page_lang", lang());
  Object.keys(session).forEach(function (key) { clarity("set", key, session[key]); });
  if (session.utm_source) clarity("set", "traffic_source", session.utm_source + " / " + (session.utm_medium || "none"));

  // ---------- what did they tap? ----------
  var RULES = [
    [/^tel:/, "click_call"],
    [/^sms:/, "click_text"],
    [/google\.[a-z.]+\/maps|maps\.google\.|maps\.apple\.com|goo\.gl\/maps|maps\.app\.goo\.gl/, "click_directions"],
    [/hrpos\.heartland\.us/, "click_order_online"],
    [/chat\.whatsapp\.com/, "click_whatsapp_group"],
    [/whatsapp\.com\/channel/, "click_whatsapp_channel"],
    [/wa\.me|api\.whatsapp\.com/, "click_whatsapp_chat"],
    [/g\.page\/.+\/review|search\.google\.com\/local\/writereview/, "click_google_review"],
    [/instagram\.com/, "click_instagram"],
    [/tiktok\.com/, "click_tiktok"],
    [/facebook\.com|fb\.com/, "click_facebook"]
  ];

  function classify(link) {
    if (link.hasAttribute("data-track")) return link.getAttribute("data-track");
    if (link.hasAttribute("hreflang")) return "select_language";
    var href = link.getAttribute("href") || "";
    for (var i = 0; i < RULES.length; i++) {
      if (RULES[i][0].test(href)) return RULES[i][1];
    }
    if (/\/socials\/?$/.test(href)) return "click_socials_hub";
    if (/\/blog\//.test(href)) return "click_blog";
    return null;
  }

  function send(name, params) {
    clarity("event", name);
    if (name === "click_call" || name === "click_directions" || name === "click_order_online" || name === "click_whatsapp_group") {
      clarity("upgrade", name);
    }
    if (typeof w.gtag === "function") {
      params.transport_type = "beacon";
      w.gtag("event", name, params);
    }
  }

  d.addEventListener("click", function (event) {
    var link = event.target.closest ? event.target.closest("a[href]") : null;
    if (!link) return;
    var name = classify(link);
    if (!name) return;
    var section = link.closest("[data-section]");
    var params = {
      link_id: link.id || "",
      link_url: link.href,
      link_section: section ? section.getAttribute("data-section") : "",
      page_lang: lang()
    };
    if (name === "share") {
      params.method = link.getAttribute("data-share") || "";
      params.content_type = "article";
      params.item_id = w.location.pathname;
      clarity("event", "share_" + params.method);
    }
    send(name, params);
  }, true);

  // "Copy link" share button: copies a UTM-tagged link so shares are traceable.
  d.addEventListener("click", function (event) {
    var button = event.target.closest ? event.target.closest("button[data-share-copy]") : null;
    if (!button) return;
    var url = button.getAttribute("data-share-copy");
    var label = button.textContent;
    send("share", { method: "copy_link", content_type: "article", item_id: w.location.pathname, page_lang: lang() });
    clarity("event", "share_copy_link");
    if (navigator.share && /Mobi|Android|iPhone|iPad/.test(navigator.userAgent || "")) {
      navigator.share({ title: d.title, url: url }).catch(function () {});
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () {
        button.textContent = button.getAttribute("data-copied") || label;
        setTimeout(function () { button.textContent = label; }, 1800);
      }, function () {});
    }
  });

  // Public hook for one-off events: window.cmmTrack("event_name", { any: "params" })
  w.cmmTrack = function (name, params) { send(name, params || {}); };
})();
