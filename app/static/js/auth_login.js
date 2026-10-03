//AcademX Interactive Auth Script

document.addEventListener('DOMContentLoaded', () => {
    const card = document.getElementById('academxCard');
    const container = document.querySelector('.academx-card-side');
    const googleBtn = document.getElementById('academxGoogleBtn');

    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    if (card && container && !isTouchDevice) {
        const maxRotationDegree = 2.5;

        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -maxRotationDegree;
            const rotateY = ((x - centerX) / centerX) * maxRotationDegree;

            card.style.transform = `rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg)`;
        });

        container.addEventListener('mouseleave', () => {
            card.style.transform = 'rotateX(0deg) rotateY(0deg)';
        });
    }

    if (googleBtn) {
        googleBtn.addEventListener('mousedown', () => {
            googleBtn.style.transform = 'translateY(0px) scale(0.98)';
        });

        googleBtn.addEventListener('mouseup', () => {
            googleBtn.style.transform = 'translateY(-3px) scale(1.01)';
        });

        googleBtn.addEventListener('mouseleave', () => {
            googleBtn.style.transform = '';
        });
    }
});
