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
    
    expected_primary_keys = {
        "Oficinas": {"CodigoOficina"},
        "Empleados": {"CodigoEmpleado"},
        "GamasProductos": {"Gama"},
        "Clientes": {"CodigoCliente"},
        "Pedidos": {"CodigoPedido"},
        "Productos": {"CodigoProducto"},
        "DetallePedidos": {"CodigoPedido", "CodigoProducto"},
        "Pagos": {"CodigoCliente", "IDTransaccion"},
    }
    
    expected_foreign_keys = {
        "Empleados": {"CodigoOficina": "Oficinas", "CodigoJefe": "Empleados"},
        "Clientes": {"CodigoEmpleadoRepVentas": "Empleados"},
        "Pedidos": {"CodigoCliente": "Clientes"},
        "Productos": {"Gama": "GamasProductos"},
        "DetallePedidos": {"CodigoPedido": "Pedidos", "CodigoProducto": "Productos"},
        "Pagos": {"CodigoCliente": "Clientes"},
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
    
    # Verificar claves primarias
    for table, expected_pk in expected_primary_keys.items():
        cursor.execute(f"SHOW KEYS FROM `{table}` WHERE Key_name = 'PRIMARY';")
        found_pk = {row[4] for row in cursor.fetchall()}
        assert found_pk == expected_pk, f"ERROR en {table}: clave primaria esperada {expected_pk}, pero encontrada {found_pk}"
    
    # Verificar claves foráneas
    for table, expected_fks in expected_foreign_keys.items():
        cursor.execute(f"SELECT COLUMN_NAME, REFERENCED_TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table}' AND REFERENCED_TABLE_NAME IS NOT NULL;")
        found_fks = {row[0]: row[1] for row in cursor.fetchall()}
        assert found_fks == expected_fks, f"ERROR en {table}: claves foráneas esperadas {expected_fks}, pero encontradas {found_fks}"
    
    print("✅ La estructura de la base de datos, claves primarias y claves foráneas son correctas.")
    conn.close()

if __name__ == "__main__":
    validate_database()
