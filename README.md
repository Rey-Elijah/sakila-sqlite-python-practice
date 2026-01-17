# sakila-sqlite-python-practice
Buscador de peliculas modular en Python utilizando la base de datos de ejemplo Sakila (SQLite). Evolucion de un script funcional a una arquitectura modular con JOINS complejos

# Instrucciones de uso
Para poder usar los scripts es necesario que descarges la base de datos Sakila (en especifico el SQLite Port) que se encuentra en los links abajo
en la seccion de Base datos y luego poner el archivo .db en la carpeta de \src\ que esta en la raiz y con eso deberian de funcionar los programas

# Base de datos
Links a la bases de datos empleada en las pruebas:
- MySQL Sakila Sample Database: https://dev.mysql.com/doc/sakila/en/sakila-structure.html
- (SQLite Port) MySQL Sakila Sample Database: https://www.kaggle.com/datasets/atanaskanev/sqlite-sakila-sample-database?resource=download

# Tecnologias empleadas
- SQLite3
- Python 3

# Aprendizajes
Empeze principalmente estas practicas para aprender a usar SQLite3 junto con Python debido a la necesidad que tuve de aprender mas
de estos temas para un pequeño proyecto de mi universidad que requeria estos conocimientos. 

Empeze primero aprendiendo como se realiza una conexion y una consulta simple a la base de datos
mediante el uso de un objeto cursor y ya de alli fui aumentando de nivel haciendo consultas complejas como por ejemplo relacionando tablas
mediante INNER JOIN's y agregacion con GROUP_CONCAT. Tambien me sirvio para mejorar mi modularizacion y manejor de errores en programacion