// main.js

document.querySelector('form').addEventListener('submit', function (e) {
    const homeTeam = document.getElementById('home_team').value;
    const awayTeam = document.getElementById('away_team').value;
    
    if (!homeTeam || !awayTeam) {
        e.preventDefault();
        alert('Veuillez saisir les deux équipes.');
    }
});
