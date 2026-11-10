"""Pruebas del motor genético con problemas cuyo óptimo conocemos."""

import math

import ga_engine
import problemas


def probar_onemax():
    """OneMax de 20 bits: debe alcanzar el óptimo (20 unos)."""
    resultado = ga_engine.run_genetic_algorithm(
        20, 20, 100, 0.05,
        problemas.generar_bitstring, problemas.fitness_onemax,
        problemas.cruce_un_punto, problemas.mutacion_bitflip,
        fitness_objetivo=20, semilla=1)
    print(f"OneMax: mejor fitness = {resultado['mejor_fitness']} (óptimo 20), "
          f"alcanzado en la generación {resultado['generacion_optimo']}")


def probar_tsp_circulo():
    """TSP de 10 ciudades en un círculo, cuyo óptimo se conoce por fórmula."""
    n, radio = 10, 100
    ciudades = [[radio * math.cos(2 * math.pi * k / n), radio * math.sin(2 * math.pi * k / n)]
                for k in range(n)]
    matriz = problemas.matriz_distancias(ciudades)
    optimo = 2 * n * radio * math.sin(math.pi / n)

    resultado = ga_engine.run_genetic_algorithm(
        50, n, 300, 0.3,
        problemas.generar_permutacion, problemas.fitness_tsp,
        problemas.cruce_ox, problemas.mutacion_intercambio,
        matriz,
        fitness_objetivo=-optimo, semilla=1)
    print(f"TSP: mejor distancia = {-resultado['mejor_fitness']:.2f} (óptimo {optimo:.2f}), "
          f"alcanzado en la generación {resultado['generacion_optimo']}")
    print(f"     ruta: {resultado['mejor_individuo']}")


def probar_dos_opt():
    """2-opt desde rutas aleatorias en el círculo: debe llegar siempre al óptimo."""
    n, radio = 10, 100
    ciudades = [[radio * math.cos(2 * math.pi * k / n), radio * math.sin(2 * math.pi * k / n)]
                for k in range(n)]
    matriz = problemas.matriz_distancias(ciudades)
    optimo = 2 * n * radio * math.sin(math.pi / n)

    for _ in range(5):
        ruta = problemas.generar_permutacion(n)
        mejorada = problemas.dos_opt(ruta, matriz)
        print(f"2-opt: {problemas.longitud_ruta(ruta, matriz):8.2f} -> "
              f"{problemas.longitud_ruta(mejorada, matriz):.2f} (óptimo {optimo:.2f})")


if __name__ == "__main__":
    probar_onemax()
    probar_tsp_circulo()
    probar_dos_opt()
