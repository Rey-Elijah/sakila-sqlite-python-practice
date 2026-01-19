'''
    Escrito por: REMP
    Fecha: 1/12/2026
    Contexto: 
        - Script .py realizado como practica para probar el uso de la libreria sqlite3 el cual
        contiene un simple programa el cual se conecta a la base de datos de uso libre Sakila
        creado por MySQL. En especifico use un port para SQLite de la base de datos Sakila proveniente de 
        Kaggle hecho por el usuario Atanas Kanev. Lo que el programa hace es realizar una consult
        de peliculas provenientes de la tabla film ya sea introduciento el nombre completo
        o parte de este y con ello el programa mostrara en la terminal las coicidencias.
        
    - Sakila DB by MySQL: https://dev.mysql.com/doc/sakila/en/sakila-introduction.html
    - Sakila DB port by Atanas Kanev: https://www.kaggle.com/datasets/atanaskanev/sqlite-sakila-sample-database?resource=download
'''

import sqlite3
# ruta relativa de la base de datos
DB_PATH = "src/database/sqlite-sakila.db"
# input del usuario para realizar la busqueda de peliculas
busqueda = input("Ingresa el nombre de la pelicula (o parte de el): ")

try:
    with sqlite3.connect(DB_PATH) as mi_conexion:
        mi_conexion.row_factory = sqlite3.Row
        cursor = mi_conexion.cursor()
        # query que buscara la pelicula con el nombre introducido.¿
        query = "SELECT film_id, title, release_year, rating FROM film WHERE title LIKE ? LIMIT 5"
        # ejecuta la consulta SQL y parasamos como segundo parametro el input como tupla
        cursor.execute(query, (f"%{busqueda}%",))
        # obtenemos los resultados
        rows = cursor.fetchall()
        # en caso de haber resultados los imprimimos
        # de otro mostrara mensaje diciendo que no encontro coincidencias
        if rows:
            print(f"\n{'ID':<5} | {'TITULO':<30} | {'ANIO'} | {'RATING'}")
            print("-" * 60)
            for row in rows:
                print(f"{row['film_id']:<5} | {row['title']:<30} | {row['release_year']} | {row['rating']}")
        else:
            print(f"No se encontraron peliculas que coincidan con: '{busqueda}'")
except sqlite3.Error as e:
    print(f"Error al conectar con SQLite3: {e}")
except Exception as e:
    print(f"Ocurrio un error inesperado: {e}")