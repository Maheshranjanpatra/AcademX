document.addEventListener('DOMContentLoaded', () => {

    // --- Sidebar Toggle ---
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');

    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });

    // --- Dark Mode Toggle ---
    const htmlElement = document.documentElement;
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    // Check localStorage
    if (localStorage.getItem('theme') === 'dark') {
        htmlElement.classList.add('dark');
        themeIcon.textContent = 'light_mode';
    }

    themeToggleBtn.addEventListener('click', () => {
        htmlElement.classList.toggle('dark');

        if (htmlElement.classList.contains('dark')) {
            localStorage.setItem('theme', 'dark');
            themeIcon.textContent = 'light_mode';
            updateChartTheme(true);
        } else {
            localStorage.setItem('theme', 'light');
            themeIcon.textContent = 'dark_mode';
            updateChartTheme(false);
        }
    });

    // --- Chart.js Initialization ---
    const ctx = document.getElementById('userChart');
    let userChart;

    if (ctx) {
        const isDark = htmlElement.classList.contains('dark');
        const gridColor = isDark ? '#2a2d3a' : '#e1e2ec';
        const textColor = isDark ? '#a5a9b8' : '#424754';

        userChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'New Users',
                    data: [12, 19, 15, 25, 22, 30, 45],
                    borderColor: '#0058be',
                    backgroundColor: 'rgba(0, 88, 190, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: gridColor }, ticks: { color: textColor } },
                    y: { grid: { color: gridColor }, ticks: { color: textColor } }
                }
            }
        });
    }

    // Helper colors on theme switch
    function updateChartTheme(isDark) {
        if(!userChart) return;
        const gridColor = isDark ? '#2a2d3a' : '#e1e2ec';
        const textColor = isDark ? '#a5a9b8' : '#424754';

        userChart.options.scales.x.grid.color = gridColor;
        userChart.options.scales.x.ticks.color = textColor;
        userChart.options.scales.y.grid.color = gridColor;
        userChart.options.scales.y.ticks.color = textColor;
        userChart.update();
    }
});

// --- Smooth hover feedback for metric cards ---
document.querySelectorAll('.metric-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
});

// --- Auto‑hide flash messages with animation ---
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 500);
    }, 5000);
});

// --- Expand collapsed sidebar on hover (if desired) ---
const sidebar = document.getElementById('sidebar');
if (sidebar) {
    sidebar.addEventListener('mouseenter', () => {
        if (sidebar.classList.contains('collapsed')) {
            sidebar.style.width = '260px';
        }
    });
    sidebar.addEventListener('mouseleave', () => {
        if (sidebar.classList.contains('collapsed')) {
            sidebar.style.width = '72px';
        }
    });
}
