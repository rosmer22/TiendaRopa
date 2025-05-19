from flask import Flask, render_template, request, redirect, flash, jsonify, json, make_response
import requests
from urllib.parse import urlparse
from flask_jwt_extended import JWTManager, jwt_required
from datetime import datetime
import clases.clase_stock as clase_stock
import clases.clase_usuario as clase_usuario
import controladores.controlador_stock_productos as controlador_stock_productos
import clases.clase_categoria as clase_categoria
import controladores.controlador_categorias as controlador_categorias
import controladores.controlador_pedido as controlador_pedido
import clases.clase_pedido as clase_pedido
import controladores.controlador_usuarios as controlador_usuarios
import controladores.controlador_productos as controlador_productos
import controladores.controlador_venta as controlador_venta
import controladores.controlador_stock as controlador_stock
import controladores.controlador_tallas as controlador_tallas
import clases.clase_calzado as clase_calzado
import clases.clase_hombre as clase_hombre
import clases.clase_mujer as clase_mujer
import clases.clase_nino as clase_nino
import clases.clase_talla as clase_talla
import os
from werkzeug.utils import secure_filename
import hashlib
from hashlib import sha256
import random
from PIL import Image

##SEGURIDAD INICIO##

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

#users = [
#    User(1, 'user1', 'abcxyz'),
#    User(2, 'user2', 'abcxyz'),
#]

#username_table = {u.username: u for u in users}
#userid_table = {u.id: u for u in users}

def authenticate(username, password):
    #user = username_table.get(username, None) # Dejamos de lado el uso del
    #diccionario
    userfrombd = controlador_usuarios.obtener_user_por_username(username)
    user = None
    if userfrombd is not None:
        user = User(userfrombd[0],userfrombd[1],userfrombd[2])
    if user is not None and (user.password == sha256(password.encode('utf-8')).hexdigest()):
        return user

def identity(payload):
    user_id = payload['identity']
    #return userid_table.get(user_id, None)#Dejamos de lado el uso del
    #diccionario y tomamos los datos de la bd
    userfrombd = controlador_usuarios.obtener_usuario_por_id(user_id)
    user = User(userfrombd[0],userfrombd[5],userfrombd[7])
    return user


##SEGURIDAD FIN##

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

UPLOAD_FOLDER = os.path.abspath('mysite/static/img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Inicio y registo

@app.route("/proceso_signup", methods=["POST"])
def proceso_signup():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    codigo = 00
    username = request.form["email"]
    password = request.form["password"]
    fecha = datetime.now()
    epass = sha256(password.encode('utf-8')).hexdigest()
    controlador_usuarios.insertar_usuario(codigo,nombre,apellido,1,username,fecha,epass)
    return redirect("/Inicio")

@app.route("/proceso_login", methods=["POST"])
def proceso_login():
    username = request.form["email"]
    password = request.form["password"]
    epass = sha256(password.encode('utf-8')).hexdigest()
    user = controlador_usuarios.obtener_user_por_username(username)
    if user:
        if user[1] == username and user[2] == epass:
            #token
            t = hashlib.new('sha256')
            entale = random.randint(1,1024)
            strEntale = str(entale)
            t.update(bytes(strEntale, encoding = 'utf-8'))
            token = t.hexdigest()
            #Preparamos respuesta para cookie
            resp = make_response(redirect(request.referrer))
            resp.set_cookie("username", username)
            resp.set_cookie('token', token)
            controlador_usuarios.atualizar_token_user(username, token)
            return resp
    return redirect(request.referrer)

def validar():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    if username:
        if username:
            user = controlador_usuarios.obtener_user_por_username(username)
            if user and token == user[3]:
                return True
    return False


@app.context_processor
def rol_usuario():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    if username:
        if username:
            user = controlador_usuarios.obtener_user_por_username(username)
            if user and token == user[3]:  # Suponiendo que user es una lista y el token está en la posición 3
                rol = user[4]
            else:
                rol = 0
        # Si no se cumple la condición anterior, redirige al usuario al formulario de inicio de sesión
        return dict(rol=rol)
    return dict(rol=0)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/Inicio"))
    resp.set_cookie('token', '', expires=0)
    resp.set_cookie("username", '', expires=0)
    return resp


#Fin de Inicio

#Rutas Simples - No Cambiar

@app.route("/")
@app.route("/Inicio")
def inicio():
    return render_template("index.html")

@app.route("/Error")
def error():
    return render_template("Errores.html")

@app.route("/Libro")
def libro():
    return render_template("libro_de_reclamaciones.html")

@app.route("/Preguntas-Frecuentes")
def preguntas():
    return render_template("preguntas_frecuentes.html")

@app.route("/Ubicanos")
def ubicanos():
    return render_template("ubicanos.html")

@app.route("/Acerca-De")
def acerca():
    return render_template("acerca_de.html")

#Usuarios

@app.route("/Formulario-Usuarios")
def formulario():
    if validar():
        return render_template("Formulario_usuarios.html")
    else:
        return render_template("index.html")


@app.route("/Usuarios")
def usuarios():
    if validar():
        usuarios = controlador_usuarios.obtener_usuarios()
        return render_template("Administrar-Usuarios.html", usuarios=usuarios)
    else:
        return render_template("index.html")


@app.route("/guardar-usuarios", methods=["POST"])
def guardar_usuario():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    rango = request.form["rango"]
    email = request.form["email"]
    contrasena = request.form["contrasena"]
    contrasena = sha256(contrasena.encode('utf-8')).hexdigest()
    fecha = datetime.now()
    controlador_usuarios.insertar_usuario(codigo,nombre,apellido,rango,email,fecha,contrasena)
    return redirect("/Usuarios")

@app.route("/Editar-Usuario",methods=["POST"])
def editarU():
    id = request.form["id"]
    usuario = controlador_usuarios.obtener_usuario_por_id(id)
    return render_template("editar_usuario.html",usuario=usuario)

@app.route("/Elimar_Usuario",methods=["POST"])
def eliminar_usuario():
    controlador_usuarios.eliminar_usuario(request.form["id"])
    return redirect(request.referrer)

@app.route("/Actualizar_Usuario", methods=["POST"])
def actualizar_usuario():
    id = request.form["id"]
    usuario = controlador_usuarios.obtener_usuario_por_id(id)
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    rango = request.form["rango"]
    email = request.form["email"]
    contrasena = request.form["contrasena"]
    if contrasena=='':
        contrasena = usuario[7]
    else:
        contrasena = sha256(contrasena.encode('utf-8')).hexdigest()
    fecha = datetime.now()
    controlador_usuarios.actualizar_usuario(codigo,nombre,apellido,rango,email,fecha,contrasena,id)
    return redirect("/Usuarios")

@app.route("/Registro-Usuarios")
def registro():
    return render_template("registro_de_usuario.html")

#Productos

@app.route("/guardar_producto/<int:cat>", methods=["POST"])
def guardar_producto(cat):
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]
    archivo = request.files['imagen']
    if archivo.filename != '':
        filename = secure_filename(archivo.filename)
        ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(ruta_completa)
    categoria = cat
    controlador_productos.insertar_producto(nombre, precio, descripcion, filename,categoria)
    controlador_stock.crear_stock(cat)
    return redirect("/Administrar-Productos")

@app.route("/Editar-Producto/<int:id>",methods=["GET"])
def editarC(id):
    producto = controlador_productos.obtener_producto_por_id(id)
    return render_template("editar_producto.html",producto=producto)

@app.route("/Elimar_Producto",methods=["POST"])
def eliminar_producto():
    controlador_productos.eliminar_producto(request.form["id"])
    return redirect(request.referrer)

@app.route("/Actualizar_Producto", methods=["POST"])
def actualizar_producto():
    id = request.form["id"]
    producto = controlador_productos.obtener_producto_por_id(id)
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]
    imagen = request.form["imagen"]
    archivo = request.files['img']
    if archivo.filename != '':
        ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], imagen)
        archivo.save(ruta_completa)
    img = producto[4]
    ruta = os.path.join(app.config['UPLOAD_FOLDER'], img)
    nruta = os.path.join(app.config['UPLOAD_FOLDER'], imagen)
    os.rename(ruta, nruta)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/Administrar-Productos")

@app.route("/Administrar-Productos")
def adminP():
    if validar():
        return render_template("administrar_productos.html")
    else:
        return render_template("index.html")


#Stock

@app.route("/Stock/<int:id>")
def stockC(id):
    if validar():
        stocks = controlador_stock.obtener_stock(id)
        return render_template("editar_stockC.html", stocks=stocks)
    else:
        return render_template("index.html")


@app.route("/Actualizar-Stock/<int:antiguo>/<int:idt>/<int:idp>", methods=["POST"])
def actualizar_stockC(antiguo,idt,idp):
    cantidad=request.form["cantidad"]
    cantidad = antiguo+int(cantidad)
    controlador_stock.actualizar_stock(cantidad,idt,idp)
    return redirect(request.referrer)

#Calzado

@app.route("/Formulario-Calzado")
def formularioC():
    if validar():
        idC=4
        return render_template("Formulario_productos.html", idC=idC)
    else:
        return render_template("index.html")


@app.route("/Lista-Calzado")
def listaC():
    if validar():
        productos = controlador_productos.obtener_productos(4)
        return render_template("lista_productos.html",productos=productos)
    else:
        return render_template("index.html")


@app.route("/Calzado")
def calzado():
    productos = controlador_productos.obtener_productos(4)
    return render_template("calzado.html",productos=productos)

#Hombre

@app.route("/Formulario-Hombre")
def formularioH():
    if validar():
        idC = 1
        return render_template("Formulario_productos.html", idC=idC)
    else:
        return render_template("index.html")


@app.route("/Lista-Hombre")
def listaH():
    if validar():
        productos = controlador_productos.obtener_productos(1)
        return render_template("lista_productos.html",productos=productos)
    else:
        return render_template("index.html")


@app.route("/Moda-Hombre")
def modaH():
    productos = controlador_productos.obtener_productos(1)
    return render_template("moda_hombre.html",productos=productos)

#Mujer

@app.route("/Formulario-Mujer")
def formularioM():
    if validar():
        idC=2
        return render_template("Formulario_productos.html", idC=idC)
    else:
        return render_template("index.html")


@app.route("/Lista-Mujer")
def listaM():
    if validar():
        productos = controlador_productos.obtener_productos(2)
        return render_template("lista_productos.html",productos=productos)
    else:
        return render_template("index.html")


@app.route("/Moda-Mujer")
def modaM():
    productos = controlador_productos.obtener_productos(2)
    return render_template("moda_mujer.html",productos=productos)

#Niño

@app.route("/Formulario-Niño")
def formularioN():
    if validar():
        idC=3
        return render_template("Formulario_productos.html", idC=idC)
    else:
        return render_template("index.html")


@app.route("/Lista-Niño")
def listaN():
    if validar():
        productos = controlador_productos.obtener_productos(3)
        return render_template("lista_productos.html",productos=productos)
    else:
        return render_template("index.html")


@app.route("/Moda-Niños")
def modaN():
    productos = controlador_productos.obtener_productos(3)
    return render_template("moda-niños.html",productos=productos)

#Compra y Pedido

@app.route("/Carrito-Compras")
def carrito():
    if validar():
        productos = request.cookies.get("productos")
        if productos:
            array=[]
            sinStock=[]
            productos = json.loads(productos)
            for i in productos.keys():
                for j in productos[i]:
                    producto = controlador_productos.obtener_stock_por_id(i,j['talla'])
                    if producto[6] >= j['cantidad']:
                        subtotal = int(producto[2]) * int(j['cantidad'])
                        array.append(producto+(j['talla'],j['cantidad'],j['clave'],subtotal))
                    else:
                        sinStock.append(producto[1])
            print(array)
            return render_template("carrito_de_compras.html", array=array, sin=sinStock)
        return render_template("carrito_de_compras.html")
    else:
        return redirect("/Inicio")

@app.route("/Pago-Productos")
def pagoP():
    if validar():
        productos = request.cookies.get("productos")
        if productos:
            array=[]
            sinStock=[]
            productos = json.loads(productos)
            for i in productos.keys():
                for j in productos[i]:
                    producto = controlador_productos.obtener_stock_por_id(i,j['talla'])
                    if producto[6] >= j['cantidad']:
                        subtotal = int(producto[2]) * int(j['cantidad'])
                        array.append(producto+(j['talla'],j['cantidad'],j['clave'],subtotal))
                    else:
                        sinStock.append(producto[1])
            print(array)
            return render_template("pago_de_productos.html", array=array, sin=sinStock)
    return redirect("/Inicio")


@app.route("/Pago-Pedido")
def pagandoPedido():
    try:
        if validar():
            productos = request.cookies.get("productos")
            print(productos)
            detalle=False
            if productos:
                productos = json.loads(productos)
                username = request.cookies.get('username')
                user = controlador_usuarios.obtener_user_por_username(username)
                controlador_venta.crear_pedido(True,user[0])
                pedidoID = controlador_venta.obtener_pedido()
                subtotal = 0
                for i in productos.keys():
                    for j in productos[i]:
                        producto = controlador_productos.obtener_stock_por_id(i,j['talla'])
                        if producto[6] >= j['cantidad']:
                            detalle = True
                            productoID = producto[0]
                            cantidad = j['cantidad']
                            precio = producto[2]
                            subtotal = subtotal + float(float(precio) * float(cantidad))
                            print(producto)
                            controlador_stock.disminuir_stock(cantidad,producto[7],productoID)
                            controlador_venta.crear_detalle(precio,cantidad,productoID,pedidoID)
                if detalle:
                    controlador_venta.crear_subtotal_pedido(subtotal,pedidoID)
                else:
                    return redirect(request.refrrer)
                resp = make_response(redirect("/Inicio"))
                resp.set_cookie('productos', '', expires=0)
                return resp

        return redirect("/Inicio")
    except:
        return redirect("/Error")


##APIS DE CALZADO NO MOVER##

@app.route("/api_obtenerCalzado")
@jwt_required()
def api_obtenerCalzado():
    listaCalzados = list()
    rpta = dict()
    try:
        productos = controlador_productos.obtener_productos(4)
        for producto in productos:
            objCalzado = clase_calzado.clsCalzado(producto[0], producto[1], producto[3], producto[2], producto[4])
            listaCalzados.append(objCalzado.dicCalzado.copy())
        rpta["data"] = listaCalzados
        rpta["message"] = "Procesamiento correcto"
        rpta["code"] = 1
    except:
        rpta["data"] = dict()
        rpta["message"] = "Ocurrió un error interno"
        rpta["code"] = 0
    return jsonify(rpta)

@app.route("/api_actualizarProducto", methods = ["POST"])
@jwt_required()
def api_actualizarCalzado():
    rpta = dict()
    rpta["data"] = dict()
    try:
        id = request.json["id"]
        producto = controlador_productos.obtener_producto_por_id(id)
        nombre = request.json["nombre"]
        precio = request.json["precio"]
        descripcion = request.json["descripcion"]
        imagen = request.json["imagen"]
        if imagen == "":
            imagen = producto[4]
        controlador_productos.actualizar_producto(nombre,precio,descripcion,imagen,id)
        rpta["message"] = "Actualizacion correcta del disco"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno" + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_guardarProducto", methods=["POST"])
@jwt_required()
def api_guardarCalzado():
    rpta = dict()
    rpta["data"] = dict()
    try:
        nombre = request.json["nombre"]
        precio = request.json["precio"]
        descripcion = request.json["descripcion"]
        url = request.json.get('url')
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        archivo = Image.open(requests.get(url, stream=True).raw)
        if filename != '':
            ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            archivo.save(ruta_completa)
        categoria = request.json["categoria"]
        controlador_productos.insertar_producto(nombre, precio, descripcion, filename,categoria)
        controlador_stock.crear_stock(int(categoria))
        rpta["message"] = "Registro correcto del Calzado"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta

@app.route("/api_eliminarProducto", methods = ["POST"])
@jwt_required()
def api_eliminarCalzado():
    rpta = dict()
    rpta["data"] = dict()
    try:
        controlador_productos.eliminar_producto(request.json["id"])
        rpta["message"] = "Eliminacion correcta del Producto"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno" + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_obtenercategoria")
@jwt_required()
def api_obtenercategori():
    listacategoria = list()
    rpta = dict()
    try:
        categorias = controlador_categorias.obtener_categorias()
        for categoria in categorias:
            objcategoria = clase_categoria.clscategoria(categoria[0], categoria[1])
            listacategoria.append(objcategoria.diccategoria.copy())
        rpta["data"] = listacategoria
        rpta["message"] = "Procesamiento correcto"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0
    return jsonify(rpta)

@app.route("/api_actualizarcategorias", methods = ["POST"])
@jwt_required()
def api_actualizarcategoria():
    rpta = dict()
    rpta["data"] = dict()
    try:
        categoriaID = request.json["id"]
        nombre = request.json["nombre"]
        controlador_categorias.actualizar_categorias( nombre, categoriaID)
        rpta["message"] = "Actualizacion correcta de la categoria"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_guardarcategorias", methods=["POST"])
@jwt_required()
def api_guardarcategoria():
    rpta = dict()
    rpta["data"] = dict()
    try:
        nombre = request.json["nombre"]
        controlador_categorias.insertar_categorias( nombre)
        rpta["message"] = "Registro correcto de la categoria"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta

@app.route("/api_eliminarcategoria", methods = ["POST"])
@jwt_required()
def api_eliminarcategoria():
    rpta = dict()
    rpta["data"] = dict()
    try:
        controlador_categorias.eliminar_categorias(request.json["id"])
        rpta["message"] = "Eliminacion correcta de la categoria"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno" + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_obtenerstock")
@jwt_required()
def api_obtenerstock():
    listastock = list()
    rpta = dict()
    try:
        stock = controlador_stock_productos.obtener_stock()
        for s in stock:
            objstock = clase_stock.clsStock(s[0], s[1], s[2], s[3])
            listastock.append(objstock.dicstock.copy())
        rpta["data"] = listastock
        rpta["message"] = "Procesamiento correcto"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0
    return jsonify(rpta)

@app.route("/api_actualizarstock", methods=["POST"])
@jwt_required()
def api_actualizarstock():
    rpta = dict()
    rpta["data"] = dict()
    try:
        stockID = request.json["id"]
        cantidad = request.json["cantidad"]
        tallaID = request.json["tallaID"]
        productoID = request.json["productoID"]
        controlador_stock_productos.actualizar_stock(cantidad, tallaID, productoID, stockID)
        rpta["message"] = "Actualización correcta del stock"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_guardarstock", methods=["POST"])
@jwt_required()
def api_guardarstock():
    rpta = dict()
    rpta["data"] = dict()
    try:
        cantidad = request.json["cantidad"]
        tallaID = request.json["tallaID"]
        productoID = request.json["productoID"]
        controlador_stock_productos.insertar_stock(cantidad, tallaID, productoID)
        rpta["message"] = "Registro correcto del stock"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta

@app.route("/api_eliminarstock", methods=["POST"])
@jwt_required()
def api_eliminarstock():
    rpta = dict()
    rpta["data"] = dict()
    try:
        controlador_stock_productos.eliminar_stock(request.json["id"])
        rpta["message"] = "Eliminación correcta del stock"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_obtenerTallas")
@jwt_required()
def api_obtenerTallas():
    listaTallas = list()
    rpta = dict()
    try:
        Tallas = controlador_tallas.obtener_tallas()
        for Talla in Tallas:
            objTalla = clase_talla.clsTalla(Talla[0], Talla[1])
            listaTallas.append(objTalla.dicTalla.copy())
        rpta["data"] = listaTallas
        rpta["message"] = "Procesamiento correcto"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0
    return jsonify(rpta)

@app.route("/api_actualizarTalla", methods = ["POST"])
@jwt_required()
def api_actualizarTalla():
    rpta = dict()
    rpta["data"] = dict()
    try:
        TallaID = request.json["tallaid"]
        medida = request.json["medida"]
        controlador_tallas.actualizar_talla(medida,TallaID)
        rpta["message"] = "Actualizacion correcta de la Talla"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_guardarTalla", methods=["POST"])
@jwt_required()
def api_guardarTalla():
    rpta = dict()
    rpta["data"] = dict()
    try:
        medida = request.json["medida"]
        controlador_tallas.insertar_talla(medida)
        rpta["message"] = "Registro correcto de la Talla"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta

@app.route("/api_eliminarTalla", methods = ["POST"])
@jwt_required()
def api_eliminarTalla():
    rpta = dict()
    rpta["data"] = dict()
    try:
        controlador_tallas.eliminar_talla(request.json["tallaid"])
        rpta["message"] = "Eliminacion correcta de la Talla"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno" + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_obtenerUsuarios")
@jwt_required()
def api_obtenerUsuarios():
    listaUsuarios = list()
    rpta = dict()
    try:
        usuarios = controlador_usuarios.obtener_usuarios()
        for usuario in usuarios:
            objUsuario = clase_usuario.clsUsuario(usuario[0], usuario[1], usuario[3], usuario[2], usuario[4],usuario[5],usuario[6])
            listaUsuarios.append(objUsuario.dicUsuario.copy())
        rpta["data"] = listaUsuarios
        rpta["message"] = "Procesamiento correcto"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0
    return jsonify(rpta)

@app.route("/api_actualizarUsuario", methods = ["POST"])
@jwt_required()
def api_actualizarUsuario():
    rpta = dict()
    rpta["data"] = dict()
    try:
        usuarioID = request.json["id"]
        codigo = request.json["codigo"]
        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        rango = request.json["rango"]
        email = request.json["email"]
        fecha = request.json["fecha"]
        contraseña = request.json["contraseña"]
        controlador_usuarios.actualizar_usuario(codigo, nombre, apellido, rango,email,fecha,contraseña,usuarioID)
        rpta["message"] = "Actualizacion correcta del Usuario"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_guardarUsuario", methods=["POST"])
@jwt_required()
def api_guardarUsuario():
    rpta = dict()
    rpta["data"] = dict()
    try:
        codigo = request.json["codigo"]
        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        rango = request.json["rango"]
        email = request.json["email"]
        fecha = request.json["fecha"]
        contraseña = request.json["contraseña"]
        controlador_usuarios.insertar_usuario(codigo, nombre, apellido, rango,email,fecha,contraseña)
        rpta["message"] = "Registro correcto del Usuario"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta

@app.route("/api_eliminarUsuario", methods = ["POST"])
@jwt_required()
def api_eliminarUsuario():
    rpta = dict()
    rpta["data"] = dict()
    try:
        controlador_usuarios.eliminar_usuario(request.json["id"])
        rpta["message"] = "Eliminacion correcta del Usuario"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrio un error interno" + repr(e)
        rpta["code"] = 0

    return rpta

@app.route("/api_obtenerPedidos")
@jwt_required()
def api_obtenerPedidos():
    listaPedidos = []
    rpta = dict()
    try:
        pedidos = controlador_pedido.obtener_pedidos()
        for pedido in pedidos:
            objPedido = clase_pedido.clsPedido(pedido[0], pedido[1], pedido[2], pedido[3], pedido[4])
            listaPedidos.append(objPedido.dicPedido.copy())
        rpta["data"] = listaPedidos
        rpta["message"] = "Procesamiento correcto"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0
    return jsonify(rpta)

@app.route("/api_actualizarPedido", methods=["POST"])
@jwt_required()
def api_actualizarPedido():
    rpta = dict()
    rpta["data"] = dict()
    try:
        pedidoID = request.json["pedidoID"]
        fecha = request.json["fecha"]
        estado = request.json["estado"]
        subtotal = request.json["subtotal"]
        usuarioID = request.json["usuarioID"]
        controlador_pedido.actualizar_pedido(fecha, estado, subtotal, usuarioID, pedidoID)
        rpta["message"] = "Actualización correcta del Pedido"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta

@app.route("/api_guardarPedido", methods=["POST"])
@jwt_required()
def api_guardarPedido():
    rpta = dict()
    rpta["data"] = dict()
    try:
        fecha = request.json["fecha"]
        estado = request.json["estado"]
        subtotal = request.json["subtotal"]
        usuarioID = request.json["usuarioID"]
        controlador_pedido.insertar_pedido(fecha, estado, subtotal, usuarioID)
        rpta["message"] = "Registro correcto del Pedido"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta

@app.route("/api_eliminarPedido", methods=["POST"])
@jwt_required()
def api_eliminarPedido():
    rpta = dict()
    rpta["data"] = dict()
    try:
        controlador_pedido.eliminar_pedido(request.json["pedidoID"])
        rpta["message"] = "Eliminación correcta del Pedido"
        rpta["code"] = 1
    except Exception as e:
        rpta["message"] = "Ocurrió un error interno: " + repr(e)
        rpta["code"] = 0
    return rpta


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)


