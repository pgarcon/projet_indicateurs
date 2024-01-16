class TransitionJSON:
    def __init__(self, IDTran, Utilisateur, Titre, Attribut, Date, Heure, Delai, RefTran, Commentaire):
        self.IDTran = IDTran
        self.Utilisateur = Utilisateur
        self.Titre = Titre
        self.Attribut = Attribut
        self.Date = Date
        self.Heure = Heure
        self.Delai = Delai
        self.RefTran = RefTran
        self.Commentaire = Commentaire

    def __str__(self):
        return f"IDTran: {self.IDTran}, Utilisateur: {self.Utilisateur}, Titre: {self.Titre}, Attribut: {self.Attribut}, Date: {self.Date}, Heure: {self.Heure}, Delai: {self.Delai}, RefTran: {self.RefTran}, Commentaire: {self.Commentaire}"
