// script.js

let currentData = []; // Variable pour stocker les données actuelles
let currentPage = 1; // Page actuelle
let totalPages = 1; // Nombre total de pages

// Gestion de la recherche
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche le rechargement de la page
    const teamName = document.getElementById('teamName').value;
    currentPage = 1; // Réinitialiser la page à 1
    fetchData(teamName, currentPage);
});

// Gestion du bouton "Afficher toutes les équipes"
document.getElementById('showAll').addEventListener('click', function() {
    currentPage = 1; // Réinitialiser la page à 1
    fetchData("", currentPage);
});

// Gestion des boutons de téléchargement
document.getElementById('downloadCSV').addEventListener('click', () => downloadFile('csv'));
document.getElementById('downloadExcel').addEventListener('click', () => downloadFile('xlsx'));
document.getElementById('downloadPDF').addEventListener('click', () => downloadFile('pdf'));

// Fonction pour télécharger les données dans un format spécifique
function downloadFile(format) {
    const teamName = document.getElementById('teamName').value;
    const downloadName = teamName ? teamName : 'all';

    console.log(`Téléchargement des données en ${format.toUpperCase()} pour :`, downloadName);

    // Rediriger vers la route de téléchargement
    window.location.href = `/download?teamName=${encodeURIComponent(downloadName)}&format=${format}`;
}

// Fonction pour récupérer les données avec pagination
function fetchData(teamName, page) {
    const url = teamName ? `/search?teamName=${encodeURIComponent(teamName)}&page=${page}` : `/all?page=${page}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            console.log("Données reçues du serveur :", data);
            currentData = data.data; // Stocker les données pour le téléchargement
            totalPages = Math.ceil(data.total / data.per_page);
            displayResults(currentData);
            updatePaginationControls();
        })
        .catch(error => console.error("Erreur lors de la récupération des données :", error));
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

// Fonction pour mettre à jour les contrôles de pagination
function updatePaginationControls() {
    const paginationDiv = document.getElementById('pagination');
    if (!paginationDiv) {
        const newPaginationDiv = document.createElement('div');
        newPaginationDiv.id = 'pagination';
        document.getElementById('results').appendChild(newPaginationDiv);
    }

    paginationDiv.innerHTML = '';

    if (currentPage > 1) {
        const prevButton = document.createElement('button');
        prevButton.innerText = 'Précédent';
        prevButton.addEventListener('click', () => {
            currentPage--;
            fetchData(document.getElementById('teamName').value, currentPage);
        });
        paginationDiv.appendChild(prevButton);
    }

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.innerText = i;
        pageButton.addEventListener('click', () => {
            currentPage = i;
            fetchData(document.getElementById('teamName').value, currentPage);
        });
        if (i === currentPage) {
            pageButton.disabled = true;
        }
        paginationDiv.appendChild(pageButton);
    }

    if (currentPage < totalPages) {
        const nextButton = document.createElement('button');
        nextButton.innerText = 'Suivant';
        nextButton.addEventListener('click', () => {
            currentPage++;
            fetchData(document.getElementById('teamName').value, currentPage);
        });
        paginationDiv.appendChild(nextButton);
    }
}