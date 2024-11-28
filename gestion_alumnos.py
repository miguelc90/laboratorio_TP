# ---------------------------------------------------------------------------- #
#                                   LIBRERÍAS                                  #
# ---------------------------------------------------------------------------- #
from funciones import *
import os

# ---------------------------------------------------------------------------- #
#                              PROGRAMA PRINCIPAL                              #
# ---------------------------------------------------------------------------- #
base_de_datos_creada = data_base_existe()
while True:
    print("GESTIÓN DE ALUMNOS -- PRIMARIA/SECUNDARIA".center(60))
    if not base_de_datos_creada:
        print("1-Crear base de datos 'gestion_alumnos'")
    else:
        print("2-Ingreso de datos")
        print("3-Consulta de datos")
        print("4-Modificar datos")
        print("5-Eliminación de datos")
        print("6-Ordenamiento")
        print("7-Salir\n")
    opcion = validar_numero(input("Seleccione una opción: "))

    match opcion:
        case '1':
            if not base_de_datos_creada:
                creacion_data_base()
                base_de_datos_creada = True
            else:
                print(
                    "La opción 1 se encuentra inhabilitada(la base de datos ya existe)"
                )
        case '2':
            os.system("cls")
            insertar_registro()
        case '3':
            os.system("cls")
            menu_de_consulta()
        case '4':
            os.system("cls")
            menu_de_actualizacion()
        case '5':
            os.system("cls")
            eliminar_registro()
        case '6':
            os.system("cls")
            menu_de_ordenamiento()
        case '7':
            break
        case _:
            print("Opción inválida, intente nuevamente: \n")
