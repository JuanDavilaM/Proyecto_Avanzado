"""Funciones relacionadas con visualización

Funcionalidades 4 y 5 involucradas aquí"""

def conocer_cuantos_problemas_cargados(cleaned_data):

    ejecuciones = cleaned_data.get("ejecuciones", [])

    if not ejecuciones:
        return 0,0,0

    n_onemax = sum(1 for e in ejecuciones if e["tipo"] == "onemax")
    n_tsp = len(ejecuciones) - n_onemax

    return len(ejecuciones), n_onemax, n_tsp

def conocer_cuantos_problemas_resueltos(cleaned_data):

    historial = cleaned_data.get("historial", [])

    resueltos = 0

    for tanda in historial:
        for resultado in tanda:
            if "error" not in resultado:
                resueltos = resueltos + 1

    return resueltos

def conocer_tiempo_real_ejecucion(cleaned_data):

    tiempos_tanda = cleaned_data.get("tiempos_tanda", [])

    tiempo_real = 0

    for tiempo in tiempos_tanda:
        tiempo_real = tiempo_real + tiempo

    return tiempo_real

def conocer_registro_resultados(cleaned_data):

    historial = cleaned_data.get("historial", [])

    registro = []

    for numero_tanda, tanda in enumerate(historial, start=1):
        for resultado in tanda:
            if "error" in resultado:
                registro.append({
                    "tanda": numero_tanda,
                    "id": resultado.get("id"),
                    "tipo": resultado.get("tipo"),
                    "tiempo (s)": None,
                    "resultado": "ERROR: " + str(resultado["error"]),
                })
            else:
                registro.append({
                    "tanda": numero_tanda,
                    "id": resultado.get("id"),
                    "tipo": resultado.get("tipo"),
                    "tiempo (s)": round(resultado.get("segundos_totales", 0), 4),
                    "resultado": resultado.get("mejor_valor"),
                })

    return registro