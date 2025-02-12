import mysql.connector

def validate_database():
    expected_tables = {
        "oficina": {"codigo_oficina", "ciudad", "pais", "region", "codigo_postal", "telefono", "linea_direccion1", "linea_direccion2"},
        "empleado": {"codigo_empleado", "nombre", "apellido1", "apellido2", "extension", "email", "codigo_oficina", "codigo_jefe", "puesto"},
        "gama_producto": {"gama", "descripcion_texto", "descripcion_html", "imagen"},
        "cliente": {"codigo_cliente", "nombre_cliente", "nombre_contacto", "apellido_contacto", "telefono", "fax", "linea_direccion1", "linea_direccion2", "ciudad", "region", "pais", "codigo_postal", "codigo_empleado_rep_ventas", "limite_credito"},
        "pedido": {"codigo_pedido", "fecha_pedido", "fecha_esperada", "fecha_entrega", "estado", "comentarios", "codigo_cliente"},
        "producto": {"codigo_producto", "nombre", "gama", "dimensiones", "proveedor", "descripcion", "cantidad_en_stock", "precio_venta", "precio_proveedor"},
        "detalle_pedido": {"codigo_pedido", "codigo_producto", "cantidad", "precio_unidad", "numero_linea"},
        "pago": {"codigo_cliente", "forma_pago", "id_transaccion", "fecha_pago", "total"},
    }
    
    expected_primary_keys = {
        "oficina": {"codigo_oficina"},
        "empleado": {"codigo_empleado"},
        "gama_producto": {"gama"},
        "cliente": {"codigo_cliente"},
        "pedido": {"codigo_pedido"},
        "producto": {"codigo_producto"},
        "detalle_pedido": {"codigo_pedido", "codigo_producto"},
        "pago": {"codigo_cliente", "id_transaccion"},
    }
    
    expected_foreign_keys = {
        "empleado": {"codigo_oficina": "oficina", "codigo_jefe": "empleado"},
        "cliente": {"codigo_empleado_rep_ventas": "empleado"},
        "pedido": {"codigo_cliente": "cliente"},
        "producto": {"gama": "gama_producto"},
        "detalle_pedido": {"codigo_pedido": "pedido", "codigo_producto": "producto"},
        "pago": {"codigo_cliente": "cliente"},
    }
    
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="jardineria"
    )
    cursor = conn.cursor()
    
    report = []
    
    # Verificar que existen las tablas esperadas
    cursor.execute("SHOW TABLES;")
    found_tables = {table[0] for table in cursor.fetchall()}
    if found_tables == set(expected_tables.keys()):
        report.append("✅ Todas las tablas están correctamente creadas.")
    else:
        report.append(f"❌ ERROR: Tablas esperadas {set(expected_tables.keys())} pero encontradas {found_tables}")
    
    # Verificar las columnas de cada tabla
    for table, expected_columns in expected_tables.items():
        cursor.execute(f"DESCRIBE `{table}`;")
        found_columns = {col[0] for col in cursor.fetchall()}
        if found_columns == expected_columns:
            report.append(f"✅ {table}: Columnas correctas.")
        else:
            report.append(f"❌ ERROR en {table}: columnas esperadas {expected_columns}, pero encontradas {found_columns}")
    
    # Verificar claves primarias
    for table, expected_pk in expected_primary_keys.items():
        cursor.execute(f"SHOW KEYS FROM `{table}` WHERE Key_name = 'PRIMARY';")
        found_pk = {row[4] for row in cursor.fetchall()}
        if found_pk == expected_pk:
            report.append(f"✅ {table}: Clave primaria correcta.")
        else:
            report.append(f"❌ ERROR en {table}: clave primaria esperada {expected_pk}, pero encontrada {found_pk}")
    
    # Verificar claves foráneas
    for table, expected_fks in expected_foreign_keys.items():
        cursor.execute(f"SELECT COLUMN_NAME, REFERENCED_TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table}' AND REFERENCED_TABLE_NAME IS NOT NULL;")
        found_fks = {row[0]: row[1] for row in cursor.fetchall()}
        if found_fks == expected_fks:
            report.append(f"✅ {table}: Claves foráneas correctas.")
        else:
            report.append(f"❌ ERROR en {table}: claves foráneas esperadas {expected_fks}, pero encontradas {found_fks}")
    
    print("\n".join(report))
    conn.close()

if __name__ == "__main__":
    validate_database()
