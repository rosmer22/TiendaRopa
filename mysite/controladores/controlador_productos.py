from bd import obtener_conexion

def insertar_producto(nombre,precio, descripcion,imagen,categoriaID):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO productos(nombre,precio, descripcion,imagen,categoriaID) VALUES (%s, %s, %s, %s, %s)",
                       (nombre,precio, descripcion,imagen,categoriaID))
    conexion.commit()
    conexion.close()


def obtener_productos(id):
    conexion = obtener_conexion()
    calzado = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT productoID, nombre,precio, descripcion,imagen,categoriaID FROM productos where categoriaID= %s ", (id))
        calzado = cursor.fetchall()
    conexion.close()
    return calzado

def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT productoID, nombre,precio, descripcion,imagen,categoriaID FROM productos WHERE productoID = %s", (id))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM stock_productos where productoID = %s", (id))
        cursor.execute("DELETE FROM productos WHERE productoID = %s", (id))
    conexion.commit()
    conexion.close()

def actualizar_producto(nombre, precio, descripcion, imagen, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE productos SET nombre = %s, precio = %s, descripcion = %s, imagen = %s WHERE productoID = %s",
                       (nombre, precio, descripcion, imagen, id))
    conexion.commit()
    conexion.close()

def obtener_stock_por_id(id,talla):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            """SELECT p.productoID, p.nombre, p.precio,
                p.descripcion,p.imagen,p.categoriaID, st.cantidad, tl.tallaID
                FROM productos as p inner join stock_productos as st on p.productoID = st.productoID
                inner join tallas as tl on tl.tallaID=st.tallaID
                WHERE p.productoID = %s and tl.medida = %s""", (id,talla))
        juego = cursor.fetchone()
    conexion.close()
    return juego



