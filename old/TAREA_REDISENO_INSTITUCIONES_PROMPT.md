# Prompt — Rediseño visual `instituciones_v2.html` (Carrera Clara)

> Usa este archivo para arrancar la sesión en frío. Lee el CLAUDE.md del proyecto antes de empezar.

---

## Contexto

El proyecto `comparador_carreras` ya tiene dos páginas funcionales:

- `web/index.html` — Comparar carreras genéricas (selector + gráficos de benchmark + panel "dónde se imparte")
- `web/instituciones.html` — Comparar instituciones×carrera (selector en 2 pasos: institución → carrera)

En la sesión anterior (2026-06-27) se creó `web/index_v2.html`: una versión de `index.html` con la identidad de marca **Carrera Clara** aplicada. **No se sobreescribió `index.html`** — es un archivo aparte.

Los cambios de `index_v2.html` respecto a `index.html` son exclusivamente de header y footer:

### Header nuevo (`index_v2.html`)
```html
<header class="app-header">
  <div class="header-inner">
    <div class="header-brand">
      <img src="assets/logo-carrera-clara-blanco.png" alt="Logo Carrera Clara" class="header-logo">
      <div class="header-brand-text">
        <span class="header-brand-name">Carrera Clara</span>
        <span class="header-brand-slogan">Elige con datos. Decide con claridad.</span>
      </div>
    </div>
    <nav class="tabs">
      <a href="index_v2.html" class="activo" aria-current="page">Comparar carreras</a>
      <a href="instituciones_v2.html">Comparar instituciones</a>
    </nav>
  </div>
</header>
```

### Footer nuevo (3 columnas, fondo navy `#0f2e45`)
```html
<footer class="app-footer">
  <div class="footer-grid">
    <div class="footer-col footer-col-brand">
      <div class="footer-logo-row">
        <img src="assets/logo-carrera-clara-blanco.png" alt="Carrera Clara" class="footer-logo">
        <span class="footer-brand-name">Carrera Clara</span>
      </div>
      <p>Herramienta independiente de visualización y análisis comparativo para explorar opciones de educación superior en Chile.</p>
      <p class="footer-copyright">© 2026 Carrera Clara. Todos los derechos reservados.<br>
      Desarrollado por <a href="https://www.linkedin.com/in/diegovp2001/" target="_blank" rel="noopener">Diego Vargas Palominos</a>.</p>
    </div>
    <div class="footer-col">
      <h3>Bases de datos</h3>
      <ul class="footer-links">
        <li><a href="https://www.mifuturo.cl/bases-de-datos-de-matriculados/#" target="_blank" rel="noopener">Bases de datos oficiales SIES</a></li>
        <li><a href="https://www.mifuturo.cl/" target="_blank" rel="noopener">Mi Futuro</a></li>
        <li><a href="https://educacionsuperior.mineduc.cl/" target="_blank" rel="noopener">Mineduc</a></li>
        <li><a href="https://demre.cl/" target="_blank" rel="noopener">DEMRE</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h3>Explorar</h3>
      <ul class="footer-links">
        <li><a href="index_v2.html">Comparar carreras</a></li>
        <li><a href="instituciones_v2.html">Comparar instituciones</a></li>
      </ul>
    </div>
  </div>
</footer>
```

### CSS agregado en `index_v2.html` (sección `<style>`)
Busca el bloque que empieza con `/* === CARRERA CLARA BRAND === */` dentro de `web/index_v2.html` — contiene todo el CSS nuevo del header/footer. Ese bloque completo debe copiarse también en `instituciones_v2.html`.

### Logo
`web/assets/logo-carrera-clara-blanco.png` ya existe (fondo transparente, "C" blanca + compás verde/ámbar). No hay que volver a generarlo.

### Elemento oculto para compatibilidad JS
`index_v2.html` tiene al final del `<body>` un `<ul id="diagnostico-list" hidden></ul>` para que el JS no rompa al buscar ese elemento. Revisa si `instituciones.html` tiene un elemento similar que el JS requiera y aplica el mismo patrón si es necesario.

---

## Tu tarea

Crear **`web/instituciones_v2.html`** aplicando exactamente los mismos cambios de header/footer de `index_v2.html`.

**Regla principal: NO sobreescribir `web/instituciones.html`.** El archivo nuevo es `instituciones_v2.html`.

### Pasos

1. Lee `web/instituciones.html` completo.
2. Lee `web/index_v2.html` para extraer:
   - El bloque CSS `/* === CARRERA CLARA BRAND === */`
   - El HTML del `<header class="app-header">`
   - El HTML del `<footer class="app-footer">`
3. Crea `web/instituciones_v2.html` como copia de `instituciones.html` con:
   - Header reemplazado por el de `index_v2.html`, pero con el tab **"Comparar instituciones"** marcado como activo (`class="activo" aria-current="page"`) y el link que apunta a `instituciones_v2.html`; "Comparar carreras" apunta a `index_v2.html`
   - Footer reemplazado por el de `index_v2.html` (idéntico, no cambia entre pestañas)
   - CSS de marca agregado (mismo bloque que en `index_v2.html`)
   - Bloque de diagnóstico/cobertura eliminado del footer visible (si existe en `instituciones.html`); si el JS lo requiere, mantenerlo oculto con `hidden`
   - Todo el JS y la lógica de la página intactos — no se toca ninguna función

### Criterio de "tarea completa"

- `web/instituciones_v2.html` existe y abre con `python -m http.server 8080` desde `web/`
- Header muestra logo (70px), "Carrera Clara", eslogan, tabs con "Comparar instituciones" activo
- Footer muestra las 3 columnas sobre fondo navy, con link a LinkedIn de Diego funcional
- El selector en 2 pasos (institución → carrera) funciona y agrega combos correctamente
- Los 5 gráficos (empleabilidad, retención, duración, banda de ingreso, arancel) se renderizan
- El panel de info institucional aparece debajo de los gráficos

---

## Archivos relevantes

| Archivo | Rol |
|---|---|
| `web/instituciones.html` | Fuente de todo el JS y lógica — leer, no modificar |
| `web/index_v2.html` | Plantilla del nuevo header/footer — extraer CSS y HTML de marca |
| `web/assets/logo-carrera-clara-blanco.png` | Logo ya generado — solo referenciar |
| `MANUAL_MARCA_CARRERA_CLARA.md` | Manual de marca para contexto de diseño |
| `PLAN.md` | Plan maestro — actualizar al cerrar esta tarea |

Al terminar, actualiza `PLAN.md` (añade una entrada en Tarea 6 indicando que `instituciones_v2.html` fue creado, fecha 2026-XX-XX) y mueve este archivo a `old/`.
