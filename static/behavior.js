let clickCount = 0;
let keyPressTimes = [];
let lastKeyTime = null;

// Count clicks
document.addEventListener("click", () => {
    clickCount++;
});

// Track typing delay (time between key presses)
document.addEventListener("keydown", () => {
    let now = Date.now();
    if (lastKeyTime !== null) {
        let delay = (now - lastKeyTime) / 1000; // convert to seconds
        keyPressTimes.push(delay);
    }
    lastKeyTime = now;
});

// On page unload, send data to backend
window.addEventListener("beforeunload", function () {

    let sessionDuration = performance.now() / 1000; // seconds

    // Average typing delay
    let typingDelay = 0;
    if (keyPressTimes.length > 0) {
        typingDelay = keyPressTimes.reduce((a, b) => a + b, 0) / keyPressTimes.length;
    }

    fetch('/predict', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        keepalive: true,
        body: JSON.stringify({
            session_duration: sessionDuration,
            typing_delay: typingDelay,
            click_rate: clickCount,
            checkin_score: 3   // default score for now
        })
    });
});