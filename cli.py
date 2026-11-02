import json

from io_json import read_json, construir_ejecuciones, leer_metadatos_nucleos_y_salida
from paralelo import nucleos_disponibles, validar_num_nucleos

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
    cleaned_data["historial"] = []

    n_onemax = sum(1 for e in ejecuciones if e["tipo"] == "onemax")
    n_tsp = len(ejecuciones) - n_onemax
    print(f"Cargadas {len(ejecuciones)} ejecuciones ({n_onemax} OneMax, {n_tsp} TSP). Núcleos: {num_nucleos}.")

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