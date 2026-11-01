"""Motor genérico del algoritmo genético.
No conoce el problema: recibe como argumentos las funciones de generación,
fitness, cruce y mutación, y los datos extra del problema mediante *args."""

import random
import time


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

def seleccionar_elites(poblacion, fitnesses, num_elites):
    """Copias de los 'num_elites' mejores individuos, que pasan intactos
    a la siguiente generación (elitismo)."""
    orden = sorted(range(len(poblacion)), key=lambda i: fitnesses[i], reverse=True)
    return [poblacion[i][:] for i in orden[:num_elites]]


def optimo_alcanzado(fitness, fitness_objetivo, tolerancia=1e-4):
    """True si la fitness alcanza el objetivo, con una pequeña tolerancia relativa.
    Si no hay objetivo (None), nunca se considera alcanzado."""
    if fitness_objetivo is None:
        return False
    return fitness >= fitness_objetivo - tolerancia * abs(fitness_objetivo)

def run_genetic_algorithm(tamano_poblacion, tamano_individuo, num_generaciones, tasa_mutacion,
                          generador, fitness, cruce, mutacion, *args,
                          fitness_objetivo=None, semilla=None, tamano_torneo=2, num_elites=1):
    """Ejecuta el algoritmo genético y devuelve un diccionario con los resultados.

    generador, fitness, cruce, mutacion: funciones del problema (ver problemas.py).
    *args: datos extra del problema que se reenvían a la fitness (matriz de distancias en TSP).
    fitness_objetivo: fitness del óptimo conocido, para medir cuándo se alcanza (None si no hay).
    semilla: fija los números aleatorios para que la ejecución sea reproducible.
    """
    if semilla is not None:
        random.seed(semilla)
    inicio = time.perf_counter()
    num_elites = min(num_elites, tamano_poblacion)

    # Generación 0: población inicial
    poblacion = generar_poblacion(tamano_poblacion, generador, tamano_individuo)
    fitnesses = evaluar_poblacion(poblacion, fitness, *args)

    mejor_fitness = max(fitnesses)
    mejor_individuo = poblacion[fitnesses.index(mejor_fitness)][:]
    evolucion = [mejor_fitness]
    generacion_optimo = None
    segundos_hasta_optimo = None
    if optimo_alcanzado(mejor_fitness, fitness_objetivo):
        generacion_optimo = 0
        segundos_hasta_optimo = time.perf_counter() - inicio

    for generacion in range(1, num_generaciones + 1):
        elites = seleccionar_elites(poblacion, fitnesses, num_elites)
        padres = seleccion_torneo(poblacion, fitnesses, tamano_torneo)

        # Cruce por parejas y mutación de cada hijo
        hijos = []
        for i in range(0, len(padres) - 1, 2):
            hijo1, hijo2 = cruce(padres[i], padres[i + 1])
            hijos.append(mutacion(hijo1, tasa_mutacion))
            hijos.append(mutacion(hijo2, tasa_mutacion))
        if len(padres) % 2 == 1:
            hijos.append(mutacion(padres[-1], tasa_mutacion))

        # Nueva generación: élites + hijos, manteniendo el tamaño de la población
        poblacion = elites + hijos[:tamano_poblacion - num_elites]
        fitnesses = evaluar_poblacion(poblacion, fitness, *args)

        mejor_de_generacion = max(fitnesses)
        if mejor_de_generacion > mejor_fitness:
            mejor_fitness = mejor_de_generacion
            mejor_individuo = poblacion[fitnesses.index(mejor_de_generacion)][:]
        evolucion.append(mejor_fitness)

        if generacion_optimo is None and optimo_alcanzado(mejor_fitness, fitness_objetivo):
            generacion_optimo = generacion
            segundos_hasta_optimo = time.perf_counter() - inicio

    return {
        "mejor_individuo": mejor_individuo,
        "mejor_fitness": mejor_fitness,
        "generacion_optimo": generacion_optimo,
        "segundos_hasta_optimo": segundos_hasta_optimo,
        "segundos_totales": time.perf_counter() - inicio,
        "evolucion": evolucion,
    }