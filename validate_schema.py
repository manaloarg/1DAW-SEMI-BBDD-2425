import mysql.connector

def validate_database():
    expected_tables = {
        "Oficinas": {"CodigoOficina", "Ciudad", "Pais", "Region", "CodigoPostal", "Telefono", "LineaDireccion1", "LineaDireccion2"},
        "Empleados": {"CodigoEmpleado", "Nombre", "Apellido1", "Apellido2", "Extension", "Email", "CodigoOficina", "CodigoJefe", "Puesto"},
        "GamasProductos": {"Gama", "DescripcionTexto", "DescripcionHTML", "Imagen"},
        "Clientes": {"CodigoCliente", "NombreCliente", "NombreContacto", "ApellidoContacto", "Telefono", "Fax", "LineaDireccion1", "LineaDireccion2", "Ciudad", "Region", "Pais", "CodigoPostal", "CodigoEmpleadoRepVentas", "LimiteCredito"},
        "Pedidos": {"CodigoPedido", "FechaPedido", "FechaEsperada", "FechaEntrega", "Estado", "Comentarios", "CodigoCliente"},
        "Productos": {"CodigoProducto", "Nombre", "Gama", "Dimensiones", "Proveedor", "Descripcion", "CantidadEnStock", "PrecioVenta", "PrecioProveedor"},
        "DetallePedidos": {"CodigoPedido", "CodigoProducto", "Cantidad", "PrecioUnidad", "NumeroLinea"},
        "Pagos": {"CodigoCliente", "FormaPago", "IDTransaccion", "FechaPago", "Cantidad"},
    }
    
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="jardineria"
    )
    cursor = conn.cursor()
    
    # Verificar que existen las tablas esperadas
    cursor.execute("SHOW TABLES;")
    found_tables = {table[0] for table in cursor.fetchall()}
    assert found_tables == set(expected_tables.keys()), f"ERROR: Tablas esperadas {set(expected_tables.keys())} pero encontradas {found_tables}"
    
    # Verificar las columnas de cada tabla
    for table, expected_columns in expected_tables.items():
        cursor.execute(f"DESCRIBE `{table}`;")
        found_columns = {col[0] for col in cursor.fetchall()}
        assert found_columns == expected_columns, f"ERROR en {table}: columnas esperadas {expected_columns}, pero encontradas {found_columns}"
    
    print("✅ La estructura de la base de datos es correcta.")
    conn.close()

if __name__ == "__main__":
    validate_database()
