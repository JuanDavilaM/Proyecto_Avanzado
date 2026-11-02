"""Ejecución en paralelo de las ejecuciones del algoritmo genético
y utilidades relacionadas con los núcleos de la máquina."""

import os
import multiprocessing

from ejecucion import ejecutar_una


def nucleos_disponibles():
    """Número de núcleos lógicos de la máquina."""
    return os.cpu_count() or 1


def validar_num_nucleos(valor):
    """Vemos si el numero de nucleos es un entero o si está fuera de rango o no es entero, devuelve None."""
    try:
        n = int(valor)
    except (ValueError, TypeError):
        return None
    if 1 <= n <= nucleos_disponibles():
        return n
    return None

def ejecutar_en_paralelo(cleaned_data):
    """Lanza las ejecuciones cargadas repartidas entre varios procesos."""

    ejecuciones = cleaned_data.get("ejecuciones", [])

    num_procesos = cleaned_data["num_nucleos"]

    if len(ejecuciones) < num_procesos:
        num_procesos = len(ejecuciones)

    # Con un solo proceso no compensa crear un pool: se ejecuta en serie.
    if num_procesos == 1:
        return [ejecutar_una(e) for e in ejecuciones]

    with multiprocessing.Pool(processes=num_procesos) as pool:
        return pool.map(ejecutar_una, ejecuciones)
