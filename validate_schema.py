import mysql.connector

expected_tables = {
    "clientes": {"idCliente", "nombre", "direccion", "telefono"},
    "productos": {"idProducto", "nombre", "precio", "stock"},
    "pedidos": {"idPedido", "idCliente", "fecha", "total"},
}

conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root", database="jardineria")
cursor = conn.cursor()

# Verificar tablas
cursor.execute("SHOW TABLES;")
tables = {table[0] for table in cursor.fetchall()}

assert tables == expected_tables.keys(), f"ERROR: Tablas esperadas {expected_tables.keys()} pero encontradas {tables}"

# Verificar estructura de cada tabla
for table, expected_columns in expected_tables.items():
    cursor.execute(f"DESCRIBE {table};")
    columns = {col[0] for col in cursor.fetchall()}
    assert columns == expected_columns, f"ERROR en {table}: columnas esperadas {expected_columns}, pero encontradas {columns}"

print("✅ La estructura de la base de datos es correcta.")

conn.close()
