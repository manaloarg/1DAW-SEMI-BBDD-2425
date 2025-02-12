import os
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

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="jardineria"
    )
    cursor = conn.cursor()
    
    report_lines = ["# 📊 Reporte de Validación de Base de Datos\n"]

    # Verificar tablas
    cursor.execute("SHOW TABLES;")
    found_tables = {table[0] for table in cursor.fetchall()}
    report_lines.append("## 📌 Verificación de Tablas")
    for table in expected_tables.keys():
        status = "✅ Correcta" if table in found_tables else "❌ Faltante"
        report_lines.append(f"- **{table}**: {status}")
    
    # Guardar reporte en archivo Markdown
    report_text = "\n".join(report_lines)
    with open("reporte_validacion.md", "w") as f:
        f.write(report_text)

    # Si se ejecuta en GitHub Actions, escribir en el summary
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as summary_file:
            summary_file.write(report_text)

    conn.close()

if __name__ == "__main__":
    validate_database()
