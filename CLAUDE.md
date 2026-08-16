# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

**Carrera Clara** — a career comparator for Chilean higher education, live at [carreraclara.cl](https://carreraclara.cl). It lets students compare university/IP/CFT programs (employability, income, retention, accreditation, tuition) using official SIES datasets from mifuturo.cl.

The MVP shipped in T23. Development continues in approved sessions (see *Flujo de sesiones* below).

### Stack

Static site, **no build step**: three self-contained HTML files with inline CSS and JS, plus Chart.js from CDN. Deployed on Vercel with root directory `web/`.

| Page | File | Production URL |
|---|---|---|
| Portada | `web/landing.html` | `/` |
| Tipos de carrera | `web/index_v2.html` | `/tipos-de-carrera` |
| Carreras por institución | `web/instituciones_v2.html` | `/carreras-por-institucion` |
| Qué NEM necesito | `web/nem.html` | `/que-nem-necesito` |

Clean URLs come from `rewrites` in `web/vercel.json` — **any new route needs its rewrite there.** `web/sw.js` caches HTML with a Cache First strategy, so **bump `CACHE_VERSION` whenever an HTML file changes** or returning visitors keep the old version.

Data is precomputed into JSON by `web/export_json.py` (→ `data/core.json` + `data/detalle/<slug>.json` + `data/instituciones_nem.json`) and `web/export_instituciones.py` (→ `data/instituciones.json`), both reading from `mifuturo/processed/comparador.db`. The datasets below are the upstream source for that DB. **Note:** `instituciones.json` (grain: institución×carrera-título, from `hecho_indicadores`) and `instituciones_nem.json` (grain: institución×carrera-genérica, from `hecho_oferta`) are deliberately separate exports — one is not a superset of the other (confirmed in T24: 1183 institución+carrera combos have real oferta data but no matching título row). Don't assume you can derive one from the other client-side.

Since these are single-file pages, header, footer, share bar and form styles are **deliberately duplicated** across them — match the existing copy when adding a shared element rather than introducing a build step.

## Repository layout

Each dataset folder corresponds to one SIES public dataset family. Files are the originals downloaded from mifuturo.cl/SIES — treat them as read-only source data; never edit them in place. They are not versioned (too large); download them from mifuturo.cl if missing.

| Folder | Dataset | Key file(s) |
|---|---|---|
| `mifuturo/` | "Buscador" dashboards: careers, institutions, employability/income, and per-career statistics | `Buscador_de_Carreras_2025_2026_SIES_EEE.xlsx`, `Buscador_Empleabilidad_ingresos_2025_2026_SIES.xlsx`, `Buscador_EstadísticasCarrera_2025_2026_SIES.xlsx`, `Buscador_Instituciones_2025_2026_SIES-vf.xlsx` |
| `oferta/` | Academic offer (Oferta Académica) — every program offered, by institution/region/area, 2010–2026 historical glossary included | `Oferta_Academica_2026_SIES_05_06_2026_WEB_E.xlsx`, `Glosario_Oferta_Academica_2010_al_2026_SIES_WEB_EE-1.pdf` |
| `matricula/` | Enrollment (Matrícula) counts by career/institution/region/demographics, 2025 | `Matricula_2025_WEB_15_07_2025.csv` (semicolon-delimited, Latin-1 encoded), `OFICIAL_GLOSARIO_MATRICULA_WEB_E.pdf` |
| `titulados/` | Graduates (Titulados) counts by career/institution/sex, 2007–2025 | `TITULADO_2025_web_27_05_2026_E.xlsx`, `GLOSARIO_DE_TITULADO_2007_2025_E.pdf` |
| `personal/` | Academic staff (PAC) — headcount and JCE (jornada completa equivalente) by institution, with age distributions | `PAC_web_2025_SIES_E.xlsx`, `OFICIAL_GLOSARIO_PAC_WEB_E.pdf` |

## Working with the datasets

- **Always check the matching glossary PDF** (`Glosario_*`/`*_GLOSARIO_*` files) before interpreting column codes (e.g. `CINE-F 1997/2013` area codes, institution classification levels I/II/III) — these acronyms are not self-explanatory.
- **Encoding/locale gotchas:**
  - `matricula/Matricula_2025_WEB_15_07_2025.csv` is `;`-delimited and Latin-1 (cp1252-ish) encoded, not UTF-8 — open with `encoding='latin-1'` in Python.
  - Spanish accented characters appear throughout headers and values (e.g. `Código`, `Educación`); avoid `print()` of raw strings on Windows consoles using cp1252 — use `PYTHONIOENCODING=utf-8` or write to files instead.
- **Excel files have decorative header rows.** Several workbooks (`Buscador_de_Carreras...`, `Buscador_EstadísticasCarrera...`, `Buscador_Instituciones...`) have a title/merged-cell row before the real column headers, and some have a throwaway `Hoja1` sheet — locate the real header row programmatically (look for the first row with multiple non-null string values) rather than assuming row 1.
- **Join key across datasets:** institution code (`CÓDIGO INSTITUCIÓN` / `Código`) and career name/code are the common keys to relate `matricula`, `titulados`, `oferta`, and `mifuturo` data. Career identifiers are not perfectly consistent across files (free-text "Nombre carrera" vs. coded fields) — expect fuzzy matching work when building any cross-dataset comparison.
- One zip in `matricula/` is prefixed `IGNORAR_` (Spanish for "ignore") — do not unpack or use it; it's an explicitly superseded/duplicate download kept for reference only.

## Flujo de sesiones y archivos de prompt

Este proyecto avanza en **sesiones discretas aprobadas por Diego**. Roadmap activo en `PLAN.md`; historial de tareas completadas (1–12) en `PLAN_HISTORIAL.md`.

Cada tarea tiene — o debe tener — un archivo `TAREA_N_PROMPT.md` en la raíz del proyecto.

**Reglas de cierre de sesión (siempre, aunque Diego no lo pida explícitamente):**

1. **Al terminar la implementación:** levantar `python dev_server.py` desde la raíz del proyecto y abrir la página con `Start-Process "http://localhost:8000/<ruta-limpia>"` para que Diego la revise en su navegador. **No usar `python -m http.server`**: no aplica los rewrites de `web/vercel.json`, así que `/` devuelve el listado de directorio y los enlaces internos (el logo del header apunta a `/`) se ven rotos aunque en producción funcionen. Rutas: `/`, `/tipos-de-carrera`, `/carreras-por-institucion`.
2. **Cuando Diego confirme que está conforme:**
   - Marcar la tarea como completada en `PLAN.md` (fecha + resumen de 2 líneas en la tabla del roadmap).
   - Generar `TAREA_N_PROMPT.md` para la siguiente tarea pendiente si aún no existe.
   - Mover el prompt ejecutado a `old/`.

**El archivo `TAREA_N_PROMPT.md`:**
- Se crea en la raíz de `comparador_carreras/` con nombre `TAREA_N_PROMPT.md` (N = número de tarea).
- Contiene: contexto mínimo para retomar en frío, archivos a tocar, decisiones ya tomadas y criterio de "tarea completa".
- **No adelanta código ni implementación** — es un prompt de arranque.

Prompt activo: `TAREA_26b_PROMPT.md` — continuación de T26: sesión de conversación con Diego para discutir `BRAINSTORM_T26.md` (ideas de datos internos T25 + investigación externa de 8 subagentes sobre comparadores similares) y decidir qué dirección priorizar. `TAREA_26_PROMPT.md` (brainstorm original) ya generó su entregable (`BRAINSTORM_T26.md`) pero T26 sigue sin marcarse ✅ hasta que esta conversación cierre con una dirección elegida. T25 (auditoría de datos) y T25b (decisión de no ampliar cobertura en "Carreras por institución", documentada en `GUIA_FUENTES_DE_DATOS.md`) completadas y aprobadas. T26c (compartir comparación — reubicar el botón, sin prompt file propio, pedido directo de Diego fuera de la cola T26/T26b) completada y en producción 2026-08-16. `TAREA_27_PROMPT.md` (Ficha de institución, post-MVP) ya está redactado y en cola desde antes de T26 — puede seguir siendo la prioridad, o T26b puede reordenarla; no se prejuzga.

## Conventions inherited from the parent workspace

See `../../CLAUDE.md` (claude_codex root) and `~/.claude/CLAUDE.md` for global conventions. Relevant ones here:
- Spanish (es-CL) for user-facing text/explanations; English for code identifiers and comments.
- If/when generating Office or PDF output from this data, use `python-docx`, `python-pptx`, `openpyxl`, `pymupdf` (never `fitz`), or `fpdf2`/`reportlab` — already the standard stack across this workspace.
- The pages follow the workspace's UI conventions: MathJax/KaTeX not needed here (no formulas), but keep everything self-contained, high-contrast and usable without a build step, per `playground`/`frontend-design` plugin guidance.
- **Never hide an empty state.** "Sin benchmark", "institución sin ficha", "sin ponderación PAES", "arancel aproximado" are always marked visually rather than omitted — a missing datum must read as missing, not as zero.
