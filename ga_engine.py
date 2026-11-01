"""Motor genérico del algoritmo genético.
No conoce el problema: recibe como argumentos las funciones de generación,
fitness, cruce y mutación, y los datos extra del problema mediante *args."""

import random


def generar_poblacion(tamano_poblacion, generador, tamano_individuo):
    """Crea la población inicial llamando al generador recibido."""
    return [generador(tamano_individuo) for _ in range(tamano_poblacion)]