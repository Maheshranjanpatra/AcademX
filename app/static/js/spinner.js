// NYMORA SPINNER — GLOBAL HELPERS

(function() {
    // Inject the full-page overlay once
    function ensureOverlay() {
        if (document.getElementById('nymoraOverlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'nymoraOverlay';
        overlay.className = 'nymora-overlay';
        overlay.innerHTML = `
            <div class="nymora-spinner nymora-spinner-lg">
                <svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
                    <rect class="spinner-squircle" x="6" y="6" width="48" height="48" rx="14"
                          fill="none" stroke="currentColor" stroke-width="3"
                          stroke-dasharray="90 40" />
                    <g class="spinner-eye">
                        <path d="M18 30 Q30 19 42 30 Q30 41 18 30 Z"
                              fill="none" stroke="currentColor" stroke-width="2"
                              stroke-linejoin="round"/>
                        <circle cx="30" cy="30" r="3" fill="currentColor"/>
                        <line x1="16" y1="44" x2="44" y2="16"
                              stroke="currentColor" stroke-width="2.5"
                              stroke-linecap="round"/>
                    </g>
                </svg>
            </div>
            <div class="nymora-overlay-text">Just a moment…</div>
        `;
        document.body.appendChild(overlay);
    }

    window.NymoraSpinner = {
        show: function(text) {
            ensureOverlay();
            const overlay = document.getElementById('nymoraOverlay');
            if (text) {
                overlay.querySelector('.nymora-overlay-text').textContent = text;
            }
            overlay.classList.add('active');
        },
        hide: function() {
            const overlay = document.getElementById('nymoraOverlay');
            if (overlay) overlay.classList.remove('active');
        },

        /* Attach a loading state to any button */
        button: function(btn, loading) {
            if (!btn) return;
            if (loading) btn.classList.add('is-loading');
            else btn.classList.remove('is-loading');
        }
    };

    // Auto-show overlay when any form is submitted (except AJAX-handled ones)
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('form:not([data-no-spinner])').forEach(form => {
            form.addEventListener('submit', function() {
                // Skip forms that are already using AJAX
                if (form.dataset.ajax === 'true') return;
                window.NymoraSpinner.show();
            });
        });

        // Auto-show overlay on internal link clicks
        document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="mailto"]):not([data-no-spinner])').forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                // Only same-origin navigation
                if (href && !href.startsWith('http') && !href.startsWith('//')) {
                    window.NymoraSpinner.show();
                }
            });
        });
    });
})();
