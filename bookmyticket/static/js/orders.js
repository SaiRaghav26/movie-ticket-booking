// Mock Data for Orders
const orders = [
    {
        id: 1,
        movie: "Avengers: Endgame",
        theatre: "PVR Cinemas",
        seats: ["A1", "A2"],
    },
    {
        id: 2,
        movie: "Inception",
        theatre: "IMAX",
        seats: ["B3", "B4"],
    },
    {
        id: 3,
        movie: "The Dark Knight",
        theatre: "Cinepolis",
        seats: ["C1", "C2", "C3"],
    },
];

// Function to Render Orders
function renderOrders() {
    const ordersList = document.getElementById("orders-list");
    ordersList.innerHTML = ""; // Clear the list

    if (orders.length === 0) {
        ordersList.innerHTML = "<p>No bookings available.</p>";
        return;
    }

    orders.forEach((order) => {
        const orderItem = document.createElement("div");
        orderItem.classList.add("order-item");

        orderItem.innerHTML = `
            <div class="order-details">
                <p><strong>Movie:</strong> ${order.movie}</p>
                <p><strong>Theatre:</strong> ${order.theatre}</p>
                <p><strong>Seats:</strong> ${order.seats.join(", ")}</p>
            </div>
            <button class="cancel-order" data-id="${order.id}">Cancel Booking</button>
        `;

        ordersList.appendChild(orderItem);
    });

    attachCancelEvent();
}

// Function to Attach Cancel Event
function attachCancelEvent() {
    const cancelButtons = document.querySelectorAll(".cancel-order");
    cancelButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const orderId = parseInt(event.target.getAttribute("data-id"));
            cancelOrder(orderId);
        });
    });
}

// Function to Cancel Order
function cancelOrder(orderId) {
    const orderIndex = orders.findIndex((order) => order.id === orderId);
    if (orderIndex !== -1) {
        orders.splice(orderIndex, 1);
        alert(`Booking for order ID ${orderId} has been canceled.`);
        renderOrders(); // Re-render the list
    }
}

// Initialize Orders Page
document.addEventListener("DOMContentLoaded", renderOrders);
