# Prompt para iniciar la Tarea 5 — Capa de consulta para el comparador

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para arrancar la Tarea 5 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto, `PLAN.md` (plan maestro completo, secciones "Visión del proyecto" y "Tarea 5"), `mifuturo/MODELO_DATOS.md` (esquema de Tarea 2 — 2 dimensiones + 3 hechos) y **`mifuturo/auditoria_tarea4_output.txt`** (auditoría de calidad de Tarea 4 — cobertura real, deudas confirmadas/corregidas, rangos de valores) para tener el contexto completo antes de empezar. El modelo cargado vive en `mifuturo/processed/comparador.db` (sqlite, 5 tablas: `dim_institucion`, `dim_carrera_generica`, `hecho_indicadores`, `hecho_oferta`, `hecho_benchmark_nacional`).

**Tu tarea (Tarea 5 del plan maestro): definir y construir la capa de consulta** — las funciones/queries concretas que la fase 1 del comparador necesita pedirle a `comparador.db`, **todavía sin UI**. El persona principal es un estudiante explorando vocacionalmente; el scope es comparación **carrera vs. carrera** (no institución vs. institución todavía — eso es fase 2, ver `PLAN.md` sección "Pendiente, explícitamente no ahora").

Concretamente, a partir de la visión del proyecto y el modelo de datos, esta tarea debe:

1. **Listar las consultas concretas que la fase 1 necesita poder hacer**, por ejemplo (ajusta/completa según lo que encuentres en el modelo, esta lista es punto de partida no exhaustivo):
   - Listado de carreras genéricas con sus indicadores nacionales (`hecho_benchmark_nacional`) para comparar carrera vs. carrera — manejando explícitamente las 26 genéricas sin benchmark (deuda 8 confirmada en Tarea 4: deben mostrarse como "sin datos de comparación nacional", no ocultarse).
   - Detalle de una carrera genérica específica: instituciones que la imparten (`hecho_oferta` + `dim_institucion`), con sus indicadores propios (`hecho_indicadores`) cuando existan.
   - Manejo explícito de los casos NULL ya cuantificados en Tarea 4 (FKs de institución colgantes, `nombre_carrera_generica` nulo en `hecho_oferta`, `s/i`→NULL en indicadores) — la capa de consulta no debe "perder" silenciosamente esas filas, debe poder devolver el dato con su estado explícito (ej. "institución sin ficha", "sin benchmark nacional").
2. **Elegir cómo se expone la capa de consulta** (decisión de arquitectura a proponer, no asumida): ¿vistas SQL dentro de `comparador.db`, funciones Python con SQL parametrizado, o un módulo tipo repositorio con una función por consulta? Justifica la elección — recuerda que SQLite ya se eligió en Tarea 3 precisamente porque la Tarea 5 necesita joins entre las 5 tablas.
3. **Implementar las consultas elegidas** en un script/módulo Python (ej. `mifuturo/queries.py`), con una función por consulta, type hints, y un pequeño bloque de prueba (`if __name__ == "__main__":` o script separado) que las ejecute contra `comparador.db` y muestre output de ejemplo (mismo patrón de "nunca print() directo de strings con tildes en consola Windows" del resto del workspace — usar `PYTHONIOENCODING=utf-8` o escribir a archivo).
4. **No construir UI ni frontend todavía** — esta tarea es solo la capa de datos que la futura UI consumirá. Tampoco resuelvas las deudas pendientes que aparecen en los datos (familia sin curar, el 4.85%/dispersión de "otros" en oferta, la fila vacía de `hecho_oferta` encontrada en Tarea 4) — la capa de consulta debe *exponer* esos estados explícitamente, no resolverlos.

**Si encuentras que una consulta necesaria no es viable con el modelo actual** (ej. falta un índice, una columna, o el grano de alguna tabla no permite la pregunta que quiere hacer el estudiante), **detente y avisa antes de improvisar un cambio al esquema o al loader** — puede requerir ajustar `MODELO_DATOS.md`/`loader.py`, lo cual es una decisión a discutir, no a tomar sola en esta tarea.

Al terminar, actualiza el estado de la Tarea 5 en `PLAN.md` (de "lista para iniciar" a "completada", con un resumen de 2-3 líneas de las consultas implementadas y la decisión de arquitectura elegida), y abre/define la siguiente tarea (arquitectura de frontend/UI, actualmente listada como "fase 2/3" en "Pendiente, explícitamente no ahora").
