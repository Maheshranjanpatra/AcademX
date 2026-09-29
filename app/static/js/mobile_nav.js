/**
 * Nymora Mobile Navigation
 * Drawer, ripple, theme toggle, icon pop — mobile only
 */
(function () {
  'use strict';

  var drawer    = document.getElementById('mobile-drawer');
  var scrim     = document.getElementById('mobile-scrim');
  var html      = document.documentElement;
  var themeBtn  = document.getElementById('mobile-theme-toggle');

  if (!drawer || !scrim) return;

  /* ============================================================
     DRAWER OPEN / CLOSE
     ============================================================ */
  function openDrawer() {
    drawer.classList.add('open');
    scrim.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    drawer.classList.remove('open');
    scrim.classList.remove('open');
    document.body.style.overflow = '';
  }

  var hamburger = document.getElementById('mobile-menu-toggle');
  if (hamburger) {
    hamburger.addEventListener('click', function (e) {
      e.preventDefault();
      openDrawer();
    });
  }

  var closeBtn = document.getElementById('mobile-drawer-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeDrawer);
  }

  scrim.addEventListener('click', closeDrawer);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeDrawer();
  });

  /* ============================================================
     RIPPLE
     ============================================================ */
  function ripple(el, ev) {
    var r = el.getBoundingClientRect();
    var x = (ev.clientX || r.left + r.width / 2) - r.left;
    var y = (ev.clientY || r.top + r.height / 2) - r.top;
    var s = document.createElement('span');
    s.className = 'ripple';
    s.style.width = s.style.height = Math.max(r.width, r.height) * 1.9 + 'px';
    s.style.left = x + 'px';
    s.style.top = y + 'px';
    el.appendChild(s);
    setTimeout(function () { s.remove(); }, 650);
  }

  document.querySelectorAll('.mobile-nav-item, .dr-item').forEach(function (el) {
    el.addEventListener('click', function (ev) {
      ripple(el, ev);
      el.classList.remove('pop');
      void el.offsetWidth;
      el.classList.add('pop');
    });
  });

  /* ============================================================
     THEME TOGGLE
     ============================================================ */
  if (themeBtn) {
    var savedTheme = 'light';
    try { savedTheme = localStorage.getItem('nymora-theme') || 'light'; } catch (e) {}

    if (savedTheme === 'dark') {
      html.classList.remove('light');
      html.classList.add('dark');
      themeBtn.classList.add('on');
    }

    themeBtn.addEventListener('click', function () {
      if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        html.classList.add('light');
        themeBtn.classList.remove('on');
        try { localStorage.setItem('nymora-theme', 'light'); } catch (e) {}
      } else {
        html.classList.remove('light');
        html.classList.add('dark');
        themeBtn.classList.add('on');
        try { localStorage.setItem('nymora-theme', 'dark'); } catch (e) {}
      }
    });
  }

  /* ============================================================
     CLOSE DRAWER AFTER NAV CLICK
     ============================================================ */
  document.querySelectorAll('.dr-item').forEach(function (el) {
    el.addEventListener('click', function () {
      setTimeout(closeDrawer, 180);
    });
  });

})();