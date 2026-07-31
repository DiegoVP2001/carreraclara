# Manual de Marca Carrera Clara

## 1. Identidad

**Carrera Clara** es una guía digital para comparar opciones de educación superior en Chile usando datos oficiales. La marca nace desde el comparador actual del proyecto, que hoy se presenta en la web como "Comparador de carreras", y le da una identidad más recordable sin cambiar su rol: ayudar a elegir con evidencia, transparencia y lenguaje entendible.

**Bajada:** "Elige con datos. Decide con claridad."

La marca no promete decidir por la persona, reemplazar orientación vocacional ni recomendar instituciones. Su promesa es ordenar información pública que suele estar fragmentada, técnica o difícil de leer. Carrera Clara debe sentirse como una herramienta neutral, seria y cercana: muestra datos, explica límites y ayuda a comparar sin exagerar certezas.

## 2. Audiencia

La audiencia principal es cualquier postulante a educación superior: estudiantes de enseñanza media, egresados que se toman un tiempo antes de postular, personas que quieren cambiar de carrera, trabajadores que buscan reconvertirse, familias que acompañan la decisión y docentes u orientadores que necesitan una herramienta clara para conversar con estudiantes.

Por eso, la comunicación no debe hablar solo a "estudiantes de 4to medio". Debe usar un lenguaje amplio: "quienes están evaluando qué estudiar", "postulantes", "personas que comparan carreras" o "familias y orientadores". Cuando el flujo requiera decisiones de admisión, como ponderaciones PAES, se puede hablar directamente de postulantes, pero evitando asumir una trayectoria única.

## 3. Rol de marca

Carrera Clara es una guía neutral basada en datos oficiales de SIES y MiFuturo.cl. Su rol es traducir información pública a una experiencia comparable, no reinterpretar los datos como ranking absoluto. En el proyecto actual, ese rol ya aparece en tres decisiones importantes:

- Se comparan carreras genéricas, instituciones y combinaciones institución + carrera sin ocultar el grano de cada dato.
- Los estados incompletos se muestran explícitamente, por ejemplo "sin comparación nacional", "institución sin ficha", "sin dato de arancel" o "arancel en UF".
- Los gráficos y tablas mantienen contexto mediante tooltips, notas secundarias y pie de transparencia de cobertura.

La marca debe proteger esa lógica. Siempre que una pantalla agregue una métrica nueva, debe responder tres preguntas: de dónde viene, a qué nivel se puede comparar y qué limitación debe conocer la persona usuaria.

## 4. Tono y personalidad

El tono es **formal en simple**: serio, claro, explicativo y sin tecnicismos innecesarios. Carrera Clara puede usar frases breves y directas, pero debe evitar tanto el lenguaje burocrático como el entusiasmo publicitario.

Personalidad esperada:

- **Confiable:** cita la fuente, muestra cobertura y no inventa datos faltantes.
- **Sobria:** prioriza legibilidad sobre decoración.
- **Cálida:** reconoce que elegir carrera es una decisión importante y a veces incierta.
- **Moderna:** usa componentes interactivos, visualizaciones limpias y navegación fluida.
- **Transparente:** explica cuándo un valor es exacto, aproximado, abierto o no comparable.

Ejemplos de microcopy adecuados:

- "Agrega al menos 2 carreras para comparar."
- "Sin comparación nacional."
- "Valor exacto cuando no hay ambigüedad entre sedes/jornadas; rango aproximado cuando sí la hay."
- "No se pudo cargar el detalle."

Evitar:

- "La mejor carrera para ti."
- "Ranking definitivo."
- "Garantiza mejores ingresos."
- "Dato no disponible" sin explicar si falta, no aplica o no es comparable.

## 5. Paleta base

La paleta actual de `web/index.html` y `web/instituciones.html` debe considerarse la base visual de Carrera Clara:

| Uso | Color | Criterio |
|---|---:|---|
| Navy institucional moderno | `#0f2e45` | Header, identidad, zonas de navegación principal. Debe comunicar seriedad sin verse estatal antiguo. |
| Verde mineral principal | `#1a7f64` | Acción primaria, datos positivos, barras principales, enlaces y foco de la marca. |
| Ámbar | `#e8960a` | Costos, retención, alertas suaves o datos que requieren atención sin ser error. |
| Fondo cálido | `#f5f6f4` | Fondo general, descanso visual, contraste suave con superficies blancas. |
| Blanco | `#ffffff` | Tarjetas, paneles, gráficos y superficies de lectura. |
| Texto principal | `#1c2b36` | Lectura larga, títulos secundarios, tablas. |
| Texto secundario | `#6b7a86` | Notas, metadatos, ayudas y contexto. |
| Bordes | `#dde1e7` | Separación discreta entre tarjetas, tablas y controles. |

El verde no debe usarse para todo. Debe reservarse para identidad, acción y datos que la interfaz quiere destacar. El ámbar es útil para costos, rangos o advertencias suaves. El rojo o fondos rosados deben quedar para faltantes relevantes o estados que requieren atención clara, como "institución sin ficha"; no para llamar la atención ornamentalmente.

## 6. Tipografía

El sistema actual usa dos familias desde Google Fonts:

- **Figtree:** títulos, navegación activa, métricas destacadas y cifras de alto impacto. Debe sentirse editorial y moderna, sin competir con los datos.
- **Inter:** cuerpo, controles, tablas, explicaciones, tooltips, notas, etiquetas y valores densos.

La fuente base mínima debe mantenerse en torno a `16px`. Las tablas y metadatos pueden bajar a tamaños compactos solo si siguen siendo legibles en móvil. Las métricas principales pueden ser grandes, pero no deben dominar una tarjeta hasta impedir comparar otros elementos. La jerarquía debe ayudar a escanear: nombre, estado, métrica principal, detalle.

## 7. Estilo visual

Carrera Clara debe evitar una estética escolar, juvenil en exceso o burocrática. El diseño debe sentirse como una herramienta pública moderna: sobria, clara y usable.

La web actual ya define varios patrones apropiados:

- Header navy con título, bajada breve y navegación por pestañas.
- Contenedor central de ancho máximo cercano a `1100px`.
- Superficies blancas sobre fondo cálido.
- Bordes suaves, sombras discretas y radios contenidos.
- Tarjetas para elementos repetidos: carreras seleccionadas, combinaciones institución + carrera y paneles institucionales.
- Gráficos Chart.js horizontales, pensados para etiquetas largas y comparación lateral.
- Estados vacíos centrados, simples y sin tono promocional.

Las sombras deben ser funcionales, no decorativas. Los radios pueden ser suaves, pero no excesivamente redondeados. Las tarjetas deben separar información comparable; las secciones de página no necesitan parecer tarjetas flotantes.

## 8. Componentes UI

**Header y navegación.** El header debe mantener el navy como ancla institucional. La navegación activa puede usar Figtree, fondo translúcido y alto contraste. El texto de bajada debe explicar qué se compara y con qué fuente, sin convertirse en un párrafo largo.

**Selectores y autocomplete.** Los selectores son la puerta de entrada a la comparación. Deben tolerar búsqueda sin tildes, mostrar metadatos secundarios y mantener ayuda breve sobre mínimos de comparación. Si el usuario todavía no selecciona nada, el estado vacío debe invitar a comenzar sin tutorializar demasiado.

**Tarjetas.** Las tarjetas deben resumir primero lo que la persona necesita reconocer: nombre de carrera o institución, área, tipo institucional y métricas titulares. Los chips de iconos pueden ayudar a escanear, pero deben tener tooltip si el significado no es evidente. Evitar mezclar demasiados badges en la primera línea.

**Badges y estados.** Los badges no son adornos. Deben señalar estados del dato: "sin comparación nacional", "sin banda de ingreso", "arancel aproximado", "arancel en UF", "Sin ponderación PAES". El color debe indicar severidad o tipo de atención, no jerarquía visual arbitraria.

**Tooltips.** Los tooltips deben definir conceptos cortos: empleabilidad, retención, duración real, percentiles, arancel o ponderaciones. Deben responder "qué significa este dato" y, cuando corresponda, "por qué no se compara directamente". No deben contener textos largos que deberían estar en una página de glosario.

**Gráficos.** Los gráficos deben usar orientación horizontal cuando haya etiquetas largas. Las barras deben conservar unidades claras: porcentajes, CLP, miles de pesos, semestres. Los rangos deben verse como rangos, no como valores exactos. Si una barra se omite por falta de dato, la nota del gráfico debe decirlo.

**Paneles institucionales.** Las fichas de institución deben separar datos generales de indicadores de carrera. Acreditación, años, vigencia, tipo de sociedad, dirección y web son contexto institucional, no métricas de desempeño de una carrera específica.

## 9. Datos, incertidumbre y transparencia

Carrera Clara debe mostrar incertidumbre de forma honesta. Usar frases explícitas:

- "sin dato"
- "sin benchmark"
- "sin comparación nacional"
- "institución sin ficha"
- "arancel en UF"
- "rango aproximado"
- "banda abierta"
- "varía por sede/jornada"

No transformar un `null` en cero. No mezclar pesos con UF en un mismo eje. No convertir rangos en promedios inventados. No esconder que el benchmark nacional está agregado por tipo de institución y no por institución específica. No usar el nombre de una institución como clave si el modelo ya definió que el cruce confiable es por código.

Cada visualización debe privilegiar lectura rápida: métrica clave primero, detalle técnico disponible en tooltip, nota o texto secundario. El pie de transparencia de cobertura debe mantenerse como una práctica de marca, porque refuerza la confianza y recuerda que la herramienta no tiene cobertura perfecta.

## 10. Accesibilidad y responsive

El diseño debe funcionar en móvil y escritorio. En móvil, los gráficos pueden apilarse en una columna y las tarjetas deben mantener texto legible sin solapamientos. En escritorio, el layout puede aprovechar grillas de dos columnas para gráficos, pero sin forzar densidad excesiva.

Requisitos mínimos:

- Contraste alto entre texto y fondo.
- Fuente base legible.
- Estados `hover` y `focus-visible` en controles interactivos.
- Botones con `aria-label` cuando el icono no sea suficiente.
- Tooltips accesibles con foco de teclado.
- Tablas que no dependan solo del color para comunicar significado.
- Mensajes de error o carga visibles y específicos.

## 11. Criterio de evolución

Este manual no reemplaza la inspección del código ni las decisiones del `PLAN.md`. Sirve como referencia para futuras mejoras visuales. Si una nueva pantalla contradice un patrón existente, debe justificarlo por una necesidad de uso concreta: más claridad, mejor comparación, mayor accesibilidad o transparencia de datos.

La regla práctica es simple: Carrera Clara debe verse clara antes que vistosa, confiable antes que persuasiva y útil antes que completa.
