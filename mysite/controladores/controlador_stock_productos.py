from bd import obtener_conexion

def insertar_stock(cantidad, tallaID, productoID):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO stock_productos(cantidad, tallaID, productoID) VALUES (%s, %s, %s)",
                       (cantidad, tallaID, productoID))
    conexion.commit()
    conexion.close()

def obtener_stock():
    conexion = obtener_conexion()
    stock = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT stockID, cantidad, tallaID, productoID FROM stock_productos")
        stock = cursor.fetchall()
    conexion.close()
    return stock

def obtener_stock_por_id(id):
    conexion = obtener_conexion()
    stock = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT stockID, cantidad, tallaID, productoID FROM stock_productos WHERE stockID = %s", (id,))
        stock = cursor.fetchone()
    conexion.close()
    return stock

def eliminar_stock(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM stock_productos WHERE stockID = %s", (id,))
    conexion.commit()
    conexion.close()

def actualizar_stock(cantidad, tallaID, productoID, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE stock_productos SET cantidad = %s, tallaID = %s, productoID = %s WHERE stockID = %s",
                       (cantidad, tallaID, productoID, id))
    conexion.commit()
    conexion.close()
