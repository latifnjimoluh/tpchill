// script.js

let currentData = []; // Variable pour stocker les données actuelles

// Gestion de la recherche
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche le rechargement de la page
    const teamName = document.getElementById('teamName').value;
    console.log("Recherche effectuée pour l'équipe :", teamName);

    fetch(`/search?teamName=${encodeURIComponent(teamName)}`)
        .then(response => response.json())
        .then(data => {
            console.log("Données reçues du serveur :", data);
            currentData = data; // Stocker les données pour le téléchargement
            displayResults(data);
        })
        .catch(error => console.error("Erreur lors de la recherche :", error));
});

// Gestion du bouton "Afficher toutes les équipes"
document.getElementById('showAll').addEventListener('click', function() {
    console.log("Affichage de toutes les équipes");

    fetch('/all')
        .then(response => response.json())
        .then(data => {
            console.log("Données reçues du serveur :", data);
            currentData = data; // Stocker les données pour le téléchargement
            displayResults(data);
        })
        .catch(error => console.error("Erreur lors de la récupération des équipes :", error));
});

// Gestion du bouton "Télécharger en CSV"
document.getElementById('downloadCSV').addEventListener('click', function() {
    downloadFile('csv');
});

// Gestion du bouton "Télécharger en Excel"
document.getElementById('downloadExcel').addEventListener('click', function() {
    downloadFile('xlsx');
});

// Gestion du bouton "Télécharger en PDF"
document.getElementById('downloadPDF').addEventListener('click', function() {
    downloadFile('pdf');
});

// Fonction pour télécharger les données dans un format spécifique
function downloadFile(format) {
    const teamName = document.getElementById('teamName').value;
    const downloadName = teamName ? teamName : 'all';

    console.log(`Téléchargement des données en ${format.toUpperCase()} pour :`, downloadName);

    // Rediriger vers la route de téléchargement
    window.location.href = `/download?teamName=${encodeURIComponent(downloadName)}&format=${format}`;
}

// Fonction pour afficher les résultats dans un tableau
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Effacer les résultats précédents

    if (data.length === 0) {
        resultsDiv.innerHTML = "<p>Aucun résultat trouvé.</p>";
        return;
    }

    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Nom de l'équipe</th>
                <th>Année</th>
                <th>Victoires</th>
                <th>Défaites</th>
                <th>OT Losses</th>
                <th>Win %</th>
                <th>Goals For (GF)</th>
                <th>Goals Against (GA)</th>
            </tr>
        </thead>
        <tbody>
            ${data.map(team => `
                <tr>
                    <td>${team.Name}</td>
                    <td>${team.Years}</td>
                    <td>${team.Victory}</td>
                    <td>${team.Losses}</td>
                    <td>${team.OtLosses}</td>
                    <td>${team.Win}</td>
                    <td>${team.Gf}</td>
                    <td>${team.Ga}</td>
                </tr>
            `).join('')}
        </tbody>
    `;
    resultsDiv.appendChild(table);
}