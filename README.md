# Solucionador de algoritmos genéticos en paralelo

Proyecto de la asignatura *Herramientas de Programación para la Ciencia de Datos y la IA* (Máster en IA y Ciencia de Datos, CUNEF).

Programa de línea de comandos que lee problemas desde un archivo JSON, los resuelve con un algoritmo genético repartiendo las ejecuciones entre varios núcleos, mide sus tiempos y exporta los resultados. Resuelve dos problemas: **OneMax** y el **problema del viajante (TSP)**.

**Equipo:** Juan Pablo Dávila, Ricardo Mataix y David Martín Montalbán.

## Instalación

Requiere Python 3.10 o superior.

```bash
git clone https://github.com/JuanDavilaM/Proyecto_Avanzado.git
cd Proyecto_Avanzado
pip install -r requirements.txt
```

## Uso

```bash
python cli.py
```

| Opción | Qué hace |
|---|---|
| 1. Cargar archivo de problemas | Lee un JSON, lo expande en ejecuciones individuales y borra el historial anterior |
| 2. Ajustar parámetros de ejecución | Cambia el número de núcleos de la sesión sin editar el JSON |
| 3. Ejecutar todo | Resuelve en paralelo las ejecuciones pendientes (una *tanda*); si ya están hechas, pregunta si repetirlas |
| 4. Consultar estado | Archivo, núcleos, ejecuciones cargadas y pendientes con su configuración, e historial con resultados y tiempos |
| 5. Exportar resultados | Guarda el historial en JSON y, si se pide, el gráfico de rendimiento |
| 6. Salir | Termina el programa (también con Ctrl+C) |

Ejemplo rápido: `1` → `ejemplos/ejemplo_completo.json` → `3` → `4` → `5`.

## Formato del archivo JSON

### Formato simple (un problema)

```json
{
  "tipo": "onemax",
  "tamano_poblacion": 20,
  "num_generaciones": 30,
  "tasa_mutacion": 0.1,
  "longitud_gen": 10
}
```

### Formato completo

```json
{
  "problemas_onemax": [
    {"tamano_poblacion": 20, "num_generaciones": 30, "tasa_mutacion": 0.1, "longitud_gen": 10, "optimo_conocido": 10},
    {"tamano_poblacion": [20, 50], "num_generaciones": 30, "tasa_mutacion": [0.05, 0.1, 0.2], "longitud_gen": 15}
  ],
  "problemas_tsp": {
    "tamano_poblacion": 50, "num_generaciones": 200, "tasa_mutacion": 0.2,
    "ciudades": [[17, 72], [97, 8], [32, 15], [63, 97]]
  },
  "salida": {"guardar_en": "resultados.json", "grafico_rendimiento": true},
  "num_nucleos": 4
}
```

`problemas_onemax` y `problemas_tsp` admiten un problema o una lista. Si `tamano_poblacion`, `num_generaciones` o `tasa_mutacion` son una lista, se ejecuta cada combinación (rejilla): el segundo problema de arriba genera 2 × 3 = 6 ejecuciones.
`semilla` también admite una lista: `"semilla": [1, 2, 3, 4]` lanza el mismo problema con cuatro semillas distintas, que se resuelven en paralelo; así se puede quedar el mejor resultado.

### Claves de cada problema

| Clave | Obligatoria | Descripción |
|---|---|---|
| `tamano_poblacion` | Sí | Entero ≥ 1, o lista (rejilla) |
| `num_generaciones` | Sí | Entero ≥ 1, o lista (rejilla) |
| `tasa_mutacion` | Sí | Número entre 0 y 1, o lista (rejilla) |
| `longitud_gen` | OneMax | Número de bits |
| `ciudades` | TSP | Lista de coordenadas `[x, y]`; la matriz de distancias se calcula a partir de ellas |
| `optimo_conocido` | No | Para medir el tiempo hasta alcanzarlo. En OneMax, si falta, se usa `longitud_gen` |
| `estrategia` | No | `"basico"` o `"memetico"` (solo TSP). Por defecto, memético en TSP y básico en OneMax |
| `num_busqueda_local` | No | Hijos mejorados con 2-opt por generación en el memético (3 por defecto) |
| `num_elites` | No | Mejores individuos que pasan intactos a la siguiente generación (1 por defecto) |
| `tamano_torneo` | No | Participantes de cada torneo de selección (2 por defecto) |
| `semilla` | No | Entero, o lista para lanzar el mismo problema con varias semillas en paralelo (por defecto, el id de la ejecución) |

`salida` y `num_nucleos` son opcionales. Si `num_nucleos` supera los núcleos de la máquina, se usan todos y se avisa.

## Estructura del proyecto

| Archivo | Responsabilidad |
|---|---|
| `cli.py` | Menú y estado de la sesión (punto de entrada) |
| `io_json.py` | Lectura del JSON y expansión en ejecuciones individuales |
| `ejecucion.py` | Validación, preparación de cada problema y lanzamiento contra el motor |
| `paralelo.py` | Núcleos disponibles y ejecución en paralelo con `multiprocessing.Pool` |
| `ga_engine.py` | Motor genérico del algoritmo genético: recibe las funciones del problema y sus datos por `*args` |
| `problemas.py` | OneMax y TSP: generadores, fitness, cruces, mutaciones y búsqueda local 2-opt |
| `estado.py` | Tablas de la opción 4 |
| `exportar.py` | Opción 5: JSON de resultados y gráfico de rendimiento |
| `comparar_estrategias.py` | Comparación entre el GA básico y el memético |
| `prueba_motor.py`, `prueba_validacion.py` | Pruebas del motor y de la validación |
| `ejemplos/` | Archivos JSON de ejemplo |
| `docs/decisiones.md` | Decisiones de diseño y ambigüedades del enunciado |

## Funcionalidad original: GA memético para TSP

Además de cruzar y mutar, en cada generación el algoritmo mejora algunos hijos con la búsqueda local **2-opt**, que elimina los cruces de la ruta. Con la misma población (100) y las mismas generaciones (300):

| Instancia | GA básico | GA memético | Mejora |
|---|---|---|---|
| TSP de 60 ciudades | 10.192 | 6.293 | −38 % |
| TSP de 100 ciudades | 19.096 | 7.763 | −59 % |

Para reproducirlo:

```bash
python comparar_estrategias.py        # tabla y gráfico de convergencia (100 ciudades)
python comparar_estrategias.py 60     # con otro número de ciudades
```

O desde el menú: `1` → `ejemplos/tsp_100_estrategias.json` → `3` → `4`.

## Pruebas

```bash
python prueba_motor.py        # OneMax, TSP en círculo con óptimo conocido y 2-opt
python prueba_validacion.py   # datos correctos e incorrectos del JSON
```