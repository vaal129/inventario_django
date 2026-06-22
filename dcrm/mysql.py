import mysql.connector

database = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
)

## preparar un cursor para recorrer las filas y las columnas 
cursorObject = database.cursor() # se crea un cursor para ejecutar comandos SQL
cursorObject.execute("CREATE DATABASE cliente") #se ejecuta el comando SQL pra crear la base de datos 
print("Base de datos creada con exito") #se imprime un msj de confirmacion 