class clsUsuario:
    id = 0
    codigo = ""
    nombre = ""
    apellido =""
    rango=0
    email=""
    fecha=''
    dicUsuario = dict()

    def __init__(self,p_id, p_codigo,p_nombre,p_apellido,p_rango,p_email,p_fecha):
        self.id = p_id
        self.codigo = p_codigo
        self.nombre = p_nombre
        self.apellido = p_apellido
        self.rango = p_rango
        self.email = p_email
        self.fecha = p_fecha
        self.dicUsuario["id"] = p_id
        self.dicUsuario["codigo"] = p_codigo
        self.dicUsuario["nombre"] = p_nombre
        self.dicUsuario["apellido"] = p_apellido
        self.dicUsuario["rango"] = p_rango
        self.dicUsuario["email"] = p_email
        self.dicUsuario["fecha"] = p_fecha