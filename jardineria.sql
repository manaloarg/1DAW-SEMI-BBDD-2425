DROP DATABASE IF EXISTS jardineria;
USE jardineria;
CREATE TABLE Oficinas (
  CodigoOficina varchar(10) NOT NULL,
  Ciudad varchar(30) NOT NULL,
  Pais varchar(50) NOT NULL,
  Region varchar(50) DEFAULT NULL,
  CodigoPostal varchar(10) NOT NULL,
  Telefono varchar(20) NOT NULL,
  LineaDireccion1 varchar(50) NOT NULL,
  LineaDireccion2 varchar(50) DEFAULT NULL,
  PRIMARY KEY (CodigoOficina)
) engine=innodb;

CREATE TABLE Empleados (
  CodigoEmpleado integer NOT NULL,
  Nombre varchar(50) NOT NULL,
  Apellido1 varchar(50) NOT NULL,
  Apellido2 varchar(50) DEFAULT NULL,
  Extension varchar(10) NOT NULL,
  Email varchar(100) NOT NULL,
  CodigoOficina varchar(10) NOT NULL,
  CodigoJefe integer DEFAULT NULL,
  Puesto varchar(50) DEFAULT NULL,
  PRIMARY KEY (CodigoEmpleado),
  CONSTRAINT Empleados_OficinasFK FOREIGN KEY (CodigoOficina) REFERENCES Oficinas (CodigoOficina),
  CONSTRAINT Empleados_EmpleadosFK FOREIGN KEY (CodigoJefe) REFERENCES Empleados (CodigoEmpleado)
) engine=innodb;

CREATE TABLE GamasProductos (
  Gama varchar(50) NOT NULL,
  DescripcionTexto text,
  DescripcionHTML text,
  Imagen blob,
  PRIMARY KEY (Gama)
) engine=innodb;

CREATE TABLE Clientes (
  CodigoCliente integer NOT NULL,
  NombreCliente varchar(50) NOT NULL,
  NombreContacto varchar(30) DEFAULT NULL,
  ApellidoContacto varchar(30) DEFAULT NULL,
  Telefono varchar(15) NOT NULL,
  Fax varchar(15) NOT NULL,
  LineaDireccion1 varchar(50) NOT NULL,
  LineaDireccion2 varchar(50) DEFAULT NULL,
  Ciudad varchar(50) NOT NULL,
  Region varchar(50) DEFAULT NULL,
  Pais varchar(50) DEFAULT NULL,
  CodigoPostal varchar(10) DEFAULT NULL,
  CodigoEmpleadoRepVentas integer DEFAULT NULL,
  LimiteCredito numeric(15,2) DEFAULT NULL,
  PRIMARY KEY (CodigoCliente),
  CONSTRAINT Clientes_EmpleadosFK FOREIGN KEY (CodigoEmpleadoRepVentas) REFERENCES Empleados (CodigoEmpleado)
) engine=innodb;

CREATE TABLE Pedidos (
  CodigoPedido integer NOT NULL,
  FechaPedido date NOT NULL,
  FechaEsperada date NOT NULL,
  FechaEntrega date DEFAULT NULL,
  Estado varchar(15) NOT NULL,
  Comentarios text,
  CodigoCliente integer NOT NULL,
  PRIMARY KEY (CodigoPedido),
  CONSTRAINT Pedidos_Cliente FOREIGN KEY (CodigoCliente) REFERENCES Clientes (CodigoCliente)
) engine=innodb;

CREATE TABLE Productos (
  CodigoProducto varchar(15) NOT NULL,
  Nombre varchar(70) NOT NULL,
  Gama varchar(50) NOT NULL,
  Dimensiones varchar(25) NULL,
  Proveedor varchar(50) DEFAULT NULL,
  Descripcion text NULL,
  CantidadEnStock smallint NOT NULL,
  PrecioVenta numeric(15,2) NOT NULL,
  PrecioProveedor numeric(15,2) DEFAULT NULL,
  PRIMARY KEY (CodigoProducto),
  CONSTRAINT Productos_gamaFK FOREIGN KEY (Gama) REFERENCES GamasProductos (Gama)
) engine=innodb;

CREATE TABLE DetallePedidos (
  CodigoPedido integer NOT NULL,
  CodigoProducto varchar(15) NOT NULL,
  Cantidad integer NOT NULL,
  PrecioUnidad numeric(15,2) NOT NULL,
  NumeroLinea smallint NOT NULL,
  PRIMARY KEY (CodigoPedido,CodigoProducto),
  CONSTRAINT DetallePedidos_PedidoFK FOREIGN KEY (CodigoPedido) REFERENCES Pedidos (CodigoPedido),
  CONSTRAINT DetallePedidos_ProductoFK FOREIGN KEY (CodigoProducto) REFERENCES Productos (CodigoProducto)
)engine=innodb;

CREATE TABLE Pagos (
  CodigoCliente integer NOT NULL,
  FormaPago varchar(40) NOT NULL,
  IDTransaccion varchar(50) NOT NULL,
  FechaPago date NOT NULL,
  Cantidad numeric(15,2) NOT NULL,
  PRIMARY KEY (CodigoCliente,IDTransaccion),
  CONSTRAINT Pagos_clienteFK FOREIGN KEY (CodigoCliente) REFERENCES Clientes (CodigoCliente)
) engine=innodb;




