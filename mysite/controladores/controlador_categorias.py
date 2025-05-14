from bd import obtener_conexion

def insertar_categorias(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO categorias(nombre) VALUES ( %s)",
                       (nombre))
    conexion.commit()
    conexion.close()
    
def obtener_categorias():
    conexion = obtener_conexion()
    categoria = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT categoriaID, nombre FROM categorias")
        categoria = cursor.fetchall()
    conexion.close()
    return categoria

def obtener_categoria_por_id(id):
    conexion = obtener_conexion()
    categoria = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT categoriaID, nombre FROM categorias WHERE categoriaID = %s", (id,))
        categoria = cursor.fetchone()
    conexion.close()
    return categoria

def eliminar_categorias(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "delete FROM categorias WHERE categoriaID = %s", (id,))
    conexion.commit()
    conexion.close()

def actualizar_categorias(nombre,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("update categorias set  nombre=%s where categoriaID=%s",
                (nombre,id))
    conexion.commit()
    conexion.close()