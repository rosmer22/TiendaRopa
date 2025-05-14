from bd import obtener_conexion

def insertar_usuario(codigo, nombre, apellido, rango, email,fecha,contraseña):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(codigo, nombre, apellido, rango, email,fecha,contraseña) VALUES (%s, %s, %s, %s, %s,%s,%s)",
                       (codigo, nombre, apellido, rango, email,fecha,contraseña))
    conexion.commit()
    conexion.close()

def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT usuarioID, codigo, nombre, apellido, rango, email,fecha FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT usuarioID, codigo, nombre, apellido, rango, email,fecha,contraseña FROM usuarios WHERE usuarioid = %s", (id,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "delete FROM usuarios WHERE usuarioid = %s", (id,))
    conexion.commit()
    conexion.close()

def actualizar_usuario(codigo, nombre, apellido, rango, email,fecha,contraseña,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("update usuarios set codigo=%s, nombre=%s, apellido=%s, rango=%s, email=%s,fecha=%s, contraseña=%s where usuarioid=%s",
                       (codigo, nombre, apellido, rango, email,fecha,contraseña,id))
    conexion.commit()
    conexion.close()


def obtener_user_por_username(username):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT usuarioid,email,contraseña,token,rango FROM usuarios WHERE email = %s", (username,))
        user = cursor.fetchone()
    conexion.close()
    return user

def atualizar_token_user(username, token):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET token = %s where email = %s",
                       (token, username))
    conexion.commit()
    conexion.close()