from bd import obtener_conexion

def crear_stock(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT productoID FROM productos WHERE categoriaID = %s ORDER BY productoID DESC", (id,))
        productos = cursor.fetchall()
        if id == 4:
            cursor.execute("Select tallaID from tallas where tallaID>=6")
            tallas = cursor.fetchall()
        else:
            cursor.execute("Select tallaID from tallas where tallaID<=5")
            tallas = cursor.fetchall()
        if productos:
            # Obtener el último producto ingresado
            ultimo_producto = productos[0]
            # Insertar el stock para el último producto
            for talla in tallas:
                cursor.execute("INSERT INTO stock_productos (cantidad, tallaID, productoID) VALUES (%s, %s, %s)",
                           (0, talla[0], ultimo_producto[0]))
    conexion.commit()
    conexion.close()


def obtener_stock(id):
    conexion = obtener_conexion()
    stock = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT st.stockID, st.cantidad, st.tallaID, st.productoID, tl.medida 
                       FROM stock_productos AS st INNER JOIN tallas 
                       AS tl ON st.tallaID = tl.tallaID WHERE st.productoID = %s """, (id))
        stock = cursor.fetchall()
    conexion.close()
    return stock


def actualizar_stock(cantidad,talla,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("update stock_productos set cantidad = %s where tallaID=%s and productoID=%s", (cantidad,talla,id))
    conexion.commit()
    conexion.close()

def disminuir_stock(cantidad,talla,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("update stock_productos set cantidad = cantidad-%s where tallaID=%s and productoID=%s", (cantidad,talla,id))
    conexion.commit()
    conexion.close()