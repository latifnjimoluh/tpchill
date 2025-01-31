// Récupérer les équipes et les années disponibles dès le chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_teams_and_years')
        .then(response => response.json())
        .then(data => {
            populateTeamSelect(data.teams);
            populateTeamCheckboxes(data.teams);
            populateYearSelect(data.years);
        })
        .catch(error => console.error("Erreur lors de la récupération des équipes et des années :", error));
});

// Remplir le menu déroulant des équipes
function populateTeamSelect(teams) {
    const teamSelect = document.getElementById('team_name');
    teamSelect.innerHTML = teams.map(team => `
        <option value="${team}">${team}</option>
    `).join('');
}

// Remplir les cases à cocher des équipes
function populateTeamCheckboxes(teams) {
    const teamsCheckbox = document.getElementById('teams_checkbox');
    teamsCheckbox.innerHTML = teams.map(team => `
        <label>
            <input type="checkbox" name="teams_list" value="${team}"> ${team}
        </label>
    `).join('');
}

// Remplir le menu déroulant des années
function populateYearSelect(years) {
    const startYearSelect = document.getElementById('start_year');
    const endYearSelect = document.getElementById('end_year');
    startYearSelect.innerHTML = years.map(year => `
        <option value="${year}">${year}</option>
    `).join('');
    endYearSelect.innerHTML = years.map(year => `
        <option value="${year}">${year}</option>
    `).join('');
}

// Gestion du formulaire pour analyser une équipe
document.getElementById('teamForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const teamName = document.getElementById('team_name').value;

    fetch(`/analyse?team_name=${encodeURIComponent(teamName)}`)
        .then(response => response.json())
        .then(data => {
            displayStatsDescriptive(data.stats_descriptive);
            displayCorrelations(data.correlations);
            displayBestYear(data.best_year);
            displayPerformanceEvolution(data.performance_evolution);
            displayBestTeams(data.best_teams);
            displayComparison(data.comparison);
        })
        .catch(error => console.error("Erreur lors de l'analyse :", error));
});

// Gestion du formulaire pour comparer des équipes
document.getElementById('compareForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedTeams = Array.from(document.querySelectorAll('input[name="teams_list"]:checked'))
        .map(checkbox => checkbox.value);
    const startYear = document.getElementById('start_year').value;
    const endYear = document.getElementById('end_year').value;

    fetch(`/analyse?teams_list=${encodeURIComponent(selectedTeams.join(','))}&start_year=${startYear}&end_year=${endYear}`)
        .then(response => response.json())
        .then(data => {
            displayComparison(data.comparison);
        })
        .catch(error => console.error("Erreur lors de la comparaison :", error));
});

// Fonctions pour afficher les résultats (inchangées)
function displayStatsDescriptive(stats) {
    const table = document.getElementById('stats_descriptive');
    table.innerHTML = `
        <tr>
            <th>Statistique</th>
            <th>Ga</th>
            <th>Gf</th>
            <th>Losses</th>
            <th>OtLosses</th>
            <th>Victory</th>
            <th>Win</th>
            <th>Years</th>
        </tr>
        ${Object.keys(stats).map(stat => `
            <tr>
                <td>${stat}</td>
                <td>${stats[stat].Ga}</td>
                <td>${stats[stat].Gf}</td>
                <td>${stats[stat].Losses}</td>
                <td>${stats[stat].OtLosses}</td>
                <td>${stats[stat].Victory}</td>
                <td>${stats[stat].Win}</td>
                <td>${stats[stat].Years}</td>
            </tr>
        `).join('')}
    `;
}

function displayCorrelations(correlations) {
    const table = document.getElementById('correlations');
    table.innerHTML = `
        <tr>
            <th>Corrélation</th>
            <th>Valeur</th>
        </tr>
        ${Object.keys(correlations).map(key => `
            <tr>
                <td>${key}</td>
                <td>${correlations[key]}</td>
            </tr>
        `).join('')}
    `;
}

function displayBestYear(bestYear) {
    const div = document.getElementById('best_year');
    if (bestYear) {
        div.innerHTML = `
            <p>Année : ${bestYear.Years}</p>
            <p>Victoires : ${bestYear.Victory}</p>
            <p>Pourcentage de victoires : ${bestYear.Win}</p>
        `;
    } else {
        div.innerHTML = "<p>Aucune donnée disponible.</p>";
    }
}

function displayPerformanceEvolution(performance) {
    const table = document.getElementById('performance_evolution');
    if (performance) {
        table.innerHTML = `
            <tr>
                <th>Année</th>
                <th>Victoires</th>
                <th>Pourcentage de victoires</th>
            </tr>
            ${performance.map(item => `
                <tr>
                    <td>${item.Years}</td>
                    <td>${item.Victory}</td>
                    <td>${item.Win}</td>
                </tr>
            `).join('')}
        `;
    } else {
        table.innerHTML = "<p>Aucune donnée disponible.</p>";
    }
}

function displayBestTeams(bestTeams) {
    const table = document.getElementById('best_teams');
    if (bestTeams) {
        table.innerHTML = `
            <tr>
                <th>Équipe</th>
                <th>Ratio de victoires</th>
            </tr>
            ${bestTeams.map(team => `
                <tr>
                    <td>${team.Name}</td>
                    <td>${team.Win}</td>
                </tr>
            `).join('')}
        `;
    } else {
        table.innerHTML = "<p>Aucune donnée disponible.</p>";
    }
}

function displayComparison(comparison) {
    const table = document.getElementById('comparison');
    if (comparison) {
        table.innerHTML = `
            <tr>
                <th>Équipe</th>
                <th>Année</th>
                <th>Victoires</th>
                <th>Pourcentage de victoires</th>
            </tr>
            ${comparison.map(item => `
                <tr>
                    <td>${item.Name}</td>
                    <td>${item.Years}</td>
                    <td>${item.Victory}</td>
                    <td>${item.Win}</td>
                </tr>
            `).join('')}
        `;
    } else {
        table.innerHTML = "<p>Aucune donnée disponible.</p>";
    }
}