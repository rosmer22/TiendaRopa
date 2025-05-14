class clsTalla:
    tallaID = 0
    medida = ""
    dicTalla = dict()

    def __init__(self,p_tallaID, p_medida):
        self.tallaID = p_tallaID
        self.medida = p_medida
        self.dicTalla["tallaID"] = p_tallaID
        self.dicTalla["medida"] = p_medida