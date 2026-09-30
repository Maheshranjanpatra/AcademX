/* ============================================================
   Nymora Math Composer
   Auto-enhances every textarea with class `mc-enabled`.
   - Inline $...$ LaTeX
   - Live preview when $ is typed
   - Mini toolbar (x², a/b, √, ∫, ∑, π)
   - Symbol palette (Greek + ops + arrows)
   - Smart insert (wraps in $...$ unless already inside math)
   ============================================================ */
(function () {
  'use strict';

  var DEBOUNCE_MS = 300;

  /* ---------- Symbol definitions ---------- */

  var QUICK_BUTTONS = [
    { label: 'x²',  insert: '$^$',           cursor: 2, title: 'Power (x^n)' },
    { label: 'a/b', insert: '$\\frac{}{}$',  cursor: 7, title: 'Fraction' },
    { label: '√x',  insert: '$\\sqrt{}$',    cursor: 7, title: 'Square root' },
    { label: '∫',   insert: '$\\int_{}^{}$', cursor: 7, title: 'Integral' },
    { label: '∑',   insert: '$\\sum_{}^{}$', cursor: 7, title: 'Sum' },
    { label: 'π',   insert: '$\\pi$',        cursor: 0, title: 'Pi' }
  ];

  var PALETTE = [
    {
      label: 'Greek',
      items: [
        ['α', '\\alpha'],   ['β', '\\beta'],   ['γ', '\\gamma'],   ['δ', '\\delta'],
        ['θ', '\\theta'],   ['λ', '\\lambda'], ['μ', '\\mu'],      ['σ', '\\sigma'],
        ['ω', '\\omega'],   ['π', '\\pi'],     ['φ', '\\phi'],     ['ψ', '\\psi'],
        ['Σ', '\\Sigma'],   ['Ω', '\\Omega'],  ['Δ', '\\Delta'],   ['Γ', '\\Gamma']
      ]
    },
    {
      label: 'Operations',
      items: [
        ['±', '\\pm'],       ['×', '\\times'],   ['÷', '\\div'],
        ['≤', '\\leq'],      ['≥', '\\geq'],     ['≠', '\\neq'],
        ['≈', '\\approx'],   ['∈', '\\in'],      ['∞', '\\infty'],
        ['∂', '\\partial'],  ['∇', '\\nabla'],   ['√', '\\sqrt{}']
      ]
    },
    {
      label: 'Arrows',
      items: [
        ['→', '\\to'],       ['←', '\\leftarrow'],
        ['↔', '\\leftrightarrow'], ['⇒', '\\Rightarrow'],
        ['⇔', '\\Leftrightarrow'], ['↦', '\\mapsto']
      ]
    },
    {
      label: 'Templates',
      items: [
        ['x²',   '^'],                ['xᵢ',  '_'],
        ['a/b',  '\\frac{}{}'],       ['√x',  '\\sqrt{}'],
        ['∫',    '\\int_{}^{}'],      ['∑',   '\\sum_{}^{}'],
        ['lim',  '\\lim_{x \\to 0}'], ['ddx', '\\frac{d}{dx}']
      ]
    }
  ];

  var HELP_TEXT =
    'Type $x^2$ for inline math.\n' +
    'Type $$x^2$$ for display math.\n\n' +
    'Examples:\n' +
    '  $x^2$         → x²\n' +
    '  $\\frac{a}{b}$ → fraction\n' +
    '  $\\sqrt{x}$    → √x\n' +
    '  $\\int_a^b$    → integral\n\n' +
    'Or just click the buttons above.';

  /* ---------- Bootstrap ---------- */

  function init() {
    var textareas = document.querySelectorAll('textarea.mc-enabled');
    textareas.forEach(enhance);
  }

  function enhance(textarea) {
    if (textarea.dataset.mcReady === '1') return;
    textarea.dataset.mcReady = '1';

    var toolbar = buildToolbar();
    var preview = buildPreview();
    var palette = buildPalette();

    toolbar.appendChild(palette);

    var parent = textarea.parentNode;
    parent.insertBefore(toolbar, textarea);
    parent.insertBefore(preview, textarea.nextSibling);

    textarea.classList.add('mc-toolbar-attached');

    /* --- Input → debounced preview update --- */
    var timer = null;
    textarea.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { updatePreview(textarea, preview); }, DEBOUNCE_MS);
    });

    /* --- Focus → if there's already $, show preview --- */
    textarea.addEventListener('focus', function () {
      if (/\$/.test(textarea.value)) updatePreview(textarea, preview);
    });

    /* --- Toolbar click --- */
    toolbar.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-insert]');
      if (btn) {
        e.preventDefault();
        var insert = btn.dataset.insert;
        var offset = parseInt(btn.dataset.cursor || '0', 10);
        insertAtCursor(textarea, insert, offset);
        updatePreview(textarea, preview);
        return;
      }
      var toggle = e.target.closest('[data-toggle-palette]');
      if (toggle) {
        e.preventDefault();
        palette.hidden = !palette.hidden;
      }
    });

    /* --- Palette click --- */
    palette.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-latex]');
      if (!btn) return;
      e.preventDefault();
      var latex = btn.dataset.latex;
      smartInsert(textarea, latex);
      updatePreview(textarea, preview);
      palette.hidden = true;
    });

    /* --- Click outside → close palette --- */
    document.addEventListener('click', function (e) {
      if (!palette.hidden && !toolbar.contains(e.target)) {
        palette.hidden = true;
      }
    });

    /* --- Escape → close palette --- */
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !palette.hidden) palette.hidden = true;
    });
  }

  /* ---------- Builders ---------- */

  function buildToolbar() {
    var bar = document.createElement('div');
    bar.className = 'mc-toolbar';
    bar.setAttribute('role', 'toolbar');
    bar.setAttribute('aria-label', 'Math shortcuts');

    QUICK_BUTTONS.forEach(function (b) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mc-btn';
      btn.textContent = b.label;
      btn.title = b.title;
      btn.dataset.insert = b.insert;
      btn.dataset.cursor = String(b.cursor);
      bar.appendChild(btn);
    });

    var more = document.createElement('button');
    more.type = 'button';
    more.className = 'mc-btn mc-more';
    more.textContent = '+';
    more.title = 'More symbols';
    more.dataset.togglePalette = '1';
    bar.appendChild(more);

    var help = document.createElement('span');
    help.className = 'mc-help';
    help.textContent = '?';
    help.dataset.tip = HELP_TEXT;
    help.setAttribute('tabindex', '0');
    help.setAttribute('role', 'button');
    help.setAttribute('aria-label', 'Math help');
    bar.appendChild(help);

    return bar;
  }

  function buildPreview() {
    var wrap = document.createElement('div');
    wrap.className = 'mc-preview';
    wrap.hidden = true;

    var label = document.createElement('div');
    label.className = 'mc-preview-label';
    label.textContent = 'Live preview';

    var content = document.createElement('div');
    content.className = 'mc-preview-content';

    wrap.appendChild(label);
    wrap.appendChild(content);
    return wrap;
  }

  function buildPalette() {
    var wrap = document.createElement('div');
    wrap.className = 'mc-palette';
    wrap.hidden = true;

    PALETTE.forEach(function (group) {
      var g = document.createElement('div');
      g.className = 'mc-palette-group';

      var label = document.createElement('div');
      label.className = 'mc-palette-label';
      label.textContent = group.label;

      var row = document.createElement('div');
      row.className = 'mc-palette-row';

      group.items.forEach(function (pair) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'mc-palette-btn';
        btn.textContent = pair[0];
        btn.dataset.latex = pair[1];
        btn.title = '$' + pair[1] + '$';
        row.appendChild(btn);
      });

      g.appendChild(label);
      g.appendChild(row);
      wrap.appendChild(g);
    });

    return wrap;
  }

  /* ---------- Insert helpers ---------- */

  function insertAtCursor(textarea, text, cursorOffset) {
    var start = textarea.selectionStart;
    var end = textarea.selectionEnd;
    var value = textarea.value;
    var before = value.slice(0, start);
    var after = value.slice(end);

    textarea.value = before + text + after;

    var pos = start + (cursorOffset || text.length);
    textarea.setSelectionRange(pos, pos);
    textarea.focus();
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
  }

  /**
   * Smart insert: if user is already inside an open $...$, insert raw latex.
   * Otherwise wrap in $...$.
   */
  function smartInsert(textarea, latex) {
    var before = textarea.value.slice(0, textarea.selectionStart);
    var dollars = (before.match(/\$/g) || []).length;
    var insideMath = dollars % 2 === 1;

    if (insideMath) {
      insertAtCursor(textarea, latex, latex.length);
    } else {
      insertAtCursor(textarea, '$' + latex + '$', latex.length + 1);
    }
  }

  /* ---------- Preview rendering ---------- */

  function updatePreview(textarea, previewEl) {
    var text = textarea.value || '';
    var hasMath = /\$[^$]+\$/.test(text);

    if (!hasMath) {
      previewEl.hidden = true;
      return;
    }

    previewEl.hidden = false;
    var content = previewEl.querySelector('.mc-preview-content');
    content.textContent = text;

    typesetWithMathJax(content);
  }

  function typesetWithMathJax(el) {
    var MJ = window.MathJax;
    if (!MJ) return;

    if (MJ.typesetPromise) {
      MJ.typesetPromise([el]).catch(function () {});
    } else if (MJ.startup && MJ.startup.promise) {
      MJ.startup.promise.then(function () {
        MJ.typesetPromise && MJ.typesetPromise([el]).catch(function () {});
      });
    }
  }

  /* ---------- Ready ---------- */

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
