from bd import obtener_conexion


def insertar_pedido(fecha, estado, subtotal, usuarioID):
    conexion = obtener_conexion()
    igv = 1.18
    sub = float(subtotal) / float(igv)
    igv = float(subtotal) - float(sub)
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO pedido(fecha, estado, total, usuarioID,subtotal,igv) VALUES (%s, %s, %s, %s,%s,%s)",
                       (fecha, estado, subtotal, usuarioID,sub,igv))
    conexion.commit()
    conexion.close()

def obtener_pedidos():
    conexion = obtener_conexion()
    pedidos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT pedidoID, fecha, estado, subtotal, usuarioID FROM pedido")
        pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def obtener_pedido_por_id(id):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT pedidoID, fecha, estado, subtotal, usuarioID FROM pedido WHERE pedidoID = %s", (id,))
        pedido = cursor.fetchone()
    conexion.close()
    return pedido

def eliminar_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM pedido WHERE pedidoID = %s", (id,))
    conexion.commit()
    conexion.close()

def actualizar_pedido(fecha, estado, subtotal, usuarioID, pedidoID):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE pedido SET fecha=%s, estado=%s, subtotal=%s, usuarioID=%s WHERE pedidoID=%s",
                       (fecha, estado, subtotal, usuarioID, pedidoID))
    conexion.commit()
    conexion.close()