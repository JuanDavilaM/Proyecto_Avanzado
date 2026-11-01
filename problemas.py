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

# ---------- Cruces (devuelven dos hijos nuevos) ----------

def cruce_un_punto(padre1, padre2):
    """OneMax: se corta en un punto aleatorio y se intercambian las colas."""
    n = len(padre1)
    if n < 2:
        return padre1[:], padre2[:]
    corte = random.randint(1, n - 1)
    return padre1[:corte] + padre2[corte:], padre2[:corte] + padre1[corte:]


def cruce_ox(padre1, padre2):
    """TSP: cruce por orden (Order Crossover). Cada hijo conserva un tramo
    aleatorio de un padre y completa el resto con las ciudades que faltan,
    en el orden en que aparecen en el otro padre. Siempre da rutas válidas."""
    n = len(padre1)
    a, b = sorted(random.sample(range(n + 1), 2))
    return _hijo_ox(padre1, padre2, a, b), _hijo_ox(padre2, padre1, a, b)


def _hijo_ox(fijo, relleno, a, b):
    """Construye un hijo: el tramo [a, b) de 'fijo' en su sitio y el resto de 'relleno'."""
    tramo = fijo[a:b]
    usadas = set(tramo)
    resto = [ciudad for ciudad in relleno if ciudad not in usadas]
    return resto[:a] + tramo + resto[a:]

# ---------- Mutaciones (devuelven un individuo nuevo, sin modificar el original) ----------

def mutacion_bitflip(individuo, tasa):
    """OneMax: cada gen se invierte (0↔1) con probabilidad 'tasa'."""
    return [1 - gen if random.random() < tasa else gen for gen in individuo]


def mutacion_intercambio(individuo, tasa):
    """TSP: con probabilidad 'tasa', se intercambian dos ciudades al azar."""
    mutado = individuo[:]
    if len(mutado) >= 2 and random.random() < tasa:
        i, j = random.sample(range(len(mutado)), 2)
        mutado[i], mutado[j] = mutado[j], mutado[i]
    return mutado