import sqlite3
# Definimos ruta de la base de datos
DB_PATH = "src/database/sqlite-sakila.db"
try:
    # Establecemos la conexion con with para asegurar el cierre de la conexion automaticamente
    # al salir del bloque de codigo
    with sqlite3.connect(DB_PATH) as mi_conexion:
        mi_conexion.row_factory = sqlite3.Row
        cursor = mi_conexion.cursor()
        # Ejecutamos la consulta
        query = "SELECT film_id, title FROM film LIMIT 3;"
        cursor.execute(query)
        # Obtenemos los resultados
        rows = cursor.fetchall()
        for row in rows:
            # Al usar sqlite3.Row, podemos usar los nombres de las columnas
            print(f"{row['film_id']:<5} | {row['title']:<10}")
except sqlite3.Error as e:
    print(f"Error al conectar con SQLite: {e}")
except Exception as e:
    print(f"Ocurrio un error: {e}")
# NOTA: no es necesario el cerrar la conexion manualmente con cursor.close() o mi_conexion.close()
# ya que el uso de 'with' lo maneja automaticamente.