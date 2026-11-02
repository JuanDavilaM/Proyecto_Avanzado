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