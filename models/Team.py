class Team:
    def __init__(self, name, years, victory, losses, ot_losses, win, gf, ga):
        self.name = name
        self.years = years
        self.victory = victory
        self.losses = losses
        self.ot_losses = ot_losses
        self.win = win
        self.gf = gf
        self.ga = ga

    def to_dict(self):
        """Convertit l'objet Team en dictionnaire pour la sérialisation JSON."""
        return {
            "Name": self.name,
            "Years": self.years,
            "Victory": self.victory,
            "Losses": self.losses,
            "OtLosses": self.ot_losses,
            "Win": self.win,
            "Gf": self.gf,
            "Ga": self.ga
        }