// Function to show different sections
function showSection(section) {
    // Hide all sections
    document.getElementById('reportsSection').style.display = 'none';
    document.getElementById('analyticsSection').style.display = 'none';
    document.getElementById('actionsSection').style.display = 'none';

    // Show selected section
    document.getElementById(section + 'Section').style.display = 'block';

    if (section === 'reports') {
        loadReports();
    } else if (section === 'analytics') {
        loadAnalytics();
    }
}

// Load reports from localStorage
function loadReports() {
    const reports = JSON.parse(localStorage.getItem('reports')) || [];
    const reportsList = document.getElementById('reportsList');

    if (reports.length === 0) {
        reportsList.innerHTML = '<p>No reports submitted yet.</p>';
        return;
    }

    reportsList.innerHTML = '';
    reports.forEach((report, index) => {
        const reportItem = document.createElement('div');
        reportItem.classList.add('report-item');
        reportItem.innerHTML = `
            <h4>Report #${index + 1}</h4>
            <p><strong>Accused:</strong> ${report.anonymous ? 'Anonymous' : report.accusedName}</p>
            <p><strong>Department:</strong> ${report.department}</p>
            <p><strong>Violation:</strong> ${report.violationType}</p>
            <p><strong>Description:</strong> ${report.description}</p>
            <p><strong>Status:</strong> <span class="status-${report.status.toLowerCase()}">${report.status}</span></p>
            <div class="report-actions">
                <button class="approve-btn" onclick="updateReportStatus(${index}, 'Approved')">Approve</button>
                <button class="reject-btn" onclick="updateReportStatus(${index}, 'Rejected')">Reject</button>
                <button onclick="assignPunishment(${index})">Assign Punishment</button>
            </div>
        `;
        reportsList.appendChild(reportItem);
    });
}

// Update report status
function updateReportStatus(index, status) {
    const reports = JSON.parse(localStorage.getItem('reports')) || [];
    reports[index].status = status;
    localStorage.setItem('reports', JSON.stringify(reports));
    loadReports();
    loadAnalytics();
}

// Assign punishment (placeholder)
function assignPunishment(index) {
    alert('Punishment assigned for report #' + (index + 1));
    updateReportStatus(index, 'Resolved');
}

// Load analytics
function loadAnalytics() {
    const reports = JSON.parse(localStorage.getItem('reports')) || [];
    const total = reports.length;
    const pending = reports.filter(r => r.status === 'Pending').length;
    const resolved = reports.filter(r => r.status === 'Resolved' || r.status === 'Approved' || r.status === 'Rejected').length;

    document.getElementById('totalReports').textContent = total;
    document.getElementById('pendingReports').textContent = pending;
    document.getElementById('resolvedReports').textContent = resolved;
}

// Logout function
function logout() {
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    window.location.href = 'index.html';
}

// Check if user is logged in as admin
window.addEventListener('DOMContentLoaded', function() {
    const userRole = localStorage.getItem('userRole');
    if (userRole !== 'admin') {
        alert('Access denied. Please login as an admin.');
        window.location.href = 'login.html';
    }
    loadAnalytics(); // Load initial analytics
});
