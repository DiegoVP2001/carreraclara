# Tarea 20c — Renombrar las dos herramientas

## Contexto

El sitio tiene tres páginas canónicas:

| Archivo | Nombre actual en UI | Rol real |
|---|---|---|
| `web/landing.html` | Inicio (landing) | Portada de la marca |
| `web/index_v2.html` | "Comparar carreras" | Compara **tipos genéricos** de carrera con benchmarks nacionales por tipo de institución (Universidad / IP / CFT). No compara ofertas específicas. |
| `web/instituciones_v2.html` | "Comparar instituciones" | Compara **combinaciones institución × carrera-título**: cómo cada institución imparte una carrera concreta. No compara instituciones en general. |

Diego identificó que los nombres actuales crean expectativas incorrectas:
- "Comparar carreras" suena a comparar dos carreras de verdad (ej. Psicología vs. Ingeniería), pero en realidad es un comparador de **tipos genéricos** con benchmarks nacionales.
- "Comparar instituciones" suena a comparar la PUCV vs. la UDP en general, pero en realidad es ver **qué instituciones ofrecen una carrera específica** y cómo varían sus indicadores.

## Objetivo de la tarea

1. **Proponer 3–4 nombres alternativos para cada herramienta**, con pro/contra de cada uno y una recomendación final.
2. **Implementar el nombre elegido** en todos los lugares donde aparece:
   - `<title>` de cada página
   - `nav.tabs` de las tres páginas (`landing.html`, `index_v2.html`, `instituciones_v2.html`)
   - Footer columna "Explorar" de las tres páginas
   - `<h2>` / encabezados internos de cada herramienta si aplica
   - Cualquier referencia cruzada en el texto ("ve a Comparar carreras", etc.)

## Restricciones de nombre

- Máximo 3 palabras (debe caber en el tab de navegación sin que se corte).
- Tono "formal en simple" del MANUAL_MARCA_CARRERA_CLARA.md: serio, claro, sin tecnicismos ni slang.
- No usar "buscar" (implica motor de búsqueda, no comparación).
- No usar "ranking" (prohibido por el manual).
- Puede incluir el verbo "comparar", "explorar" o "ver", o ser un sustantivo directo.

## Pistas para las propuestas

**Para `index_v2.html`** (carreras genéricas con benchmark):
- "Comparar carreras" — actual, inexacto
- "Explorar carreras" — neutro, no implica comparación específica
- "Carreras genéricas" — técnico, descriptivo pero frío
- "Tipos de carrera" — preciso pero suena raro en nav
- "Ver indicadores por carrera" — demasiado largo

**Para `instituciones_v2.html`** (oferta específica por institución):
- "Comparar instituciones" — actual, inexacto
- "Oferta por institución" — preciso, pero "oferta" puede confundirse con descuento
- "Carreras por institución" — describe bien lo que hay
- "Dónde se estudia" — conversacional, claro
- "Ver oferta académica" — técnico, correcto pero frío

## Archivos a editar

- `web/landing.html` — tabs + footer Explorar
- `web/index_v2.html` — `<title>`, tabs, footer Explorar, posibles referencias internas
- `web/instituciones_v2.html` — `<title>`, tabs, footer Explorar, posibles referencias internas

## Criterio de "tarea completa"

- Los nuevos nombres son coherentes entre sí y reflejan con precisión lo que hace cada herramienta.
- Aparecen consistentemente en todos los lugares listados arriba.
- Pasan el "test de lectura fría": alguien que no conoce el sitio entiende la diferencia entre las dos herramientas solo leyendo sus nombres en el nav.
