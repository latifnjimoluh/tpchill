from flask import Flask, render_template, request, jsonify, send_file
from services.HockeyService import HockeyService
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
hockey_service = HockeyService()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    team_name = request.args.get('teamName', '').strip()
    print(f"Recherche côté serveur pour l'équipe : {team_name}")

    # Utiliser la fonction de scraping pour récupérer les données
    results = hockey_service.scrape_all_pages(team_name)

    if not results:
        return jsonify({"error": "Aucune équipe trouvée"}), 404

    return jsonify(results)

@app.route('/all')
def all_teams():
    print("Affichage de toutes les équipes")
    
    # Scraper toutes les équipes (sans filtre)
    all_teams = hockey_service.scrape_all_pages("")

    if not all_teams:
        return jsonify({"error": "Aucune équipe trouvée"}), 404

    return jsonify(all_teams)

@app.route('/download')
def download():
    team_name = request.args.get('teamName', '').strip()
    format_type = request.args.get('format', 'csv')  # Par défaut, CSV
    print(f"Téléchargement des données pour l'équipe : {team_name} au format {format_type}")

    data = hockey_service.scrape_all_pages(team_name if team_name.lower() != 'all' else "")

    if not data:
        return jsonify({"error": "Aucune donnée trouvée"}), 404

    filename = f"{team_name if team_name != 'all' else 'all_teams'}.{format_type}"
    df = pd.DataFrame(data)

    if format_type == 'csv':
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return send_file(
            io.BytesIO(csv_buffer.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )

    elif format_type == 'xlsx':
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        excel_buffer.seek(0)
        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

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
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    return jsonify({"error": "Format non supporté"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
