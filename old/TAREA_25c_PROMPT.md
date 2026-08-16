# TAREA 25c — Cerrar T25-1 documentando la decisión, y dejar una guía de fuentes de datos

## Contexto de arranque en frío

Proyecto: `comparador_carreras` / **Carrera Clara** — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl, en producción en [carreraclara.cl](https://carreraclara.cl) (Vercel, root `web/`, sin build step).

**Estado al inicio de esta tarea:**
- MVP completo y desplegado. T24 ("Qué NEM necesito") y T25 (auditoría de datos) cerradas.
- Cuatro páginas canónicas:

| Página | Archivo | URL en producción |
|---|---|---|
| Portada | `web/landing.html` | `/` |
| Tipos de carrera | `web/index_v2.html` | `/tipos-de-carrera` |
| Carreras por institución | `web/instituciones_v2.html` | `/carreras-por-institucion` |
| Qué NEM necesito | `web/nem.html` | `/que-nem-necesito` |

## Por qué existe esta tarea

`TAREA_25b_PROMPT.md` partió de un hallazgo real de T25 (hallazgo T25-1, ver `AUDITORIA_DATOS_T25.md`): 1183 combinaciones institución+carrera-genérica tienen oferta real (arancel, vacantes, ponderaciones PAES) en `hecho_oferta` pero son invisibles en "Carreras por institución", porque esa pantalla se construye solo desde `hecho_indicadores` (grano institución×título).

Antes de implementar, se discutió el enfoque con Diego (sesión previa a esta). La conversación llegó a una conclusión **distinta** a la que proponía el prompt original: **no se agregan esos 1183 combos a `instituciones.json`/`instituciones_v2.html`.** Ver "Decisiones ya tomadas" abajo para el razonamiento completo — no se repite el análisis, ya está cerrado.

Diego pidió, en vez de tocar código, dejar bien documentada esta distinción entre fuentes de datos (grano y cobertura distintos) para que sesiones futuras que quieran construir algo nuevo sepan de entrada a qué tabla/export ir, sin tener que redescubrir la brecha desde cero como pasó en T24→T25→T25b.

## Qué hace esta tarea

1. **Crear una guía de fuentes de datos nueva**, sugerida como `GUIA_FUENTES_DE_DATOS.md` en la raíz del proyecto (junto a `PLAN.md`/`CLAUDE.md`). No es un reemplazo de `mifuturo/MODELO_DATOS.md` (ese es el contrato de esquema/loader, Tarea 2, y debe seguir siendo la referencia de columnas/tipos) ni de `AUDITORIA_DATOS_T25.md` (ese es un reporte puntual de auditoría, con fecha y alcance fijo). Esta guía nueva es un documento vivo, orientado a "voy a construir una función nueva, ¿a qué fuente voy y qué me puede/no me puede dar".
2. **Documentar explícitamente, dentro de esa guía, la decisión de T25-1/T25b** (no agregar los 1183 combos a "Carreras por institución", con el razonamiento) para que quede registrada de forma permanente y no se vuelva a investigar desde cero en una sesión futura.
3. **Corregir un `aria-label` desactualizado** en `web/instituciones_v2.html` línea ~1600: dice `"Mostrar todas las carreras de esa institución"`, y ya no es exacto una vez confirmada la decisión de no mostrar el universo completo de oferta. Cambiar a un texto que no prometa exhaustividad (ej. algo en la línea de "Mostrar las carreras con datos disponibles de esa institución" — el agente puede ajustar la redacción exacta).
4. **Cierre de sesión estándar** (ver regla del `CLAUDE.md` del proyecto): marcar T25b como completada en `PLAN.md` con el resumen de esta decisión, mover `TAREA_25b_PROMPT.md` a `old/`, y mover este mismo prompt a `old/` una vez Diego apruebe el resultado.

## Decisiones ya tomadas (no volver a discutir)

- **No se agregan los 1183 combos institución+genérica-sin-título a `instituciones.json`/`instituciones_v2.html`.** Razones acordadas con Diego:
  - `hecho_oferta` (fuente de esos 1183) no tiene, ni tendrá nunca, columnas de empleabilidad/ingreso/retención — son estructuralmente inexistentes en esa tabla (confirmado revisando `mifuturo/loader.py`), no "a veces faltan". Agregar esos combos metería ~41% de filas nuevas con las 3 columnas centrales de la página (el eje de comparación que le da sentido a esta pantalla) permanentemente vacías.
  - El mismo pool de 1183 ya está cubierto por `web/nem.html`/`instituciones_nem.json` (T24), que es la pantalla correcta para ese ángulo del dato (qué NEM/PAES necesito, no qué resultado obtuve). No se pierde información real del sitio al no duplicarlo acá.
  - Es fiel a cómo SIES/mifuturo.cl separa estos dos datasets (una encuesta retrospectiva de egresados vs. datos de oferta/admisión vigente) — no es una limitación artificial de nuestro modelo de datos.
- **Esta tarea es documentación + un fix cosmético de 1 línea, no una reapertura de la implementación de T25b.** No se vuelve a evaluar si conviene agregar los combos — eso ya se decidió.
- **La guía nueva no reemplaza `MODELO_DATOS.md` ni `AUDITORIA_DATOS_T25.md`, los complementa** — no fusionar contenido, solo referenciar/linkear entre ellos donde corresponda.

## Contenido mínimo que debe tener la guía nueva

Para no repetir el análisis ya hecho en la sesión de T25b, la guía debe cubrir al menos:

1. **Para cada uno de los 3 hechos** (`hecho_indicadores`, `hecho_oferta`, `hecho_benchmark_nacional`): grano, qué preguntas de estudiante responde bien, qué preguntas **no puede responder nunca** (estructural, no solo "a veces falta"), qué export/JSON ya lo consume hoy, y qué función de `mifuturo/queries.py` o de los scripts de export (`resolver_arancel`, `resolver_ponderaciones`, `resolver_tiene_oferta_nem` en `web/export_instituciones.py`) ya resuelve el cruce institución+carrera — para que una sesión futura no reinvente ese cruce.
2. **Tabla de números de T25** (re-verificar contra `comparador.db` en el momento de escribir, no solo confiar en estos): pares institución+genérica en `hecho_oferta` (2652), en `hecho_indicadores` (1690), solo en `hecho_oferta` (1183), solo en `hecho_indicadores` (221), en ambos (1469) — con link a `AUDITORIA_DATOS_T25.md` para el detalle completo.
3. **Un ejemplo real concreto** que ilustre el contraste (ya verificado en la sesión de T25b, reproducible con SQL directo sobre `comparador.db`):
   - Universidad de Santiago de Chile + Derecho: solo en `hecho_oferta` (arancel $6.535.000, 200 vacantes, ponderación PAES real NEM10%/Ranking40%/Lenguaje20%/Matemática10%), sin fila en `hecho_indicadores`.
   - Universidad de Santiago de Chile + Arquitectura: en ambas fuentes — mostrar qué aporta cada una (empleabilidad/ingreso/retención de una vs. arancel/vacantes/ponderación PAES de la otra) para dejar claro que cuando ambas existen, son complementarias, no redundantes.
4. **El registro de la decisión T25-1/T25b** (sección "Decisiones ya tomadas" de arriba, resumida).

## Archivos que probablemente se tocan

- `GUIA_FUENTES_DE_DATOS.md` (nuevo, raíz del proyecto)
- `web/instituciones_v2.html` (aria-label línea ~1600)
- `PLAN.md` (cierre de T25b)

## Criterio de "tarea completa"

- La guía nueva existe, cubre los 4 puntos de arriba, y sus números/ejemplos están re-verificados contra `comparador.db` en el momento de la sesión (no solo copiados de este prompt).
- El `aria-label` corregido no promete mostrar "todas" las carreras.
- `PLAN.md` marca T25b como completada, con el resumen de la decisión (2 líneas, mismo formato que el resto de la tabla de roadmap).
- `TAREA_25b_PROMPT.md` movido a `old/`.
- Revisado y aprobado por Diego antes de mover este mismo prompt (`TAREA_25c_PROMPT.md`) a `old/`.

## Recordatorio de flujo

Este proyecto avanza por sesiones aprobadas: **plan → aprobación explícita de Diego → ejecución**. Esta tarea es mayormente documentación (bajo riesgo), pero igual cierra con la aprobación de Diego antes de mover archivos a `old/` o marcar T25b como completada en `PLAN.md`.
