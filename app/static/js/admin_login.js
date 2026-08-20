// Nymora Administration Interface Engine

document.addEventListener('DOMContentLoaded', () => {
    const adminCard = document.getElementById('adminCard');
    const adminLoginForm = document.getElementById('adminLoginForm');
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    const eyeOff = passwordToggle ? passwordToggle.querySelector('.eye-off') : null;
    const eyeOn = passwordToggle ? passwordToggle.querySelector('.eye-on') : null;

    /*

       // 1. 3D Tilt Effect
    if (adminCard && window.innerWidth > 768) {
        const container = document.querySelector('.admin-wrapper');

        container.addEventListener('mousemove', (e) => {
            const rect = adminCard.getBoundingClientRect();
            const cardCenterX = rect.left + rect.width / 2;
            const cardCenterY = rect.top + rect.height / 2;

            const mouseX = e.clientX - cardCenterX;
            const mouseY = e.clientY - cardCenterY;

            // Limit rotation angle
            const rotateX = (-mouseY / (window.innerHeight / 2)) * 2.5;
            const rotateY = (mouseX / (window.innerWidth / 2)) * 2.5;

            adminCard.style.transform = `rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg)`;
        });

        container.addEventListener('mouseleave', () => {
            adminCard.style.transform = 'rotateX(0deg) rotateY(0deg)';
        });
    }

     // 2. Password Visibility Toggle

    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', () => {
            const isPassword = passwordInput.getAttribute('type') === 'password';

            passwordInput.setAttribute('type', isPassword ? 'text' : 'password');

            if (eyeOff && eyeOn) {
                eyeOff.classList.toggle('hidden', isPassword);
                eyeOn.classList.toggle('hidden', !isPassword);
            }
        });
    }

    // 3. Submission Dynamics & Shake Animation

    if (adminLoginForm) {
        adminLoginForm.addEventListener('submit', (e) => {
            const usernameInput = document.getElementById('username');
            let hasError = false;

            // Basic Client-side verification pass
            if (!usernameInput.value.trim() || !passwordInput.value.trim()) {
                hasError = true;
            }

            if (hasError) {
                e.preventDefault();
                triggerShake();
            }
        });
    }

    // Trigger Shake Effect function
    function triggerShake() {
        if (!adminCard) return;
        adminCard.classList.remove('shake');
        // Force Reflow
        void adminCard.offsetWidth;
        adminCard.classList.add('shake');
    }

    // Auto-shake if backend returned flash error messages
    const flashMessages = document.querySelector('.flash-message');
    if (flashMessages) {
        triggerShake();
    }
});
