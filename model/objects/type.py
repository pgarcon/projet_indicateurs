class TypeUtilisateurJSON:
    def __init__(self, IDTypeU, Titre):
        self.IDTypeU = IDTypeU
        self.Titre = Titre

    def __str__(self):
        return f"IDTypeU: {self.IDTypeU}, Titre: {self.Titre}"