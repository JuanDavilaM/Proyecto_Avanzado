"""Motor genérico del algoritmo genético.
No conoce el problema: recibe como argumentos las funciones de generación,
fitness, cruce y mutación, y los datos extra del problema mediante *args."""

import random


def generar_poblacion(tamano_poblacion, generador, tamano_individuo):
    """Crea la población inicial llamando al generador recibido."""
    return [generador(tamano_individuo) for _ in range(tamano_poblacion)]

def evaluar_poblacion(poblacion, fitness, *args):
    """Calcula la fitness de cada individuo.
    *args son los datos extra del problema (para TSP, la matriz de distancias)
    y se reenvían tal cual a la función de fitness."""
    return [fitness(individuo, *args) for individuo in poblacion]

def seleccion_torneo(poblacion, fitnesses, tamano_torneo=2):
    """Elige tantos padres como individuos tiene la población.
    En cada torneo se escogen al azar 'tamano_torneo' individuos distintos
    y gana el de mayor fitness."""
    padres = []
    k = min(tamano_torneo, len(poblacion))
    for _ in range(len(poblacion)):
        participantes = random.sample(range(len(poblacion)), k)
        ganador = max(participantes, key=lambda i: fitnesses[i])
        padres.append(poblacion[ganador])
    return padres