class CategorieJSON:
    def __init__(self, IDCat, Titre):
        self.IDCat = IDCat
        self.Titre = Titre

    def __str__(self):
        return f"IDCat: {self.IDCat}, Titre: {self.Titre}"