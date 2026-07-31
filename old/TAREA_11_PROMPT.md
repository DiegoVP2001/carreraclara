# Prompt para iniciar la Tarea 11 — Polish de tarjetas (íconos + hover + métricas titulares)

> Copia y pega el contenido de abajo al iniciar una nueva sesión de Claude Code en
> `comparador_carreras/` para ejecutar la Tarea 11 del plan maestro.
>
> **Requisito previo:** Tarea 10 (tooltips inline) completada. Tarea 6 Sesión 3 (rediseño visual)
> puede ejecutarse antes o después — si ya se ejecutó, el polish de tarjetas debe respetar el nuevo
> sistema de diseño resultante; si no, esta tarea usa el estilo funcional-mínimo actual.

---

Estamos construyendo un comparador de carreras sobre datos públicos SIES para estudiantes de 4to
medio. Lee primero `CLAUDE.md` y `PLAN.md` completo (especialmente la sección "Tarea 11" y el
item 7 del backlog de Tarea 8).

**Tu tarea (Tarea 11): mejorar el polish visual de las tarjetas de comparación existentes en ambas
pestañas (`web/index.html` y `web/instituciones.html`), adoptando el patrón de tarjeta de College
Scorecard ya verificado en Tarea 8b.**

## Qué adoptar del patrón de tarjeta de Scorecard (verificado en vivo, Tarea 8b)

Las tarjetas de resultado de Scorecard (`/search/`) tienen:
1. **Fila de íconos** — atributos clave de la institución/carrera (ej. duración, tipo, ubicación,
   tamaño) representados como ícono + etiqueta breve. Los íconos tienen tooltip hover corto.
2. **Métricas titulares** — 2-3 métricas clave (las más importantes para decidir) destacadas
   visualmente arriba, antes de los detalles secundarios.
3. **Botones de acción** claros ("Ver detalle", "Agregar a comparación").

Adaptar este patrón a **nuestras tarjetas actuales** en ambas pestañas (que representan combos
carrera/institución, no instituciones solas): decidir qué métricas van arriba (candidatos: empleabilidad
1er año, ingreso 4° año, arancel si está disponible) y qué íconos de atributo tienen sentido para
el contexto chileno (tipo de institución, acreditación, región).

## Item 7 del backlog (incluir en esta sesión)

Agregar un **aviso de usabilidad no bloqueante** cuando la comparación tiene muchas tarjetas (sin
tope duro — el tope duro se quitó en Tarea 7 Iteración 3 a propósito). Scorecard tiene un tope de
10; nosotros lo quitamos para no limitar al usuario, pero un mensaje suave ("Estás comparando N
combinaciones — muchas puede dificultar la lectura") mejora la experiencia sin revertir esa decisión.
Umbral a elegir: proponer uno razonable (7-8 tarjetas o similar).

## Restricciones

- No cambiar lógica de datos ni scripts de export.
- No implementar tabs ni acordeón (eso es Tarea 6 Sesión 3) — solo el interior de cada tarjeta.
- No agregar métricas que no existan en el JSON actual.
- Si Tarea 6 Sesión 3 ya se ejecutó: respetar las variables CSS y el sistema de diseño resultante.

## Verificación

- `node --check` sobre el JS modificado.
- Aserciones de Node sobre la lógica del aviso de usabilidad (N tarjetas → aviso, M < umbral → sin aviso).
- `python -m http.server` + `curl` confirmando 200 en ambos HTML.
- Verificación visual en navegador: pendiente de Diego.

Al terminar, actualiza el estado de la Tarea 11 en `PLAN.md` y verifica si corresponde generar el
prompt de la siguiente sesión (Tarea 6 Sesión 3 o Tarea 12, según el roadmap en ese momento).
