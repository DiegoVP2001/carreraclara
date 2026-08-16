# Plan maestro — Comparador de carreras

> Roadmap activo. Para el historial de tareas completadas (Tareas 1–12), arquitectura de datos y decisiones de diseño, ver **[PLAN_HISTORIAL.md](PLAN_HISTORIAL.md)**.

## Visión del proyecto

Visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES que permita a un estudiante explorar y comparar carreras (empleabilidad, ingresos, retención) sin procesar tablas crudas. Persona principal: estudiante explorando vocacionalmente.

## Archivos activos

| Archivo | Rol |
|---|---|
| `web/index_v2.html` | Tipos de carrera — **canónico** |
| `web/instituciones_v2.html` | Carreras por institución — **canónico** |
| `web/nem.html` | Qué NEM necesito — **canónico** (T24) |
| `old/web_v1/index.html` | Backup de versión anterior (movido en T22) |
| `old/web_v1/instituciones.html` | Backup de versión anterior (movido en T22) |
| `web/data/core.json` | 190 carreras genéricas + benchmarks |
| `web/data/detalle/<slug>.json` | Oferta por carrera (lazy load), incluye `promedio_nem_2025`/`promedio_paes_2025` desde T24 |
| `web/data/instituciones.json` | 1690 combos institución × carrera-título (`hecho_indicadores`) — usado por "Carreras por institución" |
| `web/data/instituciones_nem.json` | Institución → carreras con oferta real en `hecho_oferta` (T24) — usado por "Qué NEM necesito"; **no** reusa `instituciones.json` porque esa fuente no es superset de `hecho_oferta` (ver T24 en el historial) |
| `mifuturo/processed/comparador.db` | SQLite fuente de verdad (índice `idx_hecho_oferta_inst_generica` agregado en T24) |
| `web/export_json.py` | Regenera `core.json` + `detalle/` + `instituciones_nem.json` |
| `web/export_instituciones.py` | Regenera `instituciones.json` |
| `dev_server.py` | Server local con los rewrites de `vercel.json` (multi-hilo desde T24; revisión antes de aprobar) |

## Reglas de sesión (siempre, aunque Diego no lo pida)

Al terminar la implementación de cada tarea:

1. **Abrir en el navegador** — levantar `python dev_server.py` desde la raíz y abrir la página con `Start-Process "http://localhost:8000/<ruta-limpia>"` (`/`, `/tipos-de-carrera`, `/carreras-por-institucion`). No usar `python -m http.server`: no aplica los rewrites de `vercel.json` y los enlaces internos se ven rotos.
2. Cuando Diego confirme que está conforme:
   - **Marcar la tarea como completada** en la tabla de abajo (fecha + resumen de 2 líneas).
   - **Generar `TAREA_N_PROMPT.md`** para la siguiente tarea pendiente si aún no existe, y moverlo a `old/` cuando se ejecute.

## Roadmap activo

| # | Nombre | Archivos principales | Estado |
|---|---|---|---|
| **13** | Layout 3 columnas | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-27 — `ul#selected-list` → CSS Grid 3/2/1 cols por breakpoint; fix desborde en `.pond-label` (quitado `white-space: nowrap`); `min-width: 0` + `flex: 1` en nombre de tarjeta. |
| **14** | Marca prominente en header/footer | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-27 — Eslogan opacidad 72→85% (contraste WCAG); atribución "Datos: SIES / MiFuturo.cl" en footer con link; fix link roto `instituciones.html`→`instituciones_v2.html`. |
| **15** | Filtros en comparación | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-27 — Select "Área" en index_v2 filtra autocomplete de carreras; select "Tipo" en instituciones_v2 filtra autocomplete de instituciones. `familia` no disponible en datos; región no exportada en instituciones.json. |
| **15b** | Filtros adicionales | `instituciones_v2.html` | ✅ 2026-06-27 — Panel lateral izquierdo sticky con 6 filtros: Tipo, Área (selects) + Acreditación mín., Empleabilidad mín., Arancel máx., Duración máx. (sliders dinámicos). Respaldo en `old/instituciones_v2_arriba.html`. |
| **15c** | Favicon | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-27 — `<link rel="icon">` con `logo_png_azul-removebg-preview.png` copiado en `web/` (ruta relativa al servidor). Visible en pestaña. |
| **16** | Compartir comparativas (Share URL) | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-27 — Hash URL (`#c=slug1,slug2` / `#i=id1,id2`); restore automático al cargar; share bar visible con ≥2 ítems; toast "¡Enlace copiado!" con fallback para contextos no-HTTPS. |
| **17** | "Dónde se imparte" mejorado | `index_v2.html` | ✅ 2026-06-27 — Stats bar (N instituciones, N regiones, rango arancel); badges tipo (Universidades/IPs/CFTs) y acreditación con color; empleabilidad 1er año en summary; regiones compactas (>3 → "N regiones"); fix `white-space: nowrap` en `<th>` y float duración real. |
| **18** | Gráfico Arancel 2026 rediseñado | `instituciones_v2.html` | ✅ 2026-06-27 — Barras ordenadas de menor a mayor arancel; color por tipo de institución (Universidad=azul, IP=naranja, CFT=verde); línea punteada roja para el promedio; leyenda dinámica muestra tipos presentes. |
| **19** | Animaciones y microinteracciones — tarjetas | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-28 — Fade-in/slide-in al agregar tarjetas (`is-entering` + doble rAF); fade-out+scale al quitar (`is-removing` + `transitionend`); tracking con `_renderedSlugs`/`_renderedIds` para animar solo tarjetas genuinamente nuevas. |
| **19b** | Animaciones extendidas — más elementos de ambas páginas | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-28 — Custom select animado (fade+translateY+chevron rotate) reemplaza `<select>` nativo en filtros Tipo/Área (`instituciones_v2`) y Área (`index_v2`). Nativo queda oculto como fuente de verdad; `buildCustomSelect()` compartido. |
| **19c** | Hover/focus animations en tarjetas y filtros | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-28 — Lift+sombra en cards; × rojo+scale; btn-agregar brightness+press; autocomplete y custom-select → hover azul header (#0f2e45); ring focus en inputs; summaries y filas de tabla con transition. Versiones de respaldo en `_T19c.html`. |
| **19d** | "Dónde se imparte" — animaciones y contraste mejorado | `index_v2.html` | ✅ 2026-06-28 — Accordion suave (open: fade+translateY, close: animación inversa via JS); flecha `▾` custom con rotate(180°) al abrir; institution-cards internas con misma animación bidireccional; filtros Región/Jornada/Tipo convertidos a custom selects animados (CSS selector generalizado de `.selector-filters` a `.custom-select-list`); zebra stripes + sticky header + hover más fuerte en tabla. |
| **20** | Optimización móvil (touch targets, scroll, viewport 375px) | `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-29 — Tabla "Dónde se imparte" con wrapper `overflow-x: auto`; nav tabs con `flex-wrap`; touch targets ≥44px en botones ×, inputs, autocomplete y btn-agregar; panel filtros colapsable en móvil (≤800px) con toggle JS; share bar apila en móvil; canvas `min-height: 200px`; custom-select `max-height` reducido. |
| **20b** | Landing Carrera Clara | `web/landing.html`, `index_v2.html`, `instituciones_v2.html` | ✅ 2026-06-29 — Nueva portada `landing.html`: hero navy (gradiente 155°) con logo 130px + marca + slogan, text-shadow en nombre, 2 CTAs blancos → verdes en hover, sección "Qué es / qué no es". Gradiente replicado en `header.app-header` de ambas herramientas. Tab "Inicio" y link "Inicio" en footer Explorar añadidos a las dos páginas. |
| **20c** | Renombrar herramientas | `index_v2.html`, `instituciones_v2.html`, `landing.html` | ✅ 2026-06-29 — "Comparar carreras" → "Tipos de carrera"; "Comparar instituciones" → "Carreras por institución". Descripciones breves añadidas en hero del landing. 7 ubicaciones actualizadas (titles, nav, footer, referencia cruzada interna). |
| **21** | PWA instalable en celular (manifest + service worker) | `web/manifest.json`, `web/sw.js`, `index_v2.html`, `instituciones_v2.html`, `landing.html` | ✅ 2026-06-29 — `manifest.json` (nombre, colores, icono); `sw.js` Cache First para HTML/datos/CDN, Network First para `detalle/`; meta tags iOS en las 3 páginas; 14 archivos en `carreraclara-v1`; SW `activated` verificado. |
| **22** | Organizar repo para GitHub (`.gitignore`, README, commit inicial) | raíz del proyecto | ✅ 2026-06-29 — `.gitignore` excluye datasets/PNGs/archivos de trabajo; obsoletos `web/v1*` movidos a `old/web_v1/`; `README.md` con instrucciones de uso; commit inicial `main` con 204 archivos (solo `web/`). |
| **23** | Despliegue en carreraclara.cl (Vercel + DNS) | `web/vercel.json`, `README.md`, GitHub, Vercel | ✅ 2026-06-29 — Repo público `DiegoVP2001/carreraclara` en GitHub; deploy en Vercel con root `web/`; nameservers NIC.cl → `ns1/ns2.vercel-dns.com`; rewrites limpios `/`, `/tipos-de-carrera`, `/carreras-por-institucion`; HTTPS activo. **MVP completo.** |
| **23b** | Sección de feedback inline (Web3Forms) | `web/landing.html` | ✅ 2026-06-29 — Formulario HTML inline entre "Qué es" y footer: campos tipo/mensaje/email, envío via `fetch()` a Web3Forms sin redirección, mensaje éxito/error inline. Card centrada (max-width 640px, border-top verde). Texto en primera persona ("me sirve"). |
| **23c** | Marca clickeable + botón de feedback siempre a mano | `index_v2.html`, `instituciones_v2.html`, `landing.html`, `sw.js` | ✅ 2026-07-31 — Header brand (logo + nombre + eslogan) convertido en `<a href="/">` en ambas herramientas. Botón flotante verde abajo-derecha en las 3 páginas: en las herramientas abre un modal con el formulario Web3Forms completo (campo oculto `pagina` + asunto por herramienta para saber el origen); en la portada baja a la sección existente y se auto-oculta cuando está a la vista. SW → `carreraclara-v3`. |
| **23d** | Anti-spam (captcha) en el formulario de feedback | `landing.html`, `index_v2.html`, `instituciones_v2.html`, `nem.html`, `sw.js` | ✅ 2026-08-16 — Se evaluó primero Cloudflare Turnstile (widget creado en la cuenta de Diego, Site Key `0x4AAAAAAERrm3424THTgZTO`) pero se descartó: la validación server-side (siteverify) requiere plan pago de Web3Forms. Se implementó en su lugar hCaptcha vía la integración nativa de Web3Forms (`web3forms.com/client/script.js`, sin llaves propias) — coincide con el "Advanced Spam Filter" que Diego ya tenía activado gratis en su cuenta. SW → `carreraclara-v11`. Verificado funcionando en producción (carreraclara.cl). |
| **24** | "Qué NEM necesito" (pestaña nueva) | `web/nem.html`, `mifuturo/queries.py`, `web/export_json.py`, `web/export_instituciones.py`, `mifuturo/loader.py` | ✅ 2026-08-15 — 4ta herramienta: institución + carrera (selector 2 pasos igual a "Carreras por institución") → tabla ordenable de NEM/PAES promedio real 2025 + ponderaciones PAES por sede/jornada. Descubrió y corrigió un hueco de cobertura real: `instituciones.json` (`hecho_indicadores`) no es superset de `hecho_oferta` — 1183 combos institución+carrera con NEM/PAES real quedaban invisibles (ej. admisión por "plan común" en U. de Chile/PUC). Nuevo `data/instituciones_nem.json` construido directo desde `hecho_oferta`. De paso: índice en `hecho_oferta` (queries de ~0.25s → <0.002s) y `dev_server.py` multi-hilo (single-thread colgaba fetches concurrentes). |
| **25** | Auditoría de datos no considerados por error | `mifuturo/`, `web/*.html`, `web/export_*.py` | Próxima sesión — motivada por el hueco de cobertura encontrado en T24: revisar sistemáticamente si hay columnas/datos disponibles en los datasets fuente que no se cargaron, se cargaron pero no se exportaron, o se exportaron pero no se muestran en ninguna de las 4 pantallas. Ver `TAREA_25_PROMPT.md`. |
| **26** | Brainstorm: qué construir con toda la data disponible | ninguno (sesión de ideación, sin código) | En cola detrás de T25 — depende de sus hallazgos. Ver `TAREA_26_PROMPT.md`. |
| **27** | Ficha de institución (pantalla nueva) | nuevo archivo | Post-MVP |
| **28** | Drawer glosario completo | `index_v2.html`, `instituciones_v2.html` | Post-MVP |
| **29** | Fuzzy-match arancel Nivel 2 | `mifuturo/`, `export_instituciones.py` | Post-MVP — prioridad mínima |

## Pendiente, explícitamente no ahora

- Cruce futuro con `matricula/`, `titulados/`, `personal/` y puntajes de corte DEMRE (fuente externa aún no descargada).
- "Explorar carreras" y "Buscar instituciones" como pantallas separadas — absorbidas en Tarea 15 como filtros sobre las vistas existentes.
- Exportación PDF/Excel — decisión de fase 3.
- Pantalla propia de "Buscar → Agregar a comparación" (backlog ítem 3) — solo aplica si se construyen pantallas de exploración dedicadas.
