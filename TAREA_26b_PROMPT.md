# TAREA 26b — Discutir los hallazgos de T26 y decidir dirección

## Contexto de arranque en frío

Proyecto: `comparador_carreras` / **Carrera Clara** — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl, en producción en [carreraclara.cl](https://carreraclara.cl) (Vercel, root `web/`, sin build step).

**Estado al inicio de esta tarea:**
- MVP completo y desplegado, 4 herramientas en producción (Tipos de carrera, Carreras por institución, Qué NEM necesito, portada).
- T25 (auditoría de datos) y T25b (decisión de cobertura en "Carreras por institución") completadas y aprobadas.
- **T26 (brainstorm) generó `BRAINSTORM_T26.md`** — léelo completo antes de arrancar. Combina dos cosas: ideas basadas en datos ya cargados pero no usados (auditoría T25) e ideas de una investigación de 8 subagentes en paralelo sobre comparadores de carreras/universidades reales (Chile, Latinoamérica, EE.UU., Reino Unido, Europa, Australia — ~55 hallazgos concretos). El documento propone 6 direcciones temáticas, una tabla resumen de 19 ideas priorizables, una sección de ideas aspiracionales fuera de alcance, y 6 "tandas" de ejecución sugeridas — pero **nada de eso está decidido todavía**.
- `TAREA_27_PROMPT.md` ya existe en la raíz, redactado **antes** de que arrancara T26, para "Ficha de institución" (pantalla nueva por institución, post-MVP). Sigue en cola, sin ejecutar. Puede que siga siendo la prioridad correcta, o puede que esta sesión decida que otra idea del brainstorm va primero — no se prejuzga acá.
- T26 **no está marcada como completada** en `PLAN.md` — esta sesión es la que la cierra, una vez que haya una dirección clara.

## Por qué existe esta tarea

Diego leyó `BRAINSTORM_T26.md` y no tiene todavía criterio armado sobre qué priorizar — hay demasiadas ideas nuevas (19 en la tabla resumen, más las aspiracionales) como para elegir a partir de una lista fría. Esta tarea existe para que la resolución de esa duda no pase por generar más documentos unilateralmente, sino por **discutir con Diego**, punto por punto donde haga falta, hasta que la prioridad quede clara para los dos.

## Qué hace esta tarea

**Es una sesión de conversación y decisión, no de generación de contenido nueva ni de implementación.** El objetivo es recorrer `BRAINSTORM_T26.md` con Diego — no leérselo de vuelta, sino discutirlo: qué le genera dudas, qué le entusiasma, qué le parece que no aplica, qué faltó. De esa conversación puede salir:

- Una tanda (o combinación de tandas) priorizada, lista para convertirse en la próxima `TAREA_N_PROMPT.md` de implementación.
- Ideas nuevas que la conversación destape y que el brainstorm original no capturó — está bien agregarlas al documento si surgen.
- Una respuesta a la pregunta abierta que quedó pendiente en `BRAINSTORM_T26.md`: si vale la pena reabrir la evaluación de integrar puntaje de corte histórico DEMRE (salió como el hallazgo más repetido de toda la investigación externa, pero implica una fuente de datos nueva que `PLAN.md` tenía marcada como "pendiente, explícitamente no ahora").
- Una decisión sobre el conflicto de numeración: si la dirección elegida no es "Ficha de institución", hay que decidir qué pasa con `TAREA_27_PROMPT.md` (¿se ejecuta después, se renumera, se descarta por ahora?).

## Cómo abordar la sesión

Esto es exactamente el tipo de situación para la que existe la skill `conoce-tus-incognitas` (ver `~/.claude/CLAUDE.md`) — en particular:

- **Entrevista antes de proponer**: no asumir que ya se sabe qué quiere Diego a partir del brainstorm escrito; preguntar directamente sobre los puntos donde hay ambigüedad real (ej. "¿te preocupa más resolver la admisión, o diferenciarte de la competencia con el test vocacional?").
- **Cuatro direcciones de diseño** ya están, de hecho, servidas en el documento (las 6 direcciones temáticas) — usarlas como punto de partida de la conversación, no repetir el ejercicio de generarlas de nuevo.
- **Quiz antes de aprobar**: antes de dar la dirección por decidida, resumirle a Diego en 2-3 frases qué se va a construir y confirmar que es realmente eso lo que quiere, no una interpretación aproximada.

No hace falta pedir la skill explícitamente — aplicar sus técnicas donde tengan sentido, en particular la conversación debe sentirse como ida y vuelta, no como un monólogo seguido de una pregunta de sí/no.

## Qué NO hacer en esta sesión

- No escribir código ni tocar ningún archivo de `web/`, `mifuturo/`, ni los exports.
- No generar un documento nuevo de ideas — `BRAINSTORM_T26.md` ya existe; esta sesión lo discute y, si acaso, lo edita con lo que surja, no lo reemplaza.
- No asumir una dirección "obvia" a partir de la recomendación que ya se dio en la sesión anterior (Calculadora de ponderación PAES completa) — esa era una recomendación, no una decisión tomada; la conversación puede terminar confirmándola, cambiándola, o combinando varias tandas.

## Qué sí entregar

- Una dirección clara (una tanda, varias, o una idea nueva surgida en la conversación) que Diego confirme explícitamente que quiere seguir.
- `BRAINSTORM_T26.md` actualizado si la conversación generó ideas nuevas o cambió el orden de prioridad sugerido.
- `PLAN.md` marcado T26 ✅ con un resumen de 2 líneas de qué dirección quedó priorizada.
- El siguiente `TAREA_N_PROMPT.md` de implementación, generado a partir de la dirección elegida — con la numeración resuelta respecto al conflicto con `TAREA_27_PROMPT.md` (Ficha de institución) ya existente.

## Recordatorio de flujo

Este proyecto avanza por sesiones aprobadas: **plan → aprobación explícita de Diego → ejecución**. Acá "aprobación" es literalmente el objetivo de la sesión — no hay nada que ejecutar hasta que la conversación llegue a una dirección que Diego confirme con sus propias palabras, no con un "ok" a una propuesta ya armada.
