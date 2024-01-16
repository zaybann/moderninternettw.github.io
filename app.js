const dataElement = document.getElementById('data');

function updateData() {
    fetch('https://api.thaistock2d.com/live')
        .then(response => response.json())
        .then(data => {
            dataElement.innerHTML = `
                Set: ${data.live.set}, Value: ${data.live.value}, Time: ${data.live.time}, 2D: ${data.live.twod}
            `;
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Update data every 1 seconds
setInterval(updateData, 1000);

// Fetch data initially
updateData();