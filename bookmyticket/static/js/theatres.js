const url = `/book_ticket/?movie=${encodeURIComponent(movieName)}&theatre=${encodeURIComponent(theatreName)}&screen=${encodeURIComponent(screen)}&time=${encodeURIComponent(showTime)}&date=${encodeURIComponent(selected_date)}`;
    console.log("Redirecting to: ", url);  // Debugging URL
    window.location.replace(url);
