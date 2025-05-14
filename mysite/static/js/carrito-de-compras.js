// Se ejecuta al abrir la página
document.addEventListener("DOMContentLoaded", function () {
    var indicadorHayProductos = Object.keys(localStorage).filter(clave => !isNaN(clave)).length;
    if (indicadorHayProductos === 0) {
        mostrarDivNoHayProductos();
        document.getElementById("titulo-carrito-de-compras").remove();
    } else {
        mostrarDivHayProductos();
    }
});

//Función que muestra los productos en el carrito de compras
function mostrarDivHayProductos() {
    var contenedorHayProductos = document.getElementById("contenedor-mostrar-hay-productos");
    var contenedorNoHayProductos = document.getElementById("contenedor-mostrar-no-hay-productos");
    contenedorHayProductos.style.display = "block";
    contenedorNoHayProductos.style.display = "none";
}

//Función que muestra una advertencia de que no hay productos agregados al carrito de compras
function mostrarDivNoHayProductos() {
    var contenedorHayProductos = document.getElementById("contenedor-mostrar-hay-productos");
    var contenedorNoHayProductos = document.getElementById("contenedor-mostrar-no-hay-productos");
    contenedorHayProductos.style.display = "none";
    contenedorNoHayProductos.style.display = "flex";
}


function cargarProductos() {
    //Obtengo el div al que le insertaré el producto
    var divContenedorProductos = document.getElementById("contenedor-productos");

    //Variable para almacenar el contenido HTML del div al que le insertaré los productos
    var registro = '';

    var id = {};

    cantidadGeneral = 0;

    //Recorro el local storage para obtener todos los productos agregados
    for (i = 0; i < localStorage.length; i++) {
        //Obtengo el producto almacenado en el local sotrage
        var clave = localStorage.key(i);
        var validar = Number(clave)
        if (Number.isInteger(validar)) {
            var itemClave = localStorage.getItem(clave);
            var objetoProductoJSON = JSON.parse(itemClave);
            var productoID = objetoProductoJSON.id;
            var tallaProd = objetoProductoJSON.talla;
            var cantidadProd = objetoProductoJSON.cantidad;
            var tituloProd = objetoProductoJSON.nombre;
            var rutaImagenProd = objetoProductoJSON.rutaImagen;
            var precioProd = parseFloat(objetoProductoJSON.precio);
            var subtotalProd = parseFloat(objetoProductoJSON.subtotal);

            if (!id[productoID]) {
                //Obtengo los datos del producto
                registro += '<div class="card-producto"><div class="cont-producto"><p class="identificador-producto">' + clave +
                    '</p><p hidden id="idP" >' + productoID + '</p><img class="img-card-producto" src="' + rutaImagenProd +
                    '" alt=""><div class="cont-descr-producto"><h6 class="titulo-producto"><b>' + tituloProd +
                    '</b></h6><h6 id="talla"><b>Talla: </b>' + tallaProd + '</h6><h6><b>Precio: </b>S/. ' + precioProd +
                    '</h6><h6 id="cantidad"><b>Cantidad: </b>' + cantidadProd + '</h6><div><b>Subtotal producto: </b>S/. ' + subtotalProd +
                    '</div></div><button id="btn-eliminar-producto" onclick="eliminarProductoDelCarrito()">Eliminar</button></div></div>';

                id[productoID] = [];
                id[productoID].push(tallaProd);

            }
            else {
                var index = id[productoID].indexOf(tallaProd);
                if (index == -1) {
                    id[productoID].push(tallaProd);
                    registro += '<div class="card-producto"><div class="cont-producto"><p class="identificador-producto">' + clave +
                        '</p><p hidden id="idP" >' + productoID + '</p><img class="img-card-producto" src="' + rutaImagenProd +
                        '" alt=""><div class="cont-descr-producto"><h6 class="titulo-producto"><b>' + tituloProd +
                        '</b></h6><h6 id="talla"><b>Talla: </b>' + tallaProd + '</h6><h6><b>Precio: </b>S/. ' + precioProd +
                        '</h6><h6 id="cantidad"><b>Cantidad: </b>' + cantidadProd + '</h6><div><b>Subtotal producto: </b>S/. ' + subtotalProd +
                        '</div></div><button id="btn-eliminar-producto" onclick="eliminarProductoDelCarrito()">Eliminar</button></div></div>';
                }
                else{
                        var items = document.querySelectorAll('#idP');
                        console.log('Items:', items);
                        items.forEach(item => {
                            var identificador = item.textContent;
                            console.log('Numero de ID', identificador);
                            if (identificador == productoID) {
                                var nodo = item.parentNode;
                                var tallaHijo = nodo.querySelector('#talla').lastChild.textContent;
                                console.log(tallaHijo);
                                if (tallaHijo == tallaProd) {
                                    var hijo = nodo.querySelector('#cantidad').lastChild;
                                    var cantidad = nodo.querySelector('#cantidad').lastChild.textContent;
                                    console.log('Cantidad del Hijo', cantidad)
                                    var cantidadActual = parseInt(cantidad) + parseInt(cantidadProd);
                                    console.log('Cantidad de la suma', cantidadActual);
                                    hijo.textContent = cantidadActual;
                                }
                            }
                        });
                }
            }


        }
    }

    var cantidadProductos = 0;

    for (let i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        var validar = Number(key)
        if (Number.isInteger(validar)) {
            cantidadProductos++;
        }
    }

    if (cantidadProductos > 1) {
        divContenedorProductos.innerHTML = registro + '<div class="cont-editar-pedido--tienes-n-productos"><label id="lbl-tienes-n-prod" for=""><i>Tienes <b><u>' + cantidadProductos + ' productos</u></b></i></label></div>';
    } else {
        divContenedorProductos.innerHTML = registro + '<div class="cont-editar-pedido--tienes-n-productos"><label id="lbl-tienes-n-prod" for=""><i>Tienes <b><u>' + cantidadProductos + ' producto</u></b></i></label></div>';
    }

    // for (i = 0; i < localStorage.length; i++) {
    //     //Obtengo el producto almacenado en el local sotrage
    //     var clave = localStorage.key(i);

    //     if (clave !== "direccionCliente") {
    //         console.log('Clave:', clave)
    //         var itemClave = localStorage.getItem(clave);
    //         var objetoProductoJSON = JSON.parse(itemClave);
    //         var productoID = objetoProductoJSON.id;
    //         var talla = objetoProductoJSON.talla;
    //         if (id[productoID] && id[productoID].includes(talla)) {
    //             var items = document.querySelectorAll('.idP')
    //             console.log('Items:', items)
    //             var cantidadProd = objetoProductoJSON.cantidad;
    //             items.forEach(item => {
    //                 var identificador = item.textContent;
    //                 console.log('Numero de ID', identificador);
    //                 if (identificador == productoID) {
    //                     var nodo = item.parentNode;
    //                     var tallaHijo = nodo.querySelector('#talla').lastChild.textContent;
    //                     console.log(tallaHijo)
    //                     if (tallaHijo == tallaProd) {
    //                         var hijo = nodo.querySelector('#cantidad').lastChild;
    //                         var cantidad = nodo.querySelector('#cantidad').lastChild.textContent;
    //                         console.log('Cantidad del Hijo', cantidad)
    //                         var cantidadActual = parseInt(cantidad) + parseInt(cantidadProd);
    //                         console.log('Cantidad de la suma', cantidadActual)
    //                         hijo.textContent = cantidadActual;
    //                     }
    //                 }
    //             });
    //         }
    //     }
    // }

}

//Función para eliminar un producto del carrito de compras
function eliminarProductoDelCarrito() {

    var identificadorProducto = event.target.parentElement.querySelector('.identificador-producto').innerText;
    console.log(identificadorProducto)
    // Elimina el producto del local storage
    localStorage.removeItem(identificadorProducto);

    // Actualiza la interfaz de usuario
    var indicadorHayProductos = Object.keys(localStorage).filter(clave => !isNaN(clave)).length;
    if (indicadorHayProductos === 0) {
        window.open("/Carrito-Compras", "_self");
    } else {
        generarCookies();
        location.reload();
    }
}

function generarCookies(){
    var productos = {}
    for (i = 0; i < localStorage.length; i++) {
        var clave = localStorage.key(i);
        var validar = Number(clave)
        if (Number.isInteger(validar)) {
            var itemClave = localStorage.getItem(clave);
            console.log('Clave: ', clave)
            console.log('Validar: ', validar)
            var objetoProductoJSON = JSON.parse(itemClave);
            var productoID = objetoProductoJSON.id;
            var tallaProd = objetoProductoJSON.talla;
            var cantidadProd = objetoProductoJSON.cantidad;

            if (!productos[productoID]) {
                productos[productoID] = [];
            }

            // Buscar si ya existe la talla en el array del producto
            var tallaExiste = false;
            for (var j = 0; j < productos[productoID].length; j++) {
                if (productos[productoID][j].talla === tallaProd) {
                    productos[productoID][j].cantidad += cantidadProd;
                    tallaExiste = true;
                    break;
                }
            }

            // Si la talla no existe, agregar un nuevo objeto con talla y cantidad
            if (!tallaExiste) {
                productos[productoID].push({ talla: tallaProd, cantidad: cantidadProd, clave: validar });
            }
        }
    }
    document.cookie = "productos=" + JSON.stringify(productos) + ";" + "expires=Session;path=/";
}

function irPaginaPagoDeProductos() {
    var valorCboBoxDep = document.getElementById("cbobox-departamento").value;
    var valorCboBoxProv = document.getElementById("cbobox-provincia").value;
    var valorCboBoxDist = document.getElementById("cbobox-distrito").value;
    var valorDireccion = document.getElementById("text-avenida-calle-jiron").value;

    if (
        valorCboBoxDep.trim() === "" ||
        valorCboBoxProv.trim() === "" ||
        valorCboBoxDist.trim() === "" ||
        valorDireccion.trim() === ""
    ) {
        alert("Por favor, ingrese una dirección válida");
    } else {
        guardarDatosCliente();
        window.location.href = "/Pago-Productos";
    }
}

//Función para obtener los datos de la dirección del cliente
function guardarDatosCliente() {
    var valorCboBoxDep = document.getElementById("cbobox-departamento").value;
    var valorCboBoxProv = document.getElementById("cbobox-provincia").value;
    var valorCboBoxDist = document.getElementById("cbobox-distrito").value;
    var valorCalle = document.getElementById("text-avenida-calle-jiron").value;
    var valorDptoOpcional = document.getElementById("text-dpto-int").value;

    var keyDireccion = 'direccionCliente';

    var datosDireccion = {
        dpto: valorCboBoxDep,
        prov: valorCboBoxProv,
        dist: valorCboBoxDist,
        calle: valorCalle,
        depapisoetc: valorDptoOpcional
    };

    localStorage.setItem(keyDireccion, JSON.stringify(datosDireccion));
}


//Agregar provincias dependiendo el departamento seleccionado
function actualizarProvincias() {
    var departamentoSeleccionado = document.getElementById("cbobox-departamento").value;

    var comboProvincias = document.getElementById("cbobox-provincia");

    comboProvincias.innerHTML = '';

    if (departamentoSeleccionado === "lambayeque") {
        agregarOpcionProvincias(comboProvincias, "chiclayo", "Chiclayo");
    } else if (departamentoSeleccionado === "lima") {
        agregarOpcionProvincias(comboProvincias, "lima", "Lima");
    }
    actualizarDistritos();
}

function agregarOpcionProvincias(selectElement, value, text) {
    var opcion = document.createElement("option");
    opcion.value = value;
    opcion.text = text;
    selectElement.add(opcion);
}


//Agregar distritos dependiendo la pronvincia seleccionada
function actualizarDistritos() {
    var provinciaSeleccionada = document.getElementById("cbobox-provincia").value;

    var comboDistritos = document.getElementById("cbobox-distrito");

    comboDistritos.innerHTML = '';

    if (provinciaSeleccionada === "chiclayo") {
        agregarOpcionDistritos(comboDistritos, "pimentel", "Pimentel");
        agregarOpcionDistritos(comboDistritos, "lagunas", "Lagunas");
        agregarOpcionDistritos(comboDistritos, "monsefu", "Monsefú");
        agregarOpcionDistritos(comboDistritos, "eten", "Eten");
        agregarOpcionDistritos(comboDistritos, "puertoeten", "Puerto Eten");
        agregarOpcionDistritos(comboDistritos, "cayaltí", "Cayaltí");
        agregarOpcionDistritos(comboDistritos, "chiclayo", "Chiclayo");
        agregarOpcionDistritos(comboDistritos, "la victoria", "La Victoria");
    } else if (provinciaSeleccionada === "lima") {
        agregarOpcionDistritos(comboDistritos, "breña", "Breña");
        agregarOpcionDistritos(comboDistritos, "sanisidro", "San Isidro");
        agregarOpcionDistritos(comboDistritos, "lamolina", "La Molina");
        agregarOpcionDistritos(comboDistritos, "santiagodesurco", "Santiago de Surco");
        agregarOpcionDistritos(comboDistritos, "lince", "Lince");
        agregarOpcionDistritos(comboDistritos, "surquillo", "Surquillo");
        agregarOpcionDistritos(comboDistritos, "chosica", "Chosica");
        agregarOpcionDistritos(comboDistritos, "comas", "Comas");
    }
}

function agregarOpcionDistritos(selectElement, value, text) {
    var opcion = document.createElement("option");
    opcion.value = value;
    opcion.text = text;
    selectElement.add(opcion);
}