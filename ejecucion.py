"""Preparación de cada ejecución del JSON y su lanzamiento contra el motor genético."""

import ga_engine
import problemas


def formatear_tiempo(segundos):
    """Convierte segundos en texto con horas, minutos y segundos con milisegundos
    (p. ej. '0h 1m 5.250s')."""
    segundos = round(segundos, 3)
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    resto = segundos - horas * 3600 - minutos * 60
    return f"{horas}h {minutos}m {resto:.3f}s"


def _es_entero(valor):
    """True si es un entero de verdad (en Python, True y False también cuentan como int)."""
    return isinstance(valor, int) and not isinstance(valor, bool)


def _es_numero(valor):
    """True si es un entero o un decimal, excluyendo True y False."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def estrategia_de(ejecucion):
    """Estrategia del algoritmo elegida en el JSON ("basico" o "memetico").
    Si no se indica: memética en TSP (la que mejores rutas da) y básica en OneMax."""
    por_defecto = "memetico" if ejecucion.get("tipo") == "tsp" else "basico"
    return str(ejecucion.get("estrategia", por_defecto)).lower()


def comprobar_ejecucion(ejecucion):
    """Comprueba claves, tipos y rangos de una ejecución antes de resolverla.
    Si algo no es correcto, lanza ValueError con un mensaje que dice qué falla."""
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

    for clave in ("tamano_poblacion", "num_generaciones"):
        valor = ejecucion[clave]
        if not _es_entero(valor) or valor < 1:
            raise ValueError(f"{clave} debe ser un entero mayor o igual que 1 (recibido: {valor!r})")

    tasa = ejecucion["tasa_mutacion"]
    if not _es_numero(tasa) or not 0 <= tasa <= 1:
        raise ValueError(f"tasa_mutacion debe ser un número entre 0 y 1 (recibido: {tasa!r})")

    if tipo == "onemax":
        longitud = ejecucion["longitud_gen"]
        if not _es_entero(longitud) or longitud < 1:
            raise ValueError(f"longitud_gen debe ser un entero mayor o igual que 1 (recibido: {longitud!r})")
    else:
        ciudades = ejecucion["ciudades"]
        if not isinstance(ciudades, list) or len(ciudades) < 2:
            raise ValueError("ciudades debe ser una lista con al menos 2 ciudades")
        for ciudad in ciudades:
            if not isinstance(ciudad, list) or len(ciudad) != 2 or not all(_es_numero(c) for c in ciudad):
                raise ValueError(f"cada ciudad debe ser [x, y] con dos números (recibido: {ciudad!r})")

    optimo = ejecucion.get("optimo_conocido")
    if optimo is not None and not _es_numero(optimo):
        raise ValueError(f"optimo_conocido debe ser un número (recibido: {optimo!r})")

    # Parámetros opcionales del algoritmo (funcionalidad original)
    estrategia = estrategia_de(ejecucion)
    if estrategia not in ("basico", "memetico"):
        raise ValueError(f'estrategia debe ser "basico" o "memetico" (recibido: {ejecucion["estrategia"]!r})')
    if estrategia == "memetico" and tipo != "tsp":
        raise ValueError('la estrategia "memetico" (búsqueda local 2-opt) solo está disponible para TSP')
    for clave, minimo in (("num_elites", 0), ("tamano_torneo", 1), ("num_busqueda_local", 0)):
        if clave in ejecucion and (not _es_entero(ejecucion[clave]) or ejecucion[clave] < minimo):
            raise ValueError(f"{clave} debe ser un entero mayor o igual que {minimo} "
                             f"(recibido: {ejecucion[clave]!r})")
    if "semilla" in ejecucion and not _es_entero(ejecucion["semilla"]):
        raise ValueError(f"semilla debe ser un entero (recibido: {ejecucion['semilla']!r})")


def preparar_problema(ejecucion):
    """Valida la ejecución y elige las funciones del problema según su tipo.
    En TSP calcula la matriz de distancias una sola vez y pasa el óptimo a escala
    de fitness (distancia en negativo), que es lo que espera el motor."""

    comprobar_ejecucion(ejecucion)
    optimo = ejecucion.get("optimo_conocido")

    # Parámetros del algoritmo: los del JSON o, si no vienen, los valores por defecto
    parametros = {
        "num_elites": ejecucion.get("num_elites", 1),
        "tamano_torneo": ejecucion.get("tamano_torneo", 2),
        "semilla": ejecucion.get("semilla", ejecucion.get("id")),
        "busqueda_local": None,
        "num_busqueda_local": 0,
    }

    if ejecucion["tipo"] == "onemax":
        return {
            "tamano_individuo": ejecucion["longitud_gen"],
            "generador": problemas.generar_bitstring,
            "fitness": problemas.fitness_onemax,
            "cruce": problemas.cruce_un_punto,
            "mutacion": problemas.mutacion_bitflip,
            "datos_extra": (),
            "fitness_objetivo": optimo,
            "parametros": parametros,
        }

    # TSP: la matriz se calcula una sola vez, antes de ejecutar el algoritmo.
    matriz = problemas.matriz_distancias(ejecucion["ciudades"])


    if estrategia_de(ejecucion) == "memetico":
        parametros["busqueda_local"] = problemas.dos_opt
        parametros["num_busqueda_local"] = ejecucion.get("num_busqueda_local", 3)

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
        "parametros": parametros,
    }


def ejecutar_una(ejecucion):
    """Resuelve una ejecución y devuelve su resultado con tiempos, o el error si falla.
    Recibe un único argumento y está definida a nivel de módulo para poder pasarla
    a multiprocessing.Pool.map, que envía la función a otro proceso."""

    identificador = ejecucion.get("id")

    try:
        p = preparar_problema(ejecucion)
        bruto = ga_engine.run_genetic_algorithm(
            ejecucion["tamano_poblacion"], p["tamano_individuo"],
            ejecucion["num_generaciones"], ejecucion["tasa_mutacion"],
            p["generador"], p["fitness"], p["cruce"], p["mutacion"],
            *p["datos_extra"],
            fitness_objetivo=p["fitness_objetivo"],
            **p["parametros"])
    except Exception as error:
        return {
            "id": identificador,
            "tipo": ejecucion.get("tipo"),
            "configuracion": ejecucion,
            "error": f"{type(error).__name__}: {error}",
        }

    # En TSP la fitness es la distancia en negativo: se devuelve en positivo.
    if ejecucion["tipo"] == "tsp":
        signo = -1
    else:
        signo = 1

    evolucion = []
    for valor in bruto["evolucion"]:
        evolucion.append(signo * valor)

    hasta_optimo = bruto["segundos_hasta_optimo"]
    if hasta_optimo is None:
        texto_hasta_optimo = None
    else:
        texto_hasta_optimo = formatear_tiempo(hasta_optimo)

    return {
        "id": identificador,
        "tipo": ejecucion["tipo"],
        "estrategia": estrategia_de(ejecucion),
        "configuracion": ejecucion,
        "mejor_valor": signo * bruto["mejor_fitness"],
        "mejor_individuo": bruto["mejor_individuo"],
        "generacion_optimo": bruto["generacion_optimo"],
        "segundos_hasta_optimo": hasta_optimo,
        "tiempo_hasta_optimo": texto_hasta_optimo,
        "segundos_totales": bruto["segundos_totales"],
        "tiempo_total": formatear_tiempo(bruto["segundos_totales"]),
        "evolucion": evolucion,
    }
