from flask import Flask, render_template, request, jsonify, send_file
from services.HockeyService import HockeyService
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
hockey_service = HockeyService()

# Créer le dossier data s'il n'existe pas
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def home():
    return render_template('index.html')

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
    filepath = os.path.join('data', filename)
    df = pd.DataFrame(data)

    if format_type == 'csv':
        df.to_csv(filepath, index=False)
    elif format_type == 'xlsx':
        df.to_excel(filepath, index=False)
    elif format_type == 'pdf':
        pdf_buffer = io.BytesIO()
        p = canvas.Canvas(pdf_buffer, pagesize=letter)
        p.drawString(100, 750, f"Données pour : {team_name if team_name != 'all' else 'Toutes les équipes'}")

        y = 730
        for _, row in df.iterrows():
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