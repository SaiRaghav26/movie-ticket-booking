// Initialize an array to store selected seat numbers and prices
let selectedSeatNumbers = [];
let selectedSeats = 0; // Track the number of selected seats
let totalPrice = 0;    // Track the total price

// Get all the seat checkboxes
const seats = document.querySelectorAll('.seat');
const ticketCountDisplay = document.getElementById('ticket-count');
const totalPriceDisplay = document.getElementById('total-price');

// Function to update ticket count and total price
function updateTicketInfo() {
    ticketCountDisplay.textContent = selectedSeats;
    totalPriceDisplay.textContent = totalPrice.toFixed(2);
}

// Add event listener to all seat checkboxes
seats.forEach(seat => {
    seat.addEventListener('change', function () {
        const seatNumber = seat.id;           // Get seat ID
        const seatPrice = parseFloat(seat.dataset.price); // Get seat price from data attribute

        if (seat.checked) {
            selectedSeats++;
            totalPrice += seatPrice;          // Add seat price to total
            selectedSeatNumbers.push(seatNumber); // Add selected seat number
        } else {
            selectedSeats--;
            totalPrice -= seatPrice;          // Subtract seat price from total
            const index = selectedSeatNumbers.indexOf(seatNumber);
            if (index !== -1) {
                selectedSeatNumbers.splice(index, 1); // Remove deselected seat number
            }
        }

        updateTicketInfo(); // Update the displayed ticket count and total price
    });
});

// Confirm Booking Button Click
document.getElementById('confirm-booking').addEventListener('click', function () {
    // Check if any tickets are selected
    if (selectedSeats > 0) {
        // Store selected seat numbers, seat count, and total price in localStorage
        localStorage.setItem('selectedSeats', selectedSeats);
        localStorage.setItem('totalPrice', totalPrice.toFixed(2));
        localStorage.setItem('seatNumbers', selectedSeatNumbers.join(', '));

        // Build URL with GET parameters
        const url = `/payments/?selected_seats=${encodeURIComponent(selectedSeatNumbers.join(','))}&total_price=${encodeURIComponent(totalPrice.toFixed(2))}`;

        // Redirect to the payment page with the data in the URL
        window.location.href = url; // Redirect to the payment page
    } else {
        // Alert if no tickets are selected
        alert("Please select at least one seat before confirming.");
    }
});
