# ---------------------------------------------------------------------------- #
#                                   LIBRERÍAS                                  #
# ---------------------------------------------------------------------------- #
import mysql.connector, os, re
from mysql.connector import errorcode
from datetime import datetime
from tabulate import tabulate #instalacion por terminal: pip install tabulate
import random
# ---------------------------------------------------------------------------- #
#                              VARIABLES GLOBALES                              #
# ---------------------------------------------------------------------------- #
opcion_orden_seleccionada = None
# ---------------------------------------------------------------------------- #
#                                 BASE DE DATOS                                #
# ---------------------------------------------------------------------------- #

def enlace_conexion():
    try:
        #establecemos la conexion a la base de datos mysql
        conexion = mysql.connector.connect(
            user = 'root',
            password = 'root',
            host = 'localhost',
            port = '3306',
        )
        #retornamos el objeto de la conexion si fue exitosa
        return conexion
    except mysql.connector.Error as e:
        #si la conexion no fue exitosa se imprime el mensaje de error
        #y retornamos None
        print(f"Error en la conexión: {e}")
        return None

def crear_data_base(data_base):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    #creamos un cursor para manipular la base de datos
    cursor = conexion.cursor()
    try:
        #consulta sql para crear la base datos si no existe
        query = f"CREATE DATABASE IF NOT EXISTS {data_base}"
        #usamos el cursor y ejecutamos la consulta
        cursor.execute(query)
        print(f"La base de datos {data_base} se creó con éxito")
    except mysql.connector.Error as e:
        #si ocurre algun error durante la consulta, se mostrara
        #por pantalla un mensaje con el error
        print(f"Ocurrio un error al crear la base de datos {e}")
    return data_base

def data_base_existe():
    try:
        mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            port='3306',
            database='gestion_alumnos'
        )
        return True
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_BAD_DB_ERROR:
            return False
        else:
            print(f"Error: {e}")
            return False

def crear_tabla_alumnos():
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    #creamos un cursor para manipular la base de datos
    cursor = conexion.cursor()
    #consulta sql para crear la tabla si no existe
    query = """
        CREATE TABLE IF NOT EXISTS gestion_alumnos.alumnos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre CHAR(20) NOT NULL,
            apellido CHAR(20) NOT NULL,
            dni CHAR(8) UNIQUE NOT NULL
        )
        INSERT INTO gestion_alumnos.alumnos(nombre, apellido, dni) VALUES('Angel, %s, %s)
    """
    try:
        #usamos el cursor y ejecutamos la consulta
        cursor.execute(query)
        print("La tabla alumnos se creó con éxito")
    except mysql.connector.Error as e:
        #si ocurre algun error durante la consulta, se mostrara
        #por pantalla un mensaje con el error
        print(f"Ocurrio un error: {e}")

def crear_tabla_datos_alumnos():
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    #creamos un cursor para manipular la base de datos
    cursor = conexion.cursor()
    #consulta sql para crear la tabla si no existe
    query = """
        CREATE TABLE IF NOT EXISTS gestion_alumnos.datos_de_alumnos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_alumno INT,
            domicilio CHAR(30) NOT NULL,
            telefono CHAR(12) NOT NULL,
            fecha_de_nacimiento DATE NOT NULL,
            FOREIGN KEY (id_alumno) REFERENCES alumnos(id) ON DELETE CASCADE
        )
    """
    try:
        #usamos el cursor y ejecutamos la consulta
        cursor.execute(query)
        print("La tabla datos_de_alumnos se creó con éxito\n")
    except mysql.connector.Error as e:
        #si ocurre algun error durante la consulta, se mostrara
        #por pantalla un mensaje con el error
        print(f"Ocurrio un error: {e}")

def creacion_data_base():
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    try:
        cursor = conexion.cursor()
        for elemento in range(4):
            match elemento:
                case 1:
                    crear_data_base("gestion_alumnos")
                case 2:
                    crear_tabla_alumnos()
                case 3:
                    crear_tabla_datos_alumnos()
    except mysql.connector.Error as e:
        print(f"Ocurrio un error insesperado: {e}")
    finally:
        cursor.close
        conexion.close

# ---------------------------------------------------------------------------- #
#                                 Función insertar                             #
# ---------------------------------------------------------------------------- #
def insertar(nombre, apellido, dni, domicilio, telefono, fecha_de_nacimiento):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    try:
        #creamos un cursor para manipular la base de datos
        cursor = conexion.cursor()
        #consulta sql para insertar un nuevo registro en la tabla alumnos
        query_alumno = """
            INSERT INTO gestion_alumnos.alumnos(nombre, apellido, dni) VALUES(%s, %s, %s)
        """
        #creamos una tupla con los valores a insertar
        alumno = (nombre, apellido, dni)
        #usamos el cursor para ejecutar la consulta
        cursor.execute(query_alumno, alumno)

        #en la variable id_alumno asignamos el ultimo id del registro insertado
        #usando el cursor y su atributo lastrowid
        id_alumno = cursor.lastrowid

        #consulta sql para insertar los datos relacionados de la tabla alumnos en la tabla datos_de_alumnos
        query_datos_alumno = """
            INSERT INTO gestion_alumnos.datos_de_alumnos(id_alumno, domicilio, telefono, fecha_de_nacimiento)
            VALUES(%s, %s, %s, %s)
        """
        #creamos una tupla con los valores a insertar
        datos_de_alumno = (id_alumno, domicilio, telefono, fecha_de_nacimiento)
        #usamos el cursor para ejecutar la consulta
        cursor.execute(query_datos_alumno, datos_de_alumno)
        
        #confirmamos los cambios realizados en la base de datos
        conexion.commit()
        print("Registro cargado con exito")
    except mysql.connector.Error as e:
        #si ocurre algun error al momento de insertar el registro, se mostrara
        #por pantalla un mensaje con el error
        print(f"Ocurrio un error al guardar el registro: {e}")
    finally:
        #cerramos el cursor y la conexion
        cursor.close()
        conexion.close()


# ---------------------------------------------------------------------------- #
#                                 Función Updates                              #
# ---------------------------------------------------------------------------- #

#Función de actulización de un registro por campos
def actualizar_por_campos(tabla, id_alumno, parametro):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    try:
        cursor = conexion.cursor()
        
         # Se compara el valor de tabla en: 1 (para los campos de la tabla alumno) y 2 (para los campos de la tabla datos_alumnos)
        if tabla == 1:
            cursor.execute("SELECT * FROM gestion_alumnos.alumnos WHERE id = %s", (id_alumno,))
        elif tabla == 2:
            cursor.execute("SELECT * FROM gestion_alumnos.datos_de_alumnos WHERE id = %s", (id_alumno,))
        
        #Se verifica la existencia del valor id_alumno entre la id de la tabla perteneciente al campo seleccionado
        registro = cursor.fetchone()
        if not registro:
            print("No existe registros con el ID proporcionado." )
            return
        #string para concatenar con la query que devuelve las funciones de actualizar_alumnos O actualizar_datos_alumnos
        id_A_actualizar = " WHERE id = %s"
        #se llama la siguiente función para mostrar el registro correspondiente a la id para visualizar el contenido
        mostrar_coincidencia_id(cursor,id_alumno)
        
        if tabla == 1:
            query, nuevo_valor = actualizar_Alumnos(parametro)
        elif tabla == 2:
            query, nuevo_valor = actualizar_datos_alumnos(parametro)
        else:
            return "Opción incorrecta"
        #Si de la funciones se retorna query se procede a concatenar segun el campo específicado a actulizar
        if query: 
            query += id_A_actualizar
            cursor.execute(query, (nuevo_valor, id_alumno))
            conexion.commit()
            print("El registro se ha actualizado exitosamente")
        #se llama la siguiente función para mostrar el registro correspondiente a la id para visualizar el contenido ACTUALIZADO
            mostrar_coincidencia_id(cursor,id_alumno)
            input("Pulse una tecla para continuar..")
            os.system('cls')
    except mysql.connector.Error as e:
        print(f"Error, no se ha podido actualizar el registro")
        input("Pulse una tecla para continuar..")
        os.system('cls')
    finally:
        cursor.close()
        conexion.close()

#Función de actulización de un registro completo
def opcion_actualizacion_completa(id_alumno):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    try:
        cursor = conexion.cursor()
        # verificar la existencia del registro
        cursor.execute("SELECT * FROM gestion_alumnos.alumnos WHERE id = %s", (id_alumno,))
        registro_alumnos = cursor.fetchone()

        cursor.execute("SELECT * FROM gestion_alumnos.datos_de_alumnos WHERE id = %s", (id_alumno,))
        registro_datos = cursor.fetchone()

        # En este caso  se utilizan la verificación de existencia de las 2 tablas ya que se van a modificar todos los campos 
        if not registro_alumnos and not registro_datos:
            print()
            print("No existe registros con el ID proporcionado.")
            
            
        #Si existe 
        if registro_alumnos and registro_datos:
            print(f"\nActualizar registro del  alumno correspondiente al id: {id_alumno}:")
            # Se llama la función que muestra los campos del registro que coincide con el id_alumno
            
            mostrar_coincidencia_id(cursor, id_alumno)
            
            #Se pasan a rrellenar los campos
            nombre = nuevo_registro_val(validar_cadena_campos,1,20,input("Ingresar Nombre: "),"Nombre").capitalize()
            apellido = nuevo_registro_val(validar_cadena_campos,1,20,input("Ingresar Apellido: "),"Apellido").capitalize()
            dni = pedir_dni()
            query_alumnos = "UPDATE gestion_alumnos.alumnos SET nombre = %s, apellido = %s, dni = %s WHERE id = %s"
            cursor.execute(query_alumnos, (nombre.capitalize(), apellido.capitalize(), dni, id_alumno))
            domicilio = validar_direccion()
            telefono = nuevo_registro_val(validar_digito_campos,10,10,input("Ingresar Teléfono: "),"Teléfono")
            fecha_de_nacimiento = validar_fecha_nacimiento()
            query_datos = "UPDATE gestion_alumnos.datos_de_alumnos SET domicilio = %s, telefono = %s, fecha_de_nacimiento = %s WHERE id = %s"
            cursor.execute(query_datos, (domicilio.title(), telefono, fecha_de_nacimiento, id_alumno))
            conexion.commit()
            print("El registro ha sido actulizado satisfactoriamente")
            mostrar_coincidencia_id(cursor, id_alumno)
            input("Pulse una tecla para continuar..")
            os.system('cls')
    except mysql.connector.Error as e:
        print("\nError al actualizar los registros")
        input("Pulse una tecla para continuar..")
        os.system('cls')
    finally:
        cursor.close()
        conexion.close()

#FUNCIÓN PARA MOSTRAR SOLO LA COINCIDENCIA ID UNA VEZ ES PORPORCIONADA POR EL USUARIO, SE LLAMA TANTO PARA ACTUALIZAR TODOS LOS DATOS O UN CAMPO ESPECIFICO
def mostrar_coincidencia_id(cursor, id_alumno):
    cursor.execute("SELECT * FROM gestion_alumnos.alumnos a join gestion_alumnos.datos_de_alumnos d on a.id=d.id_alumno where a.id=%s",(id_alumno,))
    mostrar=cursor.fetchone()
    print(f"\n{"id":<3} {"Nombre":<15} {"Apellido":<15} {"DNI":<10} {"Domicilio":20} {"Telefono":<13} {"Fecha de nacimiento"}")
    print(f"{mostrar[0]:<3} {mostrar[1]:<15} {mostrar[2]:<15} {mostrar[3]:<10} {mostrar[6]:<20} {mostrar[7]:<13} {mostrar[8]}")
    print()

#FUNCION actulizar_Alumnos y FUNCION actulizar_datos_alumnos
# Estas funciones sivern para actualizar un campo especifico y se llaman segun que campo se indicó , 1 = actualizar_alumnos, 2 = actualizar_datos_alumnos
#Ambos devuelen la query segun el campo a modificar y su nuevo valor en la Funcion actualizar_por_campos
def actualizar_Alumnos(parametro):
    query = "UPDATE gestion_alumnos.alumnos SET"
    match parametro:
        case 1:
            query += " nombre = %s"
            nuevo_valor = nuevo_registro_val(validar_cadena_campos,1,20,input("Ingresar Nombre: "),"Nombre").capitalize()
        case 2:
            query += " apellido = %s"
            nuevo_valor = nuevo_registro_val(validar_cadena_campos,1,20,input("Ingresar Apellido: "),"Apellido").capitalize()
        case 3:
            query += " dni = %s"
            nuevo_valor = pedir_dni()
            
        case _:
            print("Opción incorrecta")
            return None, None
        
    return query, nuevo_valor

def actualizar_datos_alumnos(parametro):
    query = "UPDATE gestion_alumnos.datos_de_alumnos SET"
    match parametro:
        case 4:
            query += " domicilio = %s"
            nuevo_valor = validar_direccion()
        case 5:
            query += " telefono = %s"
            nuevo_valor = nuevo_registro_val(validar_digito_campos,10,10,input("Ingresar Teléfono: "),"Teléfono")
        case 6:
            query += " fecha_de_nacimiento = %s"
            nuevo_valor = validar_fecha_nacimiento()
        case _:
            print("Opción incorrecta")
            return None, None
    return query, nuevo_valor

# ---------------------------------------------------------------------------- #
#                                 Función Eliminar                             #
# ---------------------------------------------------------------------------- #
def eliminar(id_alumno):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    try:
        #creamos un cursor para manipular la base de datos
        cursor = conexion.cursor()
        #iniciamos una transaccion para asegurar que las operaciones se realicen con exito
        conexion.start_transaction()
        #verificamos que el id exista
        query_verificar = "SELECT id FROM gestion_alumnos.alumnos WHERE id = %s"
        cursor.execute(query_verificar, (id_alumno,))
        resultado = cursor.fetchone()
        if not resultado:
            print(f"El ID solicitado ({id_alumno}) no existe.")
            return
        else:
            mostrar_coincidencia_id(cursor, id_alumno)
            numeros_random=captcha()
            decision = validar_numero(input(f"Para confirmar la eliminación resuelva el calculo matemático\n{numeros_random[1]}+{numeros_random[2]}: "))
            decision=int(decision)
            if decision == numeros_random[0]:
                #consulta sql para eliminar un registro de la tabla alumnos
                query_alumno = """
                        DELETE FROM gestion_alumnos.alumnos WHERE id = %s
                """
                #usamos el cursor y ejecutamos la consulta junto a la tupla que contiene el id
                #del registro que queremos eliminar
                cursor.execute(query_alumno, (id_alumno,))

                #consulta sql para eliminar un registro de la tabla datos_de_almnos
                query_datos_alumno = """
                        DELETE FROM gestion_alumnos.datos_de_alumnos WHERE id_alumno = %s
                """
                #usamos el cursor y ejecutamos la consulta junto a la tupla que contiene el mismo id
                #del registro que queremos eliminar
                cursor.execute(query_datos_alumno, (id_alumno,))
                #confirmamos los cambios realizados en la base de datos
                conexion.commit()
                print(f"Registro con id: {id_alumno} eliminado con éxito")
                input("Puse una tecla para continuar...")
                os.system("cls")
            else:
                print("Respuesta incorrecta, el registro no se eliminó")
                input("Puse una tecla para continuar...")
                os.system("cls")
                return
    
    except mysql.connector.DatabaseError as e:
        print(f"Primero debes crear la base de datos: {e}\n")
    
    except mysql.connector.Error as e:
        #si ocurre un error al momento de querer eliminar un registro, se revertiran los cambios
        #realizados utilizando rollback
        conexion.rollback()
        #se mostrara por pantalla un mensaje con el error
        print(f"Ocurrió un error al eliminar el registro seleccionado, error: {e}")
    
    finally:
        #cerramos el cursor y la conexion
        cursor.close()
        conexion.close()
        
def captcha():
    nums_randoms=random.randint(1,10),random.randint(1,10)
    resultado= nums_randoms[0] + nums_randoms[1]
    return resultado, nums_randoms[0], nums_randoms[1]

# ---------------------------------------------------------------------------- #
#                                 Función consultas                            #
# ---------------------------------------------------------------------------- #


#FUNCION CONSULTA_TODO
#segun la opción que se elija en el menú esta función va mostrar el cantenido general, o solo todo el contenido de una tabla de la BASE DE DATOS        
def consulta_todo(consulta):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion=enlace_conexion()
    try:
        cursor=conexion.cursor()

        match consulta:
            case 1:
                # Si LA OPCION ES 1 SE HACE LA CONSULTA GENERAL DE LOS REGISTROS EN LA BASE DE DATOS
                cursor.execute('SELECT * FROM gestion_alumnos.alumnos a join gestion_alumnos.datos_de_alumnos d on a.id=d.id_alumno')
                resultado=cursor.fetchall()
                print(f"{"id":<3} {"Nombre":<21} {"Apellido":<21} {"DNI":<9} {"Domicilio":31} {"Telefono":<13} {"Fecha de nacimiento"}")
                print()
                for fila in resultado:
                    print(f"{fila[0]:<3} {fila[1].title():<21} {fila[2].title():<21} {fila[3]:<9} {fila[6].title():<31} {fila[7]:<13} {fila[8]}") 
            case 2:
                # SI LA OPCIÓN ES 2 SE CONSULTA SOLO LOS DATOS DE LA TABLA ALUMNOS
                cursor.execute('SELECT * FROM gestion_alumnos.alumnos')
                resultado=cursor.fetchall()
                print(f"{"ID":<3} {"Nombre".title():<21} {"Apellido".title():<21} {"DNI":<10}")
                print()
                for fila in resultado:
                    print(f"{fila[0]:<3} {fila[1].title():<21} {fila[2].title():<21} {fila[3]:<10}")  
                
            case 3:
                # SI LA OPCIÓN ES 3 SE CONSULTA SOLO LOS DATOS DE LA TABLA DATOS_ALUMNOS
                cursor.execute('SELECT * FROM gestion_alumnos.datos_de_alumnos')
                resultado=cursor.fetchall()
                print(f"{"ID":<3} {"Domicilio":<30} {"Teléfono":<13} {"Fecha de nacimiento"}")
                print()
                for fila in resultado:
                    print(f"{fila[1]:<3} {fila[2].title():<30} {fila[3]:<13} {fila[4]}") 
    except mysql.connector.Error as e:
        print(f"Error, no se ha podido relizar las consultas")
    finally:
        cursor.close()
        conexion.close()

def crear_vistas():
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    cursor = conexion.cursor()
    cursor.execute("USE gestion_alumnos")
    vistas = {
        "ordenamiento_anio_de_nacimiento":"""
                                    CREATE
                                        ALGORITHM = UNDEFINED 
                                        DEFINER = `root`@`localhost` 
                                        SQL SECURITY DEFINER
                                    VIEW `ordenamiento_anio_de_nacimiento` AS
                                        SELECT 
                                            `alumnos`.`id` AS `id`,
                                            `alumnos`.`nombre` AS `nombre`,
                                            `alumnos`.`apellido` AS `apellido`,
                                            `alumnos`.`dni` AS `dni`,
                                            `datos_de_alumnos`.`telefono` AS `telefono`,
                                            `datos_de_alumnos`.`domicilio` AS `domicilio`,
                                            `datos_de_alumnos`.`fecha_de_nacimiento` AS `fecha_de_nacimiento`
                                        FROM
                                            (`alumnos`
                                            JOIN `datos_de_alumnos` ON ((`alumnos`.`id` = `datos_de_alumnos`.`id_alumno`)))
                                        ORDER BY `datos_de_alumnos`.`fecha_de_nacimiento`
                                  """,

        "ordenamiento_apellido":"""
                                    CREATE 
                                        ALGORITHM = UNDEFINED 
                                        DEFINER = `root`@`localhost` 
                                        SQL SECURITY DEFINER
                                    VIEW `ordenamiento_apellido` AS
                                        SELECT 
                                            `alumnos`.`id` AS `id`,
                                            `alumnos`.`nombre` AS `nombre`,
                                            `alumnos`.`apellido` AS `apellido`,
                                            `alumnos`.`dni` AS `dni`,
                                            `datos_de_alumnos`.`telefono` AS `telefono`,
                                            `datos_de_alumnos`.`domicilio` AS `domicilio`,
                                            `datos_de_alumnos`.`fecha_de_nacimiento` AS `fecha_de_nacimiento`
                                        FROM
                                            (`alumnos`
                                            JOIN `datos_de_alumnos` ON ((`alumnos`.`id` = `datos_de_alumnos`.`id_alumno`)))
                                        ORDER BY `alumnos`.`apellido`
                                """,
        
        "ordenamiento_dni":"""
                                    CREATE 
                                        ALGORITHM = UNDEFINED 
                                        DEFINER = `root`@`localhost` 
                                        SQL SECURITY DEFINER
                                    VIEW `ordenamiento_dni` AS
                                        SELECT 
                                            `alumnos`.`id` AS `id`,
                                            `alumnos`.`nombre` AS `nombre`,
                                            `alumnos`.`apellido` AS `apellido`,
                                            `alumnos`.`dni` AS `dni`,
                                            `datos_de_alumnos`.`telefono` AS `telefono`,
                                            `datos_de_alumnos`.`domicilio` AS `domicilio`,
                                            `datos_de_alumnos`.`fecha_de_nacimiento` AS `fecha_de_nacimiento`
                                        FROM
                                            (`alumnos`
                                            JOIN `datos_de_alumnos` ON ((`alumnos`.`id` = `datos_de_alumnos`.`id_alumno`)))
                                        ORDER BY `alumnos`.`dni`
                           """
    }

    for vista, query in vistas.items():
        try:
            cursor.execute(f"DROP VIEW IF EXISTS {vista}")
            cursor.execute(query)
        except mysql.connector.Error as e:
            print(f"Error al crear la vista {vista}: {e}")
        
# ---------------------------------------------------------------------------- #
#                                 VALIDACIONES                                 #
# ---------------------------------------------------------------------------- #
def validar_cadena(dato):
    while True:
        if dato.isalpha():
            return dato
        else:
            dato = input("El dato ingresado es incorrecto, intente nuevamente: ")

def validar_numero(dato):
    while True:
        if dato.isdigit():
            return dato
        else:
            dato = input("El dato ingresado es incorrecto, intente nuevamente: ")

def validar_direccion():
    caracteres_validos = re.compile(r'^[0-9a-zA-Z\s,.-]+$')
    while True:
        direccion = input("Ingrese la dirección: ")
        if not direccion:
            print("El campo no puede estar vacío, intente nuevamente")
        elif len(direccion) > 30:
            print("La dirección no puede superar los 30 caracteres, intente nuevamente.")
        elif not caracteres_validos.match(direccion) or direccion[0] == ' ':
            print("Dirección inválida, intente nuevamente")
        else:
            return direccion
        
def limitar_longitud(cantidad, dato_a_cargar):
    while True:
        dato = validar_numero(input(f"Ingrese su {dato_a_cargar} (mínimo {cantidad} caracteres, máximo {cantidad} caracteres): "))
        if len(dato) < cantidad:
            print(f"El dato no es válido, debe contener como mínimo {cantidad} caracteres, intente de nuevo")
        elif len(dato) > cantidad:
            print(f"El dato no es válido, no puede superar los {cantidad} caracteres, intente de nuevo")
        else:
            break
    return dato

def validar_fecha_nacimiento():
    while True:
        fecha = input("Nueva fecha de nacimiento (Año-Mes-Día): ")

        # se convierte en Año-Mes-Día
        
        try:
            fecha_nacimiento = datetime.strptime(fecha, '%Y-%m-%d')
            fecha_minima = datetime(2007, 1, 1)
            fecha_maxima = datetime(2018, 12, 31)

            if fecha_nacimiento < fecha_minima or fecha_nacimiento > fecha_maxima:
                print(f"La fecha de nacimiento debe estar entre {fecha_minima.date()} y {fecha_maxima.date()}.")
                continue

            # se vuelve a pedir la fecha si el usuaruio la puso en el futuro
            if fecha_nacimiento > datetime.now():
                print("La fecha de nacimiento no puede ser en el futuro.")
                continue 
            return fecha_nacimiento
        except ValueError:
            print("La fecha debe estar en formato: Año-Mes-Día (por ejemplo, 2000-01-01).")

def dni_existente(dni):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    try:
        cursor = conexion.cursor()
        query = "SELECT COUNT(*) FROM gestion_alumnos.alumnos WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Ocurrió un error: {e}")
    finally:
        cursor.close()
        conexion.close()
    return resultado[0] > 0

def pedir_dni():
    while True:
        dni = limitar_longitud(8, 'dni')
        if dni_existente(dni):
            print("El dni ingresado ya existe en nuestro sistema, ingrese un dni diferente")
        else:
            return dni

def validar_cadena_campos(dato):
    if dato.isalpha():
        return True
    return False
        
def validar_digito_campos(dato):
    if dato.isdigit():
        return True
    return False

def nuevo_registro_val(funcion_val_tipo, limiteMin,limiteMax, dato,nombre_dato):
    while True:
        if len(dato) < limiteMin or len(dato) > limiteMax:
            if limiteMin==limiteMax:
                print(f"El campo {nombre_dato} no puede qudar vacío, y tiene que ser exactamente {limiteMax} dígitos")
                dato = input(f"Ingrese nuevamente el {nombre_dato}: ")
            else:
                print(f"Error,no puede quedar el campo vacío, ni superar los {limiteMax} caracteres")
                dato = input(f"Ingrese nuevamente el {nombre_dato}: ")
        elif not funcion_val_tipo(dato): 
            print("Error, Valores incorrectos")
            dato = input(f"Ingrese nuevamente el {nombre_dato}: ")
        else:
            return dato  

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

def menu_de_consulta():
    opcion=''
    while True:
        print("Consulta de registros".center(40))
        print("Sleccione una de las opciones a consultar")
        print()
        print("1-Ver todos los registros")
        print("2-Ver registros de Alumnos")
        print("3-Ver registros de Datos de Alumnos")
        print("4-Volver atrás")
        try:
            opcion = input()
        except KeyboardInterrupt:
            print()
        
        
        if opcion.isdigit():
            opcion=int(opcion)
            match opcion:
                case 1:
                    consulta_todo(1)
                    input("Pulse una tecla para continuar...")
                    os.system("cls")
                case 2:
                    consulta_todo(2)
                    input("Pulse una tecla para continuar...")
                    os.system("cls")
                case 3:
                    consulta_todo(3)
                    input("Pulse una tecla para continuar...")
                    os.system("cls")
                case 4:
                    
                    break
                case _:
                    print("Opción Incorrecta, intentelo nuevamente")
        else:
            print("\nPor favor elija una de las opcines utilizando dígitos del 1 al 4\n")
    os.system("cls")

def insertar_registro():
    print("Ingresar registro".center(40))
    decision = 'si'
    while decision.lower() == 'si':
        print("Por favor ingrese los datos solicitados para agregarlos a la base de datos")
        nombre = nuevo_registro_val(validar_cadena_campos,1,20,input("Ingresar Nombre: "),"Nombre").capitalize()
        apellido = nuevo_registro_val(validar_cadena_campos,1,20,input("Ingresar Apellido: "),"Apellido").capitalize()
        dni = pedir_dni()
        direccion = validar_direccion()
        telefono = nuevo_registro_val(validar_digito_campos,10,10,input("Ingresar Teléfono: "),"Teléfono")
        fecha_de_nacimiento = validar_fecha_nacimiento()
        insertar(nombre.capitalize(), apellido.capitalize(), dni, direccion.title(), telefono, fecha_de_nacimiento)
        decision = input("Para cargar otro registro ingrese SI, de lo contrario pulse ENTER: ")
        os.system("cls")

def menu_de_actualizacion():
    while True: 
        print("Actualizar".center(40))
        try:
            opcion=int(input("1-Actualizar Registro Completo.\n2-Actualizar Campo específico.\n3-Volver "))
            print()
            os.system('cls')
            if opcion==1:
                 while True:
                    id_alumno = input("Ingrese el ID del alumno para actualizar: ")
                    if id_alumno.isdigit():
                        id_alumno = int(id_alumno)
                        opcion_actualizacion_completa(id_alumno)
                        break
                    else:
                        print("Debe ingresar un número válido para el ID.")
            elif opcion==2:
                while True:
                    print("Selecciona el campo a actualizar")
                    print()
                    parametro=input("1-Actualizar Nombre\n2-Actualizar Apellido\n3-Actualizar DNI\n4-Actualizar Domicilio\n5-Actualizar Teléfono\n6-Actualizar fecha de nacimiento\n")
                    os.system('cls')
                    if parametro.isdigit():
                        parametro=int(parametro)
                        match parametro:
                            case 1 | 2 | 3: 
                                tabla = 1
                                id_alumno = int(input("Ingrese el ID del alumno: "))
                                actualizar_por_campos(tabla, id_alumno, parametro)
                                break
                            case 4 | 5 | 6:  
                                tabla = 2
                                id_alumno = int(input("Ingrese el ID del alumno: "))
                                actualizar_por_campos(tabla, id_alumno, parametro)
                                break
                            case _:  # Caso por defecto
                                print("Opción incorrecta")
                    else:
                        print("Opción incorrecta,vuelva a intentarlo")
            elif opcion== 3:
                os.system('cls')
                break
            else:
                print("\nOpcion incorrecta, vuelva a intentarlo.\n")
                
        except ValueError:
            print("\nOpción incorrecta, vuelva a intentarlo\n")
        except KeyboardInterrupt:
            print()

def eliminar_registro():
    print("Eliminar registro".center(40))
    id_alumno = validar_numero(input("Ingrese el id del alumno que desea eliminar: "))
    eliminar(id_alumno)

def ordenar_datos(opcion_orden):
    #asignamos el retorno de la funcion enlace_onexion() a la variable conexion
    conexion = enlace_conexion()
    cursor = conexion.cursor()
    global opcion_orden_seleccionada
    opcion_orden_seleccionada = validar_numero(opcion_orden)

    match opcion_orden:
        case '0':
            return
        case '1':
            query = "SELECT * FROM gestion_alumnos.ordenamiento_anio_de_nacimiento;"
        case '2':
            query = "SELECT * FROM gestion_alumnos.ordenamiento_apellido;"
        case '3':
            query = "SELECT * FROM gestion_alumnos.ordenamiento_dni;"
        case _:
            print("Opción invalida")
            return None
            
    cursor.execute(query) 
    resultados = cursor.fetchall() 
    headers = [i[0] for i in cursor.description]
    cursor.close() 
    conexion.close()

    return resultados, headers

def menu_de_ordenamiento():
    try:
        crear_vistas()
        opciones_validas = ['1','2','3']
        while True:
            print("Métodos de ordenamiento".center(40))
            print("1-Fecha de nacimiento")
            print("2-Apellido")
            print("3-DNI")
            opcion = validar_numero(input("Seleccione la opción deseada: "))
            if opcion in opciones_validas:
                ordenar_datos(opcion)
                resultados, headers = ordenar_datos(opcion)

                if resultados: 
                    print(tabulate(resultados, headers, tablefmt="grid"))
                    input("Puse una tecla para continuar...")
                    os.system("cls")
                    return
                else:
                    print("Debe ingresar registros para poder ordenarlos(menú principal>opción 2)")
                    input("Pulse una tecla para continuar...")
                    os.system("cls")
                    return
            else:
                print("Debe seleccionar una de las opciones ofrecidas\n")
    except mysql.connector.ProgrammingError as e:
        print(f"Primero debe crear la base de datos(menú principal>opción 1)")
        input("Puse una tecla para continuar...")
        os.system("cls")
        return
       
