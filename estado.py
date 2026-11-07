"""Opción 4 del menú: resumen del estado de la sesión y tablas de texto
con las ejecuciones cargadas y el historial de resultados."""


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


def tabla_ejecuciones_cargadas(ejecuciones):
    """Líneas de texto con los parámetros de cada ejecución cargada."""
    if not ejecuciones:
        return ["  (no hay ejecuciones cargadas)"]
    lineas = [f"{'id':>4}  {'tipo':<7}{'N':>5}{'población':>11}{'generaciones':>14}{'mutación':>10}{'óptimo':>9}"]
    for e in ejecuciones:
        lineas.append(
            f"{_texto(e.get('id')):>4}  {_texto(e.get('tipo')):<7}{_texto(_tamano(e)):>5}"
            f"{_texto(e.get('tamano_poblacion')):>11}{_texto(e.get('num_generaciones')):>14}"
            f"{_texto(e.get('tasa_mutacion')):>10}{_texto(e.get('optimo_conocido')):>9}")
    return lineas


def tabla_historial(historial):
    """Líneas de texto con el resultado y los tiempos de cada ejecución hecha, por tandas."""
    if not historial:
        return ["  (todavía no se ha ejecutado nada: usa la opción 3)"]
    lineas = [f"{'tanda':>5}{'id':>4}  {'tipo':<7}{'N':>5}{'mejor valor':>13}"
              f"{'gen. óptimo':>13}{'hasta óptimo':>15}{'tiempo total':>15}"]
    lineas = [f"{'tanda':>5}{'id':>6}  {'tipo':<7}{'N':>5}{'mejor valor':>13}"
          f"{'gen. óptimo':>13}{'hasta óptimo':>15}{'tiempo total':>15}"]
    for numero_tanda, tanda in enumerate(historial, start=1):
        for r in tanda:
            id_visible = f"{numero_tanda}.{_texto(r.get('id'))}"
            inicio = (f"{numero_tanda:>5}{id_visible:>6}  {_texto(r.get('tipo')):<7}"
                    f"{_texto(_tamano(r.get('configuracion', {}))):>5}")
            if "error" in r:
                lineas.append(f"{inicio}  ERROR: {r['error']}")
            else:
                lineas.append(
                    f"{inicio}{_texto(r.get('mejor_valor')):>13}{_texto(r.get('generacion_optimo')):>13}"
                    f"{_texto(r.get('tiempo_hasta_optimo')):>15}{_texto(r.get('tiempo_total')):>15}")
    return lineas