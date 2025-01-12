// Function to handle signup form submission
document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevents the form from submitting and page reload

    // Get form values
    const email = document.getElementById('signup-email').value;
    const age = document.getElementById('signup-age').value;
    const gender = document.getElementById('signup-gender').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('confirm-signup-password').value;

    // Simple validation for password match
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // You can add your logic here to send the data to the server (e.g., using AJAX/fetch)

    // Simulating successful signup (you can replace this with an actual API call)
    setTimeout(function() {
        alert("Signup successful! Redirecting to login page...");

        // Redirect to login page
        window.location.href = "/login/";  // Replace with your actual login page URL
    }, 1000);
});
