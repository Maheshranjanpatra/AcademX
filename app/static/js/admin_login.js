// AcademX Administration Interface Engine

document.addEventListener('DOMContentLoaded', () => {
    const adminCard = document.getElementById('adminCard');
    const adminLoginForm = document.getElementById('adminLoginForm');
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    const eyeOff = passwordToggle ? passwordToggle.querySelector('.eye-off') : null;
    const eyeOn = passwordToggle ? passwordToggle.querySelector('.eye-on') : null;

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

    if (adminLoginForm) {
        adminLoginForm.addEventListener('submit', function () {
            const submitBtn = adminLoginForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.setAttribute('aria-busy', 'true');
                submitBtn.classList.add('is-loading');
                const textEl = submitBtn.querySelector('.btn-text');
                if (textEl) {
                    textEl.textContent = 'Authenticating...';
                }
            }
        });
    }

    const flashMessages = document.querySelector('.flash-message');
    if (flashMessages && adminCard) {
        adminCard.classList.remove('shake');
        void adminCard.offsetWidth;
        adminCard.classList.add('shake');
    }
});
