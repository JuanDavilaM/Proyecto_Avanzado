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