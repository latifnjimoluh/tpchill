import pandas as pd

class DataAnalyzer:
    def __init__(self, file_path="data/csv/all_teams.csv"):
        """
        Initialise l'analyseur de données avec le fichier CSV.
        """
        self.file_path = file_path
        self.df = self.load_data()
    
    def load_data(self):
        """
        Charge les données depuis le fichier CSV.
        """
        return pd.read_csv(self.file_path)
    
    def analyze(self, team=None):
        """
        Analyse les données et retourne les statistiques descriptives et les corrélations.
        """
        df = self.df
        
        if team:
            df = df[df["Name"] == team]
        
        if df.empty:
            return None, None, None
        
        stats = {}
        columns = ["Victory", "Win", "Gf", "Ga"]
        
        for col in columns:
            stats[col] = {
                "Moyenne": df[col].mean(),
                "Médiane": df[col].median(),
                "Mode": df[col].mode()[0] if not df[col].mode().empty else None,
                "Écart-type": df[col].std()
            }
        
        # Calcul des corrélations
        corr_victory_gf = df["Victory"].corr(df["Gf"], method="pearson")
        corr_win_ga = df["Win"].corr(df["Ga"], method="pearson")
        
        return stats, corr_victory_gf, corr_win_ga

    def best_year(self, team):
        """
        Retourne l'année où l'équipe a eu le meilleur pourcentage de victoires.
        """
        df = self.df[self.df["Name"] == team]
        if df.empty:
            return None

        best_row = df.loc[df["Win"].idxmax()]
        return {"year": best_row["Years"], "win_percentage": best_row["Win"]}

    def performance_over_years(self, team):
        """
        Retourne les performances de l'équipe sur plusieurs années sous forme de dictionnaire {année: win_percentage}.
        """
        df = self.df[self.df["Name"] == team]
        if df.empty:
            return {}

        return df.set_index("Years")["Win"].to_dict()

    def correlation_victory_gf(self):
        """
        Calcule la corrélation entre le nombre de victoires et les buts marqués (GF).
        """
        return self.df["Victory"].corr(self.df["Gf"], method="pearson")

    def best_teams_by_win_ratio(self, top_n=10):
        """
        Retourne les équipes avec le meilleur ratio de victoires sur plusieurs années.
        """
        # Calculer la moyenne du pourcentage de victoires par équipe
        win_ratio = self.df.groupby("Name")["Win"].mean().reset_index()
        win_ratio = win_ratio.sort_values(by="Win", ascending=False).head(top_n)
        
        return win_ratio.to_dict(orient="records")
    
    def compare_teams_performance(self, team_names, start_year=None, end_year=None):
        """
        Compare les performances de plusieurs équipes sur une période donnée.
        :param team_names: Liste des noms des équipes à comparer.
        :param start_year: Année de début (optionnelle).
        :param end_year: Année de fin (optionnelle).
        :return: Un DataFrame contenant les performances des équipes sélectionnées.
        """
        # Filtrer les données pour les équipes sélectionnées
        df_filtered = self.df[self.df["Name"].isin(team_names)]
        
        # Filtrer par période si les années sont spécifiées
        if start_year and end_year:
            df_filtered = df_filtered[(df_filtered["Years"] >= start_year) & (df_filtered["Years"] <= end_year)]
        
        # Retourner les données filtrées
        return df_filtered