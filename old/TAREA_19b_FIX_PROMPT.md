# TAREA 19b FIX — Fade en filtros Tipo/Área de instituciones_v2.html

## Contexto de arranque en frío

Proyecto: `comparador_carreras` — visualizador estático HTML/JS sobre datos SIES.
Servidor: `python -m http.server 8000` desde `web/`. Sin build step.

Archivo a tocar: **`web/instituciones_v2.html`** (solo este).

---

## Qué se hizo en T19b (contexto)

Se implementó un sistema de fade-in para elementos que usan `[hidden]`:

```js
function fadeIn(el) {
  el.hidden = false;
  el.classList.add('is-fade-entering');
  requestAnimationFrame(() => requestAnimationFrame(() => el.classList.remove('is-fade-entering')));
}
```

CSS asociado:
```css
ul.autocomplete-list { transition: opacity 0.13s ease, transform 0.13s ease; }
.is-fade-entering { opacity: 0; }
ul.autocomplete-list.is-fade-entering { transform: translateY(-5px); }
```

El dropdown de instituciones (`<ul id="institucion-list">`) ya tiene este fade cuando se abre normalmente (al hacer focus/input en el campo de texto). El problema está solo en los filtros del panel izquierdo.

---

## El bug exacto

En `instituciones_v2.html` hay un panel izquierdo con:
- `<select id="filtro-tipo">` — Tipo de institución (Todos / Universidades / IP / CFT)
- `<select id="filtro-area">` — Área (Todas / Administración / Salud / etc.)

**Comportamiento deseado**: al cambiar cualquiera de estos selects, el dropdown `#institucion-list` debería abrirse (o re-abrirse) con el efecto fade-in mostrando las instituciones filtradas.

**Causa raíz**: el `document.addEventListener("click")` cierra el dropdown ANTES de que dispare el evento `change` del `<select>`. Cuando llega el `change`, el dropdown ya está oculto y el código no lo reabre.

El orden real de eventos del browser al hacer click en un `<select>`:
1. `mousedown/click` en el document → el listener cierra `#institucion-list` (`hidden = true`)
2. Usuario elige una opción
3. `change` dispara en el `<select>`

Por eso el efecto no funciona: para cuando llega el `change`, el dropdown ya fue cerrado por el click-outside.

---

## Lo que se intentó (no funcionó del todo)

Se modificaron los listeners de `filtroTipo` y `filtroArea` y el click-outside handler. Puede que los cambios estén parcialmente aplicados en el archivo. **Antes de cualquier edición, lee el estado actual del archivo.**

---

## Solución esperada

Debes asegurarte de que en `web/instituciones_v2.html` queden aplicados estos dos cambios:

### Cambio 1 — Click-outside handler
Busca el `document.addEventListener("click", ...)` que llama a `ocultarListaInstituciones()`. Agrégale la condición de excluir los selects de filtro:

```js
// ANTES:
if (!el.institucionList.contains(ev.target) && ev.target !== el.institucionInput && ev.target !== el.institucionArrow) {
  ocultarListaInstituciones();
}

// DESPUÉS:
if (!el.institucionList.contains(ev.target) && ev.target !== el.institucionInput && ev.target !== el.institucionArrow && ev.target !== el.filtroTipo && ev.target !== el.filtroArea) {
  ocultarListaInstituciones();
}
```

### Cambio 2 — Handler de cambio de filtros
Busca el `[el.filtroTipo, el.filtroArea].forEach(...)` con el listener `"change"`. Debe quedar sin condicional (siempre abre el dropdown con fade):

```js
// DEBE QUEDAR ASÍ:
[el.filtroTipo, el.filtroArea].forEach((sel) =>
  sel.addEventListener("change", () => {
    el.institucionList.hidden = true;
    mostrarListaInstituciones(el.institucionInput.value);
  })
);
```

---

## Cómo verificar que funciona

1. Levanta el servidor: `python -m http.server 8000` desde `web/`
2. Abre `http://localhost:8000/instituciones_v2.html`
3. Cambia el select "Tipo de institución" a "Institutos Profesionales"
4. El dropdown de instituciones debe abrirse con un fade suave mostrando solo IPs
5. Cambia a "Universidades" — el dropdown debe re-fadear con nuevos resultados
6. Mismo test con el select "Área"

## Criterio de "tarea completa"

- Cambiar Tipo o Área abre el dropdown con fade, incluso si estaba cerrado
- No hay regresiones: el click-outside sigue cerrando el dropdown al hacer click en cualquier otro lugar
- Diego confirma visualmente en su navegador
