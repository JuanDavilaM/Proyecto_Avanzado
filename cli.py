"""Punto de entrada del programa: menú de la línea de comandos y estado de la sesión."""

import json
import time

from io_json import read_json, construir_ejecuciones, leer_metadatos_nucleos_y_salida
from paralelo import nucleos_disponibles, validar_num_nucleos, ejecutar_en_paralelo
from ejecucion import formatear_tiempo
from estado import (conocer_cuantos_problemas_cargados, conocer_cuantos_problemas_resueltos,
                    conocer_tiempo_real_ejecucion, mostrar_ejecuciones_cargadas, mostrar_historial)
from exportar import exportar_resultados, preguntar_si_no


def mostrar_menu_inicio():
    """Muestra el menú principal y devuelve las opciones válidas."""
    valid_options = [1, 2, 3, 4, 5, 6]

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

    return valid_options


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
        print(f"Aviso: num_nucleos = {num_nucleos_json!r} no es válido "
              f"(debe ser un entero entre 1 y {num_nucleos}); se usarán {num_nucleos}.")

    cleaned_data["archivo"] = ruta
    cleaned_data["ejecuciones"] = ejecuciones
    cleaned_data["salida"] = salida
    cleaned_data["num_nucleos"] = num_nucleos
    cleaned_data["historial"] = []
    cleaned_data["tiempos_tanda"] = []
    cleaned_data["pendientes"] = len(ejecuciones)

    n_onemax = sum(1 for e in ejecuciones if e["tipo"] == "onemax")
    n_tsp = len(ejecuciones) - n_onemax
    print(f"Cargadas {len(ejecuciones)} ejecuciones ({n_onemax} OneMax, {n_tsp} TSP). Núcleos: {num_nucleos}.")


def mostrar_menu_ejecutar(cleaned_data):
    """Opción 3: resuelve en paralelo las ejecuciones pendientes del archivo cargado y
    guarda sus resultados como una tanda nueva del historial, junto con su tiempo real.
    Si ya están todas hechas, pregunta si volver a ejecutarlas."""
    ejecuciones = cleaned_data.get("ejecuciones", [])
    if not ejecuciones:
        print("No hay ejecuciones cargadas: usa la opción 1 para cargar un archivo de problemas.")
        return
    if cleaned_data.get("pendientes", 0) == 0:
        print("Todas las ejecuciones cargadas ya están hechas.")
        if not preguntar_si_no("¿Volver a ejecutarlas en una tanda nueva?"):
            return

    print(f"Ejecutando {len(ejecuciones)} ejecuciones con {cleaned_data['num_nucleos']} núcleo(s)...")
    inicio = time.perf_counter()
    resultados = ejecutar_en_paralelo(cleaned_data)
    segundos = time.perf_counter() - inicio

    cleaned_data["historial"].append(resultados)
    cleaned_data["tiempos_tanda"].append(segundos)
    cleaned_data["pendientes"] = 0

    errores = sum(1 for r in resultados if "error" in r)
    print(f"Tanda {len(cleaned_data['historial'])} terminada en {formatear_tiempo(segundos)}: "
          f"{len(resultados) - errores} correctas, {errores} con error. Detalles en la opción 4.")


def mostrar_menu_consultar_estado(cleaned_data):
    """Opción 4: muestra todo lo que mantiene el programa (§9): archivo, núcleos,
    ejecuciones cargadas con sus parámetros e historial de resultados con sus tiempos."""
    ejecuciones = cleaned_data.get("ejecuciones", [])
    historial = cleaned_data.get("historial", [])
    if not ejecuciones and not historial:
        print("Todavía no hay nada cargado: usa la opción 1 para cargar un archivo de problemas.")
        return

    total, n_onemax, n_tsp = conocer_cuantos_problemas_cargados(cleaned_data)
    resueltos = conocer_cuantos_problemas_resueltos(cleaned_data)
    hechas = sum(len(tanda) for tanda in historial)
    tiempo_real = conocer_tiempo_real_ejecucion(cleaned_data)

    print()
    print("========== ESTADO DE LA SESIÓN ==========")
    print(f"Archivo cargado:      {cleaned_data.get('archivo', '-')}")
    print(f"Núcleos en uso:       {cleaned_data.get('num_nucleos', 1)} (disponibles: {nucleos_disponibles()})")
    print(f"Ejecuciones cargadas: {total} ({n_onemax} OneMax, {n_tsp} TSP), "
          f"pendientes: {cleaned_data.get('pendientes', 0)}")
    print(f"Resultados guardados: {hechas} en {len(historial)} tanda(s): "
          f"{resueltos} correctas, {hechas - resueltos} con error")
    print(f"Tiempo real total:    {formatear_tiempo(tiempo_real)}")

    print()
    print("--- Ejecuciones cargadas ---")
    mostrar_ejecuciones_cargadas(ejecuciones)

    print()
    print("--- Historial de resultados ---")
    mostrar_historial(historial)


def user_request(valid_options, cleaned_data):
    """Lee una opción y la ejecuta. Devuelve False solo si el usuario sale."""
    try:
        comando = int(input("Introduce un comando válido: "))
    except ValueError:
        print("Comando no válido: escribe un número del 1 al 6.")
        return True

    if comando not in valid_options:
        print("Comando no válido: escribe un número del 1 al 6.")
        return True

    if comando == 6:
        print("Programa Finalizado")
        return False

    try:
        if comando == 1:
            mostrar_menu_cargar_json(cleaned_data)
        elif comando == 2:
            mostrar_menu_parametros_ejecucion(cleaned_data)
        elif comando == 3:
            mostrar_menu_ejecutar(cleaned_data)
        elif comando == 4:
            mostrar_menu_consultar_estado(cleaned_data)
        elif comando == 5:
            exportar_resultados(cleaned_data)
    except Exception as error:
        print(f"Error inesperado en la opción {comando} ({type(error).__name__}: {error}). Volviendo al menú.")
    return True


def main():
    """Bucle principal del programa: muestra el menú hasta que el usuario sale."""
    seguir = True
    cleaned_data = {}

    try:
        while seguir:
            valid_options = mostrar_menu_inicio()
            seguir = user_request(valid_options, cleaned_data)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")


if __name__ == "__main__":
    main()
