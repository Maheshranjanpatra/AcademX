// NYMORA SPINNER — ANONYMOUS SCHOLAR

(function() {
    function ensureOverlay() {
        if (document.getElementById('nymoraOverlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'nymoraOverlay';
        overlay.className = 'nymora-overlay';
        overlay.innerHTML = `
            <div class="nymora-spinner nymora-spinner-lg">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">
                    <defs>
                        <filter id="nymoraGlow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="1.6" result="blur"/>
                            <feMerge>
                                <feMergeNode in="blur"/>
                                <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                        </filter>
                    </defs>

                    <g class="scholar-glow" fill="none" stroke="currentColor" stroke-width="2.6"
                       stroke-linecap="round" stroke-linejoin="round"
                       filter="url(#nymoraGlow)">

                        <path d="M 14,39 Q 50,47 86,39"/>
                        <path d="M 32,40 Q 32,16 50,16 Q 68,16 68,40"/>
                        <path d="M 33,33 L 67,33"/>

                        <circle cx="37" cy="62" r="9.5"/>
                        <circle cx="63" cy="62" r="9.5"/>

                        <path d="M 46.5,60 Q 50,57.5 53.5,60"/>

                    </g>
                </svg>
            </div>
            <div class="nymora-overlay-text" id="nymoraOverlayText">Just a moment…</div>
        `;
        document.body.appendChild(overlay);
    }

    window.NymoraSpinner = {
        show: function(text) {
            ensureOverlay();
            const overlay = document.getElementById('nymoraOverlay');
            const label = document.getElementById('nymoraOverlayText');
            if (text && label) label.textContent = text;
            overlay.classList.add('active');
        },
        hide: function() {
            const overlay = document.getElementById('nymoraOverlay');
            if (overlay) overlay.classList.remove('active');
        },
        button: function(btn, loading) {
            if (!btn) return;
            if (loading) btn.classList.add('is-loading');
            else btn.classList.remove('is-loading');
        }
    };

    document.addEventListener('DOMContentLoaded', function() {
        // Auto-show on regular form submits (skip AJAX-opted-out forms)
        document.querySelectorAll('form:not([data-no-spinner])').forEach(form => {
            form.addEventListener('submit', function() {
                if (form.dataset.ajax === 'true') return;
                window.NymoraSpinner.show();
            });
        });

        // Auto-show on internal link clicks
        document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="mailto"]):not([data-no-spinner])').forEach(link => {
            link.addEventListener('click', function() {
                const href = this.getAttribute('href');
                if (href && !href.startsWith('http') && !href.startsWith('//')) {
                    window.NymoraSpinner.show();
                }
            });
        });
    });
})();
