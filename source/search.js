/* Search across every page of the notebook. Runs entirely in the browser. */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const esc = s => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const SKIP = new Set(['page-sim', 'page-rsim', 'page-buildlog']);
  let index = null, active = -1, hits = [];

  function textOf(root) {
    const parts = [];
    const walk = n => {
      if (n.nodeType === 3) { parts.push(n.nodeValue); return; }
      if (n.nodeType !== 1) return;
      const tag = n.tagName.toLowerCase();
      if (tag === 'svg' || tag === 'script' || tag === 'style' || tag === 'select' || tag === 'pre' || n.classList.contains('pn') || n.classList.contains('links')) return;
      n.childNodes.forEach(walk);
      if (/^(p|li|h[1-6]|tr|td|th|div|dd|dt|a|b|span|summary)$/.test(tag)) parts.push(' ');
    };
    walk(root);
    return parts.join('').replace(/\s+/g, ' ').trim();
  }

  function group(hash) {
    if (/^ex-/.test(hash)) return 'Practical Lab';
    if (/^robot-/.test(hash)) return 'Robot Exercise';
    if (/^sensor-/.test(hash)) return 'Sensor';
    if (/^quiz/.test(hash)) return 'Quiz';
    return 'Notebook';
  }

  function build() {
    index = [];
    document.querySelectorAll('[data-page]').forEach(p => {
      if (SKIP.has(p.id)) return;
      const h1 = p.querySelector('h1'), heads = Array.from(p.querySelectorAll('h2,h3,dt')).map(h => h.textContent).join(' ');
      index.push({ hash: p.id.slice(5), title: h1 ? h1.textContent : '', heads: heads.toLowerCase(), text: textOf(p) });
    });
    (window.ELAB_EXAMPLES || []).forEach(e => {
      const clean = s => (s || '').replace(/&#?\w+;/g, ' ');
      const text = clean(`${e.goal} ${e.happen} ${e.tryit}`);
      index.push({ hash: 'ex-' + e.n, title: `Example ${e.n}: ${e.title}`, heads: e.title.toLowerCase(), text });
    });
    index.forEach(x => { x.low = x.text.toLowerCase(); x.tl = x.title.toLowerCase(); });
  }

  function find(q) {
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    const out = [];
    for (const x of index) {
      let score = 0, all = true;
      for (const t of terms) {
        const inT = x.tl.includes(t), inH = x.heads.includes(t), inB = x.low.includes(t);
        if (!inT && !inH && !inB) { all = false; break; }
        score += (inT ? 10 : 0) + (inH ? 4 : 0) + (inB ? 1 : 0) + (x.tl.startsWith(t) ? 6 : 0);
      }
      if (all) out.push({ x, score, terms });
    }
    return out.sort((a, b) => b.score - a.score).slice(0, 12);
  }

  function snippet(x, terms) {
    let at = -1;
    for (const t of terms) { at = x.low.indexOf(t); if (at >= 0) break; }
    if (at < 0) return esc(x.text.slice(0, 110));
    const start = Math.max(0, at - 40), raw = (start ? '&#8230;' : '') + esc(x.text.slice(start, start + 120)) + '&#8230;';
    const re = new RegExp('(' + terms.map(t => esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'ig');
    return raw.replace(re, '<mark>$1</mark>');
  }

  function close() { const r = $('nb-results'); r.hidden = true; r.innerHTML = ''; $('nb-search').setAttribute('aria-expanded', 'false'); active = -1; }

  function show() {
    const q = $('nb-search').value.trim(), r = $('nb-results');
    if (!q) { close(); return; }
    if (!index) build();
    hits = find(q); active = -1;
    r.innerHTML = hits.length
      ? hits.map((h, i) => `<a role="option" id="nb-r${i}" href="#${h.x.hash}"><span class="sr-g">${group(h.x.hash)}</span><b>${esc(h.x.title)}</b><span>${snippet(h.x, h.terms)}</span></a>`).join('')
      : `<div class="sr-none">Nothing found for &#8220;${esc(q)}&#8221;. Try a shorter word.</div>`;
    r.hidden = false; $('nb-search').setAttribute('aria-expanded', 'true');
  }

  function move(d) {
    const links = $('nb-results').querySelectorAll('a');
    if (!links.length) return;
    active = (active + d + links.length) % links.length;
    links.forEach((a, i) => a.classList.toggle('on', i === active));
    links[active].scrollIntoView({ block: 'nearest' });
    $('nb-search').setAttribute('aria-activedescendant', links[active].id);
  }

  window.ENotebookSearch = {
    init() {
      const input = $('nb-search'), box = $('nb-results');
      input.addEventListener('input', show);
      input.addEventListener('focus', () => { if (input.value.trim()) show(); });
      input.addEventListener('keydown', e => {
        if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
        else if (e.key === 'Enter') {
          e.preventDefault();
          const links = box.querySelectorAll('a'), go = links[active >= 0 ? active : 0];
          if (go) go.click();
        } else if (e.key === 'Escape') { close(); input.blur(); }
      });
      box.addEventListener('click', e => { if (e.target.closest('a')) { input.value = ''; close(); } });
      document.addEventListener('click', e => { if (!e.target.closest('.search')) close(); });
      addEventListener('hashchange', close);
      addEventListener('keydown', e => {
        if (e.key === '/' && !e.target.matches('input,textarea,select') && !e.ctrlKey && !e.metaKey) { e.preventDefault(); input.focus(); }
      });
    },
    find(q) { if (!index) build(); return find(q).map(h => h.x.hash); },
  };
})();
