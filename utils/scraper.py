import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

class Scraper:
    BASE_URL = "https://www.scrapethissite.com/pages/forms/?q="

    @staticmethod
    def recuperer_donnees(nom_equipe):
        """Récupère les données d'une équipe de hockey via web scraping"""
        url = Scraper.BASE_URL + nom_equipe.replace(" ", "+")
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Erreur de requête : {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        equipes = []

        for row in soup.select("tr.team"):
            def safe_int(value):
                return int(value.strip()) if value and value.strip().isdigit() else 0

            def safe_float(value):
                return float(value.strip()) if value and value.strip().replace('.', '', 1).isdigit() else 0.0

            def get_text_or_default(element, default="0"):
                return element.get_text(strip=True) if element else default

            equipe = {
                "nom": get_text_or_default(row.select_one("td.name"), "Inconnu"),
                "annee": safe_int(get_text_or_default(row.select_one("td.year"))),
                "victoires": safe_int(get_text_or_default(row.select_one("td.wins"))),
                "defaites": safe_int(get_text_or_default(row.select_one("td.losses"))),
                "defaites_prolongation": safe_int(get_text_or_default(row.select_one("td.ot-losses"))),
                "pourcentage_victoires": safe_float(get_text_or_default(row.select_one("td.winpct"), "0.0")),
                "buts_marques": safe_int(get_text_or_default(row.select_one("td.goals-for"))),
                "buts_encaisses": safe_int(get_text_or_default(row.select_one("td.goals-against"))),
            }
            
            equipes.append(equipe)

        return equipes

    @staticmethod
    def sauvegarder_csv(equipes, nom_equipe):
        """Sauvegarde ou met à jour les données dans un fichier CSV existant"""
        if not equipes:
            print("❌ Aucune donnée trouvée ! Vérifiez le site ou les sélecteurs CSS.")
            return

        nom_equipe = "".join(c for c in nom_equipe if c.isalnum() or c in ["", "-"]).replace(" ", "")
        nom_fichier = f"hockey_{nom_equipe}.csv"

        if os.path.exists(nom_fichier):
            # Charger l'ancien fichier et fusionner les nouvelles données
            df_ancien = pd.read_csv(nom_fichier)
            df_nouveau = pd.DataFrame(equipes)

            # Vérifier s'il y a des doublons avant de concaténer
            df_final = pd.concat([df_ancien, df_nouveau]).drop_duplicates(subset=["nom", "annee"], keep="last")
        else:
            df_final = pd.DataFrame(equipes)

        # Sauvegarder le fichier CSV mis à jour
        df_final.to_csv(nom_fichier, index=False)
        print(f"📁 Données sauvegardées dans {nom_fichier}")


# Exemple d'utilisation
nom_equipe = "Canadiens de Montréal"
equipes = Scraper.recuperer_donnees(nom_equipe)
Scraper.sauvegarder_csv(equipes, nom_equipe)
