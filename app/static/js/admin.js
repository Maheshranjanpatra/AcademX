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

// --- Auto Dismiss Flash Messages ---
function initAutoDismissAlerts() {
    setTimeout(() => {
        document.querySelectorAll('.alert-dismissible').forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 4000);
}
