# Guía de fuentes de datos — a qué tabla ir antes de construir algo nuevo

> Documento vivo, orientado a "voy a construir una función/pantalla nueva, ¿a qué fuente voy y qué me puede/no me puede dar". No reemplaza:
> - **[`mifuturo/MODELO_DATOS.md`](mifuturo/MODELO_DATOS.md)** — el contrato de esquema/loader (columnas, tipos, decisiones de diseño de cada tabla). Ve ahí para el detalle de una columna específica.
> - **[`AUDITORIA_DATOS_T25.md`](AUDITORIA_DATOS_T25.md)** — reporte puntual de auditoría (fecha y alcance fijo, 2026-08-15). Ve ahí para el detalle completo de los hallazgos T25-1 a T25-4.
>
> Esta guía existe porque T24 → T25 → T25b redescubrieron el mismo agujero de cobertura tres veces desde cero. La idea es que la próxima sesión no tenga que hacerlo una cuarta vez.

---

## Los 3 hechos, de un vistazo

| Hecho | Grano | Fuente Excel | Pares institución+genérica |
|---|---|---|---|
| `hecho_indicadores` | carrera (genérica+título) × institución | `Buscador_Empleabilidad_ingresos` | 1690 |
| `hecho_oferta` | carrera × institución × sede × jornada | `Buscador_de_Carreras` | 2652 |
| `hecho_benchmark_nacional` | carrera genérica × tipo de institución (agregado nacional) | `Buscador_EstadísticasCarrera` | — (no tiene institución) |

Verificado en vivo contra `comparador.db` el 2026-08-15 (mismos números que reportó `AUDITORIA_DATOS_T25.md`):

```
Pares institución+genérica en hecho_oferta:      2652
Pares institución+genérica en hecho_indicadores: 1690
Pares SOLO en hecho_oferta:                       1183
Pares SOLO en hecho_indicadores:                   221
Pares en ambos:                                   1469
```

---

## `hecho_indicadores` — resultados de egreso reales

**Responde bien:** empleabilidad 1er/2do año, retención 1er año, duración real (lo que efectivamente demoraron los titulados), ingreso promedio al 4° año (banda de texto, por institución), % con continuidad de estudios. Es la única fuente con estos indicadores a nivel institución×título.

**No puede responder nunca (estructural, no "a veces falta"):** arancel, vacantes, ponderación PAES/NEM, sede, jornada. Estas columnas simplemente no existen en esta tabla — no es que falten datos, es que la encuesta de origen (retrospectiva, a egresados) no las releva.

**Quién lo consume hoy:** `mifuturo/queries.py::detalle_carrera_generica()` (bloque `hecho_indicadores h LEFT JOIN dim_institucion`, ~línea 366) → `web/export_json.py` → `core.json`/`detalle/<slug>.json` → `index_v2.html`. También `web/export_instituciones.py::main()` (itera `detalle.indicadores`) → `instituciones.json` → `instituciones_v2.html`.

**Cruce institución+carrera ya resuelto por:** el `SELECT` de `detalle_carrera_generica` en `queries.py` (join directo por `codigo_institucion` + `nombre_carrera_generica`, sin fuzzy-match — esta tabla no lo necesita porque viene del ancla).

---

## `hecho_oferta` — oferta académica y admisión vigente

**Responde bien:** arancel 2026, vacantes, ponderación PAES (NEM/Ranking/Lenguaje/Matemática/Historia/Ciencias/Otros), promedio NEM/PAES real de la matrícula 2025, sede, jornada, nivel (profesional/técnico), región. Es la única fuente con estos datos, y vive a nivel institución×sede×jornada (más fino que institución×genérica).

**No puede responder nunca (estructural):** empleabilidad, retención, ingreso, continuidad de estudios. Estas columnas no existen en `Buscador_de_Carreras` — es una encuesta de oferta/admisión vigente, no de resultados de egresados. No va a aparecer nunca, no importa qué se agregue al loader.

**Quién lo consume hoy:**
- `mifuturo/queries.py::detalle_carrera_generica()` (bloque `hecho_oferta o LEFT JOIN dim_institucion`, ~línea 329) → `detalle/<slug>.json.ofertas` → `index_v2.html` (panel "Dónde se imparte") y `web/export_json.py` (construye `instituciones_nem.json` iterando estas mismas ofertas) → `nem.html`.
- `web/export_instituciones.py::resolver_arancel()` (línea 164), `resolver_ponderaciones()` (línea 249), `resolver_tiene_oferta_nem()` (línea 283) — **enriquecen** un combo de `instituciones.json` que ya existe desde `hecho_indicadores`, nunca generan un combo nuevo. Por eso los 1183 combos solo-`hecho_oferta` quedan invisibles en "Carreras por institución" (ver sección "Decisión T25-1/T25b" abajo).

**Cruce institución+carrera ya resuelto por:** las tres funciones de arriba en `export_instituciones.py` (manejan bien la ausencia de filas: `arancel_moneda: None`, `tiene_ponderacion_paes: False`, nunca inventan datos) y, para el índice completo por institución, el bloque de `web/export_json.py::main()` (~línea 130, comentario "instituciones_nem.json") que arma `instituciones_index` iterando `detalle.ofertas` de las 190 genéricas.

**Nota de esquema:** el join a `dim_carrera_generica` es vía `Área Carrera Genérica` (fuzzy-match resuelto, 99.47% de cobertura — decisión 8 en `MODELO_DATOS.md`), no vía `Nombre carrera` (el nombre real del programa, que se guarda tal cual como texto descriptivo sin mapear 1:1). El 0.53%/23.48% restante sin match queda con `nombre_carrera_generica = NULL`, contado en `diagnostico_cobertura()`.

---

## `hecho_benchmark_nacional` — comparación agregada nacional

**Responde bien:** ingreso al 4° año (numérico continuo, 2020-2024), empleabilidad 1er/2do año (2020-2024), percentiles de ingreso (10/25/50/75/90 al 1er año y al 5to año), retención — todo a nivel carrera genérica × tipo de institución (agregado nacional).

**No puede responder nunca (estructural):** nada específico de una institución individual. Es deliberadamente un agregado nacional (decisión de `MODELO_DATOS.md` sección 7) — materializarlo contra cada institución inflaría filas sin aportar información real, porque el dato SIES ya viene agregado y no varía por institución.

**Quién lo consume hoy:** `mifuturo/queries.py::detalle_carrera_generica()` (~línea 314) y `listar_carreras_genericas()` (~línea 256) → `core.json`/`detalle/<slug>.json` → `index_v2.html` (comparación carrera vs. carrera). Solo se exporta el año 2024 de cada serie y 3 de los 10 percentiles (10/50/90 del 5to año) — el resto (históricos 2020-2023, percentiles 1er año, percentiles 25/75 del 5to año) está cargado en `comparador.db` pero no se consulta (hallazgo T25-3, 19 columnas).

**Cruce institución+carrera:** no aplica — este hecho no tiene institución.

---

## Ejemplo real concreto (USACH, verificado 2026-08-15)

Universidad de Santiago de Chile = `codigo_institucion` 71.

**Derecho — solo en `hecho_oferta`:**
```
arancel_anual_2026: "$ 6.535.000"
vacantes_1er_semestre: 200.0
ponderación PAES: NEM 10% / Ranking 40% / Lenguaje 20% / Matemática 10%
hecho_indicadores: sin fila (0 resultados)
```
Un estudiante puede ver arancel y ponderación en "Qué NEM necesito", pero esta institución+carrera **no aparece en absoluto** en "Carreras por institución" — no es una fila con badge "sin dato", es una fila que no se genera (ver `AUDITORIA_DATOS_T25.md`, Hallazgo T25-1).

**Arquitectura — en ambas fuentes, de forma complementaria:**
```
hecho_oferta:       arancel_anual_2026: "$ 5.958.000"
hecho_indicadores:  empleabilidad_1er_anio: 0.694  (69.4%)
                     retencion_1er_anio:    0.901  (90.1%)
```
Ninguna fuente sustituye a la otra — cuando ambas existen para un combo, cada una aporta un eje de comparación distinto (arancel/admisión vs. resultados de egreso). No hay redundancia que resolver.

---

## Decisión T25-1 / T25b (cerrada, no reabrir)

**Contexto:** T25 confirmó que "Carreras por institución" (`instituciones_v2.html`) se construye solo desde `hecho_indicadores`, dejando invisibles los 1183 combos institución+genérica que solo tienen fila en `hecho_oferta` (mismo agujero que T24 encontró y resolvió para `nem.html`).

**Decisión (sesión previa a T25c, discutida con Diego):** **no se agregan esos 1183 combos a `instituciones.json`/`instituciones_v2.html`.** Razones:

1. `hecho_oferta` no tiene, ni tendrá nunca, columnas de empleabilidad/ingreso/retención — son estructuralmente inexistentes en esa tabla (confirmado en `mifuturo/loader.py`), no "a veces faltan". Agregar esos combos metería ~41% de filas nuevas con las 3 columnas centrales de la página (el eje de comparación que le da sentido a esta pantalla) permanentemente vacías.
2. El mismo pool de 1183 ya está cubierto por `web/nem.html`/`instituciones_nem.json` (T24), que es la pantalla correcta para ese ángulo del dato (qué NEM/PAES necesito, no qué resultado obtuve). No se pierde información real del sitio al no duplicarlo acá.
3. Es fiel a cómo SIES/mifuturo.cl separa estos dos datasets (una encuesta retrospectiva de egresados vs. datos de oferta/admisión vigente) — no es una limitación artificial de nuestro modelo de datos.

**No se vuelve a evaluar esta decisión** salvo que cambie algo estructural en las fuentes SIES (por ejemplo, si `hecho_oferta` empezara a traer empleabilidad/ingreso, lo que hoy no ocurre). Si una sesión futura quiere mostrar "arancel/ponderación PAES sin resultados de egreso" para una institución, la fuente correcta ya existe y ya está resuelta: `nem.html`/`instituciones_nem.json`.

Ver `AUDITORIA_DATOS_T25.md` (Hallazgo T25-1) para el detalle completo de la auditoría, y `PLAN.md` (fila T25b) para el registro en el roadmap.
