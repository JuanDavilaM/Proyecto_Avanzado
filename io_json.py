"""Lectura de archivos JSON de problemas y su expansión en ejecuciones individuales."""

import json


def read_json(ruta):
    """Lee el archivo JSON y lo devuelve como diccionario de Python."""
    with open(ruta, encoding="utf-8") as json_file:
        data = json.load(json_file)
    if not isinstance(data, dict):
        raise ValueError("el JSON debe ser un objeto { ... } en el nivel superior")
    return data


def a_lista_de_problemas(valor, nombre):
    """Acepta un único problema (dict) o varios (lista de dicts) y devuelve siempre una lista."""
    if isinstance(valor, dict):
        return [valor]
    if isinstance(valor, list) and all(isinstance(p, dict) for p in valor):
        return valor
    raise ValueError(f'"{nombre}" debe ser un objeto o una lista de objetos')


def separar_problemas(data):
    """Devuelve dos listas (OneMax y TSP) con los problemas del JSON.
    Admite el formato simple (un problema con "tipo") y el completo
    (problemas_onemax / problemas_tsp, cada uno objeto o lista)."""
    if "tipo" in data:
        tipo = str(data["tipo"]).lower()
        problema = {clave: valor for clave, valor in data.items() if clave != "tipo"}
        if tipo == "onemax":
            return [problema], []
        if tipo == "tsp":
            return [], [problema]
        raise ValueError(f'tipo de problema desconocido: "{data["tipo"]}"')

    problemas_onemax = a_lista_de_problemas(data.get("problemas_onemax", []), "problemas_onemax")
    problemas_tsp = a_lista_de_problemas(data.get("problemas_tsp", []), "problemas_tsp")
    return problemas_onemax, problemas_tsp


def individualizar_problemas(problemas):
    """Expande cada problema en una ejecución por combinación de hiperparámetros."""
    resultado = []
    for problema in problemas:
        combinaciones = [{}]
        for clave, valor in problema.items():
            if type(valor) == list and clave != "ciudades":
                opciones = valor
            else:
                opciones = [valor]
            nuevas = []
            for combinacion in combinaciones:
                for opcion in opciones:
                    nueva = combinacion.copy()
                    nueva[clave] = opcion
                    nuevas.append(nueva)
            combinaciones = nuevas
        resultado = resultado + combinaciones
    return resultado


def construir_ejecuciones(data):
    """Lista única de ejecuciones individuales, cada una con su "tipo" y un "id"."""
    problemas_onemax, problemas_tsp = separar_problemas(data)

    ejecuciones = []
    for config in individualizar_problemas(problemas_onemax):
        config["tipo"] = "onemax"
        ejecuciones.append(config)
    for config in individualizar_problemas(problemas_tsp):
        config["tipo"] = "tsp"
        ejecuciones.append(config)

    for numero, ejecucion in enumerate(ejecuciones, start=1):
        ejecucion["id"] = numero
    return ejecuciones


def leer_metadatos_nucleos_y_salida(data):
    """Lee las claves opcionales del JSON. Si faltan: sin salida y 1 núcleo.
    La sección de salida se acepta como "salida" (ejemplo del enunciado) o "output" (texto)."""
    salida = data.get("salida", data.get("output"))
    num_nucleos = data.get("num_nucleos", 1)
    return salida, num_nucleos