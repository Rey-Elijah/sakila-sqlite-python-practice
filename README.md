# sakila-sqlite-python-practice
Buscador de peliculas modular en Python utilizando la base de datos de ejemplo Sakila (SQLite). Evolucion de un script funcional a una arquitectura modular con JOINS complejos

# Requisitos
- Python 3.10 o superior.
- Base de datos Sakila en formato SQLite (`sqlite-sakila.db`).

# Instrucciones de uso
1. Clona o descarga el respositorio
2. Descarga la base de datos Sakila para SQLite desde Kaggle (el link se encuentra en la seccion de Base de datos que esta mas abajo)
3. Coloca el archivo sqlite_sakila.db en la carpeta src/database/

# Base de datos
Links a la bases de datos empleada en las pruebas:
- MySQL Sakila Sample Database: https://dev.mysql.com/doc/sakila/en/sakila-structure.html
- (SQLite Port) MySQL Sakila Sample Database: https://www.kaggle.com/datasets/atanaskanev/sqlite-sakila-sample-database?resource=download

# Aprendizajes
Empeze principalmente estas practicas para aprender a usar SQLite3 junto con Python debido a la necesidad que tuve de aprender mas
de estos temas para un pequeño proyecto de mi universidad que requeria estos conocimientos. 

Empeze primero aprendiendo como se realiza una conexion y una consulta simple a la base de datos
mediante el uso de un objeto cursor y ya de alli fui aumentando de nivel haciendo consultas complejas como por ejemplo relacionando tablas
mediante INNER JOIN's y agregacion con GROUP_CONCAT. Tambien me sirvio para mejorar mi modularizacion y manejor de errores en programacion