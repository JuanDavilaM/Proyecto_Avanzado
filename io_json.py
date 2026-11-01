import json

# Opening JSON file

def read_json(ruta):

    with open(file=ruta) as json_file:
        data = json.load(json_file)

    return data

def separar_problemas(data):

    problemas_onemax = []
    problemas_tsp = []

    for problema, value in data.items():
        if problema == "problemas_onemax":
            if type(value) == list:
                problemas_onemax = problemas_onemax + value
            else:
                problemas_onemax.append(value)
        elif problema == "problemas_tsp":
            if type(value) == list:
                problemas_tsp = problemas_tsp + value
            else:
                problemas_tsp.append(value)

    return problemas_onemax, problemas_tsp

def individualizar_problemas(problemas):
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

# problemas_onemax, problemas_tsp = separar_problemas(data)
# problemas_onemax = individualizar_problemas(problemas_onemax)
# problemas_tsp = individualizar_problemas(problemas_tsp)