'''
    Escrito por: REMP
    Fecha: 1/13/2026
    Contexto: 
        - Script .py hecho como practiva para probar los joins con la libreria de sqlite3. Este
        script es una modificacion de uno hecho el 1/12/2026 (movie_seach.py) el cual aparte de mostrar el id,
        titulo y año de las busquedas, tambien hace un join para mostrar el nombre de los actores
        que salen en la pelicula.
        
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
        # query buscara el filme y sus datos correspondientes junto al
        # nombre del actor que participo en el filme mediante un Join a la
        # tabla intermedia film_actor y la tabla actor para ello.
        # se emplea la funcion GROUP_CONCAT para concatenar las columnas de first_name
        # y last_name de la tabla actor y se agrupo con GROUP BY por ids de film para que
        # todos los actores de un mismo film sean colocados en vez de uno por cada resultado
        query = '''
                SELECT f.film_id
                     , f.title
                     , f.release_year
                     , f.rating
                     , GROUP_CONCAT(a.first_name || ' ' || a.last_name, ', ') AS actores
                FROM film AS f
                INNER JOIN film_actor AS fa
                ON fa.film_id = f.film_id
                INNER JOIN actor AS a
                ON fa.actor_id = a.actor_id
                WHERE f.title LIKE ?
                GROUP BY f.film_id
                LIMIT 5;
                '''
        # ejecuta la consulta SQL y parasamos como segundo parametro el input como tupla
        cursor.execute(query, (f"%{busqueda}%",))
        # obtenemos los resultados
        rows = cursor.fetchall()
        # en caso de haber resultados los imprimimos
        # de otro mostrara mensaje diciendo que no encontro coincidencias
        if rows:
            print(f"\n{'ID':<5} | {'TITULO':<30} | {'ANIO'} | {'RATING'} | {'ACTOR'}")
            print("-" * 60)
            for row in rows:
                print(f"{row['film_id']:<5} | {row['title']:<30} | {row['release_year']} | {row['rating']:<5} | {row['actores']}")
        else:
            print(f"No se encontraron peliculas que coincidan con: '{busqueda}'")
except sqlite3.Error as e:
    print(f"Error al conectar con SQLite3: {e}")
except Exception as e:
    print(f"Ocurrio un error inesperado: {e}")