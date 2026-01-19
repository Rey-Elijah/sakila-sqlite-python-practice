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
import textwrap
import json
from datetime import datetime

# fnc encargada de leer la configuracion dentro de config.json
def load_config():
    # valores por default para la configuracion por si falla el leer config.json
    default_config = {
        "db_path": "data/sqlite-sakila.db",
        "debug_mode": False,
        "max_results": 5
    }
    try:
        # Lee el archivo Json y devuelve un diccionario con los datos
        with open("config/config.json", "r") as archivo:
            return json.load(archivo)
    # por si no se encuentra config.json
    except FileNotFoundError:
        print("Aviso: config.json no encontrado. Usando valores por defecto.")
        return default_config
    # Por si hay un error formato en config.json
    except json.JSONDecodeError as e:
        print(f"Error: El archivo config.json tiene un error en formato: {e}")
        print("Se usaran los valores por defecto")
        return default_config
# fnc que exporta los resultados de busqueda si el usuario lo desea
def export_results(rows, search_type):
    if not rows:
        return
    # Confirmamos si el usuario quiere exportar
    confirmar = input("\n¿Deseas exportar estos resultados a un archivo .txt? (s/n)...: ").lower()
    if confirmar != "s":
        return
    # Generamos una estampa de tiempo: AnioMesDia_HoraMinutoSegundo
    timeStamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Creamos el nuevo nombre del archivo
    nombre_archivo = f"exports/resultado_{search_type}_{timeStamp}.txt"
    try:
        # Si no existe el directorio 'exports' entonces lo crea
        if not os.path.exists("exports"):
            os.makedirs("exports")
        # Escribimos el archivo
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            # Encabezado principal
            f.write(f"REPORTE DE BUSQUEDA - TIPO: {search_type}\n")
            f.write("=" * 60 + "\n")
            # Escribimos los datos
            for row in rows:
                # obtenemos los nombres de cada columna y sus valores. 
                # ej; {key} seria film_id y row[key] seria el valor de esa key
                linea = " | ".join([f"{key}: {row[key]}" for key in row.keys()])
                # escribe la linea
                f.write(linea + "\n")
                # Linea de separacion entre fila
                f.write("-" * 60 + "\n")
        print(f"Resultados exportados con exito a: {nombre_archivo}")
    except Exception as e:
        print(f"Error al exportar: {e}")

# configuracion global
CONFIG = load_config()
DEBUGGIN = CONFIG["debug_mode"] # activa el modo debug que habilita mensajes e impide que no se limpie la terminal al usar el programa
DB_PATH = CONFIG["db_path"] # ruta relativa de la base de datos

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
def do_query(conn, search, search_type):
    debug_print(f"Buscando coincidencias con: {search}...")
    cursor = conn.cursor()
    match search_type:
        case "by_film":            
            query = f'''
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
                    LIMIT {CONFIG["max_results"]};
                    '''
            # ejecuta la consulta SQL y parasamos como segundo parametro el input como tupla
            cursor.execute(query, (f"%{search}%",))
        case "by_actor":
            query = f'''
                    SELECT a.actor_id
                         , a.first_name
                         , a.last_name
                         , GROUP_CONCAT(f.title, ', ') AS films
                    FROM actor AS a
                    INNER JOIN film_actor AS fa
                    ON fa.actor_id = a.actor_id
                    INNER JOIN film as f
                    ON f.film_id = fa.film_id
                    WHERE (a.first_name || ' ' || a.last_name) LIKE ?
                    GROUP BY a.actor_id
                    LIMIT {CONFIG["max_results"]}
                    '''
            cursor.execute(query, (f"%{search}%",))
        case "top5":
            query = f'''
                    SELECT ca.category_id
                         , ca.name as category
                         , COUNT(fl.film_id) as total_films
                    FROM film_category as fc
                    INNER JOIN film as fl
                    ON fl.film_id = fc.film_id
                    INNER JOIN category as ca
                    ON ca.category_id = fc.category_id
                    GROUP BY ca.name
                    ORDER BY Total_Films DESC
                    LIMIT {CONFIG["max_results"]};
                    '''
            cursor.execute(query)
    # obtenemos los resultados
    rows = cursor.fetchall()
    return rows
# fnc para imprimir el query del tipo de busqueda que haya realizado el usuario
# rows: lista de datos obtenidas de un query
def print_query(rows, busqueda, search_type):
    if rows:
        match search_type:
            case "by_film":
                debug_print("Mostrando peliculas...")
                print_films(rows)
            case "by_actor":
                debug_print("Mostrando Actores...")
                print_actors(rows)
            case "top5":
                debug_print("Mostrando Top 5 Categorias...")
                print_top5(rows)
    else:
        print(f"No se encontraron peliculas que coincidan con: '{busqueda}'")

def print_films(rows):
    # Definimos los anchos para las columnas
    id_w, t_w, an_w, r_w, a_w = 5, 20, 5, 5, 50
    # Encabezados por columna
    header = f"{'ID':<{id_w}} | {'TITULO':<{t_w}} | {'ANIO':<{an_w}} | {'RATING':<{r_w}} | {'ACTOR':<{a_w}}"
    print(f"\n{header}")
    print("-" * len(header))
    # Datos por fila
    for row in rows:
        print(f"{row['film_id']:<{id_w}} | {row['title']:<{t_w}} | {row['release_year']:<{an_w}} | {row['rating']:<{r_w}} | {row['actores']:<{a_w}}") 

def print_actors(rows):
    # Anchos para las columnas
    id_w, fn_w, ln_w, films_w = 5, 12, 12, 50
    # Definimos e imprimimos los encabezados de cada columna
    header = f"\n{'ID':<{id_w}} | {'PRIMER NOMBRE':<{fn_w}} | {'SEGUNDO NOMBRE':<{ln_w}} | {'FILMES':<{films_w}}"
    print(f"\n{header}")
    print("-" * len(header))
    
    for row in rows:
        # Envolvemos el texto de peliculas a 50 caracteres (films_w) para que no ocupe tanto espacio en consola
        wrapped_films = textwrap.wrap(row['films'], width=films_w)
        first_line_films = wrapped_films[0] if wrapped_films else ""
        # Imprimimos junto con los demas valores de columnas
        print(f"{row['actor_id']:<{id_w}} | {row['first_name']:<{fn_w}} | {row['last_name']:<{ln_w}} | {first_line_films}")
        # Si hay mas lineas de peliculas, las imprimimos indentadas
        for line in wrapped_films[1:]:
            # Dejamos espacios vacios en las columnas de ID, Nombre y Apellido
            indent = " " * (id_w + 3 + fn_w + 3 + ln_w + 1)
            print(f"{indent}| {line}")
        # Separador entre cada actor
        print("-" * len(header))

def print_top5(rows):
    # Definimos anchos de columnas
    id_w, c_w, tf_w = 3, 15, 3
    # Encabezados por columna
    header = f"\n{'ID':<{id_w}} | {'CATEGORIAS':<{c_w}} | {'TOTAL DE FILMS':<{tf_w}}"
    print(f"\n{header}")
    print("-" * len(header))
    # Datos por fila
    for row in rows:
        print(f"{row['category_id']:<{id_w}} | {row['category']:<{c_w}} | {row['total_films']:<{tf_w}}") 

# fnc que muestra el menu se seleccion y que devuelve la opcion ingresada la cual es un int
def option_selection():
    print('''
Selecciona una opcion de busqueda:
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
            search("by_film")
            pause()
            clean_screen()
        case 2:
            search("by_actor")
            pause()
            clean_screen()
        case 3:
            search("top5")
            pause()
            clean_screen()
        case 4:
            print("bye bye!")
        case _:
            print("error: OPCION INVALIDA")
# fnc encargada de buscar y mostrar las peliculas apartir del texto que ingrese el usuario
def search(search_type):
    match search_type:
        case "by_film":
            busqueda = input("Ingresa el nombre de la pelicula (o parte de el)...: ")
        case "by_actor":
            busqueda = input("Ingresa el nombre del actor (o parte de el)...: ")
        case "top5":
            busqueda = ""

    # obtenemos la conexion a la db en la ruta de la variable global DB_PATH
    with obtener_conexion(DB_PATH) as mi_conexion:
        if mi_conexion:
            # Obtenemos los resultados del query
            rows = do_query(mi_conexion, busqueda, search_type)
            # Imprimimos el query en consola
            print_query(rows, busqueda, search_type)
            export_results(rows, search_type)

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
    # opcion del usuario
    opcion = -1
    # mientras la opcion no sea 4 no se acabara el programa
    while opcion != 4:
        # la opcion seleccionada por el usuario del menu
        opcion = option_selection()
        clean_screen()
        # funcion que se ejecutara dependiendo la opcion del usuario
        do_func(opcion)

if __name__ == "__main__":
    main()