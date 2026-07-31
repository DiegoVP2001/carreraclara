# Carrera Clara

Visualizador interactivo de carreras de educación superior en Chile. Permite explorar y comparar programas universitarios, de institutos profesionales y centros de formación técnica según empleabilidad, ingresos, matrícula, acreditación y aranceles.

Datos fuente: [SIES / MiFuturo.cl](https://mifuturo.cl) — Servicio de Información de Educación Superior (MINEDUC).

## Demo

[carreraclara.cl](https://carreraclara.cl)

## Correr localmente

```bash
python dev_server.py
```

Luego abrir en el navegador:
- **Inicio:** http://localhost:8000/
- **Tipos de carrera:** http://localhost:8000/tipos-de-carrera
- **Carreras por institución:** http://localhost:8000/carreras-por-institucion

No hay build step — todo es HTML/CSS/JS vanilla + Chart.js (CDN).

`dev_server.py` sirve `web/` aplicando los mismos rewrites que Vercel usa en producción, leídos de `web/vercel.json`. **Un `python -m http.server` a secas no sirve para revisar el sitio:** las URLs limpias no existirían y `/` devolvería el listado de directorio en vez de la portada, así que los enlaces internos (incluido el logo del header) se verían rotos aunque en producción funcionen.

## Regenerar los datos JSON

Los archivos en `web/data/` se generan a partir de los datasets SIES con dos scripts Python:

```bash
# Carreras genéricas + benchmarks (web/data/core.json y web/data/detalle/)
python web/export_json.py

# Datos por institución (web/data/instituciones.json)
python web/export_instituciones.py
```

Requieren los datasets SIES originales en las carpetas `mifuturo/`, `matricula/`, `oferta/`, `titulados/` y `personal/` (no incluidos en este repo por tamaño).

## Estructura del repo

| Ruta | Qué es |
|---|---|
| `web/` | La app: 3 HTML autocontenidos, `data/`, `assets/`, `sw.js`, `manifest.json`, `vercel.json` |
| `dev_server.py` | Server local con los rewrites de producción |
| `PLAN.md` | Roadmap activo, tarea por tarea |
| `PLAN_HISTORIAL.md` | Tareas 1–12, arquitectura de datos y decisiones de diseño |
| `TAREA_N_PROMPT.md` | Prompt de arranque de la sesión siguiente |
| `CLAUDE.md` | Instrucciones de trabajo para Claude Code |
| `MANUAL_MARCA_CARRERA_CLARA.md` | Manual de marca |
| `old/` | Prompts ya ejecutados y respaldos de versiones anteriores |

Los datasets SIES originales (`mifuturo/`, `matricula/`, `oferta/`, `titulados/`, `personal/`) no están versionados por tamaño — se descargan de mifuturo.cl.

## Fuente de datos

Todos los datos provienen de fuentes públicas del MINEDUC:

| Dataset | Fuente |
|---|---|
| Buscador de Carreras 2025–2026 | [mifuturo.cl](https://mifuturo.cl) |
| Empleabilidad e Ingresos 2025–2026 | SIES |
| Oferta Académica 2026 | SIES |
| Matrícula 2025 | SIES |
| Titulados 2007–2025 | SIES |
