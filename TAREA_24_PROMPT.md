# TAREA 24 — Ficha de institución (pantalla nueva)

## Contexto de arranque en frío

Proyecto: `comparador_carreras` / **Carrera Clara** — visualizador estático HTML/JS sobre datos SIES/MiFuturo.cl, en producción en [carreraclara.cl](https://carreraclara.cl) (Vercel, root `web/`, sin build step).

**Estado al inicio de esta tarea:**
- MVP completo y desplegado. Todas las tareas hasta **T23c** cerradas.
- Tres páginas canónicas, cada una un HTML autocontenido (CSS y JS inline, sin bundler):

| Página | Archivo | URL en producción |
|---|---|---|
| Portada | `web/landing.html` | `/` |
| Tipos de carrera | `web/index_v2.html` | `/tipos-de-carrera` |
| Carreras por institución | `web/instituciones_v2.html` | `/carreras-por-institucion` |

- Las URLs limpias vienen de `web/vercel.json` (`rewrites`). **Cualquier ruta nueva necesita su rewrite ahí.**
- `web/sw.js` cachea el HTML con Cache First → **subir `CACHE_VERSION`** (hoy `carreraclara-v3`) al terminar, o los usuarios recurrentes no verán la pantalla nueva.
- Ambas herramientas tienen header con marca clickeable (`<a href="/">`) y botón flotante de feedback con modal. La pantalla nueva debería heredar los dos.

## Qué hace esta tarea

Una **página propia por institución**: hoy el usuario ve una institución solo como fila dentro de una comparación de carreras. Falta la vista inversa — "cuéntame todo sobre esta institución".

Es la pantalla 6 del roadmap original (ver `PLAN_HISTORIAL.md:60`).

## Datos disponibles

Todo sale de `web/data/instituciones.json` (**2,9 MB**, 1690 combos institución × carrera-título, **105 instituciones únicas**). Generado por `web/export_instituciones.py` desde `mifuturo/processed/comparador.db`.

Cada combo trae `institucion` (mismo objeto repetido en todos sus combos):

```
codigo, nombre, tipo, acreditacion, anios_acreditacion, vigencia_acreditacion,
areas_acreditadas, direccion_sede_central, pagina_web, tipo_sociedad, tiene_ficha
```

…y los indicadores de esa carrera en esa institución:

```
carrera_titulo, carrera_generica, area, familia,
empleabilidad_1er_anio, empleabilidad_2do_anio, retencion_1er_anio,
duracion_real_semestres, ingreso_banda_*, arancel_* ,
tiene_ponderacion_paes, ponderacion_* (nem, ranking, lenguaje, matematicas, …)
```

**Límites conocidos, no descubrirlos de nuevo:**
- **Región no está exportada** en `instituciones.json` (se detectó en T15). Si la ficha la necesita, hay que tocar `export_instituciones.py`.
- `familia` viene `null` en la práctica (curaduría manual nunca hecha).
- 16 de 1690 combos tienen `tiene_ficha=False` (FK colgante en `dim_institucion`) — hay que decidir qué mostrar ahí.
- Muchos indicadores son `null` por carrera. La convención del proyecto es **no ocultar el vacío**: se marca explícitamente ("sin dato", "arancel aproximado", "sin ponderación PAES").

## Decisiones que hay que tomar CON Diego antes de escribir código

1. **¿Archivo nuevo o pantalla dentro de `instituciones_v2.html`?** Un `institucion.html` aparte es más limpio pero duplica header/footer/estilos otra vez (el proyecto ya duplica bastante). Traer una recomendación, no una encuesta.
2. **URL.** ¿`/institucion?codigo=143`, o limpia tipo `/institucion/aiep` con rewrite? La segunda es compartible y se ve mejor, pero necesita slugs estables.
3. **Peso.** Cargar 2,9 MB para mostrar una sola institución es caro en celular. ¿Se justifica un `export_instituciones.py` que además emita `data/institucion/<codigo>.json` (patrón que ya existe en `data/detalle/<slug>.json`)?
4. **Qué muestra la ficha.** Mínimo probable: identidad + acreditación (con vigencia y áreas), y la lista de carreras que imparte con sus indicadores, ordenable/filtrable. ¿Algún gráfico? ¿Comparación contra el promedio de su tipo (Universidad/IP/CFT)?
5. **Cómo se llega.** Desde `instituciones_v2.html` los nombres de institución deberían enlazar a su ficha. ¿También un buscador de instituciones en la portada?

## Archivos que probablemente se tocan

- Nuevo: `web/institucion.html` (si se opta por archivo aparte)
- `web/instituciones_v2.html` — enlaces hacia la ficha
- `web/vercel.json` — rewrite de la ruta nueva
- `web/sw.js` — subir `CACHE_VERSION` y sumar el archivo nuevo a `PRECACHE_URLS`
- `web/export_instituciones.py` — solo si se decide emitir JSON por institución o exportar región

## Criterio de "tarea completa"

- Ficha accesible para cualquiera de las 105 instituciones, con datos reales.
- Se llega a ella desde `instituciones_v2.html` sin pasos raros.
- URL compartible (se puede pegar el link y abre la misma institución).
- Estados vacíos marcados explícitamente, nunca ocultos.
- Header con marca clickeable y botón de feedback, igual que las otras páginas.
- Revisada en escritorio y a 375px.
- `vercel.json` y `sw.js` actualizados; `PLAN.md` marcado T24 ✅.

## Recordatorio de flujo

Este proyecto avanza por sesiones aprobadas: **plan → aprobación explícita de Diego → ejecución**. Al terminar, levantar el server local y abrirle la página en el navegador antes de dar la tarea por cerrada.
