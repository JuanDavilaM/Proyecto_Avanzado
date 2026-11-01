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