// User Signup Form Validation
const signupForm = document.getElementById('signupForm');

if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent form from submitting
        
        // Get input values
        const name = document.getElementById('signupName').value.trim();
        const email = document.getElementById('signupEmail').value.trim();
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Validation: Check if name is empty
        if (name === '') {
            alert('Please enter your name');
            return;
        }
        
        // Validation: Check if email is valid
        if (!email.includes('@') || !email.includes('.')) {
            alert('Please enter a valid email address');
            return;
        }
        
        // Validation: Check if password is at least 6 characters
        if (password.length < 6) {
            alert('Password must be at least 6 characters long');
            return;
        }
        
        // Validation: Check if passwords match
        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }
        
        // If all validations pass
        alert('Signup Successful! Welcome ' + name);
        signupForm.reset(); // Clear the form
    });
}

// User Login Form Validation
const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent form from submitting
        
        // Get input values
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;
        
        // Validation: Check if email is empty
        if (email === '') {
            alert('Please enter your email');
            return;
        }
        
        // Validation: Check if email is valid
        if (!email.includes('@') || !email.includes('.')) {
            alert('Please enter a valid email address');
            return;
        }
        
        // Validation: Check if password is empty
        if (password === '') {
            alert('Please enter your password');
            return;
        }
        
        // If all validations pass
        alert('Login Successful!');
        loginForm.reset(); // Clear the form
    });
}

// Admin Login Form Validation
const adminForm = document.getElementById('adminForm');

if (adminForm) {
    adminForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent form from submitting
        
        // Get input values
        const email = document.getElementById('adminEmail').value.trim();
        const password = document.getElementById('adminPassword').value;
        
        // Validation: Check if email is empty
        if (email === '') {
            alert('Please enter admin email');
            return;
        }
        
        // Validation: Check if email is valid
        if (!email.includes('@') || !email.includes('.')) {
            alert('Please enter a valid email address');
            return;
        }
        
        // Validation: Check if password is empty
        if (password === '') {
            alert('Please enter admin password');
            return;
        }
        
        // If all validations pass
        alert('Admin Login Successful!');
        adminForm.reset(); // Clear the form
    });
}
