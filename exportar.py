"""Opción 5 del menú: exportar los resultados a un JSON y dibujar el gráfico de rendimiento."""

import json
import os

from ejecucion import formatear_tiempo


def obtener_resultados(historial):
    """Junta en una lista los resultados de todas las tandas."""
    resultados = []
    for lista in historial:
        for resultado in lista:
            resultados.append(resultado)
    return resultados


def guardar_resultados(historial, tiempos, ruta):
    """Guarda en JSON la configuración, el resultado y los tiempos de cada ejecución."""
    ejecuciones = []
    for numero_tanda, tanda in enumerate(historial, start=1):
        for r in tanda:
            id_visible = f"{numero_tanda}.{r.get('id')}"
            if "error" in r:
                ejecuciones.append({
                    "id": id_visible,
                    "tipo": r.get("tipo"),
                    "configuracion": r.get("configuracion"),
                    "error": r["error"],
                })
            else:
                ejecuciones.append({
                    "id": id_visible,
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


def tamano_problema(configuracion):
    """Tamaño del problema (N): número de ciudades en TSP o longitud_gen en OneMax."""
    if "ciudades" in configuracion:
        return len(configuracion["ciudades"])
    return configuracion["longitud_gen"]


def puntos_grafico(historial):
    """Tiempo medio hasta el óptimo por tipo de problema y tamaño N."""
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


def dibujar_grafico(puntos, ruta):
    """Dibuja N frente al tiempo hasta el óptimo y lo guarda en ruta."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # dibuja a un archivo, sin abrir ventanas
        import matplotlib.pyplot as plt
    except ImportError:
        print("No se puede dibujar el gráfico: falta matplotlib (pip3 install matplotlib).")
        return False

    dibujado = False
    plt.figure()
    for tipo, lista in puntos.items():
        if len(lista) < 2:
            continue
        xs = [n for n, _ in lista]
        ys = [t for _, t in lista]
        plt.plot(xs, ys, marker="o", label=tipo)
        dibujado = True

    if dibujado:
        plt.xlabel("Tamaño del problema (N)")
        plt.ylabel("Segundos hasta alcanzar el óptimo")
        plt.title("Rendimiento del algoritmo genético")
        plt.legend()
        plt.savefig(ruta)
    plt.close()
    return dibujado


def preguntar_si_no(pregunta):
    """Repite la pregunta hasta que el usuario responda Si o No."""
    while True:
        respuesta = input(f"{pregunta} (Si/No): ").strip().lower()
        if respuesta in ("si", "sí", "s"):
            return True
        if respuesta in ("no", "n"):
            return False
        print("Responde Si o No.")


def exportar_resultados(cleaned_data):
    """Opción 5: exporta el historial a JSON y, si se pide, dibuja el gráfico."""
    historial = cleaned_data.get("historial", [])
    if not historial:
        print("No hay resultados todavía: ejecuta primero con la opción 3.")
        return

    salida = cleaned_data.get("salida")
    if not isinstance(salida, dict):
        salida = {}

    if "guardar_en" not in salida:
        print("No hay salida declarada en el último archivo cargado.")
        if not preguntar_si_no("¿Desea exportarlo en resultados.json?"):
            print("No se exporta nada.")
            return
        salida = {**salida, "guardar_en": "resultados.json"}

    ruta = salida["guardar_en"]
    try:
        cuantas = guardar_resultados(historial, cleaned_data.get("tiempos_tanda", []), ruta)
    except OSError as error:
        print(f"No se pudo escribir {ruta}: {error}")
        return

    print(f"Guardadas {cuantas} ejecuciones en {ruta}")

    if salida.get("grafico_rendimiento"):
        ruta_grafico = os.path.splitext(ruta)[0] + "_rendimiento.png"
        puntos = puntos_grafico(historial)

        if not any(len(lista) >= 2 for lista in puntos.values()):
            print("No se generó el gráfico: hacen falta problemas del mismo tipo con "
                  "optimo_conocido, de al menos 2 tamaños distintos, que hayan llegado al óptimo.")
        elif dibujar_grafico(puntos, ruta_grafico):
            print(f"Gráfico guardado en {ruta_grafico}")
