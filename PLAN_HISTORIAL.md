# Historial de tareas completadas — Comparador de carreras

> Archivo de referencia. Para el roadmap activo, ver **[PLAN.md](PLAN.md)**.

---

## Hallazgos confirmados (sesión de scoping, 2026-06-24)

- El ancla (`Buscador_Empleabilidad_ingresos`) trae jerarquía de nombres: **"Nombre carrera genérica"** (190 valores únicos) vs. **"Nombre carrera (del título)"** (649 únicos, 1693 filas totales). La genérica es la consolidación que SIES ya hizo.
- `Buscador_EstadísticasCarrera` no tiene columna de institución — está agregado a nivel carrera genérica × tipo de institución. Es la tabla correcta para comparación carrera-vs-carrera; el ancla es la correcta para comparación institución-vs-institución.
- Valores faltantes reales: `n/a`, `s/i` en empleabilidad e ingreso. Tratarlos como estado explícito, nunca null silencioso.
- Formato de ingreso inconsistente: banda de texto en el ancla ("De $900 mil a $1 millón") vs. número continuo en `EstadísticasCarrera`.
- `Buscador_de_Carreras` tiene grano más fino (carrera × institución × sede × jornada) y solo un `Nombre carrera` — es una tercera convención de escritura (solo 24.7% match exacto contra el ancla).
- Códigos de institución comparten el mismo esquema numérico entre archivos.
- Archivos `mifuturo/` quirks: hojas "Hoja1" descartables, fila de encabezado decorativa antes de la real.

---

## Tareas completadas

### Tarea 1 — Auditoría de claves y grano
**Completada (2026-06-24).** Hallazgos en [`mifuturo/NOTAS_CRUCE.md`](mifuturo/NOTAS_CRUCE.md). Script: `mifuturo/auditoria_tarea1.py`.
- Código institución: join limpio por código (84–95% cobertura ancla↔Carreras/Instituciones).
- "Nombre carrera" de `Buscador_de_Carreras` es tercera convención real (24.7% match exacto, necesita fuzzy-match real).
- `Buscador_EstadísticasCarrera` vs ancla: cruce casi limpio (86% cobertura, 1 typo `Insitutos`→`Institutos`).
- El ancla trae 1 fila de nota al pie mezclada como dato — el loader debe filtrarla.

### Tarea 2 — Diseño del modelo de datos
**Completada (2026-06-24).** Esquema en [`mifuturo/MODELO_DATOS.md`](mifuturo/MODELO_DATOS.md).
Decisiones clave: 2 dimensiones (`dim_institucion`, `dim_carrera_generica`) + 3 hechos (`hecho_indicadores`, `hecho_oferta`, `hecho_benchmark_nacional`). `familia` es columna nullable a curar a mano. `Área Carrera Genérica` de `Buscador_de_Carreras` cubre 99.47% de las genéricas del ancla.

### Tarea 3 — Loader/normalizador
**Completada (2026-06-24).** Script: [`mifuturo/loader.py`](mifuturo/loader.py). Output: SQLite en `mifuturo/processed/comparador.db` (5 tablas). Log: `mifuturo/loader_log.txt`.
- Códigos de institución a `Int64` nullable. `s/i` mapeado a `NULL` vía `clean_sentinel`.
- Join `hecho_oferta`→carrera por `Área Carrera Genérica` vía diccionario normalizado.
- 0 filas de nota al pie remanentes; 0 genéricas con `Área` inconsistente.

### Tarea 4 — Validación de calidad de datos
**Completada (2026-06-24).** Script: [`mifuturo/auditoria_tarea4.py`](mifuturo/auditoria_tarea4.py). Log: `mifuturo/auditoria_tarea4_output.txt`.
- "1 `Código único de carrera` duplicado" de Tarea 2 era 1 sola fila completamente vacía, no duplicado real.
- `s/i` confirmado como único centinela en columnas numéricas.
- 26/190 genéricas sin benchmark nacional. 480 filas de `hecho_oferta` sin genérica, dispersas en 59 valores (fuzzy-match manual tendría retorno bajo).

### Tarea 5 — Capa de consulta
**Completada (2026-06-24).** Módulo: [`mifuturo/queries.py`](mifuturo/queries.py). Demo: `mifuturo/queries_demo.py`.
Funciones: `listar_carreras_genericas`, `comparar_carreras`, `detalle_carrera_generica`, `diagnostico_cobertura`. `hecho_benchmark_nacional` tiene filas separadas por `tipo_institucion` para 72/164 genéricas con benchmark — se devuelve la lista completa (decisión de UX diferida a Tarea 6).

### Tarea 6 — Diseño UI del comparador (múltiples sesiones)

**Decisiones cerradas (sesión de planificación, 2026-06-24):**
- Stack: HTML/JS estático + JSON export Python, sin bundler.
- Gráficos: Chart.js por CDN.
- Benchmark multi-tipo: 3 vistas como toggles de cliente (todo lado a lado / priorizar Universidad / filtro global).
- Alcance MVP: solo pantalla "Comparar" absorbiendo "dónde se imparte".

**Roadmap de pantallas (todas, incluyendo TODO):**
1. **Explorar carreras** (TODO) — filtros: Área, Familia, tipo institución. Data: `core.json`.
2. **Comparar carreras** (MVP — construida en Sesión 2).
3. **Detalle / dónde se imparte** (parcial en MVP) — oferta por institución + indicadores.
4. **Comparar instituciones** (construida en Tarea 7).
5. **Buscar instituciones** (TODO) — filtros: región, acreditación, tipo. Data: `dim_institucion`.
6. **Ficha de institución** (TODO — Tarea 20) — página propia por institución.

**Linaje de datos (dato en UI → tabla DB → archivo fuente):**

| Dato en pantalla | `queries.py` | Tabla DB | Archivo fuente | Columna origen |
|---|---|---|---|---|
| Nombre carrera (selector) | `CarreraGenericaResumen.nombre_carrera_generica` | `dim_carrera_generica` | `Buscador_Empleabilidad_ingresos…xlsx` | `Nombre carrera genérica` |
| Área (filtro/chip) | `.area` | `dim_carrera_generica` | ancla | `Área` |
| Familia (filtro) | `.familia` | `dim_carrera_generica` | — (curaduría manual, nullable) | — |
| Ingreso 4° año | `BenchmarkNacional.ingreso_4to_anio_2024` | `hecho_benchmark_nacional` | `Buscador_EstadísticasCarrera…xlsx` | `Ingresos al 4° año 2024` |
| Empleabilidad 1er/2do año | `.empleabilidad_1er/2do_anio_2024` | `hecho_benchmark_nacional` | `Buscador_EstadísticasCarrera…xlsx` | `Empleabilidad 1er/2° año 2024` |
| Retención 1er/2do año | `.retencion_1er/2do_anio` | `hecho_benchmark_nacional` | `Buscador_EstadísticasCarrera…xlsx` | `Retención …` |
| Percentiles 5° año | `.percentil_10/50/90_5to_anio` | `hecho_benchmark_nacional` | `Buscador_EstadísticasCarrera…xlsx` | `10% inferior…` |
| Tipo institución (toggle) | `BenchmarkNacional.tipo_institucion` | `hecho_benchmark_nacional` | `Buscador_EstadísticasCarrera…xlsx` | `Tipo de institución` |
| Institución (dónde se imparte) | `InstitucionInfo.nombre/tipo/acreditacion` | `dim_institucion` | `Buscador_Instituciones…xlsx` | `Nombre/Tipo de institución`, `Acreditación…` |
| Región/jornada/sede/arancel/vacantes/nivel | `OfertaInstitucion.*` | `hecho_oferta` | `Buscador_de_Carreras…xlsx` | columnas homónimas |
| Indicadores por institución (banda ingreso, continuidad, duración real) | `IndicadorTitulo.*` | `hecho_indicadores` | `Buscador_Empleabilidad_ingresos…xlsx` | columnas homónimas |

**Sesión 2 — MVP funcional (completada 2026-06-24):** `web/export_json.py` + `web/index.html`. Slug determinista NFKD+kebab-case. Paridad exacta JS↔Python sobre 190 carreras (0 mismatches). Iteración v2 de UX el mismo día: combobox con flecha, checkboxes de tipo por carrera, barras horizontales 2×2, acordeón "dónde se imparte" con filtros región/jornada/tipo.

**Sesión 3a (completada 2026-06-25):** Solo CSS. Paleta verde mineral `#1a7f64` + navy `#0f2e45` + ámbar `#e8960a`. Tipografía Figtree+Inter. Header navy invertido. Card polish (surface blanca, `border-radius: 1rem`, sombra).

**Sesión 3b (completada 2026-06-25):** JS/DOM sin acordeón (acordeón construido y revertido — Diego prefiere layout plano). Permanente: estado vacío rediseñado (SVG+heading+párrafo); colores Chart.js unificados con paleta; gráfico arancel hybrid dot-range en `instituciones.html` (DELTA=40000, verde=exacto, gris=rango, leyenda HTML estática).

**Rediseño `index_v2.html` (completado 2026-06-27):** Logo `logo_png_blanco-removebg-preview.png` (70px) en header navy, nombre "Carrera Clara" Figtree bold, eslogan, tabs debajo. Footer navy 3 columnas (logo+créditos / bases de datos / explorar). Diagnóstico de cobertura movido a elemento oculto. No sobreescribe `index.html`.

**Rediseño `instituciones_v2.html` (completado 2026-06-27):** Mismo shell de marca aplicado. Tab "Comparar instituciones" activo. `diagnostico-list` oculto con `hidden`. No sobreescribe `instituciones.html`.

### Tarea 7 — Comparar instituciones entre carreras distintas
**Completada (2026-06-24).** Scripts: [`web/export_instituciones.py`](web/export_instituciones.py), [`web/instituciones.html`](web/instituciones.html).

- Grano: `hecho_indicadores` (institución × carrera-título). Identificador: `f"{codigo_institucion}--{slugify(carrera_titulo)}"`. 0 colisiones sobre 1690 filas válidas.
- Índice único: `web/data/instituciones.json` (1690 combos + bandas de ingreso ordenadas + diagnóstico).
- Banda de ingreso: `ingreso_banda_min`/`ingreso_banda_max` en CLP. Banda abierta ("Sobre $3.5M") con `ingreso_banda_abierta=True`.
- 16 de 1690 combos con `tiene_ficha=False` (FK colgante en `dim_institucion`).
- UF detectada en 42 combos (113 filas de `hecho_oferta`) — se expone `arancel_moneda` explícito, nunca se mezcla con CLP.
- **Panel de info general de institución:** `InstitucionInfo` extendido con `anios_acreditacion`, `vigencia_acreditacion`, `areas_acreditadas`, `direccion_sede_central`, `pagina_web`, `tipo_sociedad`.
- **Arancel cruzado escalonado por certeza:** Nivel 1 exacto (1196 combos, 70.77%) vs. Nivel 2 rango (494, 29.23%). Nivel 2 cae directo a rango `[mín, máx]` — fuzzy-match diferido (Tarea 22).
- **TODO explícito:** fuzzy-match de los 494 combos Nivel 2 → Tarea 22 (ver roadmap activo).

### Tarea 8 — Auditoría comparativa College Scorecard
**Completada (2026-06-25).** Sin código. 3 sub-agentes WebFetch/WebSearch.

Hallazgo clave: Scorecard separa instituciones/programas en toggle dentro de `/compare/` — confirma nuestra arquitectura de dos pestañas separadas.

Backlog aprobado (ítems vigentes):
- 1: Filtros "Buscar instituciones" → absorbido en Tarea 15.
- 2: Autocomplete "Explorar carreras" → absorbido en Tarea 15.
- 3: Búsqueda→Comparar (botón "Add to Compare") → descartado hasta que existan pantallas de exploración.
- 6: Validación con estudiantes reales antes del rediseño visual.
- 7: Aviso de usabilidad suave (≥7 tarjetas) → implementado en Tarea 11.
- 8: Ponderaciones PAES → implementado en Tarea 9.
- 10: Share URL → Tarea 16.

### Tarea 8b — Exploración complementaria en vivo
**Completada (2026-06-25).** Diego navegó `collegescorecard.ed.gov` con extensión Claude en Chrome. Hallazgos en [`tarea_8b_exploracion/hallazgos.md`](tarea_8b_exploracion/hallazgos.md).

Correcciones al backlog: ítem 4 no son 4 tabs sino 6 secciones acordeón (`College Information / Costs / Graduation & Retention / Financial Aid & Debt / Typical Earnings / Test Scores & Acceptance`). "Student Body" no existe en `/compare/`, solo en `/school/`. Acordeón confirmado para Sesión 3b (luego revertido a layout plano por preferencia de Diego). Ítem 10 (Share URL) agregado.

### Tarea 9 — Ponderaciones PAES
**Completada (2026-06-25).** Fuente: `mifuturo/Buscador_de_Carreras_2025_2026_SIES_EEE.xlsx` (7 de 8 columnas ya en `hecho_oferta`; solo faltaba `Otros ` con espacio trailing). DB regenerada.

- `OfertaInstitucion` extendido con 8 campos de ponderación + `tiene_ponderacion_paes`.
- `index.html`: mini barra apilada CSS (8 segmentos normalizados por suma real) en "dónde se imparte". Badge "Sin ponderación PAES" para IPs/CFTs.
- `instituciones.html`: mini barra + badge "varía por sede/jornada" (81 combos, 4.8%).
- 974/1690 combos con ponderación; 716 sin ella. Suma > 100 normal (electivos chilenos).

### Tarea 10 — Glosario interactivo (tooltip inline)
**Completada (2026-06-25).** Solo `web/index.html` y `web/instituciones.html`.

Componente: `initTooltip()` + `.tooltip-btn` + `#tooltip-popup` (position:fixed, arrow via `::after`, cierre con Escape/focusout/clic fuera, `role=tooltip` + `aria-describedby`). Helper `infoIcon(texto)` reutilizado en todas las funciones JS de renderizado. 19 tooltips en total (10 en index, 9 en instituciones). Drawer lateral → diferido a Tarea 21.

### Tarea 11 — Polish de tarjetas
**Completada (2026-06-25).** Solo `web/index.html` y `web/instituciones.html`.

- Fila de íconos (`.card-icon-chip`): 🎓 Área · 🏛/🏢/🏫 tipo · ⭐ acreditación.
- Métricas titulares (`.card-metrics-row`): Emp. 1er año + Ingreso 4° año por tarjeta.
- Aviso de usabilidad suave en `hidden`, se activa cuando `selected.length >= 7`.
- Ajustes post-cierre: colores electivos (Hist./Ciencias) unificados a rosado `#e879a0`; nota de asteriscos eliminada; agrupación `Hist./Ciencias X%` restaurada.

### Tareas 6 Sesión 3a y 3b (registro integrado en Tarea 6 arriba)

### Rediseño marca Carrera Clara — index_v2.html e instituciones_v2.html (2026-06-27)
Registrado en la sección Tarea 6 arriba. Logo blanco con fondo transparente en `web/assets/logo-carrera-clara-blanco.png`. Manual de marca en [`MANUAL_MARCA_CARRERA_CLARA.md`](MANUAL_MARCA_CARRERA_CLARA.md).

---

## Notas de cruce de datos (referencia permanente)

- Join institución: siempre por **código** (no por nombre — formatos distintos entre archivos).
- Join `hecho_oferta`→carrera: por **`Área Carrera Genérica`** (99.47% cobertura).
- Benchmark NO se cruza a institución (es agregado nacional).
- `matricula/Matricula_2025_WEB_15_07_2025.csv`: `;`-delimitado, encoding Latin-1, usar `encoding='latin-1'`.
- Ningún estado explícito se oculta: "sin benchmark", "institución sin ficha", "sin ponderación PAES", "arancel en UF" siempre se marcan visualmente.
