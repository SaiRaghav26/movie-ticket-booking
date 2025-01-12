// JavaScript for Forgot Password Page Interactivity
document.addEventListener("DOMContentLoaded", () => {
    const forgotPasswordForm = document.getElementById("forgot-password-form");

    // Handle Reset Password Form Submission
    forgotPasswordForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const newPassword = document.getElementById("new-password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        // Validate Passwords
        if (newPassword === confirmPassword) {
            alert("Password reset successful!");
            // Redirect or perform password reset logic here
        } else {
            alert("Passwords do not match. Please try again.");
        }
    });
});
