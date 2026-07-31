# Prompt para iniciar la Tarea 2 — Diseño del modelo de datos

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para arrancar la Tarea 2 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto, `PLAN.md` (plan maestro completo, secciones "Hallazgos ya confirmados" y "Tarea 2") y `mifuturo/NOTAS_CRUCE.md` (resultado de la auditoría de la Tarea 1) para tener el contexto completo antes de empezar.

**Tu tarea (Tarea 2 del plan maestro): diseñar el esquema del modelo de datos en markdown — sin escribir código de producción todavía.** El output es el contrato que usará el loader de la Tarea 3, no una implementación.

Concretamente:

1. **Definir las entidades** del modelo hub-and-spoke (la tabla ancla es `Buscador_Empleabilidad_ingresos_2025_2026_SIES.xlsx`, las otras 3 le aportan atributos):
   - **Dimensión carrera**, con jerarquía genérica → título → familia. Decide cómo representar que "Ingeniería Civil" es una familia con 19 hijos a nivel genérico (ver hallazgo en `PLAN.md`) — ¿una columna `familia` en la dimensión genérica, una tabla separada, o algo distinto?
   - **Dimensión institución**, alimentada por `Buscador_Instituciones` (acreditación, dirección, web, tipo de sociedad), enlazada por código de institución — **clave confirmada como limpia en la auditoría** (84–95% cobertura). No usar el nombre de institución como clave: los formatos difieren entre archivos (`"IP INACAP"` en el ancla/`Buscador_de_Carreras` vs. `"Instituto Profesional INACAP"` en `Buscador_Instituciones`).
   - **Hecho "oferta"** (de `Buscador_de_Carreras`): grano carrera × institución × sede × jornada, con `Código único de carrera`. **Decisión pendiente clave:** la auditoría confirmó que la columna `Nombre carrera` de este archivo es una *tercera convención* (nombre de programa registrado por la institución, no la curaduría SIES) con solo 24.7% de match exacto contra "genérica"/"título" del ancla. Define cómo el esquema maneja esto: ¿se deja sin resolver por ahora (oferta como hecho "huérfano" de la jerarquía de carrera, solo enlazado por institución), ¿se usa la columna `Área Carrera Genérica` (no auditada en detalle, revisar si ayuda) como puente parcial, o se posterga la resolución fina a una tabla de equivalencias manual futura?
   - **Hecho "indicadores"** (del ancla): empleabilidad, ingreso, retención, continuidad por carrera×institución. Recuerda los `n/a`/`s/i` reales — deben quedar como estado explícito en el esquema (¿columna de flag, tipo nullable documentado, o valor centinela?), y la fila de nota al pie ("FUENTE: Portal mifuturo.cl...") que debe excluirse, no modelarse.
   - **Hecho "benchmark nacional"** (de `Buscador_EstadísticasCarrera`): agregado a nivel carrera genérica × tipo de institución, **mantenido separado** — no lo materialices contra cada institución individual para no inflar/duplicar filas. El cruce con el ancla está casi limpio (86% cobertura de carrera genérica); define cómo se representa el 14% sin benchmark (carrera sin dato de comparación nacional) y considera el typo conocido `"Insitutos Profesionales"` → `"Institutos Profesionales"` como una corrección de datos a aplicar en el loader, no como una variante válida del esquema.

2. **Decidir formato de ingreso**: banda de texto en el ancla ("De $900 mil a $1 millón") vs. número continuo en `EstadísticasCarrera`. El esquema debe dejar claro cuál alimenta los gráficos (el numérico) y cuál es fallback legible (la banda de texto), y si conviene guardar ambos o derivar uno del otro.

3. **Output esperado:** un documento markdown nuevo (sugerido: `mifuturo/MODELO_DATOS.md`) con:
   - Las entidades/tablas del modelo final, sus columnas clave (no necesitas listar cada columna de los excels, solo las relevantes para el esquema), y sus relaciones (qué se une con qué, por qué clave).
   - Las decisiones explícitas tomadas en los puntos 1–2 arriba, con la razón.
   - Qué queda **sin resolver** y se posterga (ej. si decides no resolver `Nombre carrera` de `Buscador_de_Carreras` contra la jerarquía del ancla todavía, dilo explícitamente como deuda conocida, no como omisión silenciosa).

**No escribas el loader todavía** — eso es la Tarea 3, y depende de que este esquema esté validado contigo antes de implementar. Al terminar, actualiza el estado de la Tarea 2 en `PLAN.md` (de "lista para iniciar" a "completada", con un resumen de 2-3 líneas de las decisiones tomadas y link a `mifuturo/MODELO_DATOS.md`), y desbloquea la Tarea 3.

Recuerda los quirks ya conocidos (documentados en `CLAUDE.md`, `PLAN.md` y `mifuturo/NOTAS_CRUCE.md`): hojas "Hoja1" descartables, fila de encabezado decorativa antes de la real, encoding que rompe en consola Windows si no usas `PYTHONIOENCODING=utf-8`, y la fila de nota al pie en el ancla.
