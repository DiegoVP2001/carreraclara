# TAREA 25b — "Carreras por institución" no muestra 1183 combos con oferta real

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

T25 (`AUDITORIA_DATOS_T25.md`, hallazgo T25-1) confirmó que el bug de cobertura que T24 encontró y arregló **solo para NEM** en realidad afecta también a "Carreras por institución" — y ahí nunca se arregló.

`web/export_instituciones.py` construye `instituciones.json` iterando exclusivamente `hecho_indicadores` (grano institución×carrera-**título**, ~1690 filas). `hecho_oferta` (grano institución×carrera-**genérica**+sede+jornada, ~9900 filas) solo se usa para *enriquecer* un combo que ya existe (arancel, ponderaciones PAES vía `resolver_arancel`/`resolver_ponderaciones`) — nunca para *agregar* combos nuevos.

Verificado por SQL directo sobre `comparador.db` (T25):

```
Pares institución+genérica únicos en hecho_oferta:      2652
Pares institución+genérica únicos en hecho_indicadores:  1690
Pares SOLO en hecho_oferta (invisibles hoy en "Carreras por institución"): 1183
Pares SOLO en hecho_indicadores (sin oferta activa este año):              221
```

Ese **1183** es el mismo número exacto que T24 reportó para NEM — es el mismo conjunto de pares, visto desde el lado que T24 no tocó. Ejemplos reales: `Derecho` en institución 71, `Arquitectura` en institución 23, `Ingeniería Comercial` en institución 84 — carreras con oferta real (arancel, vacantes, ponderaciones PAES, y NEM/PAES desde T24) que hoy son invisibles al navegar "Carreras por institución" para esa institución, aunque sí aparezcan en "Qué NEM necesito".

## Qué hace esta tarea

Cerrar la brecha de cobertura en `instituciones.json`/`instituciones_v2.html`, siguiendo el mismo criterio que ya usa `tiene_oferta_nem` (T24) en la dirección inversa: **ningún combo con datos reales queda fuera, y ningún dato ausente se rellena o inventa** — se marca explícito.

Puntos a resolver (sin implementar en el plan, solo dejarlos identificados para la sesión de implementación):

1. **Agregar los 1183 combos institución+genérica que solo existen en `hecho_oferta`** al índice que consume `instituciones_v2.html`, con sus datos de oferta (arancel, vacantes, ponderaciones PAES, NEM/PAES) — sin `empleabilidad_1er_anio`/`retencion_1er_anio`/`ingreso_banda_texto` porque esos son atributos de `hecho_indicadores` (grano título) que este combo no tiene. Necesita un flag explícito tipo `tiene_indicadores_propios: false` para que la UI muestre "sin datos de empleabilidad/ingreso reportados a nivel de título" en vez de ocultar la fila o mostrar un vacío sin explicar.
2. **Decidir el identificador de estos combos nuevos.** El `id` actual es `f"{codigo}--{slugify(carrera_titulo)}"` (depende de un título que estos combos no tienen). Evaluar `f"{codigo}--{slugify(carrera_generica)}"` o un prefijo que distinga claramente "título real" de "genérica sin título" para no colisionar con los ids existentes.
3. **Revisar `instituciones_v2.html`** — el HTML/JS de tarjetas, filtros y tabla asume implícitamente que todo combo tiene `carrera_titulo`. Confirmar qué se muestra en vez del título para estos 1183 combos nuevos (¿el nombre de la carrera genérica, con una etiqueta que aclare que es "plan general" sin título específico?).
4. **Actualizar el diagnóstico.** `instituciones.json.diagnostico` debería sumar un contador para estos combos nuevos (ej. `combos_sin_indicadores_propios`) — y de paso exponer en el HTML los 5 contadores que T25 (hallazgo T25-4b) encontró ya calculados pero nunca renderizados (`combos_con_ponderacion_paes`, `combos_sin_ponderacion_paes`, `combos_ponderacion_varia_por_sede`, `combos_con_oferta_nem`, `combos_sin_oferta_nem`), ya que se está tocando ese panel de todos modos.

## Decisiones que ya están tomadas (no volver a discutir)

- **No se inventa empleabilidad/ingreso/retención para los combos sin indicador propio.** Si `hecho_indicadores` no tiene fila para ese institución+título, esos campos quedan `null` con su estado explícito — mismo principio que toda la Decisión 8/9 de `MODELO_DATOS.md`.
- **La solución replica el patrón de `tiene_oferta_nem` (T24), no lo reemplaza.** `tiene_oferta_nem` sigue existiendo para los 221 combos de `hecho_indicadores` sin oferta activa; esta tarea agrega el caso simétrico.
- **No se toca `nem.html` ni `instituciones_nem.json`** — ya están correctos (T24/T25 lo confirmaron), esta tarea es solo sobre `instituciones.json`/`instituciones_v2.html`.
- **T25-2 y T25-3 (columnas cargadas y no exportadas: costo de titulación, duración formal, matrícula/titulación por sexo, series históricas de ingreso/empleabilidad) quedan fuera de esta tarea** — Diego las evaluó junto con el informe T25 y decidió que son material para T26 (brainstorm de qué construir con la data disponible), no bugs a corregir.

## Archivos que probablemente se tocan

- `web/export_instituciones.py` (lógica de construcción del índice)
- `web/instituciones_v2.html` (render de combos sin título/indicador propio)
- `mifuturo/queries.py` — revisar si necesita una consulta nueva o si alcanza con SQL directo como ya hace `resolver_arancel` (no se modifica el esquema de `comparador.db`, los datos ya están cargados)
- `PLAN.md` (cierre de tarea)

## Criterio de "tarea completa"

- `web/data/instituciones.json` incluye los 1183 combos nuevos, cada uno con su flag explícito de "sin indicadores propios" y sin ningún campo de empleabilidad/ingreso relleno artificialmente.
- `instituciones_v2.html` renderiza esos combos de forma coherente (no rompe el layout de tarjeta/tabla existente, deja claro visualmente que son datos de oferta sin indicador propio de título).
- Sanity check cuantitativo en el propio script (mismo patrón que los `assert`/`raise AssertionError` que ya tiene `export_instituciones.py`): el total de combos exportados debe ser `1690 (título) + 1183 (solo oferta) = 2873`, verificado contra la DB en tiempo de export, no solo confiado a los números de este prompt.
- Diagnóstico actualizado y con los 5 contadores de T25-4b visibles en el HTML.
- Revisado en el navegador (`python dev_server.py`, `/carreras-por-institucion`) antes de pedir aprobación — buscar específicamente una de las instituciones/carreras de ejemplo citadas arriba (ej. Derecho, institución 71) para confirmar que ahora aparece.

## Recordatorio de flujo

Este proyecto avanza por sesiones aprobadas: **plan → aprobación explícita de Diego → ejecución**. Antes de tocar código, confirmar con Diego el enfoque de los 4 puntos abiertos arriba (especialmente el formato del `id` y qué mostrar en vez de "carrera-título" para los combos nuevos) — no son decisiones de datos ya cerradas, son decisiones de UX/estructura que le corresponden a él.
