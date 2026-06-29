# Carrera Clara

Visualizador interactivo de carreras de educación superior en Chile. Permite explorar y comparar programas universitarios, de institutos profesionales y centros de formación técnica según empleabilidad, ingresos, matrícula, acreditación y aranceles.

Datos fuente: [SIES / MiFuturo.cl](https://mifuturo.cl) — Servicio de Información de Educación Superior (MINEDUC).

## Demo

🚧 *Próximamente en carreraclara.cl*

## Correr localmente

```bash
# Desde la raíz del repositorio
python -m http.server 8000 --directory web
```

Luego abrir en el navegador:
- **Inicio:** http://localhost:8000/landing.html
- **Tipos de carrera:** http://localhost:8000/index_v2.html
- **Carreras por institución:** http://localhost:8000/instituciones_v2.html

No hay build step — todo es HTML/CSS/JS vanilla + Chart.js (CDN).

## Regenerar los datos JSON

Los archivos en `web/data/` se generan a partir de los datasets SIES con dos scripts Python:

```bash
# Datos de tipos de carrera (web/data/carreras.json)
python web/export_json.py

# Datos por institución (web/data/instituciones.json)
python web/export_instituciones.py
```

Requieren los datasets SIES originales en las carpetas `mifuturo/`, `matricula/`, `oferta/`, `titulados/` y `personal/` (no incluidos en este repo por tamaño).

## Fuente de datos

Todos los datos provienen de fuentes públicas del MINEDUC:

| Dataset | Fuente |
|---|---|
| Buscador de Carreras 2025–2026 | [mifuturo.cl](https://mifuturo.cl) |
| Empleabilidad e Ingresos 2025–2026 | SIES |
| Oferta Académica 2026 | SIES |
| Matrícula 2025 | SIES |
| Titulados 2007–2025 | SIES |
