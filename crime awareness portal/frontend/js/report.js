// Handle report form submission
document.getElementById('reportForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const reportData = {
        accusedName: formData.get('accusedName'),
        department: formData.get('department'),
        violationType: formData.get('violationType'),
        description: formData.get('description'),
        anonymous: formData.get('anonymous') === 'on',
        evidence: formData.get('evidence'),
        submittedAt: new Date().toISOString(),
        status: 'Pending'
    };

    // In a real app, send to server. For demo, store in localStorage
    let reports = JSON.parse(localStorage.getItem('reports')) || [];
    reports.push(reportData);
    localStorage.setItem('reports', JSON.stringify(reports));

    alert('Report submitted successfully! It will be reviewed by the authorities.');
    this.reset();
});

// Logout function
function logout() {
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    window.location.href = 'index.html';
}

// Check if user is logged in as student
window.addEventListener('DOMContentLoaded', function() {
    const userRole = localStorage.getItem('userRole');
    if (userRole !== 'student') {
        alert('Access denied. Please login as a student.');
        window.location.href = 'login.html';
    }
});