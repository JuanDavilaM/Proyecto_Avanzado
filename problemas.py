"""Definición de los problemas concretos (OneMax y TSP):
cómo se crea un individuo, cómo se evalúa, cómo se cruza y cómo se muta."""

import random
import math


# ---------- Generadores de individuos ----------

def generar_bitstring(tamano):
    """Individuo de OneMax: lista de 0s y 1s aleatorios."""
    return [random.randint(0, 1) for _ in range(tamano)]


def generar_permutacion(tamano):
    """Individuo de TSP: orden aleatorio de visita de las ciudades 0..tamano-1."""
    individuo = list(range(tamano))
    random.shuffle(individuo)
    return individuo

# ---------- TSP: distancias ----------

def matriz_distancias(ciudades):
    """Matriz n x n con la distancia euclídea entre cada par de ciudades.
    Se calcula una sola vez al preparar el problema, antes de ejecutar el algoritmo."""
    n = len(ciudades)
    matriz = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distancia = math.dist(ciudades[i], ciudades[j])
            matriz[i][j] = distancia
            matriz[j][i] = distancia
    return matriz


def longitud_ruta(ruta, matriz):
    """Distancia total del recorrido cerrado (incluye la vuelta a la ciudad de inicio)."""
    total = matriz[ruta[-1]][ruta[0]]
    for i in range(len(ruta) - 1):
        total += matriz[ruta[i]][ruta[i + 1]]
    return total


# ---------- Funciones de fitness (mayor = mejor) ----------

def fitness_onemax(individuo):
    """Número de unos del individuo."""
    return sum(individuo)


def fitness_tsp(individuo, matriz):
    """Distancia con signo negativo: la ruta más corta tiene la fitness más alta."""
    return -longitud_ruta(individuo, matriz)