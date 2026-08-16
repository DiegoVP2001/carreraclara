# Auditoría de datos no considerados por error — Tarea 25

> Diagnóstico de punta a punta (fuente → loader → queries → export → pantalla). No se modifica código en esta sesión — ver `TAREA_25_PROMPT.md` para el encargo completo. Verificaciones cuantitativas corridas ad-hoc contra `mifuturo/processed/comparador.db` vía `sqlite3` directo; los números citados son reproducibles con las mismas consultas.

## Resumen ejecutivo

El hallazgo de T24 (`instituciones.json` no es superset de `hecho_oferta`) **no era un caso aislado de "Qué NEM necesito" — es un síntoma de una decisión de grano que también deja huérfana la pantalla principal, "Carreras por institución".** `web/instituciones_v2.html` se construye enteramente desde `hecho_indicadores` (grano institución×título), igual que el `instituciones.json` que T24 diagnosticó como incompleto. Se confirmó por SQL directo: **1183 combinaciones institución+carrera-genérica con oferta real (arancel, vacantes, ponderaciones PAES) son invisibles en "Carreras por institución"**, mismo número exacto que T24 encontró para NEM/PAES — es el mismo agujero, visto desde el otro lado. `nem.html` ya lo resuelve (T24 lo construyó directo desde `hecho_oferta`) e `index_v2.html` no lo sufre (agrupa por institución sin exigir intersección) — ver Hallazgo T25-1 para el detalle.

Además se confirmaron **31 columnas cargadas en `comparador.db` con datos reales, nunca consultadas por `mifuturo/queries.py`** (12 en `hecho_oferta`: costo de titulación, duración formal, matrícula y titulación por sexo, rango de ingreso PAES; 19 en `hecho_benchmark_nacional`: series históricas 2020-2023 de ingreso/empleabilidad y la mayoría de los percentiles de ingreso) — dato disponible que nunca sale del backend. Y **6 campos que sí llegan a algún JSON pero ninguna pantalla lee** (`tipos_institucion` de `core.json`, 5 de los 11 contadores del diagnóstico de `instituciones.json`).

`matricula/`, `titulados/` y `personal/` — confirmado (grep + listado de tablas de la DB): cero referencias en código, cero tablas a medio poblar. Nada que limpiar ahí.

---

## Hallazgo T25-1 (confirmado) — "Carreras por institución" hereda el mismo agujero de cobertura que T24 encontró en NEM

**Tipo de brecha:** 3 — cobertura silenciosamente incompleta.

**Dónde se verificó:** `web/export_instituciones.py` líneas 1-42 (docstring, decisión de grano) y su `main()` (líneas 355-398), que itera `detalle.indicadores` (grano `hecho_indicadores`, institución×título) para construir cada `combo` de `instituciones.json`. Nunca itera `detalle.ofertas` (grano `hecho_oferta`, institución×genérica×sede×jornada) para *agregar* combos — solo la usa para *enriquecer* uno ya existente (`resolver_arancel`/`resolver_ponderaciones`, líneas 164-280).

**Verificación cuantitativa** (SQL directo sobre `comparador.db`):

```
Pares institución+genérica únicos en hecho_oferta:      2652
Pares institución+genérica únicos en hecho_indicadores:  1690
Pares SOLO en hecho_oferta (invisibles en "Carreras por institución"): 1183
Pares SOLO en hecho_indicadores (sin oferta activa este año):            221
Pares en ambos:                                                        1469
```

El número **1183** coincide exactamente con el que T24 reportó para el selector de NEM — confirma que es el mismo conjunto de pares, no una coincidencia. Ejemplos reales de la muestra: `Derecho` en institución 71, `Arquitectura` en institución 23, `Ingeniería Comercial` en institución 84 — carreras con oferta real (arancel, vacantes, ponderaciones PAES, y desde T24 también NEM/PAES) que un estudiante **no puede encontrar navegando "Carreras por institución"** para esa institución, aunque sí pueda encontrarlas en "Qué NEM necesito".

**Por qué no se detectó como el mismo bug en T24:** T24 se scopeó a resolver el síntoma en la pantalla nueva (`nem.html`), construyendo `instituciones_nem.json` directo desde `hecho_oferta` — una solución puntual y correcta para esa pantalla, pero que no tocó `export_instituciones.py` ni `instituciones_v2.html`, donde el mismo patrón de causa raíz sigue presente.

**Por qué la transparencia existente no lo cubre:** `instituciones.json.diagnostico` reporta `combos_sin_oferta_nem` (los 221 pares que están en `hecho_indicadores` pero no en `hecho_oferta` — la dirección *opuesta*), pero no hay ningún contador para los 1183 pares que existen solo en `hecho_oferta`, porque el script nunca los alcanza a iterar. El "sin dato" explícito que exige `CLAUDE.md` ("nunca ocultar un vacío") no puede aplicar aquí — el combo ni siquiera se construye, no es una fila con badge "sin dato", es una fila que no existe.

**Páginas NO afectadas (confirmado, no solo supuesto):**
- `web/index_v2.html` — `agruparPorInstitucion()` (líneas 2305-2328) agrupa por código de institución y agrega tanto `detalle.ofertas` como `detalle.indicadores` **independientemente**, sin exigir que ambas listas tengan la misma institución representada; una institución con solo `ofertas` (sin `indicadores`) igual aparece en el panel "Dónde se imparte", solo que sin la tabla "Indicadores propios por título". Verificado leyendo el código, no requiere fix.
- `web/nem.html` — construido desde `instituciones_nem.json`, que en `export_json.py` (líneas 130-166, 219-230) se arma iterando `detalle.ofertas` de las 190 genéricas — cubre el universo completo de `hecho_oferta`, no el de `hecho_indicadores`. Es la pantalla que ya no tiene el problema, precisamente porque T24 cambió su fuente.

**Confianza:** confirmado — verificado con conteo SQL real, coincide con el número ya conocido de T24, y se confirmó línea por línea que `export_instituciones.py` nunca itera `hecho_oferta` para generar combos nuevos.

**No se corrige en esta sesión** (regla de T25). Queda para que Diego decida si se replica el patrón de T24 (un índice adicional construido desde `hecho_oferta`, o fusionar ambas fuentes con un flag "sin indicadores propios, pero con oferta real") — candidato natural para T26 (brainstorm) dado que toca la pantalla más usada del sitio.

---

## Hallazgo T25-2 (confirmado) — 12 columnas de `hecho_oferta` cargadas, con datos reales, nunca consultadas

**Tipo de brecha:** 1 — cargado pero no exportado.

**Dónde se verificó:** `mifuturo/loader.py` líneas 204-238 (carga las 31 columnas de `hecho_oferta` desde `Buscador_de_Carreras`) vs. el `SELECT` de `mifuturo/queries.py` líneas 320-333 (`detalle_carrera_generica`) y el `SELECT` de `resolver_arancel`/`resolver_ponderaciones` en `export_instituciones.py` (líneas 190-196, 261-266) — ninguno de los tres puntos de consulta toca estas 12 columnas.

Confirmado que no son datos vacíos — conteo real sobre `comparador.db` (9900 filas totales):

| Columna | No nulos | Ejemplo |
|---|---|---|
| `costo_titulacion` | 9898/9900 | `"$ 321.000"` |
| `duracion_formal_semestres` | 9898/9900 | `8.0` |
| `matricula_total_femenina_2025` | 9898/9900 | `25.0` |
| `matricula_total_masculina_2025` | 9898/9900 | `43.0` |
| `matricula_total_2025` | 9898/9900 | `68.0` |
| `matricula_1er_anio_femenina_2025` | 9898/9900 | `4.0` |
| `matricula_1er_anio_masculina_2025` | 9898/9900 | `3.0` |
| `matricula_1er_anio_total_2025` | 9898/9900 | `7.0` |
| `titulacion_femenina_2024` | 9898/9900 | `4.0` |
| `titulacion_masculina_2024` | 9898/9900 | `6.0` |
| `titulacion_total_2024` | 9898/9900 | `10.0` |
| `rango_ingreso_paes_2025` | 9898/9900 | (texto banda, sentinela `-` frecuente) |

**Nota:** `duracion_formal_semestres` es distinto de `duracion_real_semestres` (este último SÍ se consulta, viene de `hecho_indicadores`/ancla). Son dos medidas legítimamente distintas (formal = duración del plan de estudios declarado; real = lo que efectivamente demoran los titulados) — ninguna sustituye a la otra, ambas podrían mostrarse.

Costo de titulación y duración formal son datos que un estudiante compararía junto al arancel; matrícula/titulación por sexo son datos de composición que hoy no se muestran en ninguna pantalla (a diferencia de `titulados/`, que está fuera de alcance por ser un dataset nunca integrado, esta matrícula/titulación **ya vive en `hecho_oferta`**, cargada desde `Buscador_de_Carreras`, no requiere integrar nada nuevo).

**Confianza:** confirmado — verificado en código (loader carga, queries no consulta) y en datos (no nulos, valores reales).

---

## Hallazgo T25-3 (confirmado) — 19 columnas de `hecho_benchmark_nacional` cargadas, con datos reales, nunca consultadas

**Tipo de brecha:** 1 — cargado pero no exportado.

**Dónde se verificó:** `mifuturo/loader.py` líneas 250-280 (carga 5 años de histórico 2020-2024 para ingreso y ambas empleabilidades, más 10 percentiles a 1er y 5to año) vs. el `SELECT` de `listar_carreras_genericas`/`detalle_carrera_generica` en `queries.py` (líneas 251-256, 311-314), que solo trae **2024** de cada serie y solo 3 de los 10 percentiles (10/50/90 del 5to año).

Confirmado con datos reales (252 filas totales en `hecho_benchmark_nacional`):

| Grupo de columnas | No nulos | Detalle |
|---|---|---|
| `ingreso_4to_anio_2020..2023` (4 cols) | 217/252 cada una | Serie histórica de ingreso — solo se usa 2024 |
| `empleabilidad_1er_anio_2020..2023` (4 cols) | 236/252 cada una | Serie histórica — solo se usa 2024 |
| `empleabilidad_2do_anio_2020..2023` (4 cols) | 236/252 cada una | Serie histórica — solo se usa 2024 |
| `percentil_10/25/50/75/90_1er_anio` (5 cols) | 252/252 cada una | Ninguna se consulta — solo existen los percentiles de 5to año |
| `percentil_25_5to_anio`, `percentil_75_5to_anio` (2 cols) | 252/252 cada una | Se consultan 10/50/90 del 5to año, pero no 25/75 |

Esto es la brecha más grande de las tres en volumen: **19 columnas con cobertura casi total** (86-100% no nulo), suficientes para un gráfico de tendencia 2020→2024 (el dato que hoy solo se muestra como punto fijo del año más reciente) y para mostrar la dispersión completa de ingresos al 1er año, no solo al 5to.

**Confianza:** confirmado — mismo patrón de verificación que T25-2.

---

## Hallazgo T25-4 (confirmado) — 6 campos que llegan al JSON pero ninguna pantalla los lee

**Tipo de brecha:** 2 — exportado pero no mostrado.

1. **`core.json.tipos_institucion`** (`web/export_json.py` líneas 132-134, 139) — el propio docstring del script (líneas 9-10) dice que existe "para el selector del toggle 'filtro por tipo' en el cliente". Verificado en `index_v2.html`: nunca se lee `coreData.tipos_institucion` (0 matches); en su lugar el JS define una constante hardcodeada `ORDEN_TIPOS = ["Universidades", "Institutos Profesionales", "Centros de Formación Técnica"]` (línea 1632) y filtra contra ella. Funcionalmente inofensivo hoy (los 3 valores hardcodeados coinciden con los reales), pero si SIES agrega o renombra un tipo de institución el dato exportado ya lo reflejaría y la UI no, silenciosamente, porque ninguna parte del código compara ambos.

2. **5 de los 11 contadores de `instituciones.json.diagnostico`** (`web/export_instituciones.py` líneas 456-469) nunca se renderizan en `instituciones_v2.html` (`renderDiagnostico`, líneas 1916-1922 — muestra 6 de los 11): `combos_con_ponderacion_paes`, `combos_sin_ponderacion_paes`, `combos_ponderacion_varia_por_sede`, `combos_con_oferta_nem`, `combos_sin_oferta_nem`. Los dos últimos son justamente los contadores que miden el hallazgo T25-1 desde el lado que sí alcanza a verse — quedan calculados y exportados, pero invisibles para Diego o cualquier visitante que no lea el JSON crudo.

**Confianza:** confirmado — verificado por grep exhaustivo contra las 4 páginas HTML (excluyendo los propios JSON de datos).

---

## Verificación del patrón T24 en las otras páginas (gap tipo 3)

- **`resolver_arancel`/`resolver_ponderaciones`/`resolver_tiene_oferta_nem`** (`export_instituciones.py`): estas SÍ manejan bien la asunción título↔genérica — nunca inventan datos cuando no hay filas de `hecho_oferta` (`arancel_moneda: None`, `tiene_ponderacion_paes: False`), y exponen el flag `tiene_oferta_nem` explícito para el caso de institución+título con indicador propio pero sin oferta activa (221 casos, ya contado). El problema real no está en cómo *enriquecen* un combo existente — está en que **nunca generan combos nuevos** desde `hecho_oferta` (ver T25-1).
- **`index_v2.html` / "Área Carrera Genérica" al 76.5% de match exacto** (Decisión 7 de `MODELO_DATOS.md`): el 23.48% sin resolver ya se materializa como `nombre_carrera_generica = NULL` en `hecho_oferta`, y `diagnostico_cobertura()` lo cuenta (`filas_oferta_sin_carrera_generica`) — confirmado que `index_v2.html` sí renderiza este contador (línea 1697). No es un hallazgo nuevo, es la Decisión 7 ya documentada y ya visible en la UI — se revisó porque el prompt de la tarea pedía descartarlo explícitamente, y se descarta.

**Confianza:** descartado (ambos, ya investigados y con manejo correcto — se documentan para no reabrir la pregunta).

---

## `matricula/`, `titulados/`, `personal/` — confirmación explícita

- `grep` de `matricula/|titulados/|personal/|PAC_web|TITULADO_|Matricula_2025` sobre todos los `.py` del proyecto: **0 coincidencias**. Las únicas menciones de esos datasets en todo el repo están en documentación (`PLAN.md`, `README.md`, `CLAUDE.md`, prompts de tarea) — ninguna en código.
- `comparador.db` tiene exactamente las 5 tablas documentadas en `MODELO_DATOS.md` (`dim_institucion`, `dim_carrera_generica`, `hecho_indicadores`, `hecho_oferta`, `hecho_benchmark_nacional`) — verificado con `sqlite_master`. No hay una sexta tabla a medio poblar ni un intento abandonado.

**Confianza:** descartado — nada a medio importar, confirmado por dos verificaciones independientes (código y esquema de la DB).

---

## Resumen por tipo de brecha

| Tipo | Hallazgo | Confianza | Alcance |
|---|---|---|---|
| 3 — Cobertura silenciosamente incompleta | T25-1: 1183 combos institución+genérica invisibles en "Carreras por institución" | Confirmado | Alto — pantalla principal del sitio |
| 1 — Cargado pero no exportado | T25-2: 12 columnas de `hecho_oferta` (costo titulación, duración formal, matrícula/titulación por sexo, rango PAES) | Confirmado | Medio |
| 1 — Cargado pero no exportado | T25-3: 19 columnas de `hecho_benchmark_nacional` (históricos 2020-2023, percentiles 1er año, 2 percentiles de 5to año) | Confirmado | Medio-alto (series de tiempo completas) |
| 2 — Exportado pero no mostrado | T25-4a: `core.json.tipos_institucion` sin leer (hardcodeado en cliente) | Confirmado | Bajo (cosmético hoy) |
| 2 — Exportado pero no mostrado | T25-4b: 5 contadores de diagnóstico de `instituciones.json` sin renderizar | Confirmado | Bajo |
| 3 — Cobertura (ya conocido) | `Área Carrera Genérica` 23.48% sin match | Descartado — ya documentado y visible | — |
| 3 — Cobertura (ya conocido) | `resolver_arancel`/`resolver_ponderaciones` | Descartado — manejo correcto, no genera combos nuevos (ver T25-1) | — |
| — | `matricula/`, `titulados/`, `personal/` | Descartado — nada a medio importar | — |

---

## Cobertura de la auditoría

- **4 páginas revisadas:** `landing.html` (no consume JSON de datos, fuera de la cadena), `index_v2.html`, `instituciones_v2.html`, `nem.html`.
- **5 fuentes de datos revisadas:** `mifuturo/` (loader completo, 3 hechos + 2 dimensiones), `oferta/` (es la fuente de `hecho_oferta`, ya cubierta vía `mifuturo/`), `matricula/`, `titulados/`, `personal/` (confirmación de no-integración).
- **Cadena completa recorrida:** loader.py → queries.py → export_json.py/export_instituciones.py → 4 HTML, campo por campo donde el volumen lo permitía, con verificación SQL directa para los conteos citados.
