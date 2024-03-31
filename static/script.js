document.addEventListener('DOMContentLoaded', function() {
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
            document.getElementById('message').textContent = data.message || "Player registered!";
            // updateRegisteredPlayers(data.players);
            if (data.matchup) {
                updateMatchupPreview(data.matchup);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function updateMatchupPreview(matchup) {
        const updateTeam = (teamData, teamPrefix) => {
            // Iterates over each role in the team data
            Object.entries(teamData).forEach(([role, playerName]) => {
                // Finds the player's name span within the team's div and updates it
                const playerNameElement = document.getElementById(`${teamPrefix}-${role}-name`);
                if (playerNameElement) {
                    playerNameElement.textContent = playerName || 'TBD';
                } else {
                    console.error(`Player name element not found for: ${teamPrefix}-${role}-name`);
                }
            });
        };

        updateTeam(matchup.blue, 'blue');
        updateTeam(matchup.red, 'red');
    }
});