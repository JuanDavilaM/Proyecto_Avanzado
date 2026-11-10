# Registro de decisiones y ambigüedades

Cada vez que el enunciado admite varias interpretaciones, anotamos aquí cuál elegimos y por qué.

## 1. Significado de "anular" el número de núcleos (Secciones 8 y 9)
- **Ambigüedad:** "anular" podía entenderse como restar núcleos o como sustituir el valor.
- **Decisión:** sustituir. El usuario introduce directamente cuántos núcleos usar (entero entre 1 y los disponibles).
- **Motivo:** el enunciado dice "anular opcionalmente cuántos núcleos usar sin editar el JSON", es decir, sobrescribir el valor del archivo.

## 2. Entrada inválida al ajustar núcleos
- **Decisión:** se rechaza y se mantiene el valor anterior (opción permitida en la Sección 8).
- **Motivo:** evita bucles de reintento y la recursión.

## 3. Núcleos lógicos frente a físicos
- **Decisión:** usamos `os.cpu_count()`, que devuelve núcleos lógicos.
- **Motivo:** es lo que el sistema operativo puede planificar en paralelo y es estándar en Python; la librería estándar no da los físicos.

## 4. Datos de problemas en el repositorio
- **Decisión:** la carpeta `problemas/` está en `.gitignore`; los JSON del propio enunciado se guardan en `ejemplos/`.
- **Motivo:** el enunciado recomienda no subir datos, pero el equipo necesita casos de prueba comunes.

## 5. num_nucleos del JSON mayor que los núcleos de la máquina
- **Decisión:** se usan todos los núcleos disponibles y se avisa al usuario.
- **Motivo:** el archivo del hackathon puede haberse escrito para otra máquina; el programa no debe fallar por ello.

## 6. Nombre de la sección de salida: "salida" u "output"
- **Ambigüedad:** el texto de la Sección 4.4 dice "output" y el ejemplo JSON usa "salida".
- **Decisión:** se aceptan ambas claves (prioridad a "salida").

## 7. Estado de la sesión
- **Decisión:** todo el estado vive en un diccionario (`archivo`, `ejecuciones`, `salida`, `num_nucleos`, `historial`) creado en `main()` y pasado como argumento.
- **Motivo:** el enunciado prohíbe variables globales. Las ejecuciones forman una única lista, cada una con su `tipo` e `id`, para repartirlas directamente entre los procesos.

## 8. Carga fallida
- **Decisión:** si la carga de un archivo falla, se conserva el estado anterior.
- **Motivo:** un error al escribir la ruta no debe hacer perder los problemas ya cargados.

## 9. Gráfico con varias ejecuciones del mismo tamaño
Cuando varias ejecuciones tienen el mismo N, se dibuja la media de sus tiempos. Solo cuentan las que tienen optimo_conocido y llegaron a él. Es fácil de leer y da un único punto por tamaño.

## 10. Exportar resultados
El JSON guarda la configuración, el resultado y los tiempos de cada ejecución, más el tiempo total. matplotlib solo se carga al dibujar el gráfico: si falta, el programa avisa y sigue funcionando.

## 11. Qué claves admiten rejilla de hiperparámetros
- **Decisión:** solo `tamano_poblacion`, `num_generaciones` y `tasa_mutacion` se expanden cuando vienen como lista. Cualquier otra lista se conserva entera.
- **Motivo:** la §4.2 dice que la rejilla afecta solo a los hiperparámetros del solucionador y que `longitud_gen` y `ciudades` "se mantienen fijos". Así, un dato nuevo en forma de lista (por ejemplo, en el JSON del hackathon) no multiplica las ejecuciones.
- **Consecuencia:** si `longitud_gen` u `optimo_conocido` llegan como lista, la ejecución se rechaza con un mensaje de validación claro. Para resolver varios tamaños hay que escribir varios problemas en la lista (`problemas_onemax: [ {...}, {...} ]`), que es lo que indica la §4.1.

## 12. Validación de tipos
- **Decisión:** cada ejecución se valida antes de resolverla (tipos y rangos). `true`/`false` no se aceptan como números aunque en Python `bool` sea subclase de `int`.
- **Motivo:** el programa no debe fallar ante un JSON incorrecto, y el mensaje debe decir qué valor hay que corregir. Una ejecución inválida queda registrada con su error y no impide que se resuelvan las demás.

## 13. Elitismo
- **Decisión:** 1 élite por defecto (`num_elites`, configurable desde el JSON).
- **Motivo:** sin elitismo el mejor individuo se puede perder entre generaciones. No lo pide el enunciado; con `num_elites: 0` el motor se comporta como el del laboratorio.

## 14. Comparación con el óptimo conocido
- **Decisión:** se considera alcanzado con una tolerancia relativa de 1e-4.
- **Motivo:** las distancias son decimales y el JSON puede dar el óptimo redondeado.

## 15. Fitness del TSP
- **Decisión:** la distancia con signo negativo (no 1/distancia como en el laboratorio).
- **Motivo:** evita dividir por cero y permite recuperar la distancia exacta.

## 16. Matriz de distancias
- **Decisión:** se calcula una vez desde las coordenadas y no se redondea.
- **Motivo:** redondear cada tramo acumula error al sumar la ruta.

## 17. Significado de la tasa de mutación
- **Decisión:** probabilidad por gen en OneMax y por individuo en TSP.
- **Motivo:** en TSP un intercambio ya cambia dos ciudades; aplicarlo por gen destrozaría las rutas.

## 18. Semilla
- **Decisión:** por defecto, el id de la ejecución, fijada dentro de cada ejecución (configurable con `semilla`).
- **Motivo:** con multiprocessing en Windows cada proceso reimporta los módulos; una semilla global daría resultados idénticos. Es reproducible en la misma versión de Python.
- **Varias semillas:** `semilla` admite una lista y se expande como la rejilla, para lanzar el mismo problema con varias semillas en paralelo y quedarse con el mejor resultado (extensión propia de la §4.2).

## 19. Funcionalidad original: a qué individuos se aplica 2-opt
- **Decisión:** a 3 hijos elegidos al azar en cada generación (`num_busqueda_local`).
- **Motivo:** aplicado a los mejores, la búsqueda se estancaba (misma distancia en la generación 50 y en la 200). Con 3 se obtiene casi toda la mejora sin perder diversidad.

## 20. Estrategia por defecto en TSP
- **Decisión:** memética, salvo que el JSON indique `"estrategia": "basico"`.
- **Motivo:** no está claro si en el hackathon se podrán añadir claves al JSON; así se usa la mejor estrategia sin tocar nada. En un TSP de 100 ciudades reduce la distancia un 59 % con las mismas generaciones.

## 21. Historial por tandas
- **Decisión:** el historial es una lista de tandas, una por cada pulsación de la opción 3.
- **Motivo:** permite ejecutar varias veces el mismo archivo y saber de qué tanda es cada resultado.

## 22. Ids compuestos en el estado y en la exportación
- **Decisión:** cada resultado se identifica como `tanda.id` (por ejemplo, `2.3`).
- **Motivo:** el id de una ejecución se repite si se ejecuta varias veces; con la tanda delante, cada resultado es único.

## 23. Óptimo de OneMax por defecto
- **Decisión:** si un problema OneMax no trae `optimo_conocido`, se usa `longitud_gen`.
- **Motivo:** el óptimo de OneMax es, por definición, la cadena de todo unos; así siempre se mide el tiempo hasta el óptimo y el gráfico de rendimiento tiene datos.

## 24. Parar al alcanzar el óptimo
- **Decisión:** el algoritmo termina en cuanto alcanza `optimo_conocido` (`parar_en_optimo=True`).
- **Motivo:** una vez alcanzado el óptimo, seguir no puede mejorar el resultado y solo gasta tiempo.

## 25. Exportar sin salida declarada
- **Decisión:** si el archivo cargado no trae `salida.guardar_en`, la opción 5 pregunta si exportar en `resultados.json`.
- **Motivo:** el usuario puede guardar sus resultados aunque el JSON no lo indique, sin tener que editarlo.

## 26. Ejecuciones pendientes
- **Ambigüedad:** la opción 3 debe ejecutar "las ejecuciones pendientes" (§9), pero el programa debe permitir "ejecutarlo tantas veces como sea necesario" (§2).
- **Decisión:** al cargar un archivo, todas sus ejecuciones quedan pendientes. La opción 3 resuelve las pendientes y, si ya no queda ninguna, pregunta si repetirlas en una tanda nueva.
- **Motivo:** cumple las dos lecturas. El estado muestra cuántas hay cargadas, cuántas pendientes y los resultados guardados por tandas.

## 27. Repetir una tanda
- **Decisión:** una tanda repetida usa las mismas semillas, así que da los mismos resultados; solo cambian los tiempos.
- **Motivo:** los resultados son reproducibles. Para obtener resultados distintos se cambia `semilla` en el JSON, que admite una lista para lanzar varias a la vez.