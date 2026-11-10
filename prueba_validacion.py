"""Pruebas de la validación de ejecuciones: datos correctos e incorrectos."""

from ejecucion import comprobar_ejecucion


def probar(descripcion, ejecucion):
    """Valida una ejecución e imprime si es correcta o el motivo del error."""
    try:
        comprobar_ejecucion(ejecucion)
        print(f"OK     {descripcion}")
    except ValueError as error:
        print(f"ERROR  {descripcion}: {error}")


def main():
    onemax = {"tipo": "onemax", "tamano_poblacion": 10, "num_generaciones": 5,
              "tasa_mutacion": 0.1, "longitud_gen": 8}
    tsp = {"tipo": "tsp", "tamano_poblacion": 10, "num_generaciones": 5,
           "tasa_mutacion": 0.2, "ciudades": [[0, 0], [3, 0], [3, 4]]}

    # Deben ser correctos
    probar("OneMax correcto", onemax)
    probar("TSP correcto", tsp)
    probar("tasa_mutacion = 0 (sin mutación)", {**onemax, "tasa_mutacion": 0})
    probar("TSP con optimo_conocido decimal", {**tsp, "optimo_conocido": 12.0})

    # Deben dar error
    probar("tasa_mutacion = true", {**onemax, "tasa_mutacion": True})
    probar("tamano_poblacion en texto", {**onemax, "tamano_poblacion": "veinte"})
    probar("tamano_poblacion decimal", {**onemax, "tamano_poblacion": 10.5})
    probar("longitud_gen = 0", {**onemax, "longitud_gen": 0})
    probar("falta longitud_gen", {k: v for k, v in onemax.items() if k != "longitud_gen"})
    probar("ciudad con tres coordenadas", {**tsp, "ciudades": [[0, 0], [1, 2, 3]]})
    probar("ciudad con texto", {**tsp, "ciudades": [[0, 0], ["a", 1]]})
    probar("ciudades no es una lista", {**tsp, "ciudades": 5})
    probar("optimo_conocido en texto", {**tsp, "optimo_conocido": "doce"})
    probar("tipo desconocido", {**onemax, "tipo": "knapsack"})


if __name__ == "__main__":
    main()
