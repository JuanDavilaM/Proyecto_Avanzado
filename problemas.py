"""Funciones de OneMax y TSP: generar, evaluar, cruzar, mutar y 2-opt."""

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
    """Matriz de distancias euclídeas entre todas las ciudades."""
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
    """Cruce por orden (OX): conserva un tramo de un padre y completa con el orden del otro."""
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


# ---------- Búsqueda local para TSP (algoritmo memético) ----------

def dos_opt(ruta, matriz):
    """Búsqueda local 2-opt: invierte tramos mientras la ruta se acorte. Devuelve una ruta nueva."""
    ruta = ruta[:]
    n = len(ruta)
    if n < 4:
        return ruta  # con menos de 4 ciudades no hay dos tramos que se puedan cruzar

    mejora = True
    while mejora:
        mejora = False
        for i in range(n - 1):
            a, b = ruta[i], ruta[i + 1]                # tramo 1: a -> b
            for j in range(i + 2, n if i > 0 else n - 1):
                c, d = ruta[j], ruta[(j + 1) % n]      # tramo 2: c -> d
                # ¿Es más corto unir a-c y b-d que a-b y c-d?
                if matriz[a][c] + matriz[b][d] < matriz[a][b] + matriz[c][d] - 1e-9:
                    ruta[i + 1:j + 1] = reversed(ruta[i + 1:j + 1])
                    b = ruta[i + 1]
                    mejora = True
    return ruta
