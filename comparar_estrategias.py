"""Funcionalidad original: compara el GA básico con el GA memético (GA + 2-opt)
en instancias TSP aleatorias y dibuja la convergencia de ambos.

Uso: python comparar_estrategias.py [num_ciudades]   (por defecto, 100)"""

import random
import sys
import time

import ga_engine
import problemas


def generar_ciudades(num_ciudades, semilla):
    """Ciudades aleatorias en un cuadrado de 1000 x 1000 (reproducibles con la semilla)."""
    generador = random.Random(semilla)
    return [[generador.uniform(0, 1000), generador.uniform(0, 1000)] for _ in range(num_ciudades)]


def resolver(matriz, num_ciudades, semilla, memetico, poblacion=100, generaciones=300, tasa=0.2):
    """Ejecuta una estrategia y devuelve (mejor distancia, segundos, evolución en distancias)."""
    inicio = time.perf_counter()
    resultado = ga_engine.run_genetic_algorithm(
        poblacion, num_ciudades, generaciones, tasa,
        problemas.generar_permutacion, problemas.fitness_tsp,
        problemas.cruce_ox, problemas.mutacion_intercambio,
        matriz,
        semilla=semilla,
        busqueda_local=problemas.dos_opt if memetico else None,
        num_busqueda_local=3 if memetico else 0)
    segundos = time.perf_counter() - inicio
    evolucion = [-fitness for fitness in resultado["evolucion"]]
    return -resultado["mejor_fitness"], segundos, evolucion


def comparar(num_ciudades, semillas):
    """Resuelve la misma instancia con las dos estrategias y varias semillas.
    Devuelve, por estrategia, la lista de distancias, de tiempos y de evoluciones."""
    matriz = problemas.matriz_distancias(generar_ciudades(num_ciudades, semilla=num_ciudades))
    resultados = {}
    for nombre, memetico in (("GA básico", False), ("GA memético (2-opt)", True)):
        distancias, tiempos, evoluciones = [], [], []
        for semilla in semillas:
            distancia, segundos, evolucion = resolver(matriz, num_ciudades, semilla, memetico)
            distancias.append(distancia)
            tiempos.append(segundos)
            evoluciones.append(evolucion)
        resultados[nombre] = (distancias, tiempos, evoluciones)
    return resultados


def mostrar_tabla(resultados, num_ciudades, num_semillas):
    """Imprime la media y la mejor distancia y el tiempo medio de cada estrategia."""
    print(f"TSP de {num_ciudades} ciudades, {num_semillas} semillas, población 100, 300 generaciones")
    print(f"{'estrategia':<22}{'media':>10}{'mejor':>10}{'tiempo medio':>15}")
    for nombre, (distancias, tiempos, _) in resultados.items():
        print(f"{nombre:<22}{sum(distancias) / len(distancias):>10.1f}{min(distancias):>10.1f}"
              f"{sum(tiempos) / len(tiempos):>14.2f}s")


def dibujar_convergencia(resultados, num_ciudades, ruta):
    """Gráfico de la mejor distancia (media de las semillas) en cada generación."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("No se puede dibujar el gráfico: falta matplotlib (pip install matplotlib).")
        return

    plt.figure()
    for nombre, (_, _, evoluciones) in resultados.items():
        media = [sum(valores) / len(valores) for valores in zip(*evoluciones)]
        plt.plot(range(len(media)), media, label=nombre)
    plt.xlabel("Generación")
    plt.ylabel("Mejor distancia encontrada")
    plt.title(f"Convergencia en un TSP de {num_ciudades} ciudades")
    plt.legend()
    plt.savefig(ruta)
    plt.close()
    print(f"Gráfico guardado en {ruta}")


def main():
    num_ciudades = 100
    if len(sys.argv) > 1:
        try:
            num_ciudades = int(sys.argv[1])
        except ValueError:
            print("El número de ciudades debe ser un entero; se usa 100.")
    if num_ciudades < 4:
        print("Hacen falta al menos 4 ciudades; se usa 4.")
        num_ciudades = 4

    semillas = [1, 2, 3]
    resultados = comparar(num_ciudades, semillas)
    mostrar_tabla(resultados, num_ciudades, len(semillas))
    dibujar_convergencia(resultados, num_ciudades, f"convergencia_tsp_{num_ciudades}.png")


if __name__ == "__main__":
    main()