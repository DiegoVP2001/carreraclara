# Prompt para iniciar la Tarea 3 — Loader/normalizador

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para arrancar la Tarea 3 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto, `PLAN.md` (plan maestro completo, sección "Tarea 3"), `mifuturo/NOTAS_CRUCE.md` (auditoría de Tarea 1) y **`mifuturo/MODELO_DATOS.md`** (esquema de Tarea 2 — es el contrato exacto que debe producir este loader) para tener el contexto completo antes de empezar.

**Tu tarea (Tarea 3 del plan maestro): escribir el primer código de producción del proyecto — un script Python (pandas/openpyxl) que lea los 4 Excel de `mifuturo/` y produzca las tablas definidas en `mifuturo/MODELO_DATOS.md`.** El script es la fuente de verdad (convención del workspace, ver `CLAUDE.md` raíz): se regenera, no se edita el output a mano.

Concretamente, el script debe:

1. **Resolver los quirks de parsing ya conocidos** (documentados en `CLAUDE.md`, `PLAN.md`, y ya resueltos una vez en `mifuturo/auditoria_tarea1.py` — puedes reusar esa lógica de `find_header_row`/`normalize_code`): hoja correcta por archivo, fila de encabezado real (no la decorativa), normalización de códigos de institución (`float` con NaNs → `int`/`str`), encoding (usar `PYTHONIOENCODING=utf-8` o escribir a archivo, nunca `print()` directo de strings con tildes en consola Windows).

2. **Construir las 2 dimensiones de `MODELO_DATOS.md`:**
   - `dim_institucion` desde `Buscador_Instituciones`, clave `Código institución`.
   - `dim_carrera_generica` desde los valores únicos de `Nombre carrera genérica` del ancla, con `area` (constante por genérica, confirmado en Tarea 2) y una columna `familia` que queda `NULL` por ahora (decisión 3 de `MODELO_DATOS.md` — la curaduría manual es deuda explícita, no se resuelve en esta tarea).

3. **Construir los 3 hechos de `MODELO_DATOS.md`:**
   - `hecho_indicadores` desde el ancla: **excluir explícitamente la fila de nota al pie** (buscar `"FUENTE:"` en cualquier columna, como hace `auditoria_tarea1.py`), mapear `s/i` → `NULL`, normalizar `Código` a int.
   - `hecho_oferta` desde `Buscador_de_Carreras`: unir a `dim_carrera_generica` vía `Área Carrera Genérica` (el puente confirmado al 99.47% en Tarea 2, no vía `Nombre carrera`), dejando `nombre_carrera_generica = NULL` para el ~23% de categorías "otros"/"bachillerato" que no resuelven (decisión 7 de `MODELO_DATOS.md` — no se fuerza un match incorrecto).
   - `hecho_benchmark_nacional` desde `Buscador_EstadísticasCarrera`: aplicar la corrección de typo `"Insitutos Profesionales"` → `"Institutos Profesionales"` en `Tipo de institución` (Tarea 1), `s/i` → `NULL` en las columnas de ingreso/empleabilidad, **sin cruzar contra institución individual** (se mantiene a su grano carrera genérica × tipo de institución).

4. **Validaciones mínimas al final del script** (no es la auditoría completa de Tarea 4, solo un chequeo de sanidad antes de confiar en el output): cantidad de filas por tabla, cantidad de FKs de institución/carrera que no resuelven (cuántas quedan `NULL` o "colgantes"), y que la fila de nota al pie efectivamente desapareció. Imprime estos números a un archivo de log (mismo patrón que `auditoria_tarea1_output.txt`), no a consola.

5. **Output:** decide entre CSV, Parquet o sqlite local para las 5 tablas (2 dimensiones + 3 hechos) — justifica brevemente la elección en un comentario corto al inicio del script o en el mensaje final, considerando que la Tarea 5 (capa de consulta) leerá este output. Si usas sqlite, una sola conexión con 5 tablas; si usas CSV/Parquet, un archivo por tabla en una carpeta de salida nueva (ej. `mifuturo/processed/` o similar — decide la ubicación y díselo a Diego).

**No diseñes el modelo de datos de nuevo ni decidas resolver la deuda pendiente de `familia` o del 23% de `Área Carrera Genérica` sin resolver** — esas son decisiones ya tomadas como deuda explícita en `MODELO_DATOS.md` (sección 8); el loader las respeta tal cual, no las resuelve por su cuenta. Si durante la implementación encuentras algo que contradiga una decisión del esquema (ej. un `Área` que sí varía dentro de una genérica, o un patrón de `s/i`/`n/a` distinto al documentado), **detente y avisa antes de improvisar** — puede ser una corrección al esquema de Tarea 2, no algo que el loader deba decidir solo.

Al terminar, actualiza el estado de la Tarea 3 en `PLAN.md` (de "lista para iniciar" a "completada", con un resumen de 2-3 líneas de las decisiones de implementación y la ubicación del output), y desbloquea la Tarea 4.
