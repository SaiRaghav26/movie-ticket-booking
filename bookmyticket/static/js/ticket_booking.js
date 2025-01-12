// Initialize an array to store selected seat numbers
let selectedSeatNumbers = [];
let selectedSeats = 0;  // Track the number of selected seats

// Get all the seat checkboxes
const seats = document.querySelectorAll('.seat');
const ticketCountDisplay = document.getElementById('ticket-count');
const totalPriceDisplay = document.getElementById('total-price');
const ticketPrice = 10.00;  // Assuming a fixed price per seat

// Function to update ticket count and total price
function updateTicketInfo() {
    ticketCountDisplay.textContent = selectedSeats;
    totalPriceDisplay.textContent = (selectedSeats * ticketPrice).toFixed(2);
}

// Add event listener to all seat checkboxes
seats.forEach(seat => {
    seat.addEventListener('change', function () {
        const seatNumber = seat.id;  // Assuming seat ids are like 'A1', 'A2', etc.

        if (seat.checked) {
            selectedSeats++;
            selectedSeatNumbers.push(seatNumber);  // Add selected seat number
        } else {
            selectedSeats--;
            const index = selectedSeatNumbers.indexOf(seatNumber);
            if (index !== -1) {
                selectedSeatNumbers.splice(index, 1);  // Remove deselected seat number
            }
        }

        updateTicketInfo();  // Update the displayed ticket count and total price
    });
});

// Confirm Booking Button Click
// Confirm Booking Button Click
document.getElementById('confirm-booking').addEventListener('click', function () {
    // Check if any tickets are selected
    if (selectedSeats > 0) {
        // Store selected seat numbers, seat count, and total price in localStorage
        localStorage.setItem('selectedSeats', selectedSeats);
        localStorage.setItem('totalPrice', (selectedSeats * ticketPrice).toFixed(2));
        localStorage.setItem('seatNumbers', selectedSeatNumbers.join(', ')); // Store selected seat numbers as a comma-separated string

        // Build URL with GET parameters
        const url = `/payments/?selected_seats=${encodeURIComponent(selectedSeatNumbers.join(','))}&total_price=${encodeURIComponent((selectedSeats * ticketPrice).toFixed(2))}`;

        // Redirect to the payment page with the data in the URL
        window.location.href = "/payments/";  // Redirect to the payment page
    } else {
        // Alert if no tickets are selected
        alert("Please select at least one seat before confirming.");
    }
});

