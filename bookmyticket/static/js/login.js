// JavaScript for Login Page Interactivity
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const forgotPasswordLink = document.getElementById("forgot-password-link");
    const signupLink = document.getElementById("signup-link");

    // Handle Login Form Submission
    loginForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (email && password) {
            alert("Login successful!");
            // Redirect or perform login logic here
        } else {
            alert("Please fill in all fields.");
        }
    });

    // Handle Forgot Password Link Click
    forgotPasswordLink.addEventListener("click", (event) => {
        event.preventDefault();
        alert("Redirecting to Forgot Password Page...");
        // Redirect to the forgot password page here
        window.location.href = "/forgot-password"; // Update this to your forgot password URL
    });

     // Handle Signup Link Click
     signupLink.addEventListener("click", (event) => {
        event.preventDefault();
        alert("Redirecting to Signup Page...");
        window.location.href = "/signup/"; // Update with the actual signup URL
    });
});
