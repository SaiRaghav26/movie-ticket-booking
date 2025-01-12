// Retrieve selected seats, total price, and seat numbers from localStorage
const selectedSeats = localStorage.getItem('selectedSeats');
const totalPrice = localStorage.getItem('totalPrice');
const seatNumbers = localStorage.getItem('seatNumbers'); // Add seat numbers storage if needed

// Check if localStorage data exists and update the page
if (selectedSeats && totalPrice) {
    document.getElementById('num-tickets').textContent = selectedSeats;
    document.getElementById('total-amount').textContent = totalPrice;
    document.getElementById('seat-numbers').textContent = seatNumbers || "No seats selected"; // Show seat numbers if available
} else {
    // Fallback if no data is available
    document.getElementById('num-tickets').textContent = '0';
    document.getElementById('total-amount').textContent = '0.00';
    document.getElementById('seat-numbers').textContent = 'No seats selected';
}

// Price per ticket (optional, if you want to recalculate)
const ticketPrice = 10.00;

// Function to calculate total amount (if not done on booking page)
function calculateTotalAmount() {
    const taxes = 2.00; // Example tax amount
    const totalAmount = (parseFloat(totalPrice) + taxes).toFixed(2);
    document.getElementById('total-amount').textContent = totalAmount;
}

// Confirm payment function
function confirmPayment() {
    // Show success message and hide the payment details
    document.querySelector('.payment-container').style.display = 'none';
    document.getElementById('success-message').classList.remove('hidden');

    // Redirect to the order page after 3 seconds
    setTimeout(function() {
        window.location.href = "/orders/";  // Replace with your actual order page URL
    }, 3000);
}

// Handle button click to confirm payment
document.getElementById('confirm-btn').addEventListener('click', confirmPayment);

// Initial calculation (if needed)
calculateTotalAmount();
