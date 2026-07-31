# TAREA 23 — Deploy en carreraclara.cl con Vercel + DNS

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl.

**Estado al inicio de esta tarea:**
- T22 completa: repo limpio con commit inicial en rama `main` (204 archivos).
- Solo `web/` está commiteado: `landing.html`, `index_v2.html`, `instituciones_v2.html`, `manifest.json`, `sw.js`, `assets/`, `data/`.
- `.gitignore` excluye datasets SIES, imágenes de debugging, archivos de trabajo.
- El repo **todavía no tiene remote en GitHub** — eso es parte de esta tarea.
- Deploy: **Vercel** (elegido por Diego porque le funcionó bien en otro proyecto). NO GitHub Pages.
- Dominio objetivo: `carreraclara.cl` (Diego tiene el dominio; verificar si ya está comprado o pendiente).

## Páginas canónicas

| Página | Archivo | URL esperada en producción |
|---|---|---|
| Landing (entrada) | `web/landing.html` | `carreraclara.cl/` ó `carreraclara.cl/landing.html` |
| Tipos de carrera | `web/index_v2.html` | `carreraclara.cl/index_v2.html` |
| Carreras por institución | `web/instituciones_v2.html` | `carreraclara.cl/instituciones_v2.html` |

## ⚠️ FLUJO OBLIGATORIO: plan → aprobación → ejecución

Antes de ejecutar cualquier acción en servicios externos (GitHub, Vercel, DNS):
1. Presentar el plan detallado a Diego.
2. Esperar confirmación explícita.

---

## Qué hace esta tarea

Dejar la app accesible en `carreraclara.cl` para cualquier usuario.

### Pasos esperados

1. **Crear repo en GitHub**
   - Nombre sugerido: `carreraclara` (público)
   - Confirmar con Diego el nombre antes de crear
   - `git remote add origin <url>` + `git push -u origin main`

2. **Configurar Vercel**
   - Importar repo desde GitHub en vercel.com
   - Vercel detectará proyecto estático (sin build step)
   - Configurar **Root Directory = `web/`** para servir solo esa carpeta
   - Verificar que `landing.html` sea la ruta raíz (o configurar redirect `/` → `/landing.html`)

3. **Configurar dominio personalizado en Vercel**
   - Añadir `carreraclara.cl` en Vercel → Project → Domains
   - Vercel entregará los DNS records (generalmente un CNAME o A record)
   - Diego actualiza los records en su registrador de dominio

4. **Actualizar README.md** — añadir link real a `carreraclara.cl`

5. **Verificar PWA en producción**
   - El Service Worker (`sw.js`) requiere HTTPS — Vercel lo provee automáticamente
   - Confirmar que el manifest y el SW se cargan correctamente
   - Probar instalación en celular (Android/iOS)

### Preguntas a hacer ANTES de diseñar el plan

- ¿El dominio `carreraclara.cl` ya está comprado? ¿En qué registrador?
- ¿Quieres que `carreraclara.cl` redirija a `landing.html` automáticamente, o prefieres que `index_v2.html` sea la página de entrada?
- ¿El repo GitHub debe ser público o privado?
- ¿Tienes cuenta en Vercel creada, o hay que crearla?

### Consideraciones técnicas

- **Vercel + sitios estáticos:** Vercel sirve archivos estáticos sin configuración. Solo hay que asegurarse de que el `Root Directory` apunte a `web/` para que las rutas relativas funcionen.
- **Service Worker y rutas:** El SW usa `./` como base; en Vercel funcionará correctamente porque el root directory es `web/`.
- **HTTPS:** Vercel incluye certificado SSL automático — el SW quedará activo desde el primer deploy.
- **Caché CDN de Vercel:** Los archivos JSON de `web/data/` se servirán desde el CDN edge de Vercel, lo que mejora la velocidad de carga.

## Archivos a crear/modificar

- `README.md` — añadir link a producción
- `vercel.json` (opcional) — solo si se necesita configurar redirects o headers

## Criterio de "tarea completa"

- Repo público en GitHub con remote configurado.
- App accesible en `carreraclara.cl` (con HTTPS).
- `landing.html` como página de entrada.
- PWA instalable verificada en celular.
- `README.md` actualizado con link a producción.
- `PLAN.md` marcado T23 ✅.
