class clscategoria:
    id = 0
    nombre = ""
    diccategoria = dict()

    def __init__(self,p_id, p_nombre):
        self.id = p_id
        self.nombre = p_nombre
        self.diccategoria["id"] = p_id
        self.diccategoria["nombre"] = p_nombre