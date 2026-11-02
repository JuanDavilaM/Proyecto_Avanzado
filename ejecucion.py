#prepara cada ejecución del json y la lanza contra el motor genético.

import ga_engine
import problemas


def formatear_tiempo(segundos):
    
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    resto = segundos - horas * 3600 - minutos * 60
    return f"{horas}h {minutos}m {resto:.2f}s"


def comprobar_ejecucion(ejecucion):
    
    tipo = ejecucion.get("tipo")
    if tipo not in ("onemax", "tsp"):
        raise ValueError(f'tipo de problema desconocido: "{tipo}"')

    claves = ["tamano_poblacion", "num_generaciones", "tasa_mutacion"]
    if tipo == "onemax":
        claves.append("longitud_gen")
    else:
        claves.append("ciudades")

    for clave in claves:
        if clave not in ejecucion:
            raise ValueError(f'falta la clave "{clave}"')

    if ejecucion["tamano_poblacion"] < 1 or ejecucion["num_generaciones"] < 1:
        raise ValueError("tamano_poblacion y num_generaciones deben ser al menos 1")
    if ejecucion["tasa_mutacion"] < 0 or ejecucion["tasa_mutacion"] > 1:
        raise ValueError("tasa_mutacion debe estar entre 0 y 1")

    if tipo == "onemax":
        if ejecucion["longitud_gen"] < 1:
            raise ValueError("longitud_gen debe ser al menos 1")
    else:
        if len(ejecucion["ciudades"]) < 2:
            raise ValueError("ciudades necesita al menos 2 ciudades")
        for ciudad in ejecucion["ciudades"]:
            if len(ciudad) != 2:
                raise ValueError(f"cada ciudad debe ser [x, y] (recibido: {ciudad})")


def preparar_problema(ejecucion):
   
      
    comprobar_ejecucion(ejecucion)
    optimo = ejecucion.get("optimo_conocido")

    if ejecucion["tipo"] == "onemax":
        return {
            "tamano_individuo": ejecucion["longitud_gen"],
            "generador": problemas.generar_bitstring,
            "fitness": problemas.fitness_onemax,
            "cruce": problemas.cruce_un_punto,
            "mutacion": problemas.mutacion_bitflip,
            "datos_extra": (),
            "fitness_objetivo": optimo,
        }

    # TSP: la matriz se calcula una sola vez, antes de ejecutar el algoritmo.
    matriz = problemas.matriz_distancias(ejecucion["ciudades"])

    if optimo is None:
        objetivo = None
    else:
        objetivo = -optimo

    return {
        "tamano_individuo": len(ejecucion["ciudades"]),
        "generador": problemas.generar_permutacion,
        "fitness": problemas.fitness_tsp,
        "cruce": problemas.cruce_ox,
        "mutacion": problemas.mutacion_intercambio,
        "datos_extra": (matriz,),
        "fitness_objetivo": objetivo,
    }
