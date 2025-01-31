import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import re
def scrape_all_pages(team_name):
    base_url = "https://www.scrapethissite.com/pages/forms/"
    page = 1  # Page initiale
    all_data = []

    while True:
        # Construire l'URL avec la pagination
        url = f"{base_url}?q={team_name}&page={page}"
        
        # Effectuer la requête HTTP
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erreur lors de la connexion au site : {response.status_code}")
            break

        # Parser le contenu HTML
        soup = BeautifulSoup(response.content, "html.parser")
        teams = soup.find_all("tr", class_="team")
        
        # Arrêter si aucune équipe n'est trouvée (fin des pages)
        if not teams:
            print(f"Fin du scraping. Aucune équipe trouvée à la page {page}.")
            break
        
        # Extraire les informations des équipes sur la page actuelle
        for team in teams:
            try:
                name = team.find("td", class_="name").text.strip()
                year = team.find("td", class_="year").text.strip()
                wins = team.find("td", class_="wins").text.strip()
                losses = team.find("td", class_="losses").text.strip()
                ot_losses = team.find("td", class_="ot-losses").text.strip()
                win_percentage = team.find("td", class_="pct").text.strip()
                goals_for = team.find("td", class_="gf").text.strip()
                goals_against = team.find("td", class_="ga").text.strip()
                
                all_data.append({
                    "Name": name,
                    "Years": year,
                    "Victory": wins,
                    "Losses": losses,
                    "OtLosses": ot_losses,
                    "Win": win_percentage,
                    "Gf": goals_for,
                    "Ga": goals_against
                })
            except AttributeError:
                continue

        page += 1  # Passer à la page suivante

    return all_data

def save_to_csv(data, team_name):
    if not data:
        print("Aucune donnée trouvée pour cette équipe.")
        return
    
    # Nettoyer le nom de fichier pour éviter les caractères spéciaux
    csv_filename = f"{re.sub(r'[^a-zA-Z0-9]', '_', team_name)}_team_data.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Years", "Victory", "Losses", "OtLosses", "Win", "Gf", "Ga"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Données sauvegardées dans le fichier {csv_filename}.")
    return csv_filename

# Exemple d'utilisation
team_name = "canadiens"  # Remplacez par un nom valide ou laissez vide pour toutes les équipes
data = scrape_all_pages(team_name)
csv_file = save_to_csv(data, team_name)

# Vérification du fichier CSV
if csv_file and os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    display(df)
else:
    print("Fichier non trouvé ou aucune donnée à afficher.")