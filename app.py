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

    # Utiliser le service pour rechercher les équipes
    results = hockey_service.search_team(team_name)

    # Convertir les objets Team en dictionnaires pour la sérialisation JSON
    results_dict = [team.to_dict() for team in results]

    return jsonify(results_dict)

@app.route('/all')
def all_teams():
    print("Affichage de toutes les équipes")

    # Récupérer toutes les équipes
    all_teams = hockey_service.teams

    # Convertir les objets Team en dictionnaires pour la sérialisation JSON
    all_teams_dict = [team.to_dict() for team in all_teams]

    return jsonify(all_teams_dict)

@app.route('/download')
def download():
    team_name = request.args.get('teamName', '').strip()
    format_type = request.args.get('format', 'csv')  # Par défaut, CSV
    print(f"Téléchargement des données pour l'équipe : {team_name} au format {format_type}")

    if team_name.lower() == 'all':
        # Récupérer toutes les équipes
        data = hockey_service.teams
        filename = f"all_teams.{format_type}"
    else:
        # Récupérer les données de l'équipe spécifique
        data = hockey_service.search_team(team_name)
        filename = f"{team_name}.{format_type}"

    # Convertir les données en DataFrame Pandas
    df = pd.DataFrame([team.to_dict() for team in data])

    if format_type == 'csv':
        # Générer un fichier CSV
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
        # Générer un fichier Excel
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
        # Générer un fichier PDF
        pdf_buffer = io.BytesIO()
        p = canvas.Canvas(pdf_buffer, pagesize=letter)
        p.drawString(100, 750, f"Données pour l'équipe : {team_name if team_name != 'all' else 'Toutes les équipes'}")

        y = 730
        for index, row in df.iterrows():
            p.drawString(100, y, str(row))
            y -= 20
            if y < 50:  # Nouvelle page si nécessaire
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

    else:
        return "Format non supporté", 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Utilise le port 8080