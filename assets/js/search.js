/*
 * Costa's Meat Market: instant site search (EN / ES / PT).
 *
 *  - Loads one small JSON index per language (/assets/search/<lang>.json, built by _build/build.py) the
 *    first time someone points at, focuses or taps a search control, then ranks results in the browser
 *    on every keystroke. There is no server round trip after that.
 *  - Matching ignores case and accents, completes the word being typed, forgives small typos, and knows
 *    cut names and synonyms across English, Spanish and Portuguese ("rabada" finds oxtail).
 *  - Results are grouped (Products, Recipes, Blog, General); the groups are ordered by their best match.
 *    A match inside an article section links straight to that section.
 *  - If the query looks like another language, it offers results in that language; if nothing matches,
 *    it searches the other two languages too.
 *  - The top-right icon opens an overlay (also "/" or Ctrl+K), the blog has an inline box with a
 *    dropdown, and /search/?q= is the full results page.
 *  - Searches go to GA4 as the recommended "search" event (search_term) and to Microsoft Clarity;
 *    searches with no results are also sent as "search_no_results".
 */
(function () {
  "use strict";
  var w = window;
  var d = document;
  var me = d.currentScript;
  var V = ((me && /[?&]v=([\w-]+)/.exec(me.src)) || [])[1] || "";
  var SEARCH = { en: "/search/", es: "/es/search/", pt: "/pt/search/" };
  var LANG_NAME = { en: "English", es: "Español", pt: "Português" };
  var CHROME = {
    en: { label: "Search", placeholder: "Search cuts, recipes, deals…", close: "Close", loading: "Loading…",
          error: "Search is unavailable right now. Press Enter to try the search page." },
    es: { label: "Buscar", placeholder: "Busca cortes, recetas, ofertas…", close: "Cerrar", loading: "Cargando…",
          error: "La búsqueda no está disponible ahora. Pulsa Enter para abrir la página de búsqueda." },
    pt: { label: "Buscar", placeholder: "Busque cortes, receitas, promoções…", close: "Fechar", loading: "Carregando…",
          error: "A busca não está disponível agora. Aperte Enter para abrir a página de busca." }
  };
  var HINT = {
    en: "Searching in English? See results in English",
    es: "¿Buscas en español? Ver resultados en español",
    pt: "Buscando em português? Ver resultados em português"
  };
  // Field weights: title, keywords, other-language title, synonyms, section heading, FAQ question,
  // category label, description, body text.
  var WEIGHT = { t: 10, k: 6, x: 5, y: 4, h: 4, q: 3.5, l: 3, s: 2.5, w: 1.2 };
  var LIMIT = { overlay: { p: 4, r: 4, b: 5, g: 3 }, inline: { p: 4, r: 4, b: 5, g: 3 },
                page: { p: 12, r: 12, b: 24, g: 8 } };
  var STOP = {};
  ("a an and are as at be by do does for from how i in is it my of on or the to what with you your " +
   "el la los las de del y o en con para por un una que como al es se mi lo le su " +
   "os as do da dos das e em no na nos nas com um uma ao aos pra").split(" ").forEach(function (s) { STOP[s] = 1; });
  // Words that only one of the three languages uses (written without accents).
  var MARKERS = {
    es: "receta recetas carniceria carnicero cerdo puerco pollo res molida cuanto cuanta cuantos donde ofertas cupon " +
        "cupones descuento frijoles costillas costilla rabo arrachera entrana parrillada picana cocinar precio precios " +
        "cerca llegar tienda abierto abren queso pan horno guiso alitas chuletas pierna hacer",
    pt: "receita receitas acougue acougueiro frango porco boi moida quanto quantos onde promocao promocoes cupom " +
        "desconto feijao costela rabada churrasqueira assar fazer preco perto chegar loja aberto queijo pao forno " +
        "panela temperada temperado asinhas maminha alcatra coxinha bisteca barriga",
    en: "recipe recipes butcher pork chicken beef ground how cook near cheap price prices hours open deals coupon " +
        "coupons store shop buy ribs wings oxtail cheese bread beans roast belly shoulder best"
  };
  var MARK = {};
  Object.keys(MARKERS).forEach(function (l) {
    MARK[l] = {};
    MARKERS[l].split(" ").forEach(function (s) { MARK[l][s] = 1; });
  });

  var indexes = {};
  var lastTracked = "";

  // ---------- text helpers ----------
  function norm(s) {
    return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/['’]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
  }
  function toks(s) {
    s = norm(s);
    return s ? s.split(" ") : [];
  }
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function fmt(s, q) { return s.replace("{q}", q); }

  function pageLang() {
    var root = d.documentElement;
    var l = (root.getAttribute("data-search-lang") || root.lang || "en").slice(0, 2).toLowerCase();
    return SEARCH[l] ? l : "en";
  }

  function clarity() {
    if (typeof w.clarity === "function") w.clarity.apply(null, arguments);
  }
  function track(name, params) {
    if (typeof w.cmmTrack === "function") w.cmmTrack(name, params);
    else if (typeof w.gtag === "function") w.gtag("event", name, params);
  }

  // ---------- index ----------
  function prepare(data) {
    var vocab = new Map();
    data.docs.forEach(function (doc, di) {
      var seen = {};
      function add(text, f, sub) {
        toks(text).forEach(function (tok) {
          var key = tok + "|" + f + "|" + sub;
          if (seen[key]) return;
          seen[key] = 1;
          var list = vocab.get(tok);
          if (!list) { list = []; vocab.set(tok, list); }
          list.push(di, f, sub);
        });
      }
      ["t", "k", "y", "l", "s"].forEach(function (f) { if (doc[f]) add(doc[f], f, -1); });
      (doc.h || []).forEach(function (h, hi) { add(h[0], "h", hi); });
      (doc.q || []).forEach(function (q, qi) { add(q, "q", qi); });
      if (doc.x) Object.keys(doc.x).forEach(function (code) { add(doc.x[code], "x", code); });
      if (doc.w) add(doc.w, "w", -1);
      doc.tn = norm(doc.t);
      doc.kn = " " + norm(doc.k) + " ";
      doc.tc = toks(doc.t).length || 1;
    });
    data.vocab = Array.from(vocab.keys());
    data.post = Array.from(vocab.values());
    return data;
  }

  function load(lang) {
    if (!indexes[lang]) {
      indexes[lang] = fetch("/assets/search/" + lang + ".json" + (V ? "?v=" + V : ""), { credentials: "same-origin" })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then(prepare)
        .catch(function (err) { delete indexes[lang]; throw err; });
    }
    return indexes[lang];
  }

  // ---------- matching ----------
  // Edit distance with adjacent swaps, giving up as soon as it passes max.
  function distance(a, b, max) {
    var la = a.length, lb = b.length;
    if (Math.abs(la - lb) > max) return max + 1;
    var prev2 = null, prev = [], cur, i, j;
    for (j = 0; j <= lb; j++) prev[j] = j;
    for (i = 1; i <= la; i++) {
      cur = [i];
      var rowMin = i;
      for (j = 1; j <= lb; j++) {
        var cost = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
        var v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
        if (i > 1 && j > 1 && a.charCodeAt(i - 1) === b.charCodeAt(j - 2) && a.charCodeAt(i - 2) === b.charCodeAt(j - 1)) {
          v = Math.min(v, prev2[j - 2] + 1);
        }
        cur[j] = v;
        if (v < rowMin) rowMin = v;
      }
      if (rowMin > max) return max + 1;
      prev2 = prev;
      prev = cur;
    }
    return prev[lb];
  }

  // 1 = exact word, 0.6-0.97 = the word starts with what was typed, < 0.58 = typo or inside a word.
  function match(q, tok, typing) {
    if (tok === q) return 1;
    var ql = q.length, tl = tok.length;
    if (tl > ql && tok.lastIndexOf(q, 0) === 0) return (typing ? 0.72 : 0.6) + 0.25 * ql / tl;
    if (ql < 4) return 0;
    if (ql >= 5 && tok.indexOf(q) > 0) return 0.45;
    var max = ql >= 8 ? 2 : 1;
    var dist = distance(q, tok, max);
    if (dist > max && typing && ql >= 5 && tl > ql) dist = distance(q, tok.slice(0, ql), max);
    return dist <= max ? 0.55 - 0.12 * (dist - 1) : 0;
  }

  function queryTokens(raw) {
    var all = toks(raw);
    var typing = !/\s$/.test(raw);
    var kept = all.filter(function (t, i) {
      var last = i === all.length - 1;
      return !(STOP[t] && (!last || !typing));
    });
    if (!kept.length) kept = all;
    var unique = [];
    kept.forEach(function (t) { if (unique.indexOf(t) < 0) unique.push(t); });
    return { list: unique, typing: typing };
  }

  function rank(data, raw, cutoff) {
    var qt = queryTokens(raw);
    var qs = qt.list;
    if (!qs.length) return [];
    var N = data.docs.length;
    var total = new Float64Array(N), hits = new Uint8Array(N), titleHits = new Uint8Array(N);
    var heading = new Array(N), other = new Array(N);
    qs.forEach(function (q, qi) {
      var typing = qi === qs.length - 1 && qt.typing;
      var single = q.length === 1;
      var found = [], strong = false;
      for (var v = 0; v < data.vocab.length; v++) {
        var tok = data.vocab[v];
        if (single && tok.charCodeAt(0) !== q.charCodeAt(0)) continue;
        var m = match(q, tok, typing);
        if (!m) continue;
        if (m >= 0.58) strong = true;
        found.push(v, m);
      }
      var per = new Float64Array(N), where = new Array(N);
      for (var i = 0; i < found.length; i += 2) {
        var score = found[i + 1];
        if (strong && score < 0.58) score *= 0.5;
        var plist = data.post[found[i]];
        for (var p = 0; p < plist.length; p += 3) {
          var di = plist[p], f = plist[p + 1];
          if (single && f !== "t" && f !== "k" && f !== "l") continue;
          var s = score * WEIGHT[f];
          if (s > per[di]) { per[di] = s; where[di] = [f, plist[p + 2], s]; }
          if ((f === "h" || f === "q") && score >= 0.58 && (!heading[di] || s > heading[di][2])) {
            heading[di] = [f, plist[p + 2], s];
          }
          if (f === "x") other[di] = plist[p + 2];
        }
      }
      for (var k = 0; k < N; k++) {
        if (per[k] > 0) {
          total[k] += per[k];
          hits[k]++;
          if (where[k][0] === "t") titleHits[k]++;
        }
      }
    });
    var need = qs.length >= 3 ? qs.length - 1 : qs.length;
    var phrase = qs.join(" ");
    var out = [];
    for (var di = 0; di < N; di++) {
      if (hits[di] < need) continue;
      var doc = data.docs[di];
      var score = total[di] * hits[di] / qs.length;
      if (phrase.length >= 2) {
        if (doc.tn.lastIndexOf(phrase, 0) === 0) score += 8;
        else if ((" " + doc.tn).indexOf(" " + phrase) >= 0) score += 5;
        else if (doc.kn.indexOf(" " + phrase) >= 0) score += 3;
      }
      score += 3 * titleHits[di] / doc.tc;
      if (doc.c === "p" && titleHits[di]) score += 1.5;
      if (doc.n) score += 0.5;
      var hit = { doc: doc, score: score, i: di };
      if (heading[di] && titleHits[di] < qs.length) hit.at = heading[di];
      if (other[di] && !titleHits[di]) hit.other = other[di];
      out.push(hit);
    }
    out.sort(function (a, b) { return b.score - a.score || a.i - b.i; });
    // Drop the long tail of weak matches (a word buried in an unrelated article).
    var floor = out.length ? out[0].score * (cutoff || 0.2) : 0;
    out = out.filter(function (r) { return r.score >= floor; });
    out.tokens = qs;
    return out;
  }

  function group(results, limits) {
    var groups = {}, order = [];
    results.forEach(function (r) {
      var c = r.doc.c;
      if (!groups[c]) { groups[c] = []; order.push(c); }
      if (groups[c].length < limits[c]) groups[c].push(r);
    });
    return order.map(function (c) { return { cat: c, items: groups[c] }; });
  }

  function guessLang(raw) {
    if (/[ãõçêô]/i.test(raw)) return "pt";
    if (/[ñ¿¡]/i.test(raw)) return "es";
    var score = { en: 0, es: 0, pt: 0 };
    toks(raw).forEach(function (t) {
      Object.keys(MARK).forEach(function (l) { if (MARK[l][t]) score[l]++; });
    });
    var best = null, top = 0, tie = false;
    Object.keys(score).forEach(function (l) {
      if (score[l] > top) { best = l; top = score[l]; tie = false; } else if (score[l] && score[l] === top) tie = true;
    });
    return tie ? null : best;
  }

  // ---------- rendering ----------
  var WORD = /[0-9A-Za-zÀ-ɏ'’]+/g;
  function highlight(text, qs) {
    var out = "", last = 0, m;
    WORD.lastIndex = 0;
    while ((m = WORD.exec(text))) {
      var word = m[0], flat = norm(word).replace(/ /g, ""), len = 0;
      for (var i = 0; i < qs.length; i++) {
        if (flat.lastIndexOf(qs[i], 0) === 0 && qs[i].length > len) len = qs[i].length;
      }
      out += esc(text.slice(last, m.index));
      if (len) {
        var cut = /['’]/.test(word) ? word.length : Math.min(len, word.length);
        out += "<mark>" + esc(word.slice(0, cut)) + "</mark>" + esc(word.slice(cut));
      } else {
        out += esc(word);
      }
      last = m.index + word.length;
    }
    return out + esc(text.slice(last));
  }

  var PATHS = {
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    pin: '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    cart: '<circle cx="9" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/><path d="M3 4h2l2.4 11h10.2L20 8H6.2"/>',
    tag: '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.4"/>',
    chat: '<path d="M4 20l1.4-4A8 8 0 1 1 8 18.6z"/>',
    share: '<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="m8.2 10.8 7.6-4.6M8.2 13.2l7.6 4.6"/>',
    star: '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    knife: '<path d="M3 21 15 9l3 3-2 2H9"/><path d="M15 9l4-4a2 2 0 0 1 2 2l-4 4"/>',
    home: '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/>',
    book: '<path d="M4 5a2 2 0 0 1 2-2h14v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>',
    faq: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.6V14"/><path d="M12 17.5h.01"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5h.01"/>'
  };
  function icon(name) {
    return '<span class="srch-ic" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      (PATHS[name] || PATHS.info) + "</svg></span>";
  }

  function itemHtml(view, data, r, pos, langBadge) {
    var doc = r.doc, ui = data.ui, qs = r.tokens || [];
    var long = qs.filter(function (t) { return t.length > 1; });
    var href = doc.u, sub = "", meta = [];
    if (r.at) {
      if (r.at[0] === "h" && doc.h && doc.h[r.at[1]]) {
        href = doc.u + "#" + doc.h[r.at[1]][1];
        sub = '<span class="srch-at">' + esc(ui.section) + ":</span> " + highlight(doc.h[r.at[1]][0], long);
      } else if (r.at[0] === "q" && doc.q && doc.q[r.at[1]]) {
        href = doc.u + "#faq";
        sub = '<span class="srch-at">' + esc(ui.question) + ":</span> " + highlight(doc.q[r.at[1]], long);
      }
    }
    if (!sub) sub = highlight(doc.s || "", long);
    if (doc.c === "p" && doc.g) meta.push(esc(ui.guide) + ": " + esc(doc.g));
    else if (doc.l) meta.push(esc(doc.l));
    if (langBadge) meta.push(esc(LANG_NAME[data.lang]));
    var target = doc.e ? ' target="_blank" rel="noopener"' : "";
    var visual = doc.i
      ? '<img src="' + esc(doc.i) + '" width="56" height="56" alt="" loading="lazy" decoding="async">'
      : icon(doc.ic);
    var id = view.id + "-o" + pos;
    var html = '<div class="srch-row' + (pos === 0 ? " srch-top" : "") + '">' +
      '<a class="srch-item" role="option" id="' + id + '" href="' + esc(href) + '"' + target +
      ' data-cat="' + doc.c + '" data-pos="' + (pos + 1) + '"' +
      (langBadge ? ' hreflang="' + data.lang + '"' : "") + ">" + visual +
      '<span class="srch-txt"><span class="srch-t">' + highlight(doc.t, qs) + "</span>" +
      '<span class="srch-s">' + sub + "</span>" +
      (meta.length ? '<span class="srch-m">' + meta.join(" · ") + "</span>" : "") + "</span></a>";
    if (doc.o && data.order) {
      html += '<a class="srch-buy" href="' + esc(data.order) + '" target="_blank" rel="noopener" tabindex="-1">' +
        esc(ui.order) + "</a>";
    }
    if (r.other && doc.a && doc.a[r.other]) {
      html += '<a class="srch-alt" href="' + esc(doc.a[r.other]) + '" hreflang="' + r.other + '" lang="' + r.other +
        '" tabindex="-1">' + esc(r.other.toUpperCase()) + "</a>";
    }
    return html + "</div>";
  }

  function render(view, data, raw, results, extra) {
    var ui = data.ui, q = raw.trim();
    var limits = LIMIT[view.mode];
    var html = "", pos = 0, count = results.length;
    var guess = guessLang(raw);
    if (guess && guess !== data.lang && q.length > 2) {
      html += '<a class="srch-hint" href="' + SEARCH[guess] + "?q=" + encodeURIComponent(q) + '" hreflang="' + guess +
        '" lang="' + guess + '">' + esc(HINT[guess]) + " →</a>";
    }
    group(results, limits).forEach(function (g) {
      html += '<div class="srch-group" role="group" aria-label="' + esc(ui.cats[g.cat]) + '"><p class="srch-cat">' +
        esc(ui.cats[g.cat]) + "</p>";
      g.items.forEach(function (r) {
        r.tokens = results.tokens;
        html += itemHtml(view, data, r, pos++);
      });
      html += "</div>";
    });
    (extra || []).forEach(function (other) {
      html += '<div class="srch-group" role="group" lang="' + other.data.lang + '"><p class="srch-cat">' +
        esc(fmt(other.data.ui.other, LANG_NAME[other.data.lang])) + "</p>";
      other.results.slice(0, limits.b).forEach(function (r) {
        r.tokens = other.results.tokens;
        html += itemHtml(view, other.data, r, pos++, true);
      });
      html += "</div>";
      count += other.results.length;
    });
    if (!pos) {
      html += '<div class="srch-empty"><p><strong>' + esc(fmt(ui.empty, q)) + "</strong></p><p>" + esc(ui.empty_help) +
        "</p></div>";
    }
    if (view.mode !== "page" && q) {
      html += '<a class="srch-all" href="' + SEARCH[data.lang] + "?q=" + encodeURIComponent(q) + '">' +
        esc(fmt(ui.all, q)) + " →</a>";
    }
    if (view.mode === "overlay") html += '<p class="srch-keys">' + esc(ui.keys) + "</p>";
    view.list.innerHTML = html;
    view.items = Array.prototype.slice.call(view.list.querySelectorAll(".srch-item"));
    view.active = -1;
    view.input.removeAttribute("aria-activedescendant");
    if (view.status) {
      view.status.textContent = q ? (count === 1 ? ui.count1 : ui.count.replace("{n}", count)) : "";
    }
    view.count = count;
  }

  // ---------- views ----------
  var views = 0;

  function View(form, mode) {
    var self = this;
    this.form = form;
    this.mode = mode;
    this.id = "srch" + (views++);
    this.input = form.querySelector('input[name="q"]');
    this.input.setAttribute("role", "combobox");
    this.input.setAttribute("aria-autocomplete", "list");
    this.input.setAttribute("aria-expanded", "false");
    if (mode === "page") {
      this.list = d.getElementById("search-results");
      this.status = d.getElementById("search-status");
      this.explore = d.getElementById("search-explore");
    } else {
      this.list = d.createElement("div");
      this.list.className = "srch-list" + (mode === "inline" ? " srch-drop" : "");
      if (mode === "inline") this.list.hidden = true;
      (mode === "inline" ? form : form.parentNode).appendChild(this.list);
    }
    if (!this.list.id) this.list.id = this.id + "-list";
    this.list.setAttribute("role", "listbox");
    this.list.setAttribute("aria-label", form.querySelector("label") ? form.querySelector("label").textContent : "Search");
    this.input.setAttribute("aria-controls", this.list.id);
    this.items = [];
    this.active = -1;
    this.timer = 0;

    this.input.addEventListener("input", function () { self.update(); });
    this.input.addEventListener("focus", function () {
      load(self.lang());
      if (self.mode === "inline" && self.input.value.trim()) self.show(true);
    });
    this.input.addEventListener("keydown", function (e) { self.key(e); });
    this.form.addEventListener("submit", function (e) {
      var q = self.input.value.trim();
      if (self.active >= 0) { e.preventDefault(); self.items[self.active].click(); return; }
      if (self.mode === "page") { e.preventDefault(); self.input.blur(); self.track(true); return; }
      if (!q) { e.preventDefault(); return; }
      self.track(true);
      self.form.action = SEARCH[self.lang()];
    });
    this.list.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest("a") : null;
      if (!a) return;
      self.track(true);
      var item = a.classList.contains("srch-item") ? a : null;
      track("search_select", {
        search_term: self.input.value.trim().toLowerCase().slice(0, 100),
        result_category: item ? item.getAttribute("data-cat") : a.className,
        result_position: item ? Number(item.getAttribute("data-pos")) : 0,
        link_url: a.href,
        search_surface: self.mode,
        page_lang: self.lang()
      });
    });
    if (mode === "inline") {
      d.addEventListener("click", function (e) {
        if (!self.form.contains(e.target)) self.show(false);
      });
    }
  }

  View.prototype.lang = function () { return pageLang(); };

  View.prototype.show = function (on) {
    if (this.mode === "inline") this.list.hidden = !on;
    this.input.setAttribute("aria-expanded", String(!!on));
  };

  View.prototype.update = function () {
    var self = this;
    var raw = this.input.value;
    var q = raw.trim();
    var lang = this.lang();
    if (this.mode === "page") this.sync(q);
    clearTimeout(this.timer);
    if (!q) {
      this.list.innerHTML = "";
      this.items = [];
      if (this.status) this.status.textContent = "";
      this.show(false);
      return;
    }
    this.timer = setTimeout(function () { self.track(false); }, 1200);
    var ticket = this.ticket = (this.ticket || 0) + 1;
    if (!indexes[lang] || !indexes[lang].ready) {
      if (this.status) this.status.textContent = CHROME[lang].loading;
    }
    load(lang).then(function (data) {
      indexes[lang].ready = true;
      if (ticket !== self.ticket) return;
      var results = rank(data, raw, self.mode === "page" ? 0.1 : 0.2);
      render(self, data, raw, results);
      self.show(true);
      if (!results.length && norm(q).length >= 3) {
        var others = Object.keys(SEARCH).filter(function (l) { return l !== lang; });
        Promise.all(others.map(function (l) { return load(l).catch(function () { return null; }); })).then(function (list) {
          if (ticket !== self.ticket) return;
          var extra = [];
          list.forEach(function (other) {
            if (!other) return;
            var found = rank(other, raw);
            if (found.length) extra.push({ data: other, results: found });
          });
          if (extra.length) render(self, data, raw, results, extra);
        });
      }
    }, function () {
      if (ticket !== self.ticket) return;
      self.list.innerHTML = '<div class="srch-empty"><p>' + esc(CHROME[lang].error) + "</p></div>";
      self.show(true);
    });
  };

  View.prototype.move = function (step) {
    if (!this.items.length) return;
    if (this.active >= 0) this.items[this.active].classList.remove("is-active");
    var slots = this.items.length + 1;  // -1 (the input) plus every result
    this.active = ((this.active + 1 + step) % slots + slots) % slots - 1;
    if (this.active < 0) {
      this.input.removeAttribute("aria-activedescendant");
      return;
    }
    var el = this.items[this.active];
    el.classList.add("is-active");
    this.input.setAttribute("aria-activedescendant", el.id);
    if (el.scrollIntoView) el.scrollIntoView({ block: "nearest" });
  };

  View.prototype.key = function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); this.move(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); this.move(-1); }
    else if (e.key === "Escape") {
      if (this.mode === "overlay") return;
      if (this.mode === "inline" && !this.list.hidden) { e.preventDefault(); this.show(false); }
      else if (this.input.value) { e.preventDefault(); this.input.value = ""; this.update(); }
    }
  };

  View.prototype.track = function (now) {
    clearTimeout(this.timer);
    var term = this.input.value.trim().toLowerCase().slice(0, 100);
    if (term.length < 2 || term === lastTracked) return;
    lastTracked = term;
    var params = { search_term: term, results_count: this.count || 0, search_surface: this.mode, page_lang: this.lang() };
    track("search", params);
    if (!this.count) track("search_no_results", params);
    clarity("set", "search_term", term);
  };

  // Full results page: keep ?q= in the address bar, the language links and the explore block in step.
  View.prototype.sync = function (q) {
    var self = this;
    if (this.explore) this.explore.hidden = !!q;
    clearTimeout(this.syncTimer);
    this.syncTimer = setTimeout(function () {
      var suffix = q ? "?q=" + encodeURIComponent(q) : "";
      try { w.history.replaceState(null, "", w.location.pathname + suffix); } catch (e) {}
      var links = d.querySelectorAll(".langbar a[hreflang]");
      for (var i = 0; i < links.length; i++) {
        links[i].href = SEARCH[links[i].getAttribute("hreflang")] + suffix;
      }
      if (!self.baseTitle) self.baseTitle = d.title;
      d.title = q ? q + " · " + self.baseTitle : self.baseTitle;
    }, 250);
  };

  // ---------- overlay (top-right icon, "/" and Ctrl+K) ----------
  var overlay = null;
  var opener = null;

  function buildOverlay(lang) {
    var c = CHROME[lang];
    var el = d.createElement("div");
    el.className = "srch-overlay";
    el.hidden = true;
    el.setAttribute("lang", lang);
    el.innerHTML = '<div class="srch-backdrop" data-srch-close></div>' +
      '<div class="srch-dialog" role="dialog" aria-modal="true" aria-label="' + esc(c.label) + '">' +
      '<form class="search-box search-overlay" role="search" action="' + SEARCH[lang] + '" method="get">' +
      '<label class="sr-only" for="srch-overlay-q">' + esc(c.label) + "</label>" +
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/>' +
      '<path d="m20 20-3.6-3.6"/></svg>' +
      '<input id="srch-overlay-q" type="search" name="q" placeholder="' + esc(c.placeholder) + '" autocomplete="off" ' +
      'autocapitalize="off" spellcheck="false" enterkeyhint="search">' +
      '<button type="button" class="srch-close" data-srch-close aria-label="' + esc(c.close) + '">Esc</button>' +
      "</form></div>";
    d.body.appendChild(el);
    var view = new View(el.querySelector("form"), "overlay");
    el.addEventListener("click", function (e) {
      if (e.target.closest && e.target.closest("[data-srch-close]")) closeOverlay();
    });
    el.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { e.preventDefault(); closeOverlay(); return; }
      if (e.key !== "Tab") return;
      var focusable = el.querySelectorAll("input, button, a[href]:not([tabindex='-1'])");
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    return { el: el, view: view, lang: lang };
  }

  function openOverlay(trigger) {
    var lang = pageLang();
    var page = d.querySelector('form[data-search="page"] input[name="q"]');
    if (page) { page.focus(); page.select(); return; }
    if (overlay && overlay.lang !== lang) { overlay.el.remove(); overlay = null; }
    if (!overlay) overlay = buildOverlay(lang);
    opener = trigger || d.activeElement;
    overlay.el.hidden = false;
    d.documentElement.classList.add("srch-lock");
    overlay.view.input.focus();
    overlay.view.input.select();
    load(lang).catch(function () {});
    clarity("event", "search_open");
  }

  function closeOverlay() {
    if (!overlay || overlay.el.hidden) return;
    overlay.view.track(true);
    overlay.el.hidden = true;
    d.documentElement.classList.remove("srch-lock");
    if (opener && opener.focus) opener.focus();
  }

  // ---------- wiring ----------
  function warm(e) {
    var t = e.target && e.target.closest ? e.target.closest("[data-search-open], form[data-search]") : null;
    if (t) load(pageLang()).catch(function () {});
  }
  d.addEventListener("pointerover", warm, { passive: true });
  d.addEventListener("touchstart", warm, { passive: true });
  d.addEventListener("focusin", warm);

  d.addEventListener("click", function (e) {
    var t = e.target.closest ? e.target.closest("[data-search-open]") : null;
    if (!t || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    openOverlay(t);
  });

  d.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    var typing = tag === "input" || tag === "textarea" || tag === "select" || e.target.isContentEditable;
    if ((e.key === "/" && !typing && !e.metaKey && !e.ctrlKey && !e.altKey) ||
        ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey))) {
      e.preventDefault();
      openOverlay();
    }
  });

  w.addEventListener("pagehide", function () {
    if (overlay && !overlay.el.hidden) overlay.view.track(true);
  });

  var forms = d.querySelectorAll("form[data-search]");
  for (var i = 0; i < forms.length; i++) {
    var view = new View(forms[i], forms[i].getAttribute("data-search"));
    if (view.mode === "page") {
      var q = new URLSearchParams(w.location.search).get("q");
      if (q) { view.input.value = q; view.update(); }
      load(pageLang()).catch(function () {});
    }
  }
})();
