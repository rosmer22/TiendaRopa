from bd import obtener_conexion

def insertar_talla(medida):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tallas(medida) VALUES (%s)",
                       (medida))
    conexion.commit()
    conexion.close()

def obtener_tallas():
    conexion = obtener_conexion()
    tallas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT tallaID, medida FROM tallas")
        tallas = cursor.fetchall()
    conexion.close()
    return tallas

def obtener_talla_por_id(tallaID):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT tallaID, medida FROM tallas WHERE tallaID = %s", (tallaID,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def eliminar_talla(tallaID):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "delete FROM tallas WHERE tallaID = %s", (tallaID,))
    conexion.commit()
    conexion.close()

def actualizar_talla(medida,tallaID):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("update tallas set medida=%s where tallaid=%s",
                       (medida,tallaID))
    conexion.commit()
    conexion.close()