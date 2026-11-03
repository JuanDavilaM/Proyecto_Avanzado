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
