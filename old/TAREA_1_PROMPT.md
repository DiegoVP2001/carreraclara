# Prompt para iniciar la Tarea 1 — Auditoría de claves y grano

> Copia y pega el contenido de abajo (o usa este archivo como referencia) al iniciar una nueva sesión de Claude Code en `comparador_carreras/` para arrancar la Tarea 1 del plan maestro.

---

Estamos construyendo un comparador de carreras (visualizador family-friendly sobre datos públicos de MiFuturo.cl/SIES) para estudiantes de 4to medio. Lee primero `CLAUDE.md` de este proyecto y `PLAN.md` (plan maestro completo, sección "Hallazgos ya confirmados" y "Tarea 1") para tener el contexto completo antes de empezar.

**Tu tarea (Tarea 1 del plan maestro): auditoría empírica de claves y grano entre los 4 archivos de `mifuturo/`, sin escribir código de producción ni diseñar el modelo de datos todavía** — solo investigar y reportar. Concretamente, usando Python (pandas/openpyxl, con `PYTHONIOENCODING=utf-8` por los acentos — ver gotchas de encoding en `CLAUDE.md`):

1. **Coincidencia de códigos de institución.** Compara la columna "Código" de `mifuturo/Buscador_Empleabilidad_ingresos_2025_2026_SIES.xlsx` (hoja "Carreras e IES (2025-2026)") contra "Código institución" de `mifuturo/Buscador_de_Carreras_2025_2026_SIES_EEE.xlsx` (hoja "Busc. Carreras 2025-2026") y `mifuturo/Buscador_Instituciones_2025_2026_SIES-vf.xlsx`. ¿Es el mismo esquema numérico? Para una muestra de códigos compartidos, ¿el nombre de institución asociado coincide? Reporta % de códigos del ancla que tienen match en cada uno de los otros dos archivos.

2. **Coincidencia de nombre de carrera.** `Buscador_de_Carreras` tiene una sola columna `Nombre carrera` (sin distinguir genérica/título). Compárala contra las columnas "Nombre carrera genérica" y "Nombre carrera (del título)" del ancla. ¿Coincide exactamente con alguna de las dos, con alguna normalización menor (mayúsculas/tildes/espacios), o es una tercera convención de escritura? Reporta % de match exacto y de match aproximado (ej. usando `difflib` o normalización simple), y muestra ejemplos de los casos que NO calzan.

3. **Coincidencia de `Buscador_EstadísticasCarrera`.** Compara los strings de "Carrera genérica" y "Tipo de institución" de `Buscador_EstadísticasCarrera_2025_2026_SIES.xlsx` (hoja "Hoja1") contra los valores equivalentes del ancla ("Nombre carrera genérica" y "Tipo de institución"). ¿Coinciden exactamente? Reporta cobertura: cuántas carreras genéricas del ancla NO aparecen en `EstadísticasCarrera` y viceversa.

4. **Documenta los hallazgos** en un archivo nuevo `mifuturo/NOTAS_CRUCE.md`: por cada uno de los 3 puntos anteriores, el % de cobertura/match, ejemplos concretos de discrepancias (con valores reales, no genéricos), y una recomendación corta de si el cruce es "limpio" (join directo), "necesita normalización menor" (lowercase/strip/tildes), o "necesita fuzzy matching real" (umbral de similitud, revisión manual de casos ambiguos).

**No diseñes el modelo de datos ni escribas el loader todavía** — eso es la Tarea 2 y 3 del plan maestro, y dependen de lo que encuentres aquí. Al terminar, actualiza el estado de la Tarea 1 en `PLAN.md` (de "pendiente" a "completada", con un resumen de 2-3 líneas de los hallazgos y link a `mifuturo/NOTAS_CRUCE.md`).

Recuerda los quirks ya conocidos de estos archivos (documentados en `CLAUDE.md` y `PLAN.md`): hojas "Hoja1" descartables, fila de encabezado decorativa antes de la real, encoding que rompe en consola Windows si no usas `PYTHONIOENCODING=utf-8`.
