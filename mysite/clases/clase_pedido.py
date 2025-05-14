class clsPedido:
    pedidoID = 0
    fecha = ""
    estado = 0
    subtotal = 0.0
    usuarioID = 0
    dicPedido = dict()

    def __init__(self, p_pedidoID, p_fecha, p_estado, p_subtotal, p_usuarioID):
        self.pedidoID = p_pedidoID
        self.fecha = p_fecha
        self.estado = p_estado
        self.subtotal = p_subtotal
        self.usuarioID = p_usuarioID
        self.dicPedido["pedidoID"] = p_pedidoID
        self.dicPedido["fecha"] = p_fecha
        self.dicPedido["estado"] = p_estado
        self.dicPedido["subtotal"] = p_subtotal
        self.dicPedido["usuarioID"] = p_usuarioID