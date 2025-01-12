function redirectToTheatres(movieName) {
    const url = `/theatres/?movie=${encodeURIComponent(movieName)}`;
    window.location.href = url;
}

let isDown = false;
let startX;
let scrollLeft;

const banner = document.querySelector('.banner');

banner.addEventListener('mousedown', (e) => {
    isDown = true;
    startX = e.pageX - banner.offsetLeft;
    scrollLeft = banner.scrollLeft;
});

banner.addEventListener('mouseleave', () => {
    isDown = false;
});

banner.addEventListener('mouseup', () => {
    isDown = false;
});

banner.addEventListener('mousemove', (e) => {
    if (!isDown) return; // If not dragging, exit the function
    e.preventDefault();
    const x = e.pageX - banner.offsetLeft;
    const walk = (x - startX) * 2; // Adjust the scroll speed
    banner.scrollLeft = scrollLeft - walk;
});

