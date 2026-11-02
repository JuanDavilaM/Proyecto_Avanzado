import json
import time
import pandas as pd

from io_json import read_json, construir_ejecuciones, leer_metadatos_nucleos_y_salida
from paralelo import nucleos_disponibles, validar_num_nucleos, ejecutar_en_paralelo
from ejecucion import formatear_tiempo
from visualizacion import *

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

def mostrar_menu_parametros_ejecucion(cleaned_data):
    """Permite sobrescribir el número de núcleos de la sesión sin editar el JSON."""
    actual = cleaned_data.get("num_nucleos", 1)
    maximo = nucleos_disponibles()

    print(f"Núcleos disponibles en esta máquina: {maximo}")
    print(f"Núcleos configurados actualmente: {actual}")
    entrada = input(f"Nuevo número de núcleos (1-{maximo}) o Enter para mantener: ").strip()

    if entrada == "":
        print(f"Se mantiene {actual}.")
        return

    nuevo = validar_num_nucleos(entrada)
    if nuevo is None:
        print(f"Valor no válido: debe ser un entero entre 1 y {maximo}. Se mantiene {actual}.")
    else:
        cleaned_data["num_nucleos"] = nuevo
        print(f"Se usarán {nuevo} núcleos.")

def mostrar_menu_cargar_json(cleaned_data):
    """Carga un JSON, lo expande en ejecuciones y reinicia el estado de la sesión.
    Si algo falla, el estado anterior se conserva intacto."""
    ruta = input("Ruta del archivo JSON: ").strip().strip('"\'')

    try:
        data = read_json(ruta)
        ejecuciones = construir_ejecuciones(data)
        salida, num_nucleos_json = leer_metadatos_nucleos_y_salida(data)
    except FileNotFoundError:
        print(f"No se encuentra el archivo: {ruta}")
        return
    except OSError as error:
        print(f"No se puede leer el archivo: {error}")
        return
    except json.JSONDecodeError as error:
        print(f"El archivo no es un JSON válido (línea {error.lineno}): {error.msg}")
        return
    except ValueError as error:
        print(f"Formato de problemas incorrecto: {error}")
        return

    if not ejecuciones:
        print("El archivo no contiene ningún problema (problemas_onemax, problemas_tsp o tipo).")
        return

    num_nucleos = validar_num_nucleos(num_nucleos_json)
    if num_nucleos is None:
        num_nucleos = nucleos_disponibles()
        print(f"Aviso: num_nucleos = {num_nucleos_json} no es válido en esta máquina; se usarán {num_nucleos}.")

    cleaned_data["archivo"] = ruta
    cleaned_data["ejecuciones"] = ejecuciones
    cleaned_data["salida"] = salida
    cleaned_data["num_nucleos"] = num_nucleos
    if "historial" not in cleaned_data:
        cleaned_data["historial"] = []
    if "tiempos_tanda" not in cleaned_data:
        cleaned_data["tiempos_tanda"] = []

    n_onemax = sum(1 for e in ejecuciones if e["tipo"] == "onemax")
    n_tsp = len(ejecuciones) - n_onemax
    print(f"Cargadas {len(ejecuciones)} ejecuciones ({n_onemax} OneMax, {n_tsp} TSP). Núcleos: {num_nucleos}.")

def mostrar_menu_ejecutar(cleaned_data):

    ejecuciones = cleaned_data.get("ejecuciones", [])

    if ejecuciones == []:
        print("No hay datos cargados, asegurate de cargar un .json")
        return []

    print("Ejecutando...")
    inicio = time.perf_counter()
    cleaned_data["historial"].append(ejecutar_en_paralelo(cleaned_data))
    cleaned_data["tiempos_tanda"].append(time.perf_counter() - inicio)
    del cleaned_data["ejecuciones"]
    print("Proceso Finalizado")

    return cleaned_data["historial"]

def mostrar_menu_consultar_estado(cleaned_data):

    if cleaned_data == {}:
        return print("Datos no cargados todavía, redirigiendo al menú principal")

    last_menu = "consultar estado"

    problemas_totales, problemas_onemax, problemas_tsp = conocer_cuantos_problemas_cargados(cleaned_data)
    problemas_resueltos = conocer_cuantos_problemas_resueltos(cleaned_data)
    suma_segundos_real = conocer_tiempo_real_ejecucion(cleaned_data)

    registro = conocer_registro_resultados(cleaned_data)

    print(f"Problemas totales cargados ahora mismo: {problemas_totales}")
    print(f"Problemas \"one max\" cargados ahora mismo: {problemas_onemax}")
    print(f"Problemas \"tsp\" cargados ahora mismo: {problemas_tsp}")
    print(f"Total de problemas resueltos en esta sesión: {problemas_resueltos}")
    print(f"Tiempo total de ejecución de problemas: {formatear_tiempo(suma_segundos_real)}")
    if registro:
        print("Registro de resultados:")
        print(pd.DataFrame(registro).to_string(index=False))

def user_request(valid_options, last_menu, cleaned_data):

    try: 
        comando = int(input("Introduce un comando válido: "))

        if comando not in valid_options:
            print("Comando no válido, introduzca comando válido")
            return True, None
        elif comando in valid_options:
            if comando == 1 and last_menu == "inicio":
                mostrar_menu_cargar_json(cleaned_data)
                return True, None
            elif comando == 2 and last_menu == "inicio":
                mostrar_menu_parametros_ejecucion(cleaned_data)
                return True, None
            elif comando == 3 and last_menu == "inicio":
                mostrar_menu_ejecutar(cleaned_data)
                return True, None
            elif comando == 4 and last_menu == "inicio":
                mostrar_menu_consultar_estado(cleaned_data)
                return True, None
            elif comando == 6 and last_menu == "inicio":
                print("Programa Finalizado")
                return False, None
            else:
                print("Opción todavía no disponible")
                return True, None
    except:
        print("ERROR, volviendo al último menú...")
        return True, None

def main():
    """Bucle principal del programa: muestra el menú hasta que el usuario sale."""
    evaluator = True
    cleaned_data = {}

    while evaluator:
        valid_options, last_menu = mostrar_menu_inicio()
        evaluator, data = user_request(valid_options, last_menu, cleaned_data)


if __name__ == "__main__":
    main()