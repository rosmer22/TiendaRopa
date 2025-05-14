class clsMujer:
    id = 0
    nombre = ""
    descripcion = ""
    precio = 0.0
    imagen = ""
    dicCalzado = dict()

    def __init__(self, p_id, p_nombre, p_descripcion, p_precio, p_imagen):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.precio = p_precio
        self.imagen = p_imagen
        self.dicCalzado["id"] = p_id
        self.dicCalzado["nombre"] = p_nombre
        self.dicCalzado["descripcion"] = p_descripcion
        self.dicCalzado["precio"] = p_precio
        self.dicCalzado["imagen"] = p_imagen