/* ============================================================
   AcademX Math Composer
   Auto-enhances every textarea with class `mc-enabled`.
   ============================================================ */
(function () {
  'use strict';

  var DEBOUNCE_MS = 300;

  var QUICK_BUTTONS = [
    { label: 'x\u00B2', insert: '$^$',           cursor: 2, title: 'Power' },
    { label: 'a/b',     insert: '$\\frac{}{}$',  cursor: 7, title: 'Fraction' },
    { label: '\u221Ax', insert: '$\\sqrt{}$',    cursor: 7, title: 'Square root' },
    { label: '\u222B',  insert: '$\\int_{}^{}$', cursor: 7, title: 'Integral' },
    { label: '\u2211',  insert: '$\\sum_{}^{}$', cursor: 7, title: 'Sum' },
    { label: '\u03C0',  insert: '$\\pi$',        cursor: 0, title: 'Pi' }
  ];

  var PALETTE = [
    {
      label: 'Greek',
      items: [
        ['\u03B1', '\\alpha'],   ['\u03B2', '\\beta'],
        ['\u03B3', '\\gamma'],   ['\u03B4', '\\delta'],
        ['\u03B8', '\\theta'],   ['\u03BB', '\\lambda'],
        ['\u03BC', '\\mu'],      ['\u03C3', '\\sigma'],
        ['\u03C9', '\\omega'],   ['\u03C0', '\\pi'],
        ['\u03C6', '\\phi'],     ['\u03C8', '\\psi'],
        ['\u03A3', '\\Sigma'],   ['\u03A9', '\\Omega'],
        ['\u0394', '\\Delta'],   ['\u0393', '\\Gamma']
      ]
    },
    {
      label: 'Operations',
      items: [
        ['\u00B1', '\\pm'],       ['\u00D7', '\\times'],
        ['\u00F7', '\\div'],      ['\u2264', '\\leq'],
        ['\u2265', '\\geq'],      ['\u2260', '\\neq'],
        ['\u2248', '\\approx'],   ['\u2208', '\\in'],
        ['\u221E', '\\infty'],    ['\u2202', '\\partial'],
        ['\u2207', '\\nabla'],    ['\u221A', '\\sqrt{}']
      ]
    },
    {
      label: 'Arrows',
      items: [
        ['\u2192', '\\to'],               ['\u2190', '\\leftarrow'],
        ['\u2194', '\\leftrightarrow'],   ['\u21D2', '\\Rightarrow'],
        ['\u21D4', '\\Leftrightarrow'],   ['\u21A6', '\\mapsto']
      ]
    },
    {
      label: 'Templates',
      items: [
        ['x^2',  '^'],                ['x_i',  '_'],
        ['a/b',  '\\frac{}{}'],       ['sqrt', '\\sqrt{}'],
        ['int',  '\\int_{}^{}'],      ['sum',  '\\sum_{}^{}'],
        ['lim',  '\\lim_{x \\to 0}'], ['ddx',  '\\frac{d}{dx}']
      ]
    }
  ];

  var HELP_TEXT =
    'Type $x^2$ for inline math.\n' +
    'Type $$x^2$$ for display math.\n\n' +
    'Examples:\n' +
    '  $x^2$         -> x squared\n' +
    '  $\\frac{a}{b}$ -> fraction\n' +
    '  $\\sqrt{x}$    -> square root\n' +
    '  $\\int_a^b$    -> integral\n\n' +
    'Or just click the buttons above.';

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

    var timer = null;
    textarea.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { updatePreview(textarea, preview); }, DEBOUNCE_MS);
    });

    textarea.addEventListener('focus', function () {
      if (/\$/.test(textarea.value)) updatePreview(textarea, preview);
    });

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

    palette.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-latex]');
      if (!btn) return;
      e.preventDefault();
      smartInsert(textarea, btn.dataset.latex);
      updatePreview(textarea, preview);
      palette.hidden = true;
    });

    document.addEventListener('click', function (e) {
      if (!palette.hidden && !toolbar.contains(e.target)) {
        palette.hidden = true;
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !palette.hidden) palette.hidden = true;
    });
  }

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

    if (MJ && MJ.typesetPromise) {
      MJ.typesetPromise([el]).catch(function () {});
      return;
    }

    if (window.loadMathJax) {
      window.loadMathJax().then(function () {
        if (window.MathJax && window.MathJax.typesetPromise) {
          window.MathJax.typesetPromise([el]).catch(function () {});
        }
      }).catch(function () {});
      return;
    }

    if (MJ && MJ.startup && MJ.startup.promise) {
      MJ.startup.promise.then(function () {
        MJ.typesetPromise && MJ.typesetPromise([el]).catch(function () {});
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
