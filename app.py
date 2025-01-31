from flask import Flask, render_template, request, jsonify, send_file
from services.HockeyService import HockeyService
from services.VisualizationService import VisualizationService
from services.DataVisualizationService import DataVisualizationService
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
hockey_service = HockeyService()
visualization_service = VisualizationService()
datadataVisualization = DataVisualizationService()

# Créer les dossiers pour chaque type de fichier s'ils n'existent pas
DATA_DIR = "data"
CSV_DIR = os.path.join(DATA_DIR, "csv")
XLSX_DIR = os.path.join(DATA_DIR, "xlsx")
PDF_DIR = os.path.join(DATA_DIR, "pdf")

for directory in [CSV_DIR, XLSX_DIR, PDF_DIR]:
    os.makedirs(directory, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visualisation', methods=['GET', 'POST'])
def visualisation():
    teams, error = visualization_service.get_teams()
    selected_team = None
    victory_plot = None
    goals_histogram_equipe = None
    goals_histogram = None

    if request.method == 'POST':
        selected_team = request.form.get('team_name')
        
        # Générer le graphique des victoires pour l'équipe choisie
        if selected_team:
            victory_plot, error = visualization_service.generate_victory_plot(selected_team)
            if error:
                return f"Erreur : {error}", 500

            # Générer l'histogramme des buts pour l'équipe choisie
            goals_histogram_equipe, error = visualization_service.generate_goals_histogram_equipe(selected_team)
            if error:
                return f"Erreur : {error}", 500

        # Générer l'histogramme des buts pour toutes les équipes
        goals_histogram, error = visualization_service.generate_goals_histogram()
        if error:
            return f"Erreur : {error}", 500

    return render_template('visualisation.html', 
                           teams=teams, 
                           selected_team=selected_team, 
                           victory_plot=victory_plot, 
                           goals_histogram_equipe=goals_histogram_equipe, 
                           goals_histogram=goals_histogram)


@app.route('/data_visualisation', methods=['GET', 'POST'])
def datavisualisation():
    boxplot_victories = None
    heatmap_performance = None
    scatter_plot = None
    performance_distribution = None

    if request.method == 'POST':
        # Générer les graphiques demandés
        boxplot_victories = datadataVisualization.generate_boxplot_victories()
        heatmap_performance = datadataVisualization.generate_heatmap_performance()
        scatter_plot = datadataVisualization.generate_scatter_plot()
        performance_distribution = datadataVisualization.generate_performance_distribution()

    return render_template('data_visualisation.html', 
                           boxplot_victories=boxplot_victories, 
                           heatmap_performance=heatmap_performance,
                           scatter_plot=scatter_plot,
                           performance_distribution=performance_distribution)


@app.route('/search')
def search():
    team_name = request.args.get('teamName', '').strip()
    page = int(request.args.get('page', 1))  # Numéro de la page
    per_page = 10  # Nombre d'éléments par page
    print(f"Recherche côté serveur pour l'équipe : {team_name}, page {page}")

    # Utiliser la fonction de scraping pour récupérer les données
    results = hockey_service.scrape_all_pages(team_name)

    if not results:
        return jsonify({"error": "Aucune équipe trouvée"}), 404

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]

    return jsonify({
        "data": paginated_results,
        "total": len(results),
        "page": page,
        "per_page": per_page
    })

@app.route('/all')
def all_teams():
    page = int(request.args.get('page', 1))  # Numéro de la page
    per_page = 10  # Nombre d'éléments par page
    print(f"Affichage de toutes les équipes, page {page}")

    # Scraper toutes les équipes (sans filtre)
    all_teams = hockey_service.scrape_all_pages("")

    if not all_teams:
        return jsonify({"error": "Aucune équipe trouvée"}), 404

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = all_teams[start:end]

    return jsonify({
        "data": paginated_results,
        "total": len(all_teams),
        "page": page,
        "per_page": per_page
    })

@app.route('/download')
def download():
    team_name = request.args.get('teamName', '').strip()
    format_type = request.args.get('format', 'csv')  # Par défaut, CSV
    print(f"Téléchargement des données pour l'équipe : {team_name} au format {format_type}")

    data = hockey_service.scrape_all_pages(team_name if team_name.lower() != 'all' else "")

    if not data:
        return jsonify({"error": "Aucune donnée trouvée"}), 404

    filename = f"{team_name if team_name != 'all' else 'all_teams'}.{format_type}"
    
    # Définir le répertoire de stockage en fonction du type de fichier
    if format_type == 'csv':
        folder = CSV_DIR
        filepath = os.path.join(folder, filename)
        pd.DataFrame(data).to_csv(filepath, index=False)
    elif format_type == 'xlsx':
        folder = XLSX_DIR
        filepath = os.path.join(folder, filename)
        pd.DataFrame(data).to_excel(filepath, index=False)
    elif format_type == 'pdf':
        folder = PDF_DIR
        filepath = os.path.join(folder, filename)

        pdf_buffer = io.BytesIO()
        p = canvas.Canvas(pdf_buffer, pagesize=letter)
        p.drawString(100, 750, f"Données pour : {team_name if team_name != 'all' else 'Toutes les équipes'}")

        y = 730
        for _, row in pd.DataFrame(data).iterrows():
            p.drawString(100, y, f"{row.to_dict()}")
            y -= 20
            if y < 50:
                p.showPage()
                y = 750

        p.save()

        with open(filepath, 'wb') as f:
            f.write(pdf_buffer.getvalue())

    return jsonify({"message": f"Fichier sauvegardé dans {filepath}"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
