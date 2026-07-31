# TAREA 22 — Organizar repo para GitHub

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Páginas canónicas: `web/index_v2.html` (Tipos de carrera) y `web/instituciones_v2.html` (Carreras por institución).
Landing: `web/landing.html`. No hay build step; todo es vanilla JS + Chart.js.

Tareas anteriores relevantes:
- **T21** — PWA completa: `web/manifest.json`, `web/sw.js`, meta tags iOS en las 3 páginas, SW activado con 14 archivos en caché `carreraclara-v1`.
- **T23** — Deploy en carreraclara.cl con GitHub Pages (siguiente después de esta).

---

## ⚠️ FLUJO OBLIGATORIO: plan → aprobación → ejecución

**Antes de escribir una sola línea de código o mover un solo archivo**, hacer lo siguiente:

1. Auditar el estado actual del repo (archivos obsoletos, estructura, `.git`).
2. Presentar a Diego un plan detallado con los cambios a hacer.
3. Esperar confirmación explícita de Diego antes de implementar.

---

## Qué hace esta tarea

Dejar el repositorio limpio y listo para publicarse en GitHub, de modo que T23 (deploy) sea solo configurar GitHub Pages y DNS.

### Componentes a revisar / implementar

1. **`.gitignore`** — Crear o revisar. Excluir:
   - `__pycache__/`, `*.pyc`
   - `.DS_Store`, `Thumbs.db`
   - Archivos temporales de Python (`*.log`, `diagnostico_*.py` si son temporales)
   - Los archivos `.xlsx`/`.csv`/`.pdf` de datos crudos SIES si son muy pesados para el repo (decidir con Diego)

2. **Archivos obsoletos en `web/`** — Evaluar qué hacer con:
   - `web/index.html` y `web/instituciones.html` (backups v1, no canónicos)
   - `web/index_v2_T19c.html` y `web/instituciones_v2_T19c.html` (snapshots intermedios)
   - `web/diagnostico_arancel.py` (script temporal de análisis)
   - Decidir: ¿mover a `old/`? ¿eliminar? ¿dejar?

3. **`README.md`** — Crear uno limpio en la raíz del repo con:
   - Qué es Carrera Clara (2–3 líneas)
   - Cómo correr localmente (`python -m http.server 8000` desde `web/`)
   - Cómo regenerar los datos (`export_json.py`, `export_instituciones.py`)
   - Link a la versión live (carreraclara.cl — se añadirá en T23)
   - Fuente de datos: SIES / MiFuturo.cl (con link)

4. **Estructura del repo** — Confirmar que la raíz tiene sentido pública:
   - ¿Los archivos de trabajo (`PLAN.md`, `TAREA_*_PROMPT.md`, `old/`) deben estar en el repo público?
   - ¿Los datos crudos SIES (`mifuturo/`, `oferta/`, `matricula/`, etc.) van al repo o solo `web/`?
   - Opción A: repo contiene todo (datos + web + scripts)
   - Opción B: repo solo contiene `web/` (lo que se sirve)

5. **Primer commit limpio** — Una vez acordada la estructura:
   - `git add` selectivo (no `git add .` ciego)
   - Commit inicial con mensaje descriptivo

### Consideraciones

- Los datasets SIES son públicos (MiFuturo.cl), por lo que no hay problema de confidencialidad, pero pesan varios MB — revisar si GitHub los acepta (límite 100 MB por archivo, 2 GB por repo).
- `web/data/instituciones.json` pesa ~2.9 MB — dentro del límite de GitHub.
- Los `.xlsx` originales pueden pesar más — evaluar con Diego.

## Archivos a crear/modificar

- `.gitignore` (nuevo o actualizar)
- `README.md` (nuevo en raíz)
- Posibles movimientos/eliminaciones en `web/` y raíz (a confirmar con Diego)

## Criterio de "tarea completa"

- Plan aprobado por Diego antes de implementar.
- `.gitignore` cubre temporales y (si se decide) datos pesados.
- `README.md` permite a cualquiera clonar y correr el proyecto.
- `git status` muestra un estado limpio y coherente.
- `PLAN.md` actualizado con T22 ✅.
- `TAREA_23_PROMPT.md` generado (deploy en carreraclara.cl).
