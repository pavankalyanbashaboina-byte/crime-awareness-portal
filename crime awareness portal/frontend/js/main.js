// Navigation functions
function goDashboard() {
    window.location.href = "dashboard.html";
}

function goToPage(page) {
    window.location.href = page;
}

// Add event listener to openDashboardBtn
document.addEventListener('DOMContentLoaded', function() {
    const openDashboardBtn = document.getElementById('openDashboardBtn');
    if (openDashboardBtn) {
        openDashboardBtn.addEventListener('click', goDashboard);
    }
});