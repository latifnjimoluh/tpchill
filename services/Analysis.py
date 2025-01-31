import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Charger les données CSV
def load_data(file_name):
    return pd.read_csv(file_name)

# Visualisation des données
def visualize_data(df):
    # Conversion des colonnes si nécessaire
    df["Years"] = pd.to_numeric(df["Years"], errors="coerce")
    df["Victory"] = pd.to_numeric(df["Victory"], errors="coerce")
    df["Gf"] = pd.to_numeric(df["Gf"], errors="coerce")
    df["Win"] = pd.to_numeric(df["Win"], errors="coerce")

    # Filtrer les données pour les visualisations
    team_name = df["Name"].iloc[0]  # Nom de l'équipe en cours (première ligne du CSV)

    # 1. Évolution des victoires d'une équipe sur plusieurs années (courbe)
    plt.figure(figsize=(10, 6))
    team_data = df[df["Name"] == team_name]
    plt.plot(team_data["Years"], team_data["Victory"], marker="o", label="Victoires")
    plt.title(f"Évolution des victoires de l'équipe {team_name}")
    plt.xlabel("Année")
    plt.ylabel("Nombre de victoires")
    plt.legend()
    plt.grid()
    plt.show()

    # 2. Comparaison du nombre de buts marqués par année
    plt.figure(figsize=(10, 6))
    sns.histplot(data=team_data, x="Years", weights="Gf", kde=False, bins=10, color="skyblue")
    plt.title(f"Nombre de buts marqués par l'équipe {team_name} par année")
    plt.xlabel("Année")
    plt.ylabel("Nombre de buts marqués")
    plt.grid()
    plt.show()

    # 3. Victoires par équipe
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Name", y="Victory", data=df)
    plt.title("Répartition des victoires par équipe")
    plt.xlabel("Équipe")
    plt.ylabel("Victoires")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

    # 4. Performances moyennes par année
    plt.figure(figsize=(12, 8))
    heatmap_data = df.groupby("Years")[["Victory", "Gf", "Ga", "Win"]].mean()
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Performances moyennes par année")
    plt.xlabel("Statistiques")
    plt.ylabel("Année")
    plt.show()

    # 5. Nombre de buts marqués vs Pourcentage de victoires
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Gf", y="Win", hue="Name", size="Victory", sizes=(50, 300), palette="viridis")
    plt.title("Corrélation entre buts marqués et pourcentage de victoires")
    plt.xlabel("Buts marqués (Gf)")
    plt.ylabel("Pourcentage de victoires (Win %)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid()
    plt.show()

    # 6. Distribution des performances pour une année donnée
    year_filter = 2010  # Vous pouvez changer l'année ici
    year_data = df[df["Years"] == year_filter]
    plt.figure(figsize=(10, 6))
    sns.barplot(data=year_data, x="Name", y="Win", palette="Blues_d")
    plt.title(f"Performances des équipes en {year_filter}")
    plt.xlabel("Équipe")
    plt.ylabel("Pourcentage de victoires (Win %)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

# Exemple d'utilisation
team_name = "canadiens"  # Remplacez par l'équipe pour laquelle les données ont été extraites
csv_file = f"{team_name}_team_data.csv"

# Charger les données du fichier CSV généré
df = load_data(csv_file)

# Visualiser les données
visualize_data(df)