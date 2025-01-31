import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64

class VisualizationService:
    def __init__(self, data_path="data/csv/all_teams.csv"):
        self.data_path = data_path

    def get_teams(self):
        """Retourne la liste des équipes disponibles dans le fichier CSV"""
        if not os.path.exists(self.data_path):
            return [], "Le fichier CSV n'existe pas"
        
        df = pd.read_csv(self.data_path)
        if df.empty or "Name" not in df.columns:
            return [], "Le fichier CSV ne contient pas les données nécessaires"
        
        return sorted(df["Name"].unique()), None

    def generate_victory_plot(self, team_name):
        """Génère la courbe d'évolution des victoires pour une équipe donnée"""
        if not os.path.exists(self.data_path):
            return None, "Le fichier CSV n'existe pas"

        df = pd.read_csv(self.data_path)
        if df.empty or "Name" not in df.columns or "Years" not in df.columns or "Victory" not in df.columns:
            return None, "Le fichier CSV ne contient pas les données nécessaires"

        team_data = df[df["Name"] == team_name].sort_values("Years")

        if team_data.empty:
            return None, f"Aucune donnée trouvée pour l'équipe {team_name}"

        # Générer le graphique
        plt.figure(figsize=(8, 5))
        plt.plot(team_data["Years"], team_data["Victory"], marker='o', linestyle='-', color='b', label=team_name)
        plt.xlabel("Année")
        plt.ylabel("Nombre de victoires")
        plt.title(f"Évolution des victoires de l'équipe {team_name}")
        plt.legend()
        plt.grid(True)

        # Convertir en base64
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode(), None
    
    def generate_goals_histogram_equipe(self, team_name):
        """Génère un histogramme du nombre de buts marqués par année pour une équipe donnée"""
        if not os.path.exists(self.data_path):
            return None, "Le fichier CSV n'existe pas"

        df = pd.read_csv(self.data_path)

        if df.empty or "Years" not in df.columns or "Gf" not in df.columns or "Name" not in df.columns:
            return None, "Le fichier CSV ne contient pas les données nécessaires"

        # Filtrer les données de l'équipe sélectionnée
        team_data = df[df["Name"] == team_name]

        if team_data.empty:
            return None, f"Aucune donnée trouvée pour l'équipe {team_name}"

        # Générer l'histogramme
        plt.figure(figsize=(8, 5))
        plt.hist(team_data["Years"], bins=10, weights=team_data["Gf"], color='g', alpha=0.7, edgecolor='black')
        plt.xlabel("Année")
        plt.ylabel("Total des buts marqués")
        plt.title(f"Histogramme des buts marqués par l'équipe {team_name} par année")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Convertir en base64
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode(), None
    
    
    def generate_goals_histogram(self):
        """Génère un histogramme du nombre de buts marqués par année pour toutes les équipes"""
        if not os.path.exists(self.data_path):
            return None, "Le fichier CSV n'existe pas"

        df = pd.read_csv(self.data_path)

        if df.empty or "Years" not in df.columns or "Gf" not in df.columns:
            return None, "Le fichier CSV ne contient pas les données nécessaires"

        # Générer l'histogramme
        plt.figure(figsize=(8, 5))
        plt.hist(df["Years"], bins=10, weights=df["Gf"], color='g', alpha=0.7, edgecolor='black')
        plt.xlabel("Année")
        plt.ylabel("Total des buts marqués")
        plt.title("Comparaison du nombre de buts marqués par année (toutes équipes)")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Convertir en base64
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode(), None
