class clsStock:
    id = 0
    cantidad = 0
    tallaID = 0
    productoID = 0
    dicstock = dict()

    def __init__(self, p_id, p_cantidad, p_tallaID, p_productoID):
        self.id = p_id
        self.cantidad = p_cantidad
        self.tallaID = p_tallaID
        self.productoID = p_productoID
        self.dicstock["id"] = p_id
        self.dicstock["cantidad"] = p_cantidad
        self.dicstock["tallaID"] = p_tallaID
        self.dicstock["productoID"] = p_productoID