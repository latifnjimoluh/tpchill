import requests
from bs4 import BeautifulSoup

class HockeyService:
    def __init__(self):
        self.base_url = "https://www.scrapethissite.com/pages/forms/"
        self.teams = []

    def scrape_all_pages(self, team_name):
        all_data = []
        page = 1  # Commence à la première page

        while True:
            # Construire l'URL avec le paramètre de recherche et la pagination
            url = f"{self.base_url}?q={team_name}&page_num={page}" if team_name else f"{self.base_url}?page_num={page}"
            print(f"Scraping {url}")

            # Faire la requête HTTP
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Erreur {response.status_code} lors de la requête.")
                break

            # Parser le HTML
            soup = BeautifulSoup(response.content, "html.parser")
            teams = soup.find_all("tr", class_="team")

            # Si aucune équipe n'est trouvée, arrêter la boucle
            if not teams:
                print(f"Aucune équipe trouvée à la page {page}. Fin du scraping.")
                break

            # Extraire les informations
            for team in teams:
                try:
                    name = team.find("td", class_="name").text.strip()
                    years = team.find("td", class_="year").text.strip()
                    victory = team.find("td", class_="wins").text.strip()
                    losses = team.find("td", class_="losses").text.strip()
                    ot_losses = team.find("td", class_="ot-losses").text.strip()
                    win = team.find("td", class_="pct").text.strip()
                    gf = team.find("td", class_="gf").text.strip()
                    ga = team.find("td", class_="ga").text.strip()

                    # Ajouter les données extraites dans la liste
                    all_data.append({
                        "Name": name,
                        "Years": years,
                        "Victory": victory,
                        "Losses": losses,
                        "OtLosses": ot_losses,
                        "Win": win,
                        "Gf": gf,
                        "Ga": ga
                    })
                except AttributeError:
                    continue


            page += 1  # Passer à la page suivante

        return all_data
