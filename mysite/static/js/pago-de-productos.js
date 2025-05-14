document.addEventListener("DOMContentLoaded", function () {
    document.body.style.opacity = "1";
    var inputEnfocarPorDefecto = document.getElementById("num1").focus();
});

function cargarProductos() {
    //Obtengo el div al que le insertaré el producto
    var divContenedorProductos = document.getElementById("contenedor-productos");

    //Variable para almacenar el contenido HTML del div al que le insertaré los productos
    var registro = '';

    var total = 0;
    var costoEnvio = 15;

    //Recorro el local storage para obtener todos los productos agregados
    for (i = 0; i < localStorage.length; i++) {
        //Obtengo el producto almacenado en el local sotrage
        var clave = localStorage.key(i);
        if (!isNaN(clave) && clave !== "direccionCliente") {
            var itemClave = localStorage.getItem(clave);
            var objetoProductoJSON = JSON.parse(itemClave);

            //Obtengo los datos del producto
            var tituloProd = objetoProductoJSON.nombre;
            var tallaProd = objetoProductoJSON.talla;
            var rutaImagenProd = objetoProductoJSON.rutaImagen;
            var cantidadProd = objetoProductoJSON.cantidad;
            var precioProd = parseFloat(objetoProductoJSON.precio);
            var subtotalProd = parseFloat(objetoProductoJSON.subtotal);
            total += subtotalProd;

            registro += '<div class="card-producto"><div class="cont-producto"><img class="img-card-producto" src="' + rutaImagenProd + '" alt=""><div class="cont-descr-producto"><h6 class="titulo-producto"><b>' + tituloProd + '</b></h6><h6><b>Talla: </b>' + tallaProd + '</h6><h6><b>Precio: </b>S/. ' + precioProd + '</h6><h6><b>Cantidad: </b>' + cantidadProd + '</h6><div><b>Subtotal producto: </b>S/. ' + subtotalProd + '</div></div></div></div>';
        }
    }

    total = parseFloat(total + costoEnvio).toFixed(2);
    var subtotalProductos = parseFloat(total - costoEnvio).toFixed(2);

    divContenedorProductos.innerHTML = registro + '<div class="subtotal-costo-envio-total"><h6><b>Subtotal productos: </b></h6><h6>S/. ' + subtotalProductos + '</h6></div><div class="subtotal-costo-envio-total"><h6><b>Costo de envío: </b></h6><h6>S/. ' + parseFloat(costoEnvio).toFixed(2) + '</h6></div><div class="subtotal-costo-envio-total"><h6><b>Total a pagar: </b></h6><h6>S/. ' + total + '</h6></div>';
}

//
function mostrarResumenPedido() {
    var numtarj1 = document.getElementById("num1").value;
    var numtarj2 = document.getElementById("num2").value;
    var numtarj3 = document.getElementById("num3").value;
    var numtarj4 = document.getElementById("num4").value;
    var fectarj1 = document.getElementById("fec1").value;
    var fectarj2 = document.getElementById("fec2").value;
    var cvvtarj = document.getElementById("cvv").value;

    if (numtarj1.trim() === '' || numtarj2.trim() === '' || numtarj3.trim() === '' || numtarj4.trim() === '' || fectarj1.trim() === '' || fectarj2.trim() === '' || cvvtarj.trim() === '') {
        alert("Por favor, ingrese sus datos para continuar");
    } else {
        mostrarValoresDireccionCliente();
        document.getElementById("contenedor-mostrar-hay-productos").style.display = "flex";
    }
}

//Setear los campos de dirección ingresada
function mostrarValoresDireccionCliente() {
    var numTarj1 = document.getElementById("num1").value;
    var numTarj2 = document.getElementById("num2").value;
    var numTarj3 = document.getElementById("num3").value;
    var numTarj4 = document.getElementById("num4").value;

    // Obtener el valor asociado a la clave "direccionCliente"
    var claveDireccion = localStorage.getItem("direccionCliente");

    // Verificar si la clave existe en localStorage antes de intentar parsear el JSON
    if (claveDireccion) {
        var objetoJSON = JSON.parse(claveDireccion);

        var valCalle = objetoJSON.calle;
        var valPisoOpc = objetoJSON.depapisoetc;
        var valDepart = formatoTitulo(objetoJSON.dpto);
        var valProv = formatoTitulo(objetoJSON.prov);
        var valDist = formatoTitulo(objetoJSON.dist);

        // Resto del código para utilizar los valores obtenidos...
    } else {
        console.log("La clave 'direccionCliente' no existe en localStorage.");
    }

    var contenedorDireccion = document.getElementById("contenedor-direccion-envio");
    var contenedorTarjeta = document.getElementById("contenedor-tarjeta");

    if (valPisoOpc.trim() === "") {
        contenedorDireccion.innerHTML = '<h6><b>Dirección de entrega: </b>' + valCalle + ', ' + valDist + ', ' + valProv + ', ' + valDepart + '</h6>';
        contenedorTarjeta.innerHTML = '<h6><b>Tarjeta: </b></h6><h6>VISA N° ' + numTarj1 + ' - ' + numTarj2 + ' - ' + numTarj3 + ' - ' + numTarj4 + '</h6>';
    } else {
        contenedorDireccion.innerHTML = '<h6><b>Dirección de entrega: </b>' + valCalle + ', ' + valPisoOpc + ', ' + valDist + ', ' + valProv + ', ' + valDepart + '</h6>';
        contenedorTarjeta.innerHTML = '<h6><b>Tarjeta: </b></h6><h6>VISA N° ' + numTarj1 + ' - ' + numTarj2 + ' - ' + numTarj3 + ' - ' + numTarj4 + '</h6>';
    }
}


// Función para convertir a formato de título
function formatoTitulo(cadena) {
    return cadena.charAt(0).toUpperCase() + cadena.slice(1).toLowerCase();
}


//Cambiar color de los botones
function cambiarColor(botonClicado) {
    var botones = document.getElementsByClassName("btn-medio-pago");
    for (var i = 0; i < botones.length; i++) {
        botones[i].style.backgroundColor = "#ebebeb";
    }
    botonClicado.style.backgroundColor = "#917c04";
}

//Validar checkboxs
function manejarCheckbox(checkboxClicado) {
    var checkboxes = document.querySelectorAll('.form-check-input');

    // Desmarcar todos los checkboxes
    checkboxes.forEach(function (checkbox) {
        if (checkbox !== checkboxClicado) {
            checkbox.checked = false;
        }
    });
}


//Validar campos de números, fechas y cvv de tarjeta
$(document).ready(function () {
    $('#num1').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 4) {
            $(this).val(inputValue.slice(0, 4).replace(/[^0-9+]/g, ''));
        }
    });

    $('#num2').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 4) {
            $(this).val(inputValue.slice(0, 4).replace(/[^0-9+]/g, ''));
        }
    });

    $('#num3').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 4) {
            $(this).val(inputValue.slice(0, 4).replace(/[^0-9+]/g, ''));
        }
    });

    $('#num4').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 4) {
            $(this).val(inputValue.slice(0, 4).replace(/[^0-9+]/g, ''));
        }
    });

    $('#fec1').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 2) {
            $(this).val(inputValue.slice(0, 2).replace(/[^0-9+]/g, ''));
        }
    });

    $('#fec2').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 2) {
            $(this).val(inputValue.slice(0, 2).replace(/[^0-9+]/g, ''));
        }
    });

    $('#cvv').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 3) {
            $(this).val(inputValue.slice(0, 3).replace(/[^0-9+]/g, ''));
        }
    });

    $('#input-dni-cliente-pago').on('input', function () {
        var inputValue = $(this).val();
        if (/[^0-9+]/.test(inputValue) || inputValue.length > 8) {
            $(this).val(inputValue.slice(0, 8).replace(/[^0-9+]/g, ''));
        }
    });
});

//Función para cerrar la ventana de pago realizado (limpia todos los items que se hayan comprado)
function cerrarVentanaPagoRealizado() {
    var ventanaPagoRealizado = document.getElementById("cont-pago-realizado");
    ventanaPagoRealizado.style.display = "none";
    window.open('/Inicio', '_self');
    // localStorage.clear();
}

//Función para ir a la página de inicio(también limpiar los items en el local storage)
function irPaginaDeInicio() {
    window.open("Inicio");

}

function abrirVentanaModalPagoConfirmado() {
    var chckbox1 = document.getElementById("chckbox-recibire-yo");
    var chckbox2 = document.getElementById("chckbox-recibira-otra-persona");
    var dniReceptorPedido = document.getElementById("input-dni-cliente-pago").value;
    var nomApeReceptorPedido = document.getElementById("input-dni-nomApe-cliente").value;

    if ((!chckbox1.checked || !chckbox2.checked) && dniReceptorPedido.trim() === '' && nomApeReceptorPedido.trim() === '') {
        alert("Por favor, complete todos sus datos");
    } else {
        const localStorageData = { ...localStorage };
        localStorage.clear();
        var ventanaPagoRealizado = document.getElementById("cont-pago-realizado");
        ventanaPagoRealizado.style.display = "flex";
    }
}

function generarCookies(){
    var productos = {}
    for (i = 0; i < localStorage.length; i++) {
        var clave = localStorage.key(i);
        var validar = Number(clave)
        if (Number.isInteger(validar)) {
            var itemClave = localStorage.getItem(clave);
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

//Pasar de un campo a otro sin necesidad de hacer tab o click en él
function checkInput(input, nextInputID) {
    var inputValueLength = input.value.length;

    if (inputValueLength === input.maxLength) {
        var nextInput = document.getElementById(nextInputID);
        if (nextInput) {
            nextInput.focus();
        }
    }
}