# Prompt para iniciar la Tarea 4 — Validación de calidad de datos

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para arrancar la Tarea 4 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto, `PLAN.md` (plan maestro completo, sección "Tarea 4"), `mifuturo/MODELO_DATOS.md` (esquema de Tarea 2 — contiene las "deudas explícitas" de la sección 8, que son justamente lo que esta tarea debe cuantificar a fondo) y **`mifuturo/loader_log.txt`** (validaciones mínimas ya hechas por el loader de Tarea 3 — son el punto de partida, no la auditoría completa) para tener el contexto completo antes de empezar. El loader en sí está en `mifuturo/loader.py` y su output ya cargado en `mifuturo/processed/comparador.db` (sqlite, 5 tablas: `dim_institucion`, `dim_carrera_generica`, `hecho_indicadores`, `hecho_oferta`, `hecho_benchmark_nacional`).

**Tu tarea (Tarea 4 del plan maestro): escribir un script Python de auditoría de calidad de datos que vaya más allá de las validaciones mínimas del loader** — el loader solo confirma que el output "no se rompió" (conteos de filas, FKs colgantes, nota al pie fuera). Esta tarea cuantifica y reporta a fondo la cobertura real y las sorpresas, leyendo `comparador.db` (no los Excel crudos — ese trabajo ya lo hizo el loader).

Concretamente, el script debe:

1. **Cobertura cruzada carrera genérica, en detalle (no solo el % agregado que ya se reportó en Tareas 1–3):**
   - Listar explícitamente las genéricas del ancla (`dim_carrera_generica`) que NO tienen ninguna fila en `hecho_benchmark_nacional` — ya sabemos que son ~26 (Tarea 1) / 1 caso inverso, pero esta tarea debe producir la lista completa y nombrarlas, no solo el conteo.
   - Listar las genéricas que SÍ tienen `hecho_oferta` pero NO tienen `hecho_indicadores` (o viceversa) — caso no auditado aún explícitamente.
   - De las filas de `hecho_oferta` con `nombre_carrera_generica = NULL` (480/9900, ~4.85%), agrupar por `Área Carrera Genérica` original para ver si son pocas categorías "otros" concentrando muchas filas, o están dispersas — esto informa si vale la pena priorizar una tabla de equivalencias manual (deuda 2 de `MODELO_DATOS.md` sección 8).

2. **FKs de institución colgantes, con detalle:** de los 18 códigos de `hecho_indicadores` y 2 de `hecho_oferta` sin ficha en `dim_institucion`, listar los códigos concretos y, si es posible, cuántas filas de hecho representan en total (no solo cuántos códigos únicos) — para que se sepa si es una institución con 1 fila perdida o con cientos.

3. **El duplicado pendiente de Tarea 2 (deuda 4 de `MODELO_DATOS.md` sección 8):** investigar el `Código único de carrera` duplicado en `Buscador_de_Carreras`/`hecho_oferta` (9900 filas, 9899 valores únicos según el conteo de Tarea 2) — identificar cuál es, por qué se duplicó (¿fila idéntica repetida, o dos filas distintas con el mismo código por error de la fuente?), y recomendar qué hacer (deduplicar en el loader, o dejarlo si es un error real de SIES que no afecta el análisis).

4. **Revisar la semántica de `s/i` (deuda 5 de `MODELO_DATOS.md` sección 8):** confirmar sobre el dato ya cargado en `comparador.db` que no apareció ningún otro centinela adicional (`n/a`, vacío real, etc.) con significado distinto a `s/i` en las columnas numéricas de los 3 hechos — si aparece evidencia de que coexisten dos significados distintos de "vacío", reportarlo como hallazgo que requiere revisar el esquema (no decidirlo solo).

5. **No es obligatorio, pero si el tiempo alcanza:** alguna validación de rangos/sanidad básica (ej. ¿hay `empleabilidad_1er_anio` fuera de [0,1]? ¿`ingreso_4to_anio_*` negativos o absurdamente altos?) — un chequeo rápido de que los valores numéricos están en rangos plausibles, no una auditoría estadística exhaustiva.

**Output:** un log de texto (mismo patrón que `auditoria_tarea1_output.txt` y `loader_log.txt` — nunca `print()` directo de strings con tildes en consola Windows, usar `PYTHONIOENCODING=utf-8` o escribir a archivo). Sugerencia de nombre: `mifuturo/auditoria_tarea4_output.txt`, generado por un script `mifuturo/auditoria_tarea4.py` (mismo patrón de "el script es la fuente de verdad" del resto del workspace).

**No rediseñes el modelo de datos ni decidas resolver las deudas que encuentres** (familia, el 4.85%/23% de "otros" en oferta, el duplicado, etc.) — esta tarea es de medición y reporte, no de remediación. Si encuentras algo que contradiga una decisión ya tomada en Tarea 2 (ej. una genérica con `Área` que sí varía, cuando Tarea 2 confirmó 0 casos), o un patrón de dato sucio no documentado, **detente y avisa antes de improvisar una corrección** — puede requerir ajustar el esquema o el loader, no solo el reporte de auditoría.

Al terminar, actualiza el estado de la Tarea 4 en `PLAN.md` (de "lista para iniciar" a "completada", con un resumen de 2-3 líneas de los hallazgos más relevantes y si retroalimentan algo de Tareas 1/2/3), y desbloquea la Tarea 5.
