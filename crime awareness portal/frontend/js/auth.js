// Demo user data (in a real app, this would be on the server)
const demoUsers = {
    student: { 'student123': 'pass123' },
    faculty: { 'faculty123': 'pass123' },
    admin: { 'admin123': 'admin123' }
};

function getUsers() {
    const saved = localStorage.getItem('portalUsers');
    if (!saved) {
        localStorage.setItem('portalUsers', JSON.stringify(demoUsers));
        return JSON.parse(JSON.stringify(demoUsers));
    }
    return JSON.parse(saved);
}

function saveUsers(users) {
    localStorage.setItem('portalUsers', JSON.stringify(users));
}

function registerUser(role) {
    const form = document.querySelector(`#${role}Form`);
    if (!form) return;

    const userId = form.querySelector('input[name="userId"]').value.trim();
    const password = form.querySelector('input[name="password"]').value.trim();

    if (!userId || !password) {
        alert('Please fill in both ID and password to register.');
        return;
    }

    const users = getUsers();
    const roleUsers = users[role] || {};
    if (roleUsers[userId]) {
        alert('This ID is already registered. Please login.');
        return;
    }

    roleUsers[userId] = password;
    users[role] = roleUsers;
    saveUsers(users);

    alert('Registration successful. Now login with your new credentials.');
}

// Function to show registration form
function showRegistrationForm() {
    document.querySelector('.auth-box:not(.login-form)').style.display = 'none';
    document.getElementById('studentForm').style.display = 'none';
    document.getElementById('facultyForm').style.display = 'none';
    document.getElementById('adminForm').style.display = 'none';
    document.getElementById('registrationForm').style.display = 'block';
}

// Function to hide registration form
function hideRegistrationForm() {
    document.getElementById('registrationForm').style.display = 'none';
    document.querySelector('.auth-box:not(.login-form)').style.display = 'block';
}

// Function to show role selection
function showRoleSelection() {
    document.querySelector('.auth-box:not(.login-form)').style.display = 'block';
    document.getElementById('studentForm').style.display = 'none';
    document.getElementById('facultyForm').style.display = 'none';
    document.getElementById('adminForm').style.display = 'none';
    document.getElementById('registrationForm').style.display = 'none';
}

// Function to show login form for selected role
function showLoginForm(role) {
    document.querySelector('.auth-box:not(.login-form)').style.display = 'none';
    document.getElementById('studentForm').style.display = 'none';
    document.getElementById('facultyForm').style.display = 'none';
    document.getElementById('adminForm').style.display = 'none';
    document.getElementById('registrationForm').style.display = 'none';

    if (role === 'student') {
        document.getElementById('studentForm').style.display = 'block';
    } else if (role === 'faculty') {
        document.getElementById('facultyForm').style.display = 'block';
    } else if (role === 'admin') {
        document.getElementById('adminForm').style.display = 'block';
    }
}

// Handle role button clicks
document.addEventListener('DOMContentLoaded', function() {
    const roleButtons = document.querySelectorAll('.role-btn');
    roleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const role = this.getAttribute('data-role');
            showLoginForm(role);
        });
    });

    // Handle login form submissions
    const loginForms = document.querySelectorAll('.loginForm');
    loginForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const role = this.getAttribute('data-role');
            const userId = this.querySelector('input[name="userId"]').value.trim();
            const password = this.querySelector('input[name="password"]').value.trim();

            const users = getUsers();
            const roleUsers = users[role] || {};

            if (!userId || !password) {
                alert('Please enter both ID and password.');
                return;
            }

            if (!roleUsers[userId]) {
                alert('This ID is not registered. Please use the Register button first.');
                return;
            }

            if (roleUsers[userId] !== password) {
                alert('Incorrect password. Please try again.');
                return;
            }

            localStorage.setItem('userRole', role);
            localStorage.setItem('userId', userId);

            alert(`Login successful as ${role}!`);

            if (role === 'student') {
                window.location.href = 'report.html';
            } else if (role === 'faculty') {
                window.location.href = 'dashboard.html';
            } else if (role === 'admin') {
                window.location.href = 'admin.html';
            }
        });
    });

    // Handle registration form submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const role = this.querySelector('select[name="role"]').value;
            const userId = this.querySelector('input[name="userId"]').value.trim();
            const password = this.querySelector('input[name="password"]').value.trim();

            if (!userId || !password) {
                alert('Please fill in both ID and password to register.');
                return;
            }

            const users = getUsers();
            const roleUsers = users[role] || {};
            if (roleUsers[userId]) {
                alert('This ID is already registered. Please login.');
                return;
            }

            roleUsers[userId] = password;
            users[role] = roleUsers;
            saveUsers(users);

            alert('Registration successful. Now login with your new credentials.');
            hideRegistrationForm();
        });
    }

    // Check if user is already logged in
    const userRole = localStorage.getItem('userRole');
    if (userRole) {
        // Go straight to your role page (no message popup)
        if (userRole === 'student') {
            window.location.href = 'report.html';
        } else if (userRole === 'faculty') {
            window.location.href = 'dashboard.html';
        } else if (userRole === 'admin') {
            window.location.href = 'admin.html';
        }
        return;
    }
});