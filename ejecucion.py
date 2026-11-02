#prepara cada ejecución del json y la lanza contra el motor genético.

import ga_engine
import problemas


def formatear_tiempo(segundos):
    
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    resto = segundos - horas * 3600 - minutos * 60
    return f"{horas}h {minutos}m {resto:.2f}s"
