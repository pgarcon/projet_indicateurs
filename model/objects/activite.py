class ActiviteJSON:
    def __init__(self, IDAct, Titre, TypeAct, IDCat):
        self.IDAct = IDAct
        self.Titre = Titre
        self.TypeAct = TypeAct
        self.IDCat = IDCat

    def __str__(self):
        return f"IDAct: {self.IDAct}, Titre: {self.Titre}, TypeAct: {self.TypeAct}, IDCat: {self.IDCat}"
