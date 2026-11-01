"""Definición de los problemas concretos (OneMax y TSP):
cómo se crea un individuo, cómo se evalúa, cómo se cruza y cómo se muta."""

import random


# ---------- Generadores de individuos ----------

def generar_bitstring(tamano):
    """Individuo de OneMax: lista de 0s y 1s aleatorios."""
    return [random.randint(0, 1) for _ in range(tamano)]


def generar_permutacion(tamano):
    """Individuo de TSP: orden aleatorio de visita de las ciudades 0..tamano-1."""
    individuo = list(range(tamano))
    random.shuffle(individuo)
    return individuo