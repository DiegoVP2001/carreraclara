# TAREA 21 — PWA instalable en celular

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.
Dos páginas canónicas: `web/index_v2.html` (comparar carreras) y `web/instituciones_v2.html` (comparar instituciones).
No hay build step; todo es vanilla JS + Chart.js. Servidor de desarrollo: `python -m http.server 8000` desde `web/`.

Tareas anteriores relevantes:
- **T20** — Optimización móvil completada: touch targets ≥44px, tabla con overflow-x, panel filtros colapsable, share bar wrap.
- **T22** — Organizar repo para GitHub (siguiente después de esta).
- **T23** — Deploy en carreraclara.cl (fin MVP).

---

## ⚠️ FLUJO OBLIGATORIO: plan → aprobación → ejecución

**Antes de escribir una sola línea de código**, hacer lo siguiente:

1. Revisar el estado actual: ¿existe ya algún `manifest.json` o `sw.js` en `web/`?
2. Presentar a Diego un plan detallado con los archivos a crear/modificar.
3. Esperar confirmación explícita de Diego antes de implementar.

---

## Qué hace esta tarea

Convertir las dos páginas en una **Progressive Web App (PWA)** que el usuario pueda instalar en la pantalla de inicio del celular y que funcione offline con los datos ya cargados.

### Componentes a implementar

1. **`web/manifest.json`** — Web App Manifest con:
   - `name`: "Carrera Clara"
   - `short_name`: "CarreraClara"
   - `start_url`: `./index_v2.html`
   - `display`: `standalone`
   - `theme_color`: `#0f2e45` (color del header)
   - `background_color`: `#f5f6f4`
   - `icons`: al menos 192×192 y 512×512 (generar desde `logo_png_azul-removebg-preview.png` o usar el PNG existente si ya tiene tamaño suficiente)
   - `scope`: `./`

2. **`web/sw.js`** — Service Worker con estrategia **Cache First** para:
   - HTML de ambas páginas (`index_v2.html`, `instituciones_v2.html`)
   - Datos JSON (`data/core.json`, `data/instituciones.json`)
   - Assets: logo, fuentes (si están en caché del navegador)
   - Chart.js desde CDN (cache externo)
   - Versión de caché: `carreraclara-v1`
   - Estrategia: precache al install, fallback a red si falta algo

3. **Registro del SW** en ambas páginas HTML:
   - `<link rel="manifest" href="manifest.json">` en `<head>`
   - Script de registro al final del `<body>`:
     ```js
     if ('serviceWorker' in navigator) {
       navigator.serviceWorker.register('./sw.js');
     }
     ```

4. **Meta tags para iOS** (Safari no lee manifest para splash screen):
   - `<meta name="apple-mobile-web-app-capable" content="yes">`
   - `<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">`
   - `<link rel="apple-touch-icon" href="logo_png_azul-removebg-preview.png">`

### Consideraciones técnicas

- Los datos de detalle por carrera están en `data/detalle/<slug>.json` (lazy load). El SW **no** debe precachear todos — son muchos archivos. Solo cachear cuando se visiten (network-first para `detalle/`).
- El manifest y SW deben servirse desde el mismo origen que las páginas (ya están en `web/`).
- Para probar la instalabilidad: Chrome DevTools → Application → Manifest + Service Workers.
- **No se necesita build step**: el SW se puede escribir en vanilla JS sin bundler.

## Archivos a crear/modificar

- `web/manifest.json` (nuevo)
- `web/sw.js` (nuevo)
- `web/index_v2.html` (agregar `<link rel="manifest">` y script de registro)
- `web/instituciones_v2.html` (ídem)

## Criterio de "tarea completa"

- Plan aprobado por Diego antes de implementar.
- Chrome DevTools → Application muestra manifest válido y SW registrado.
- El prompt de instalación "Agregar a pantalla de inicio" aparece en móvil (o se puede instalar manualmente desde el menú del browser).
- La página carga offline después de la primera visita (al menos `index_v2.html` y `instituciones_v2.html` con los datos `core.json` e `instituciones.json`).
- `PLAN.md` actualizado con T21 ✅.
- `TAREA_22_PROMPT.md` generado (organizar repo para GitHub).
