"""Opción 4 del menú: resumen del estado de la sesión y tablas de texto
con las ejecuciones cargadas y el historial de resultados."""

import pandas as pd

def conocer_cuantos_problemas_cargados(cleaned_data):
    """Número de ejecuciones cargadas: total, OneMax y TSP."""
    ejecuciones = cleaned_data.get("ejecuciones", [])
    n_onemax = sum(1 for e in ejecuciones if e.get("tipo") == "onemax")
    n_tsp = len(ejecuciones) - n_onemax
    return len(ejecuciones), n_onemax, n_tsp


def conocer_cuantos_problemas_resueltos(cleaned_data):
    """Número de ejecuciones del historial que terminaron sin error."""
    resueltos = 0
    for tanda in cleaned_data.get("historial", []):
        for resultado in tanda:
            if "error" not in resultado:
                resueltos += 1
    return resueltos


def conocer_tiempo_real_ejecucion(cleaned_data):
    """Suma de los tiempos reales de todas las tandas ejecutadas (segundos)."""
    return sum(cleaned_data.get("tiempos_tanda", []))


def _tamano(configuracion):
    """Tamaño del problema (N): número de ciudades en TSP, longitud_gen en OneMax."""
    ciudades = configuracion.get("ciudades")
    if isinstance(ciudades, list):
        return len(ciudades)
    return configuracion.get("longitud_gen", "-")


def _texto(valor):
    """Valor preparado para una celda: decimales con 2 cifras y None como guion."""
    if valor is None:
        return "-"
    if isinstance(valor, float):
        return f"{valor:.2f}"
    return str(valor)

def df_ejecuciones_cargadas(ejecuciones):
    """DataFrame con los parámetros de cada ejecución cargada."""

    COLUMNAS_CARGADAS = ["id", "tipo", "N", "población", "generaciones", "mutación", "óptimo"]

    filas = []
    for e in ejecuciones:
        filas.append([_texto(e.get("id")), _texto(e.get("tipo")), _texto(_tamano(e)),
                      _texto(e.get("tamano_poblacion")), _texto(e.get("num_generaciones")),
                      _texto(e.get("tasa_mutacion")), _texto(e.get("optimo_conocido"))])
    return pd.DataFrame(filas, columns=COLUMNAS_CARGADAS)


def mostrar_ejecuciones_cargadas(ejecuciones):
    if not ejecuciones:
        print("  (no hay ejecuciones cargadas)")
        return
    print(df_ejecuciones_cargadas(ejecuciones).to_string(index=False))


def df_historial(historial):

    COLUMNAS_HISTORIAL = ["tanda", "id", "tipo", "N", "mejor valor", "gen. óptimo",
                      "hasta óptimo", "tiempo total", "mejor individuo (TSP)"]
    
    """DataFrame con una fila por ejecución hecha, en el orden de las tandas."""
    filas = []
    for numero_tanda, tanda in enumerate(historial, start=1):
        for r in tanda:
            fila = [numero_tanda, f"{numero_tanda}.{_texto(r.get('id'))}", _texto(r.get("tipo")),
                    _texto(_tamano(r.get("configuracion", {})))]
            if "error" in r:
                fila += ["-", "-", "-", "-", f"ERROR: {r['error']}"]
            else:
                individuo = r.get("mejor_individuo") if r.get("tipo") == "tsp" else None
                fila += [_texto(r.get("mejor_valor")), _texto(r.get("generacion_optimo")),
                         _texto(r.get("tiempo_hasta_optimo")), _texto(r.get("tiempo_total")),
                         _texto(individuo)]
            filas.append(fila)
    return pd.DataFrame(filas, columns=COLUMNAS_HISTORIAL)


def mostrar_historial(historial):
    if not historial:
        print("  (todavía no se ha ejecutado nada: usa la opción 3)")
        return
    print(df_historial(historial).to_string(index=False, max_colwidth=40))