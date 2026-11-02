"""Funciones relacionadas con visualización"""

def conocer_cuantos_problemas_cargados(cleaned_data):

    ejecuciones = cleaned_data.get("ejecuciones", [])

    if not ejecuciones:
        return 0,0,0

    n_onemax = sum(1 for e in ejecuciones if e["tipo"] == "onemax")
    n_tsp = len(ejecuciones) - n_onemax

    return len(ejecuciones), n_onemax, n_tsp