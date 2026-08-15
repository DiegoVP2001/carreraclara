# TAREA 26 — Brainstorm: qué construir con toda la data disponible

## Contexto de arranque en frío

Proyecto: `comparador_carreras` / **Carrera Clara** — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl, en producción en [carreraclara.cl](https://carreraclara.cl) (Vercel, root `web/`, sin build step).

**Estado al inicio de esta tarea:**
- MVP completo y desplegado, 4 herramientas en producción (Tipos de carrera, Carreras por institución, Qué NEM necesito, más la portada).
- **Corre después de T25** (auditoría de datos no considerados por error) — **leer su informe primero**. Esta sesión parte de un inventario más completo de qué datos existen realmente (cargados, exportados, o solo disponibles en la fuente) en vez de partir solo de lo que ya se muestra hoy.

## Por qué existe esta tarea

T24 mostró que había una herramienta entera (NEM/PAES real de matrícula) escondida en datos que ya estaban cargados hace sesiones — nadie había preguntado "¿qué más hay ahí que no estamos usando?". Esta tarea es esa pregunta, a propósito, sin comprometerse todavía a construir nada.

## Qué hace esta tarea

**Es una sesión de ideación, no de implementación.** El objetivo es generar y evaluar (no construir) ideas de nuevas herramientas/pantallas/features usando:
1. Los datos que **ya se exportan y se muestran** hoy, pero combinados de formas nuevas.
2. Los datos que T25 encontró **cargados pero no exportados**, o **exportados pero no mostrados**.
3. Los tres datasets nunca integrados — `matricula/`, `titulados/`, `personal/` — evaluando por primera vez qué aportarían si se integraran (sin comprometerse a hacerlo).

El backlog "Post-MVP" que ya existe en `PLAN.md` (Ficha de institución, Drawer glosario completo, Fuzzy-match arancel Nivel 2) son candidatos conocidos, no el punto de partida — la idea es no limitarse a esa lista.

## Cómo abordar la sesión

Este es exactamente el tipo de trabajo ambiguo para el que existe la skill `conoce-tus-incognitas` (ver `~/.claude/CLAUDE.md`: "para trabajo ambiguo, en un dominio nuevo, o antes de comprometerme a una versión final"). En particular pueden servir:

- **Blindspot pass** sobre los datos de T25 — qué hay ahí que ni se nos había ocurrido preguntar.
- **Cuatro direcciones de diseño** — en vez de una sola propuesta, generar variantes con ángulos distintos (ej. una dirección orientada a "decisión de postulación", otra a "comparación exploratoria", otra a "seguimiento de una institución específica").
- **Entrevista antes de proponer** — si hay ambigüedad real sobre qué problema del estudiante se está resolviendo, preguntarle a Diego antes de generar 10 ideas al aire.

No hace falta pedir la skill explícitamente — aplicar sus técnicas donde tengan sentido.

## Qué NO hacer en esta sesión

- No escribir código ni crear archivos nuevos de producto (HTML, exports, etc.).
- No comprometerse a una sola idea "ganadora" — el entregable es un mapa de opciones con su viabilidad, no una decisión final.
- No repetir el ejercicio de "¿qué falta en los datos?" — eso ya lo hizo T25; esta tarea parte de sus hallazgos, no los re-investiga.

## Qué sí entregar

Para cada idea generada, idealmente:
- **Qué resuelve** para el estudiante (no "qué dato muestra" — qué decisión ayuda a tomar).
- **Con qué datos ya disponibles se puede construir hoy** vs. **qué requeriría integrar algo nuevo** (`matricula/`, `titulados/`, `personal/`, o una fuente externa como puntajes de corte DEMRE — ver "Pendiente, explícitamente no ahora" en `PLAN.md`).
- **Tamaño aproximado** (¿es una sesión, o varias?) — sin comprometerse a un número, solo para priorizar.

## Archivos que probablemente se leen

- `PLAN_HISTORIAL.md` (visión y roadmap original del proyecto, sección de pantallas planeadas)
- El informe de T25 (nombre exacto a confirmar cuando esa tarea cierre)
- `mifuturo/MODELO_DATOS.md`
- Los 4 archivos HTML canónicos, para entender qué tan caro es agregar una pantalla nueva vs. extender una existente

## Criterio de "tarea completa"

- Un documento o resumen con las ideas generadas, evaluadas con el criterio de arriba.
- Diego elige (o no) una dirección para convertir en la próxima `TAREA_N_PROMPT.md` — esa siguiente tarea sí puede ya ser de implementación.
- `PLAN.md` marcado T26 ✅ con un resumen de 2 líneas de qué dirección(es) quedaron priorizadas.

## Recordatorio de flujo

Este proyecto avanza por sesiones aprobadas: **plan → aprobación explícita de Diego → ejecución**. Para esta tarea en particular, "aprobación" probablemente significa que Diego elige qué idea(s) seguir, no que apruebe una implementación — no hay código que ejecutar en esta sesión.
