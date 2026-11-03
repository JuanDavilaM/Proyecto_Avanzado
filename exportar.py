#Opción 5 de menu:exportar los resultados a un json y el gráfico de rendimiento.

import json
import os

from ejecucion import formatear_tiempo


def obtener_resultados(historial):
    """El historial es una lista de vueltas (una por cada vez que se ejecuta la opción 3);
    devuelve una única lista con todos los resultados."""
    resultados = []
    for tanda in historial:
        for resultado in tanda:
            resultados.append(resultado)
    return resultados


def guardar_resultados(historial, tiempos, ruta):
    """Escribe en un único JSON la configuración, el resultado y el tiempo de cada ejecución.
    Devuelve cuántas ejecuciones se han guardado."""
    ejecuciones = []
    for r in obtener_resultados(historial):
        if "error" in r:
            ejecuciones.append({
                "id": r.get("id"),
                "tipo": r.get("tipo"),
                "configuracion": r.get("configuracion"),
                "error": r["error"],
            })
        else:
            ejecuciones.append({
                "id": r["id"],
                "tipo": r["tipo"],
                "configuracion": r["configuracion"],
                "mejor_valor": r["mejor_valor"],
                "mejor_individuo": r["mejor_individuo"],
                "generacion_optimo": r["generacion_optimo"],
                "tiempo_total": r["tiempo_total"],
                "segundos_totales": r["segundos_totales"],
                "tiempo_hasta_optimo": r["tiempo_hasta_optimo"],
                "segundos_hasta_optimo": r["segundos_hasta_optimo"],
            })

    tiempo_conjunto = sum(tiempos)
    datos = {
        "tiempo_real_total": formatear_tiempo(tiempo_conjunto),
        "segundos_reales_total": tiempo_conjunto,
        "ejecuciones": ejecuciones,
    }

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
    return len(ejecuciones)

# Calcula los datos para el gráfico.
def tamano_problema(configuracion):
    if "ciudades" in configuracion:
        return len(configuracion["ciudades"])
    return configuracion["longitud_gen"]


def puntos_grafico(historial):
    tiempos_por_tamano = {}

    for r in obtener_resultados(historial):
        if "error" in r:
            continue
        configuracion = r["configuracion"]
        if "optimo_conocido" not in configuracion:
            continue
        if r["segundos_hasta_optimo"] is None:
            continue

        tipo = r["tipo"]
        n = tamano_problema(configuracion)
        tiempos_por_tamano.setdefault(tipo, {}).setdefault(n, []).append(r["segundos_hasta_optimo"])

    puntos = {}
    for tipo, por_tamano in tiempos_por_tamano.items():
        lista = []
        for n in sorted(por_tamano):
            tiempos = por_tamano[n]
            lista.append((n, sum(tiempos) / len(tiempos)))
        puntos[tipo] = lista

    return puntos
