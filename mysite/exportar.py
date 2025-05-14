import pymysql

# Configuración
DB_HOST = 'ProyectoWeb2024A.mysql.pythonanywhere-services.com'
DB_USER = 'ProyectoWeb2024A'
DB_PASS = 'grupo03-2025'  # Reemplázala
DB_NAME = 'ProyectoWeb2024A$bd_proyecto'
BACKUP_FILE = "estructura.sql"

# Conexión y exportación
conn = pymysql.connect(host='ProyectoWeb2024A.mysql.pythonanywhere-services.com', user='ProyectoWeb2024A', password='grupo03-2025', db='ProyectoWeb2024A$bd_proyecto')
cursor = conn.cursor()

with open(BACKUP_FILE, 'w') as f:
    # Obtener tablas
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table in tables:
        # Exportar CREATE TABLE
        cursor.execute(f"SHOW CREATE TABLE {table}")
        create_table = cursor.fetchone()[1]
        f.write(f"{create_table};\n\n")

print(f"structura guardada en: {BACKUP_FILE}")
conn.close()