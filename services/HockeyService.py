from models.Team import Team

class HockeyService:
    def __init__(self):
        # Données factices pour l'exemple (à remplacer par un scraper ou une base de données)
        self.teams = [
            Team("Canadiens de Montréal", 2021, 24, 21, 11, 0.53, 159, 168),
            Team("Maple Leafs de Toronto", 2021, 35, 14, 7, 0.69, 187, 148)
        ]

    def search_team(self, team_name):
        """
        Recherche une équipe par son nom.
        :param team_name: Nom de l'équipe à rechercher.
        :return: Liste des équipes correspondantes.
        """
        return [team for team in self.teams if team_name.lower() in team.name.lower()]