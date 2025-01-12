document.getElementById('profile-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;

    // Assuming here we just show a success message
    const message = `Profile updated successfully!<br>Email: ${email}<br>Age: ${age}<br>Gender: ${gender}`;
    
    document.getElementById('message').innerHTML = message;
});
