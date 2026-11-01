"""Ejecución en paralelo de las ejecuciones del algoritmo genético
y utilidades relacionadas con los núcleos de la máquina."""

import os


def nucleos_disponibles():
    return os.cpu_count() or 1

"""Vemos si el numero de nucleos es un entero o si está fuera de rango o no es entero, devuelve None."""

def validar_num_nucleos(valor):
    try:
        n = int(valor)
    except (ValueError, TypeError):
        return None
    if 1 <= n <= nucleos_disponibles():
        return n
    return None
