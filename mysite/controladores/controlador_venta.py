from bd import obtener_conexion
import datetime


def crear_pedido(estado,cliente):
    conexion = obtener_conexion()
    dia_fecha = datetime.datetime.now()
    estado = True
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO pedido(fecha,estado,usuarioID) VALUES (%s, %s,%s)",
                       (dia_fecha,estado,cliente))
    conexion.commit()
    conexion.close()

def crear_subtotal_pedido(subtotal, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE pedido SET subtotal = %s WHERE pedidoID = %s",
                       (subtotal,id))
    conexion.commit()
    conexion.close()

def obtener_pedido():
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT pedidoID from pedido order by pedidoID desc")
        juego = cursor.fetchone()
    conexion.close()
    return juego

def crear_detalle(precio,cantidad,productoID,pedidoID):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO detalle_pedido(precio,cantidad,productoID,pedidoID) VALUES (%s, %s,%s, %s)",
                       (precio,cantidad,productoID,pedidoID))
    conexion.commit()
    conexion.close()