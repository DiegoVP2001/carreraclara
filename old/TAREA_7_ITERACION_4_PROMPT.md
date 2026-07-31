# Prompt para iniciar la Tarea 7, Iteración 4 — Panel institucional + arancel cruzado

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/`.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto, `PLAN.md` (sección "Tarea 7 — Comparar instituciones entre carreras distintas", específicamente "Iteración 4" al final de esa sección, y la tabla "Roadmap general actualizado"), `mifuturo/MODELO_DATOS.md` (sección 2 `dim_institucion` y sección 6 `hecho_oferta`), `mifuturo/queries.py` y `web/export_instituciones.py` + `web/instituciones.html` (estado actual tras la Iteración 3) para tener el contexto completo antes de empezar.

**Tu tarea: dos adiciones a la pestaña "Comparar instituciones", decididas con Diego en sesión de scoping previa (no re-abrir esas decisiones, solo ejecutarlas):**

## 1. Panel de info general de institución (debajo de los gráficos)

Por cada institución presente en la comparación actual, mostrar: acreditación, años de acreditación, vigencia, áreas acreditadas, tipo de sociedad, dirección de sede central, página web.

- Estos campos **ya existen en `dim_institucion`** (columnas `años_acreditacion`, `vigencia_acreditacion`, `areas_acreditadas`, `direccion_sede_central`, `pagina_web`, `tipo_sociedad` — ver `MODELO_DATOS.md` sección 2) pero el dataclass `InstitucionInfo` en `queries.py` solo expone `codigo_institucion`/`nombre_institucion`/`tipo_institucion`/`acreditacion`.
- Extiende `InstitucionInfo` (nuevos campos, todos `| None`) y el SELECT + mapeo de `_row_to_institucion`. Es un cambio **aditivo**: revisa los 2 call sites existentes (`detalle_carrera_generica` para `index.html`, y `export_instituciones.py`) para confirmar que no rompen con campos nuevos en el dataclass (no deberían, son solo más atributos).
- Actualiza `export_instituciones.py` (`institucion_a_dict`) para incluir los campos nuevos en el JSON.
- En `web/instituciones.html`, agrega el panel debajo de los gráficos existentes: una tarjeta por institución única en la comparación actual (deduplicada por código, igual que ya hace `institucionesUnicas`). Estado explícito si `tiene_ficha=False` (no inventar "sin información" genérico — usar el mismo patrón de badge ya existente en el archivo).
- `index.html` no se toca en este punto (el panel es específico de `instituciones.html`), salvo que detectes que extender `InstitucionInfo` requiere tocar algo compartido — en ese caso, documenta por qué.

## 2. Gráfico de arancel cruzado, escalonado por nivel de certeza

**No implementes "siempre rango" ni "siempre mapeo manual a ciegas".** El enfoque acordado con Diego:

El join confiable que ya existe (`codigo_institucion` + `Área Carrera Genérica`, 99.47% cobertura, el mismo que usa "dónde se imparte" en `index.html` vía `hecho_oferta`) llega a institución×carrera-**genérica**, no a institución×carrera-**título** (que es el grano real de esta pestaña, vía `hecho_indicadores`). El texto libre `Nombre carrera` de `hecho_oferta` solo matchea 24.7% contra título — no es una clave usable directamente.

**Paso 1 — diagnóstico antes de tocar la UI:** escribe un script (puede ser parte de `export_instituciones.py` o uno separado de exploración) que, para cada uno de los 1690 combos de `instituciones.json`, busque las filas de `hecho_oferta` con el mismo `codigo_institucion` y la misma `Área Carrera Genérica` que la carrera genérica del combo, y clasifique:
- **Nivel 1 (sin ambigüedad):** 0 filas encontradas, o todas las filas encontradas comparten el mismo `arancel_anual_2026`.
- **Nivel 2 (ambiguo):** 2+ filas con `arancel_anual_2026` distintos entre sí.

Imprime el conteo de cada nivel (y el % del total). **Este número decide el resto de la sesión:**
- Si Nivel 2 es chico (de orden decenas, no cientos) → sigue al Paso 2.
- Si Nivel 2 es grande → no intentes resolverlo a mano en esta sesión; documenta el conteo en `PLAN.md` como hallazgo, implementa solo Nivel 1 (valor exacto) + Nivel 3 (rango) para el resto, y deja el fuzzy-match de Nivel 2 como TODO explícito para una sesión futura dedicada solo a eso.

**Paso 2 — si Nivel 2 es manejable:** para cada combo en Nivel 2, genera candidatos por similitud de texto entre `nombre_carrera_programa` (de las filas de `hecho_oferta` ya filtradas a esa institución+genérica — universo chico, no las 9900 filas totales) y `nombre_carrera_titulo` del combo (usa `difflib.SequenceMatcher` de la stdlib o una heurística de normalización simple, no hace falta una librería nueva para un universo tan chico). **Ningún candidato se acepta automáticamente** — preséntaselos a Diego en esta misma sesión (lista corta, comparación lado a lado) para que confirme o rechace cada uno explícitamente. Solo lo confirmado se guarda en una tabla de curaduría pequeña y separada del loader principal (mismo patrón ya usado para `familia`, ver `MODELO_DATOS.md` decisión 3 — un JSON o CSV chico en `mifuturo/` o `web/`, documentado).

**Paso 3 — export y UI:**
- `export_instituciones.py`: agrega al dict de cada combo el arancel resuelto, con un campo explícito de cómo se resolvió (ej. `arancel_anual_2026_exacto` si Nivel 1, `arancel_anual_2026_min`/`_max` + `arancel_aproximado=True` si Nivel 3, o el valor confirmado si Nivel 2 se resolvió). Nunca mezcles ambos casos en el mismo campo sin distinguirlos — la UI necesita saber si el dato es exacto o aproximado para etiquetarlo bien.
- `web/instituciones.html`: nuevo gráfico de arancel (mismo patrón horizontal `dibujarChartHorizontal` que los otros 4 gráficos de esta pestaña — ver Iteración 3). Etiqueta visualmente la diferencia entre valor exacto y rango aproximado (ej. barra sólida vs. barra con patrón/opacidad distinta + tooltip aclarando "varias sedes/jornadas, rango aproximado").
- Badge de "sin dato de arancel" si el combo no tiene ninguna fila de `hecho_oferta` matcheable (ni siquiera a nivel genérica) — estado explícito, mismo criterio que el resto del proyecto.

## Restricciones

- No tocar `comparador.db` (capa de loader/modelo ya cerrada). Sí se puede extender `queries.py` (es aditivo, ver punto 1) y crear archivos nuevos chicos de curaduría si el Paso 2 aplica.
- No construir filtros de región/acreditación/tipo todavía — siguen siendo Tarea 8/9.
- No tocar `index.html` salvo que sea estrictamente necesario por el cambio aditivo a `InstitucionInfo` (no debería serlo).

## Verificación antes de cerrar la sesión

(No hay herramienta de navegador en este entorno — verificación por script, igual que en iteraciones anteriores; la prueba visual queda para Diego.)

- Script de diagnóstico del Paso 1 corre y reporta los conteos reales de Nivel 1/2 (anota el resultado en el resumen de cierre).
- `export_instituciones.py` corre sin error, con asserts de cobertura/consistencia análogos a los ya existentes (ningún combo queda sin clasificar entre exacto/aproximado/sin-dato).
- Si hubo Paso 2 (mapeo manual), la lista de candidatos confirmados/rechazados con Diego queda documentada (qué se confirmó, qué se rechazó y por qué) antes de tocar el export.
- Si hay lógica JS nueva no trivial (panel institucional, gráfico de arancel, badges nuevos), pruébala con Node contra fixtures sintéticas (extraer el `<script>`, mismo método ya usado en iteraciones previas).
- `python -m http.server` desde `web/` + `curl` confirmando 200 en `instituciones.html` y `data/instituciones.json` regenerado, con los campos/funciones nuevas presentes.
- Comparación directa de 1-2 casos contra `comparador.db`/`Buscador_Instituciones`/`Buscador_de_Carreras` vía sqlite3/pandas para confirmar que el panel institucional y el arancel resuelto coinciden con la fuente.

Al terminar, actualiza `PLAN.md`: marca la Iteración 4 de la Tarea 7 como completada, con el conteo real de Nivel 1 vs. Nivel 2 del arancel, qué se implementó de cada nivel, y si quedó un TODO pendiente para una sesión de mapeo manual futura. Confirma que la Tarea 8 (auditoría College Scorecard) puede empezar.
