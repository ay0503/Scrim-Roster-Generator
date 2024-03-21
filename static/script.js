document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = data.message;
        updateRegisteredPlayers(data.players);
        if (data.matchup) {
            updateMatchupPreview(data.matchup);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function updateRegisteredPlayers(players) {
    const playerList = document.getElementById('player-list');
    playerList.innerHTML = '';
    players.forEach(player => {
        const listItem = document.createElement('li');
        listItem.textContent = player;
        playerList.appendChild(listItem);
    });
}

function updateMatchupPreview(matchup) {
    document.getElementById('blue-top').textContent = matchup.blue.top;
    document.getElementById('blue-jungle').textContent = matchup.blue.jungle;
    document.getElementById('blue-mid').textContent = matchup.blue.mid;
    document.getElementById('blue-adc').textContent = matchup.blue.adc;
    document.getElementById('blue-support').textContent = matchup.blue.support;

    document.getElementById('red-top').textContent = matchup.red.top;
    document.getElementById('red-jungle').textContent = matchup.red.jungle;
    document.getElementById('red-mid').textContent = matchup.red.mid;
    document.getElementById('red-adc').textContent = matchup.red.adc;
    document.getElementById('red-support').textContent = matchup.red.support;

    document.getElementById('matchup-preview').style.display = 'block';
}