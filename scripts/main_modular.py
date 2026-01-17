'''
    Escrito por: REMP
    Fecha: 1/14/2026
    Contexto: 
        - Script .py hecho como practiva para mejorar mi arquitectura de software y modalizar un script
        anteriormente hecho por mi del 1/13/2026 (movie_search_joins.py) el cual contenia codigo suelto
        y sin funciones el cual lo que hacia y sigue haciendo en este codigo es servir como un buscador
        de peliculas en la base de datos de Sakila y en la terminal deberia de aparecer la lista de coincidencias
        con el nombre dado, ya sea completo o parcial.  
        
    - Sakila DB by MySQL: https://dev.mysql.com/doc/sakila/en/sakila-introduction.html
    - Sakila DB port by Atanas Kanev: https://www.kaggle.com/datasets/atanaskanev/sqlite-sakila-sample-database?resource=download
'''

import sqlite3
import os
# configuracion global
DEBUGGIN = False # activa el modo debug que habilita mensajes e impide que no se limpie la terminal al usar el programa
DB_PATH = "src/database/sqlite-sakila.db" # ruta relativa de la base de datos

# fnc para realizar la conexion de la base de datos parasada como argumento
# - db_path: String el cual indica la ruta de la base de datos
def obtener_conexion(db_path):
    debug_print(f"Conectando con db en ruta: {db_path}")
    try:
        conexion = sqlite3.connect(db_path)
        conexion.row_factory = sqlite3.Row
        return conexion
    except Exception as e:
        debug_print(f"Error de conexion: {e}")
        return None
# funcion que realiza un query en la base de datos para buscar el nombre
# de la pelicula ingresada por el usuario ya sea el nombre completo o parcial
# conn: conexion de la base de datos
# seach: String el cual se usara para realizar las comparaciones y obtener las coincidencias
def seach_movies(conn, search):
    debug_print(f"Buscando coincidencias con: {search}...")
    cursor = conn.cursor()
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
    cursor.execute(query, (f"%{search}%",))
    # obtenemos los resultados
    rows = cursor.fetchall()
    return rows
# fnc para imprimir la lista de peliculas dada y darles formato
# rows: lista de peliculas obtenidas de un query
def print_movies(rows, busqueda):
    debug_print("Mostrando peliculas...")
    if rows:
        print(f"\n{'ID':<5} | {'TITULO':<30} | {'ANIO'} | {'RATING'} | {'ACTOR'}")
        print("-" * 60)
        for row in rows:
            print(f"{row['film_id']:<5} | {row['title']:<30} | {row['release_year']} | {row['rating']:<5} | {row['actores']}")
    else:
        print(f"No se encontraron peliculas que coincidan con: '{busqueda}'")
# fnc que muestra el menu se seleccion y que devuelve la opcion ingresada la cual es un int
def option_selection():
    print('''
    Selecciona una opcion:
    1- Buscar pelicula por nombre
    2- Buscar pelicula por actor
    3- Ver Top 5 de categorias
    4- Salir
    ''')    
    opcion = input("Opcion...: ")
    # si la opcion ingresada es un digito esta se retorna, de otro modo retornara
    # un numero invalido para la seleccion (-1) y se pedira ingresar denuevo
    if opcion.isdigit():
        return int(opcion)
    return -1
# fnc que ejecuta una de varias funciones dependiendo la seleccion del usuario pasada como parametro
# - selection: int que se evalua para ejecutar la fnc
def do_func(selection):
    match selection:
        case 1:
            search_movie()
            pause()
            clean_screen()
        case 2:
            pass
        case 3:
            pass
        case 4:
            print("bye bye!")
        case _:
            print("error: OPCION INVALIDA")
# fnc encargada de buscar y mostrar las peliculas apartir del texto que ingrese el usuario
def search_movie():
    # input del usuario para realizar la busqueda de peliculas
    busqueda = input("Ingresa el nombre de la pelicula (o parte de el): ")
    # obtenemos la conexion a la db en la ruta de la variable global DB_PATH
    mi_conexion = obtener_conexion(DB_PATH)
    if mi_conexion:
        rows = seach_movies(mi_conexion, busqueda)
        print_movies(rows, busqueda)
        mi_conexion.close()

# fnc para imprimir mensajes debug en la consola cuando la variable 'DEBUGGIN' es True
# - message: mensaje de tipo String que sera impreso
def debug_print(message):
    if not (DEBUGGIN): return
    print(f"DEBUG: {message}")
# fnc que limpia la terminal al ser llamada

def clean_screen():
    if (DEBUGGIN): return
    # "nt" es para Windows, por defecto sera "clear" para otros sistemas
    os.system("cls" if os.name == "nt" else "clear")

# funcion que detiene el proceso del programa con un input
def pause(menssage = "\nPresiona <Enter> para continuar..."):
    input(menssage)

def main():
    opcion = -1
    clean_screen()
    # mientras la opcion no sea 4 no se acabara el programa
    while opcion != 4:
        # la opcion seleccionada por el usuario del menu
        opcion = option_selection()
        clean_screen()
        # funcion que se ejecutara dependiendo la opcion del usuario
        do_func(opcion)

if __name__ == "__main__":
    main()