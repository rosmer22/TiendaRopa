CREATE TABLE `categorias` (
  `categoriaID` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`categoriaID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `detalle_pedido` (
  `detalleID` int NOT NULL AUTO_INCREMENT,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `productoID` int DEFAULT NULL,
  `pedidoID` int DEFAULT NULL,
  PRIMARY KEY (`detalleID`),
  KEY `productoID` (`productoID`),
  KEY `pedidoID` (`pedidoID`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`productoID`) REFERENCES `productos` (`productoID`),
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`pedidoID`) REFERENCES `pedido` (`pedidoID`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `pedido` (
  `pedidoID` int NOT NULL AUTO_INCREMENT,
  `fecha` date DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `usuarioID` int DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  `igv` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`pedidoID`),
  KEY `usuarioID` (`usuarioID`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`usuarioID`) REFERENCES `usuarios` (`usuarioID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `productos` (
  `productoID` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `descripcion` text,
  `imagen` varchar(255) DEFAULT NULL,
  `categoriaID` int DEFAULT NULL,
  PRIMARY KEY (`productoID`),
  KEY `categoriaID` (`categoriaID`),
  CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`categoriaID`) REFERENCES `categorias` (`categoriaID`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `stock_productos` (
  `stockID` int NOT NULL AUTO_INCREMENT,
  `cantidad` int DEFAULT NULL,
  `tallaID` int DEFAULT NULL,
  `productoID` int DEFAULT NULL,
  PRIMARY KEY (`stockID`),
  KEY `tallaID` (`tallaID`),
  KEY `productoID` (`productoID`),
  CONSTRAINT `stock_productos_ibfk_1` FOREIGN KEY (`tallaID`) REFERENCES `tallas` (`tallaID`),
  CONSTRAINT `stock_productos_ibfk_2` FOREIGN KEY (`productoID`) REFERENCES `productos` (`productoID`)
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `tallas` (
  `tallaID` int NOT NULL AUTO_INCREMENT,
  `medida` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`tallaID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `usuarios` (
  `usuarioID` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(20) DEFAULT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `rango` int NOT NULL,
  `email` varchar(100) NOT NULL,
  `fecha` date DEFAULT NULL,
  `contraseña` varchar(255) NOT NULL,
  `token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`usuarioID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;

