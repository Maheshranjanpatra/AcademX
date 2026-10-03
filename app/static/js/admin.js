// ACADEMX ADMIN PANEL - COMMON JAVASCRIPT

document.addEventListener('DOMContentLoaded', () => {
    initDarkMode();
    initSidebar();
    initSelectAllCheckboxes();
    initConfirmDialogs();
    initAutoDismissAlerts();
});

// --- Dark Mode ---
function initDarkMode() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('academx_theme', isDark ? 'dark' : 'light');
    });
}

// --- Sidebar ---
function initSidebar() {
    const sidebar = document.getElementById('admin-sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle');
    if (!sidebar || !toggleBtn) return;

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
}

// --- Batch Checkbox Toggle ---
function initSelectAllCheckboxes() {
    const selectAll = document.getElementById('select-all-items');
    if (!selectAll) return;

    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    selectAll.addEventListener('change', (e) => {
        itemCheckboxes.forEach(cb => cb.checked = e.target.checked);
        toggleBatchActionButton();
    });

    itemCheckboxes.forEach(cb => {
        cb.addEventListener('change', toggleBatchActionButton);
    });
}

function toggleBatchActionButton() {
    const selected = document.querySelectorAll('.item-checkbox:checked');
    const batchBtn = document.getElementById('batch-action-btn');
    if (batchBtn) {
        batchBtn.disabled = selected.length === 0;
    }
}

// --- Confirm Action Modal / Alert ---
function initConfirmDialogs() {
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', (e) => {
            const message = element.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// --- AJAX Author Reveal (Q&A) ---
async function revealAuthor(questionId) {
    const modal = document.getElementById('author-modal');
    const content = document.getElementById('author-modal-content');

    if (!modal || !content) return;

    content.innerHTML = '<p class="text-muted">Loading author details...</p>';
    modal.classList.add('active');

    try {
        const response = await fetch(`/admin/qa/${questionId}/reveal-author`);
        const data = await response.json();

        if (response.ok && data.success) {
            content.innerHTML = `
                <div style="text-align: left;">
                    <p><strong>Name:</strong> ${data.author.name}</p>
                    <p><strong>Email:</strong> ${data.author.email}</p>
                    <p><strong>Role:</strong> ${data.author.role}</p>
                    <p><strong>Joined:</strong> ${data.author.joined_at}</p>
                </div>
            `;
        } else {
            content.innerHTML = `<p style="color: var(--accent-danger);">${data.error || 'Failed to reveal author details.'}</p>`;
        }
    } catch (err) {
        content.innerHTML = '<p style="color: var(--accent-danger);">Network error occurred.</p>';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

// --- Auto Dismiss Flash Messages ---
function initAutoDismissAlerts() {
    setTimeout(() => {
        document.querySelectorAll('.alert-dismissible').forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 4000);
}
