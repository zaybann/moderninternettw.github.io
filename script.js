// script.js
let intervalId;

function getRandomCount() {
    return Math.floor(Math.random() * 100);
}

function updateCount() {
    const randomCount = getRandomCount();
    const formattedCount = (randomCount < 10 ? '0' : '') + randomCount;
    document.getElementById("counter").innerHTML = formattedCount;
}

function startCounting() {
    if (intervalId) {
        // Stop counting if already started
        clearInterval(intervalId);
        intervalId = null;
    } else {
        // Start counting every second
        intervalId = setInterval(updateCount, 1000);
    }
}
