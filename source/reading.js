/* Reading modes, the round buttons and the print menu, modelled on the MBA notebook. */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const MODES = ['day', 'sepia', 'dark', 'night'], KEY = 'elec-reading';
  const THEME_COLOUR = { day: '#0d6049', sepia: '#0d6049', dark: '#62d0a8', night: '#2e2414' };

  // ---------- reading mode ----------
  function current() {
    const set = document.documentElement.getAttribute('data-reading');
    if (set) return set;
    const viewer = document.documentElement.getAttribute('data-theme');
    if (viewer) return viewer === 'dark' ? 'dark' : 'day';
    return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'day';
  }
  function paintPicker() {
    const now = current();
    document.querySelectorAll('[data-set-reading]').forEach(b => b.setAttribute('aria-pressed', b.getAttribute('data-set-reading') === now ? 'true' : 'false'));
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', THEME_COLOUR[now]);
  }
  function setMode(mode) {
    document.documentElement.setAttribute('data-reading', mode);
    try { localStorage.setItem(KEY, mode); } catch (e) { /* the mode still applies until the page closes */ }
    paintPicker();
    window.dispatchEvent(new CustomEvent('nb-reading', { detail: mode }));
  }

  // ---------- printing ----------
  let saved = null, scroll = 0, copies = [];
  const pages = () => document.querySelectorAll('[data-page]');
  function pageId() { return (location.hash || '').slice(1) || 'home'; }

  function stack(ids) {
    const all = Array.from(pages());
    saved = all.map(p => p.hidden); scroll = window.scrollY;
    all.forEach(p => { p.hidden = true; p.classList.remove('print-break'); });
    let n = 0;
    ids.forEach(id => { const el = $('page-' + id); if (el) { el.hidden = false; if (n++) el.classList.add('print-break'); } });
  }
  function unstack() {
    if (!saved) return;
    const was = saved, all = Array.from(pages());
    saved = null;
    all.forEach((p, i) => { p.hidden = was[i]; p.classList.remove('print-break'); });
    window.scrollTo(0, scroll);
  }
  function prepare() {
    document.querySelectorAll('main details').forEach(d => { d.setAttribute('data-was', d.open ? '1' : ''); d.open = true; });
    // A text box only prints the lines it's showing, so print a full copy of the code instead.
    document.querySelectorAll('main textarea').forEach(ta => {
      if (!ta.value || ta.offsetParent === null) return;
      const pre = document.createElement('pre'); pre.className = 'code print-copy'; pre.textContent = ta.value;
      ta.after(pre); copies.push(pre);
    });
    const fp = $('fc-print');
    if (fp && !$('page-flashcards').hidden) {
      const v = $('deck').value, list = (window.NB_CARDS || []).filter(c => v === 'all' || c.s === v || 'g:' + c.g === v);
      fp.innerHTML = '<dl class="terms">' + list.map(c => `<dt>${c.t}</dt><dd>${c.d}</dd>`).join('') + '</dl>';
    }
  }
  function finish() {
    document.querySelectorAll('main details[data-was]').forEach(d => { d.open = d.getAttribute('data-was') === '1'; d.removeAttribute('data-was'); });
    copies.forEach(c => c.remove()); copies = [];
    const fp = $('fc-print'); if (fp) fp.innerHTML = '';
    setTimeout(unstack, 40);
  }

  function rows() {
    const id = pageId(), sets = window.PRINT_SETS || {}, out = [];
    const isTopic = (sets.unit1.pages.concat(sets.unit2.pages)).includes(id) && !/^notes|^unit2$/.test(id);
    const rm = /^rsim-(\d+)$/.exec(id), ex = /^ex-\d+$/.test(id);
    if (rm) out.push({ label: 'This exercise', sub: 'The steps, wiring and code', ids: ['robot-' + rm[1]] });
    else if (ex) out.push({ label: 'This example', sub: 'The circuit, steps and code' });
    else if (id === 'flashcards') out.push({ label: 'This deck', sub: 'Every card in the deck as a list' });
    else out.push({ label: isTopic ? 'This topic' : 'This page' });
    const owner = rm ? 'robots' : Object.keys(sets).find(k => k !== 'all' && sets[k].pages.includes(id));
    if (owner) out.push({ label: sets[owner].name, sub: `${sets[owner].desc}, about ${sets[owner].approx} pages`, ids: sets[owner].pages });
    if (!ex && !rm) out.push({ label: sets.all.name, sub: `${sets.all.desc}, about ${sets.all.approx} pages`, ids: sets.all.pages });
    return out;
  }
  function closeMenu() {
    const menu = $('nb-print-menu'), btn = $('nb-print-btn');
    if (!menu.classList.contains('open')) return;
    menu.classList.remove('open'); btn.setAttribute('aria-expanded', 'false');
  }
  function openMenu() {
    const menu = $('nb-print-menu'), btn = $('nb-print-btn');
    if (window.NB_CAN_PRINT) {
      const list = rows();
      menu.innerHTML = '<div class="hd">What to print</div>' + list.map((r, i) => `<button type="button" role="menuitem" data-row="${i}"><b>${r.label}</b>${r.sub ? `<small>${r.sub}</small>` : ''}</button>`).join('');
      menu._rows = list;
    } else {
      const url = window.NB_PUBLIC + (location.hash || '');
      menu.innerHTML = `<div class="hd">Print</div><div class="pm-note">This view can't print. Open the full copy, then use its print button:</div><a role="menuitem" href="${url}" target="_blank" rel="noopener"><b>Open the printable copy</b><small>${window.NB_PUBLIC.replace(/^https:\/\//, '')}</small></a>`;
    }
    menu.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
    const first = menu.querySelector('button,a'); if (first) first.focus();
  }

  window.EReading = {
    init() {
      paintPicker();
      document.querySelectorAll('[data-set-reading]').forEach(b => b.addEventListener('click', () => setMode(b.getAttribute('data-set-reading'))));
      new MutationObserver(paintPicker).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

      $('nb-search-btn').addEventListener('click', e => { e.stopPropagation(); closeMenu(); window.ENotebookSearch.open(); });

      const menu = $('nb-print-menu'), btn = $('nb-print-btn');
      btn.addEventListener('click', e => { e.stopPropagation(); if (menu.classList.contains('open')) closeMenu(); else openMenu(); });
      menu.addEventListener('click', e => {
        const b = e.target.closest('[data-row]');
        if (!b) return;
        const r = menu._rows[+b.getAttribute('data-row')];
        closeMenu();
        if (r.ids) { stack(r.ids); window.scrollTo(0, 0); }
        setTimeout(() => window.print(), 60);
      });
      menu.addEventListener('keydown', e => {
        const items = Array.from(menu.querySelectorAll('button,a')), at = items.indexOf(document.activeElement);
        if (e.key === 'ArrowDown') { e.preventDefault(); items[(at + 1) % items.length].focus(); }
        if (e.key === 'ArrowUp') { e.preventDefault(); items[(at - 1 + items.length) % items.length].focus(); }
      });
      document.addEventListener('click', e => { if (!menu.contains(e.target)) closeMenu(); });
      document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.classList.contains('open')) { closeMenu(); btn.focus(); } });
      addEventListener('hashchange', closeMenu);
      addEventListener('beforeprint', prepare);
      addEventListener('afterprint', finish);
    },
    stack, unstack, rows, MODES,
  };
})();
