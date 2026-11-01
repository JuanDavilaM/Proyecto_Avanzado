#ruta pruebas ricardo: C:\Users\Ricardo\Downloads\problemas.json

from io_json import read_json, separar_problemas, individualizar_problemas, leer_metadatos_nucleos_y_salida

from paralelo import request_hilos

import os

### MENÚS ###

def mostrar_menu_inicio():

    valid_options = [1,2,3,4,5,6]
    last_menu = "inicio"
    
    print()
    
    print("Menú: ")
    print()
    print("1. Cargar Archivo de problemas (Pulsar 1)")
    print("2. Ajustar parámetros de ejecución (Pulsar 2)")
    print("3. Ejecutar todo (Pulsar 3)")
    print("4. Consultar estado (Pulsar 4)")
    print("5. Exportar resultados (Pulsar 5)")
    print("6. Salir del programa (Pulsar 6)")
    print()

    return valid_options, last_menu

def mostrar_menu_parametros_ejecucion():

    last_menu = "ajustar parámetros de ejecución" #Por si luego es necesario

    try:
        numero_hilos_usar = request_hilos()
    except:
        print("Número erroneo")
        numero_hilos_usar = mostrar_menu_parametros_ejecucion()

    return numero_hilos_usar

def mostrar_menu_cargar_json(cleaned_data):

    last_menu = "mostrar menú json" #Por si luego es necesario

    try:
        ruta = input("Introduce una ruta válida del equipo de donde extraer el .json: ")
        data = read_json(ruta)
        problemas_onemax, problemas_tsp = separar_problemas(data)
        problemas_onemax = individualizar_problemas(problemas_onemax)
        problemas_tsp = individualizar_problemas(problemas_tsp)
        data = leer_metadatos_nucleos_y_salida(data, cleaned_data)
        data["problemas_onemax"] = problemas_onemax
        data["problemas_tsp"] = problemas_tsp
        print("Problemas cargados con éxito")
        print(data)
    except:
        print("Ruta inválida, ¿Se te ha olvidado quitarle las 2 comillas a la ruta?")

    return data

def user_request(valid_options, last_menu, cleaned_data):

    try: 
        comando = int(input("Introduce un comando válido: "))

        if comando not in valid_options:
            print("Comando no válido, introduzca comando válido")
            return True, None
        elif comando in valid_options:
            if comando == 1 and last_menu == "inicio":
                data = mostrar_menu_cargar_json(cleaned_data)
                return True, data
            elif comando == 2 and last_menu == "inicio":
                data = mostrar_menu_parametros_ejecucion()
                cleaned_data["numero_nucleos_introducido"] = data
                return True, data
            elif comando == 6 and last_menu == "inicio":
                print("Programa Finalizado")
                return False, None
            else:
                return None, None
    except:
        print("ERROR, volviendo al último menú...")
        return True, None

if __name__ == "__main__":

    evaluator = True
    cleaned_data = {}

    while evaluator == True:
        valid_options, last_menu = mostrar_menu_inicio()
        evaluator, data = user_request(valid_options, last_menu, cleaned_data)