import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

class DataVisualizationService:
    def __init__(self, data_path="data/csv/all_teams.csv"):
        self.data_path = data_path
        self.df = pd.read_csv(self.data_path)

    def generate_boxplot_victories(self):
        """Génère un boxplot des victoires par équipe"""
        plt.figure(figsize=(10, 5))
        sns.boxplot(x="Name", y="Victory", data=self.df)
        plt.xticks(rotation=90)
        plt.xlabel("Équipe")
        plt.ylabel("Nombre de victoires")
        plt.title("Boxplot des victoires par équipe")
        
        # Convertir en base64
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode()

    def generate_heatmap_performance(self):
        """Génère une heatmap des performances moyennes par année"""
        pivot_table = self.df.pivot_table(values=["Victory", "Gf", "Ga"], index="Years", aggfunc="mean")
        plt.figure(figsize=(10, 5))
        sns.heatmap(pivot_table, cmap="coolwarm", annot=True, fmt=".1f")
        plt.title("Heatmap des performances moyennes par année")
        
        # Convertir en base64
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode()

    def generate_scatter_plot(self):
        """Génère un scatter plot entre les buts marqués et le pourcentage de victoires"""
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x="Gf", y="Win", data=self.df, hue="Name", palette="deep", size="Victory", sizes=(20, 200))
        plt.xlabel("Nombre de buts marqués")
        plt.ylabel("Pourcentage de victoires")
        plt.title("Scatter plot entre buts marqués et pourcentage de victoires")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Convertir en base64
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode()

    def generate_performance_distribution(self):
        """Génère un graphique de distribution des victoires pour une année donnée"""
        year_selected = self.df["Years"].max()  # Sélectionner la dernière année disponible
        df_year = self.df[self.df["Years"] == year_selected]
        
        plt.figure(figsize=(8, 5))
        sns.histplot(df_year["Victory"], bins=10, kde=True, color="blue")
        plt.xlabel("Nombre de victoires")
        plt.ylabel("Fréquence")
        plt.title(f"Distribution des victoires des équipes en {year_selected}")
        
        # Convertir en base64
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        return base64.b64encode(img_io.getvalue()).decode()
