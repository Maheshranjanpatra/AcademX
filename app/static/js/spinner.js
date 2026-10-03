/* ==========================================================================
   ACADEMX OVERLAY CONTROLLER
   - Nav overlay: Data Burst + animated phrase
   - Upload overlay: Data Burst + phrase + gilded progress bar
   ========================================================================== */

(function () {
    'use strict';

    const ACADEMX_MARK = `
        <defs>
            <linearGradient id="nym-body-grad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0" stop-color="#0f3157"/>
                <stop offset="1" stop-color="#0b2243"/>
            </linearGradient>
        </defs>
        <path d="M115.0 175.9C140.2 169.2 157.7 151.9 160.7 130.6C161.1 127.8 161.3 93.9 161.0 88.5C159.2 59.2 141.7 35.1 115.1 25.2C72.1 9.3 26.5 39.7 22.5 87.1C21.8 94.7 22.3 128.7 23.1 133.2C23.9 137.4 23.9 137.8 23.3 146.4C22.9 152.2 22.4 165.8 22.6 166.5C22.9 167.8 23.3 167.8 35.5 167.7C48.7 167.5 49.5 167.5 54.1 165.3C57.5 163.7 58.3 163.6 59.2 165.1C61.6 169.4 73.3 163.4 77.1 155.9C81.1 147.8 76.3 134.9 67.4 130.0C51.2 121.2 44.2 109.4 44.3 90.9C44.3 77.4 47.0 69.0 53.9 61.6C57.0 58.4 56.5 58.6 59.8 58.1C66.5 57.1 71.9 59.5 76.9 65.6C79.5 68.8 81.3 69.5 89.3 70.6C92.1 71.0 92.1 71.1 92.2 79.9C92.4 89.1 92.2 88.5 95.8 90.4C98.2 91.6 98.3 91.3 99.3 85.5C102.2 67.1 112.1 56.1 124.1 57.9C131.1 58.9 138.1 71.0 139.4 84.4C141.2 102.8 136.4 115.8 123.9 126.1C112.4 135.6 108.5 146.2 108.9 166.8C109.1 178.2 108.6 177.5 115.0 175.9Z" fill="url(#nym-body-grad)"/>
        <path d="M68.8 88.9C71.8 88.3 72.2 87.1 70.5 83.6C68.2 78.7 58.4 77.0 59.1 81.6C59.8 86.9 63.8 89.9 68.8 88.9Z" fill="#0f3157"/>
        <path d="M119.6 88.7C122.2 87.9 123.7 86.2 124.9 82.8C125.9 79.8 125.2 79.1 121.1 79.1C116.6 79.1 113.9 81.4 113.0 85.9C112.6 88.1 112.9 88.7 114.9 88.8C118.0 89.0 118.5 89.0 119.6 88.7Z" fill="#0f3157"/>
        <path d="M92.8 91.2L103.2 102L92.5 103Z" fill="#f08041"/>
        <path d="M92.8 91.2L81.5 101.5L92.5 103Z" fill="#fec384"/>
        <path d="M103.2 102L92 119.8L92.5 103Z" fill="#da6a2a"/>
        <path d="M81.5 101.5L92 119.8L92.5 103Z" fill="#f5a05a"/>
    `;

    function ensureOverlay() {
        if (document.getElementById('academxOverlay')) return;
        const overlay = document.createElement('div');
        overlay.id = 'academxOverlay';
        overlay.className = 'academx-overlay';
        overlay.innerHTML = `
            <div class="academx-burst">
                <div class="burst-rays">
                    <i></i><i></i><i></i><i></i><i></i><i></i>
                    <i></i><i></i><i></i><i></i><i></i><i></i>
                </div>
                <div class="burst-core">
                    <svg viewBox="0 0 192 192" xmlns="http://www.w3.org/2000/svg">${ACADEMX_MARK}</svg>
                </div>
            </div>
            <p class="academx-phrase" id="academxPhrase"></p>
            <div class="academx-bar" id="academxBar">
                <div class="bar-head">
                    <div class="pct-num" id="academxBarPct">0%</div>
                </div>
                <div class="bar-body">
                    <div class="fill"></div>
                    <div class="tip"></div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
        renderPhrase('Just a moment....');
    }

    function renderPhrase(text) {
        const el = document.getElementById('academxPhrase');
        if (!el) return;
        el.textContent = '';
        let dotIndex = 0;
        [...text].forEach((ch) => {
            const span = document.createElement('span');
            const isDot = ch === '.';
            span.className = 'char' + (isDot ? ' is-dot' : '');
            span.textContent = ch === ' ' ? '\u00A0' : ch;
            if (isDot) span.style.setProperty('--di', dotIndex++);
            el.appendChild(span);
        });
    }

    function setPhrase(text) {
        renderPhrase(text);
    }

    function setBarProgress(pct) {
        const bar = document.getElementById('academxBar');
        if (!bar) return;
        const clamped = Math.max(0, Math.min(100, pct));
        bar.style.setProperty('--p', clamped / 100);
        const label = document.getElementById('academxBarPct');
        if (label) label.textContent = Math.round(clamped) + '%';
    }

    function setBarState(state) {
        // state: 'idle' | 'done' | 'error'
        const bar = document.getElementById('academxBar');
        if (!bar) return;
        bar.classList.remove('is-done', 'is-error');
        if (state === 'done') bar.classList.add('is-done');
        if (state === 'error') bar.classList.add('is-error');
    }

    const AcademXSpinner = {
        // ---- Navigation overlay ----
        show(text) {
            ensureOverlay();
            const overlay = document.getElementById('academxOverlay');
            overlay.classList.remove('is-upload');
            overlay.classList.add('active');
            overlay.dataset.shownAt = Date.now();
            setPhrase(text || 'Just a moment....');
        },
        hide() {
            const overlay = document.getElementById('academxOverlay');
            if (overlay) overlay.classList.remove('active');
        },

        // ---- Upload overlay ----
        upload: {
            start(text) {
                ensureOverlay();
                const overlay = document.getElementById('academxOverlay');
                overlay.classList.add('active', 'is-upload');
                setPhrase(text || 'Uploading your file....');
                setBarProgress(0);
                setBarState('idle');
            },
            progress(pct) {
                setBarProgress(pct);
            },
            done(text) {
                setBarProgress(100);
                setBarState('done');
                setPhrase(text || 'Done!');
            },
            error(message) {
                setBarState('error');
                setPhrase(message || 'Upload failed.');
            },
            hide() {
                const overlay = document.getElementById('academxOverlay');
                if (overlay) overlay.classList.remove('active', 'is-upload');
            },
        },

        // ---- Attach AJAX upload to a form ----
        attach(formEl, options) {
            if (!formEl) return;
            const opts = options || {};
            const redirectUrl = opts.redirect || null;
            const uploadingText = opts.uploadingText || 'Uploading your file....';
            const doneText = opts.doneText || 'Done!';
            const holdMs = opts.holdMs != null ? opts.holdMs : 500;

            formEl.addEventListener('submit', function (e) {
                e.preventDefault();

                AcademXSpinner.upload.start(uploadingText);

                const xhr = new XMLHttpRequest();
                const formData = new FormData(formEl);

                xhr.upload.addEventListener('progress', function (evt) {
                    if (!evt.lengthComputable) return;
                    let pct = (evt.loaded / evt.total) * 100;
                    // Cap at 95 until server finishes
                    if (pct >= 95) pct = 95;
                    AcademXSpinner.upload.progress(pct);
                });

                xhr.onload = function () {
                    if (xhr.status >= 200 && xhr.status < 400) {
                        AcademXSpinner.upload.done(doneText);
                        setTimeout(function () {
                            const target = redirectUrl || xhr.responseURL || '/';
                            window.location.href = target;
                        }, holdMs);
                    } else {
                        AcademXSpinner.upload.error(
                            'Upload failed. Please try again.'
                        );
                        setTimeout(function () {
                            AcademXSpinner.upload.hide();
                            window.location.reload();
                        }, 1800);
                    }
                };

                xhr.onerror = function () {
                    AcademXSpinner.upload.error('Network error. Please try again.');
                    setTimeout(function () {
                        AcademXSpinner.upload.hide();
                        window.location.reload();
                    }, 1800);
                };

                xhr.open('POST', formEl.action, true);
                xhr.send(formData);
            });
        },
    };

    window.AcademXSpinner = AcademXSpinner;

        // ---- Auto show overlay on internal navigation (delayed) ----
    document.addEventListener('DOMContentLoaded', function () {

        // Delay before showing the spinner so fast navigations don't trigger it.
        const NAV_DELAY_MS = 200;
        let navTimer = null;

        function scheduleNavSpinner(text) {
            clearTimeout(navTimer);
            navTimer = setTimeout(function () {
                AcademXSpinner.show(text || 'Just a moment....');
            }, NAV_DELAY_MS);
        }

        function cancelNavSpinner() {
            clearTimeout(navTimer);
            AcademXSpinner.hide();
        }

        // Simple forms with auto spinner
        document.querySelectorAll('form[data-auto-spinner]').forEach(function (form) {
            form.addEventListener('submit', function () {
                scheduleNavSpinner(form.dataset.spinnerText);
            });
        });

        // Internal link clicks
        document.querySelectorAll(
            'a[href]:not([target="_blank"]):not([href^="#"]):not([href^="mailto"]):not([data-no-spinner])'
        ).forEach(function (link) {
            link.addEventListener('click', function (e) {
                // Ignore modified clicks (cmd/ctrl/middle-click) — those open new tabs
                if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;

                const href = link.getAttribute('href');
                if (href && !href.startsWith('http') && !href.startsWith('//')) {
                    scheduleNavSpinner(link.dataset.spinnerText);
                }
            });
        });

        // If browser restores the page from bfcache, make sure no overlay is stuck
        window.addEventListener('pageshow', function (event) {
            if (event.persisted) cancelNavSpinner();
        });

        // Safety: if the spinner somehow stays longer than 3s, hide it
        // (prevents "spinner forever" bugs on slow servers)
        setInterval(function () {
            const overlay = document.getElementById('academxOverlay');
            if (overlay && overlay.classList.contains('active')) {
                const startedAt = overlay.dataset.shownAt ? parseInt(overlay.dataset.shownAt, 10) : 0;
                if (startedAt && Date.now() - startedAt > 3000) {
                    cancelNavSpinner();
                }
            }
        }, 500);
    });
})();
