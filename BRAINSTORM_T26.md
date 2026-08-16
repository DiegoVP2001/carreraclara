# Brainstorm T26 — qué construir con toda la data disponible + referencias externas

> Sesión de ideación, sin código ni decisiones tomadas. Parte de `AUDITORIA_DATOS_T25.md` y `GUIA_FUENTES_DE_DATOS.md` (datos internos ya cargados) y se extiende con una investigación de 8 subagentes en paralelo sobre comparadores de carreras/universidades reales en Chile, Latinoamérica, EE.UU., Reino Unido, Europa y Australia (~55 hallazgos concretos, ver "Fuentes externas revisadas"). Para cada idea: qué decisión del estudiante ayuda a tomar, con qué datos se puede construir hoy vs. qué requeriría integrar algo nuevo, y tamaño aproximado.

---

## Resumen ejecutivo

La primera pasada de este brainstorm (solo datos internos T25) ya identificaba tres ideas de bajo costo y alto valor: costo total real, tendencia histórica, y exponer diagnóstico oculto. La investigación externa confirma esas tres de forma independiente (aparecen en College Scorecard, ICFES, PayScale) y agrega algo más importante: **revela un eje entero que Carrera Clara no cubre hoy y que la competencia directa chilena sí resuelve — todo lo relacionado con "¿a qué puntaje alcanzo?"** (calculadora PAES completa, simulador inverso desde la carrera meta, puntaje de corte histórico). Apareció de forma independiente en dos ejes de investigación distintos (comparadores comerciales EE.UU. vía CollegeVine, y competidores directos en Chile vía calculadorapaes.cl/DEMRE/ponderadores institucionales) — no es una coincidencia, es la brecha más visible frente a lo que un estudiante chileno ya usa hoy.

También surgió un ángulo de producto que ningún backlog anterior había planteado: Carrera Clara **asume que el estudiante ya sabe qué carrera comparar**. Ningún test vocacional chileno encontrado en la investigación es neutral — todos son herramientas de captación de una universidad específica. Un test corto, sin conflicto de interés, que alimente el propio catálogo de Carrera Clara y conecte directo a datos reales de empleabilidad/ingreso (algo que ni los líderes globales del rubro hacen), es un diferenciador real y no requiere ninguna fuente de datos externa.

Cuatro ideas se destacan por combinar valor alto con costo bajo, construibles **hoy, sin integrar ninguna fuente nueva**:

1. **Calculadora de ponderación PAES completa** (extiende "Qué NEM necesito" a las 5 pruebas, no solo NEM) — el dato ya está cargado en `hecho_oferta`, solo falta exponerlo.
2. **Simulador CAE/FES** (cuota mensual estimada de crédito) — fórmulas públicas y fijas, usa arancel/duración que ya se muestran.
3. **Paquete de confianza del dato** (tamaño de muestra, vigencia/fecha, "mediana no promesa") — extiende la regla ya vigente de "nunca ocultar un vacío" a "nunca ocultar cuánto confiar en un número".
4. **Costo total real** (arancel + costo de titulación) — ya identificado en la primera pasada, dato cargado y no exportado.

---

## Fuentes externas revisadas

Ocho subagentes de investigación en paralelo, cada uno con un eje temático propio, usando WebSearch/WebFetch sobre sitios reales (no inferencias por nombre). ~55 hallazgos concretos, clasificados por tipo: `dato_externo` (requiere integrar una fuente nueva), `patron_ux` (construible con datos que Carrera Clara ya tiene), `herramienta_nueva` (tipo de herramienta distinto, ej. test/calculadora), `contenido` (editorial, no interactivo).

| Eje | Sitios revisados |
|---|---|
| Comparadores oficiales de gobierno | College Scorecard (EE.UU.), Discover Uni (Reino Unido), U-Multirank (Europa), ComparED/QILT (Australia) |
| Comparadores comerciales EE.UU. | Niche.com, BigFuture (College Board), CollegeVine, PayScale College ROI Report, Unigo.com |
| Mercado laboral / exploración de carreras | O*NET OnLine, My Next Move/CareerOneStop, Occupational Outlook Handbook (BLS), Glassdoor Know Your Worth, LinkedIn Career Explorer |
| Latinoamérica | Ponte en Carrera (Perú), Observatorio Laboral para la Educación + SNIES (Colombia), RENOES (México), Becas Progresar + Educ.ar (Argentina) |
| Competidores directos en Chile | calculadorapaes.cl, DEMRE/tuadmision.cl, herramientasfinancieras.cl (CAE), Ranking Universitas/El Mercurio, admision.uc.cl/admisionuchile.cl, mifuturo.cl |
| Tests vocacionales | CareerExplorer.com, Truity Career Personality Profiler, Test Vocacional U. Autónoma de Chile (+ patrón repetido en UNAB/USS/UDLA/UCM), O*NET Interest Profiler |
| ROI financiero | College Scorecard, PayScale College ROI Report, CIPER Chile, calc.cl (CAE), Degree ROI Calculator |
| Periodismo de datos / dataviz | NYT Upshot (2 piezas), ProPublica Debt by Degrees, Opportunity Insights Mobility Report Cards, ICFES Interactivo |

---

## Blindspot pass — lo que ningún backlog anterior había planteado

- **El estudiante que no sabe qué carrera comparar.** Todas las herramientas actuales de Carrera Clara asumen que el estudiante ya llega con un nombre de carrera o tipo de carrera en mente. Ningún test vocacional chileno encontrado es neutral (todos capturan contacto para una universidad específica) — es un vacío de mercado real, no solo una función bonita de tener.
- **"¿A qué puntaje alcanzo?" es la pregunta más común y la que menos se cubre.** Apareció en dos ejes de investigación independientes sin que se les pidiera buscarlo específicamente — es la señal más fuerte de todo este ejercicio.
- **Un ROI aproximado** (ya detectado en la primera pasada con datos internos) ahora tiene un patrón de referencia claro: "gráfico de punto de equilibrio" (degree-roi.com) y "microcopy de mediana, no promesa" (College Scorecard) — resuelve el riesgo de mala interpretación que ya se había marcado como pendiente.
- **La confianza en el dato es su propio eje**, no un detalle del eje de transparencia. Casi todos los comparadores de gobierno serios (College Scorecard, Discover Uni, ProPublica) tratan "cuánto puedo confiar en este número" como una pregunta de primera clase, con copy fijo y visible, no como una nota al pie.

---

## Dirección 1 — Decisión de postulación

*¿Dónde postulo, con qué NEM/PAES, a qué costo real?*

| Idea | Qué resuelve | Datos | Tamaño | Origen |
|---|---|---|---|---|
| **Calculadora de ponderación PAES completa** (NEM + Ranking + Lenguaje + M1/M2 + Historia/Ciencias, no solo NEM) | Hoy "Qué NEM necesito" solo cubre NEM; el estudiante igual tiene que ir institución por institución a calcular su puntaje ponderado real con sus 5 notas PAES | Ponderaciones ya cargadas en `hecho_oferta` (mismo origen que "Qué NEM necesito") | 1-2 sesiones — extiende una pantalla existente, no requiere dato nuevo | T26 (investigación externa: CollegeVine "chancing", admision.uc.cl/admisionuchile.cl) |
| **Costo total real** (arancel 2026 + costo de titulación) | "El arancel anual no es lo que voy a pagar en total" | Ya cargado (`hecho_oferta.costo_titulacion`, T25-2), falta exportar y mostrar | 1 sesión | T25/T26a (datos internos) |
| **Simulador CAE/FES** (cuota mensual estimada de crédito) | "Si financio esto con crédito, ¿cuánto voy a pagar al mes por 15 años?" | Arancel/duración ya cargados; fórmulas de CAE (tasa 2%, 15 años) y FES son públicas y estables — no requiere dato externo, solo lógica de cálculo | 1-2 sesiones — calculadora nueva y autocontenida | T26 (investigación externa: calc.cl, herramientasfinancieras.cl) |
| **Rango de puntaje PAES real de la matrícula** (`rango_ingreso_paes_2025`) | Complementa "Qué NEM necesito" con el rango real con que efectivamente entró la matrícula 2025, no solo la ponderación de la fórmula | Ya cargado (T25-2), falta exportar/mostrar | 1 sesión | T25/T26a |
| **NEM/PAES inline en "Carreras por institución"** | Evita que el estudiante cambie de pestaña para ver el dato de admisión de una carrera que ya está comparando | `instituciones_nem.json` ya existe (T24), join cliente-side sin tocar el export | 1 sesión | T25/T26a |
| **Nota de confianza del dato de admisión** (tamaño de matrícula usada para el promedio) | "¿Este promedio de NEM/PAES es de 3 alumnos o de 300?" | SIES entrega tamaños de cohorte que hoy no se muestran junto al promedio | 1 sesión, mismo patrón visual en toda la pantalla | T26 (investigación externa: Discover Uni) |
| **Duración formal vs. duración real** | "¿En esta institución los alumnos se demoran más de lo planificado?" | `duracion_formal_semestres` ya cargado (T25-2); requiere cruzar `hecho_oferta`×`hecho_indicadores`, gap de grano similar a T25-1 | 2 sesiones | T25/T26a |
| **ROI aproximado** (arancel total ÷ ingreso 4° año, con gráfico de punto de equilibrio) | "¿Cuántos años me demoro en recuperar lo que gasté/dejé de ganar por estudiar esto?" | Combina `costo_titulacion`+arancel con `ingreso_4to_anio_2024`; falta una línea base externa de "ingreso sin educación superior" (ej. INE/CASEN) para el gráfico comparativo completo | 2-3 sesiones — la métrica es fácil, la UX de riesgo/interpretación necesita cuidado real | T26a + T26 (patrón: degree-roi.com, College Scorecard) |

---

## Dirección 2 — Comparación exploratoria y personalizada

*¿Cómo se ve esta carrera en el tiempo, en dispersión, y según lo que A MÍ me importa — no solo como un punto fijo o un ranking genérico?*

| Idea | Qué resuelve | Datos | Tamaño | Origen |
|---|---|---|---|---|
| **Gráfico de tendencia 2020→2024** (ingreso y empleabilidad) | Distingue una carrera estable de una en declive o en auge; hoy solo se ve 2024 | Ya cargado (T25-3), requiere tocar `queries.py` + `export_json.py` + gráfico Chart.js | 1-2 sesiones | T25/T26a, reforzado por ICFES Interactivo (mismo patrón) |
| **Ranking personalizado por ponderación del usuario** (sliders: "dame más peso a empleabilidad, menos a arancel") | "¿Cuál me conviene más A MÍ según lo que a mí me importa, no según un ranking genérico?" | Construible con datos ya exportados (empleabilidad, ingreso, retención, arancel, acreditación); requiere UI de sliders + score compuesto en cliente. Riesgo: no tratar "sin dato" como 0 en el cálculo — hay que excluir/marcar esas filas explícitamente | 2 sesiones | T26 (investigación externa: U-Multirank, NYT Upshot "Build Your Own Rankings") |
| **Modo "Versus" 1 a 1** (admisión + laboral en una sola vista para 2 opciones concretas) | "¿Enfermería en la U. X o Kinesiología en la U. Y?" — hoy se resuelve cruzando dos pantallas separadas | Construible con datos ya existentes (empleabilidad, ingreso, arancel, ponderación PAES/NEM) | 1-2 sesiones | T26 (investigación externa: calculadorapaes.cl modo Versus, ProPublica Head to Head) |
| **Distribución completa de ingreso** (percentiles 10/25/50/75/90, 1er y 5to año) | Hoy solo se muestran 3 de 10 percentiles; no hay forma de ver progresión salarial temprana ni dispersión completa | Ya cargado (T25-3) | 1 sesión | T25/T26a, reforzado por Ponte en Carrera (Perú, rango P10-P90 explícito) |
| **Gráfico tipo radar/sunburst del perfil de la carrera** | "¿Cómo se ve esta carrera de un vistazo en todas sus dimensiones, sin leer columna por columna?" | Construible con Chart.js (ya en el stack) normalizando los indicadores existentes a escala común | 1-2 sesiones | T26 (investigación externa: U-Multirank) |
| **Composición de matrícula por sexo** | Señal de orientación vocacional que hoy no existe en ninguna pantalla | Ya cargado (T25-2) | 1 sesión — requiere cuidado de presentación para no estigmatizar, reforzado por hallazgo externo de brecha de retorno por género (ver sección aspiracional) | T25/T26a, reforzado por OLE Colombia |
| **"Carreras del área"** (sugerencias relacionadas) | Cuando el estudiante ya eligió una carrera, sugerir otras del área como comparación adicional | `area` ya poblada y usada como filtro | 1 sesión | T25/T26a |

---

## Dirección 3 — Transparencia y confianza en los datos

*Reforzar la regla ya vigente del proyecto: "nunca ocultar un vacío" — y extenderla a "nunca ocultar cuánto confiar en un número".*

| Idea | Qué resuelve | Datos | Tamaño | Origen |
|---|---|---|---|---|
| **Microcopy fijo "mediana, no promesa"** junto a cada cifra de ingreso | "¿Este sueldo es lo que voy a ganar seguro, o solo una referencia?" | No requiere datos nuevos, es copy/tooltip consistente | Medio día | T26 (investigación externa: College Scorecard, Degree ROI Calculator) |
| **Caveats fijos sobre qué NO mide cada indicador** (excluye independientes, es de un año específico, etc.) | "¿Qué me estoy perdiendo si tomo este número al pie de la letra?" | Redactar 2-3 líneas fijas por indicador basadas en las limitaciones ya documentadas en `GUIA_FUENTES_DE_DATOS.md` | Medio día | T26 (investigación externa: Discover Uni) |
| **Rótulo de vigencia del dato por sección** (arancel 2026, benchmark 2024, matrícula 2025 — años distintos) | Hoy no siempre es obvio qué año se está mirando en cada bloque | No requiere datos nuevos, es UI/copy | Medio día — auditar qué secciones ya lo dicen | T25/T26a, reforzado por ProPublica (rótulo explícito de última actualización) |
| **Exponer los 5 contadores de diagnóstico ocultos** (T25-4b) | `instituciones.json.diagnostico` ya calcula 11 contadores, la UI solo renderiza 6 | Ya exportado, solo falta HTML | Medio día | T25/T26a |
| **`tipos_institucion` desde el JSON, no hardcodeado** (T25-4a) | Previene un bug futuro silencioso si SIES agrega/renombra un tipo | Ya exportado en `core.json` | Trivial | T25/T26a |

---

## Dirección 4 — Ficha de institución (ya en backlog, T27)

No es una idea nueva — ya está en `PLAN.md` como próxima tarea después de T26. Varios hallazgos T25 y varios patrones externos aplican directo a esa ficha cuando se construya: costo total, composición de matrícula/titulación por sexo, rótulo de vigencia por fuente, y (si se resuelve el cruce de grano) duración formal vs. real. El sello tipo "programa vigente y acreditado según SIES" (patrón SNIES/Colombia) también encaja mejor ahí que en las pantallas de comparación.

---

## Dirección 5 — Descubrimiento vocacional (eje nuevo, no estaba en la primera pasada)

*Para el estudiante que todavía no sabe qué carrera quiere — hoy Carrera Clara no tiene ningún punto de entrada para esto.*

| Idea | Qué resuelve | Datos | Tamaño | Origen |
|---|---|---|---|---|
| **Test corto de intereses tipo RIASEC/Holland, propio y neutral** | "No sé ni por dónde partir a elegir carrera" — resuelve el problema central del estudiante indeciso, que ninguna herramienta actual de Carrera Clara cubre porque todas asumen que ya se sabe el nombre de la carrera | El test en sí (metodología pública, 20-30 preguntas) no requiere dato externo; lo que sí requiere trabajo es **taguear cada una de las ~190 carreras genéricas del catálogo con un perfil RIASEC** — curatoría única, se puede partir con heurística por área/subárea CINE-F y refinar a mano | 2-3 sesiones (curatoría del catálogo + test + integración con las herramientas de comparación existentes) | T26 (investigación externa: O*NET Interest Profiler/My Next Move, Ponte en Carrera Perú) |
| **Resultado del test conectado a datos reales de empleabilidad/ingreso, gratis y sin paywall** | Diferenciador directo: ni Truity (paywall US$29) ni CareerExplorer (se queda solo en el perfil de personalidad, sin conectar a datos duros) cierran este ciclo — Carrera Clara ya tiene los datos SIES para hacerlo gratis | Mismos datos que las herramientas actuales, solo cambia el punto de entrada | Incluido en el ítem anterior, no es trabajo adicional relevante | T26 (investigación externa: Truity, CareerExplorer — comparación de posicionamiento) |
| **Búsqueda por lenguaje libre/coloquial** ("me gusta ayudar a la gente" → carreras relacionadas) | Un estudiante de 4to medio rara vez conoce los nombres formales de las carreras | Matching de texto contra nombres/descripciones ya cargadas; requiere mapeo de sinónimos/frases coloquiales (curatoría, o un LLM en el momento de búsqueda) | 1 sesión, complementario al test | T26 (investigación externa: My Next Move) |

**Nota de posicionamiento:** la investigación confirmó que los tests vocacionales chilenos más visibles en buscadores (U. Autónoma, y el mismo patrón en UNAB/USS/UDLA/UCM) son herramientas de captación de matrícula de esa universidad específica — piden 2 carreras preferidas y autorización de contacto antes de mostrar resultado, y el catálogo de resultado está limitado a la oferta propia. Un test gratuito, sin afiliación institucional y sin captura de contacto sería una alternativa que hoy no existe en el mercado chileno — coherente con el posicionamiento neutral que Carrera Clara ya tiene.

---

## Lo que definitivamente NO se hace ahora — aspiracional, requiere fuente externa nueva

Ideas de alto valor detectadas en la investigación pero que requieren integrar una fuente de datos que Chile no publica de forma abierta hoy, o que son sensibles/riesgosas de comunicar sin curaduría seria. Se documentan para no reabrir la pregunta desde cero en una sesión futura, no para descartarlas para siempre.

| Idea | Por qué es valiosa | Por qué no ahora |
|---|---|---|
| **Puntaje de corte histórico + simulador inverso desde la carrera meta** | Es el gap más grande detectado frente a la competencia directa chilena (calculadorapaes.cl, DEMRE) — apareció en dos ejes de investigación independientes sin pedirlo | `PLAN.md` ya lo marca como "pendiente, explícitamente no ahora" (fuente externa DEMRE aún no descargada) — esta investigación no cambia esa decisión, pero sí sube su prioridad relativa si Diego alguna vez la reabre. **Vale la pena que Diego decida explícitamente si esto sigue en pausa o pasa a evaluarse**, dado lo repetido que salió. |
| **Costo neto tras becas/gratuidad** (no arancel de lista) | El arancel bruto puede espantar a estudiantes que en la práctica pagarían $0 por gratuidad | Requiere modelar reglas de elegibilidad (deciles de ingreso, instituciones adscritas, tramos) que cambian por año y dependen de datos del propio estudiante — mucho más complejo que un dato estático |
| **Reviews reales de estudiantes/egresados** | "¿Cómo es realmente estudiar ahí?" — ningún dato SIES lo responde | Requiere recolectar, moderar y verificar contenido generado por usuarios durante años (Niche lleva más de una década); no viable de corto plazo |
| **TIR / % de carreras con retorno económico negativo** | Dato fuerte y citado por la FNE (35% de las carreras con TIR negativa en Chile, brecha de género 4,5x) | No existe como dataset abierto fácil de cruzar hoy; es un dato sensible que puede leerse como "esta carrera es mala" si no se presenta con mucho cuidado |
| **Tasa de formalidad laboral (cotizantes)** | Separa "cuánto gana el que trabaja formal" de "qué tan fácil es conseguir trabajo formal" — SIES no distingue esto | Requeriría una fuente nueva tipo Dirección del Trabajo/Previred, no referenciada hoy en el proyecto |
| **Transición entre ocupaciones** ("si esto no me gusta, ¿a qué más me puedo cambiar?") | Responde la reversibilidad de una elección de carrera — ningún comparador chileno lo aborda | Requiere microdatos de trayectorias laborales reales post-titulación, que no existen públicos en Chile |
| **Movilidad socioeconómica intergeneracional** (quintil de ingreso de los padres → quintil del egresado) | Responde probabilidad real de ascenso social condicionada al origen, no solo el promedio agregado | Exige datos longitudinales cruzados (tipo CASEN/SII) a nivel de institución que probablemente no están disponibles públicamente en Chile |
| **Ranking de terceros (tipo U-Ranking) como fuente adicional** | Señal de calidad/reputación que ningún dato de empleabilidad captura | Es una decisión editorial (adoptar metodología de un tercero, con riesgo de sesgo) más que técnica — alternativa: construir señal propia desde `personal/` (JCE por institución), dataset que el proyecto ya evaluó y descartó por ahora en la primera pasada de este brainstorm |
| **Cupos/postulación en tiempo real** | "¿Todavía alcanzo a postular, cuántos cupos quedan?" | Requiere datos operacionales en vivo, un tipo de dato completamente distinto a los datasets estáticos anuales de SIES que usa Carrera Clara |

---

## Los tres datasets nunca integrados — evaluación (sin comprometerse, sin cambios respecto a la primera pasada)

| Dataset | Qué aportaría | Solapamiento con lo ya cargado | Costo | Veredicto |
|---|---|---|---|---|
| `matricula/` (matrícula 2025 por región/demografía) | Series y desagregaciones que `hecho_oferta` no tiene | **Alto** — `hecho_oferta` ya cubre matrícula por institución+carrera | Alto (loader nuevo) | Dudoso por ahora |
| `titulados/` (histórico 2007-2025) | Serie larga de titulados — señal de "carrera con historia" vs. nueva | Medio — `hecho_oferta` solo tiene 2024 puntual | Alto (loader nuevo + join) | Interesante pero nicho |
| `personal/` (PAC — planta docente, JCE, edad) | Proxy de "tamaño de planta académica" | Ninguno — dato completamente nuevo | Alto | Riesgoso sin curaduría pedagógica seria |

Puntajes de corte DEMRE: ver fila correspondiente en la sección aspiracional arriba — misma decisión de fondo, ahora con más evidencia de por qué importa.

---

## Tabla resumen priorizable (fusionada — datos internos T25 + investigación externa T26)

| # | Idea | Dirección | Tamaño | Requiere código nuevo en | Origen |
|---|---|---|---|---|---|
| 1 | Calculadora de ponderación PAES completa | 1 | 1-2 sesiones | `queries.py`/`export_json.py` o `export_instituciones.py`, `nem.html` | T26 externo |
| 2 | Costo total real (arancel + titulación) | 1 | 1 sesión | `export_json.py`, `export_instituciones.py`, `index_v2.html`, `instituciones_v2.html` | T25/T26a |
| 3 | Simulador CAE/FES | 1 | 1-2 sesiones | pantalla nueva o módulo dentro de una existente | T26 externo |
| 4 | Paquete de confianza del dato (N muestral, vigencia, "mediana no promesa", caveats) | 3 | 1-2 sesiones combinadas | copy en las 4 páginas + exponer tamaños de cohorte ya cargados | T26 externo |
| 5 | Test vocacional RIASEC propio y neutral | 5 | 2-3 sesiones | catálogo (curatoría), pantalla nueva, integración con herramientas existentes | T26 externo |
| 6 | Ranking personalizado por ponderación del usuario | 2 | 2 sesiones | `index_v2.html`/`instituciones_v2.html`, UI de sliders + score cliente | T26 externo |
| 7 | Tendencia histórica 2020-2024 | 2 | 1-2 sesiones | `queries.py`, `export_json.py`, `index_v2.html` | T25/T26a |
| 8 | Rango PAES real de matrícula | 1 | 1 sesión | `export_json.py`, `nem.html` | T25/T26a |
| 9 | NEM/PAES inline en "Carreras por institución" | 1 | 1 sesión | `instituciones_v2.html` (solo cliente) | T25/T26a |
| 10 | Modo "Versus" 1 a 1 (admisión + laboral) | 2 | 1-2 sesiones | pantalla nueva o extensión | T26 externo |
| 11 | Distribución completa de ingreso (percentiles) | 2 | 1 sesión | `queries.py`, `export_json.py`, `index_v2.html` | T25/T26a |
| 12 | Exponer diagnóstico oculto (T25-4b) | 3 | medio día | `instituciones_v2.html` | T25/T26a |
| 13 | `tipos_institucion` desde JSON (T25-4a) | 3 | trivial | `index_v2.html` | T25/T26a |
| 14 | Gráfico radar/sunburst de perfil | 2 | 1-2 sesiones | `index_v2.html`/`instituciones_v2.html` | T26 externo |
| 15 | Composición matrícula por sexo | 2 | 1 sesión | `export_json.py`, `export_instituciones.py`, ambas pantallas | T25/T26a |
| 16 | Duración formal vs. real | 1 | 2 sesiones | `queries.py`, `export_instituciones.py` | T25/T26a |
| 17 | ROI aproximado (con gráfico de punto de equilibrio) | 1 | 2-3 sesiones | varios + copy/UX de riesgo | T25a + T26 externo |
| 18 | Carreras del área (sugerencias) | 2 | 1 sesión | `index_v2.html` | T25/T26a |
| 19 | Búsqueda por lenguaje libre | 5 | 1 sesión | complementario al ítem 5 | T26 externo |
| — | `matricula/`, `titulados/`, `personal/`, puntaje de corte DEMRE, resto de aspiracionales | — | alto si se hace | loader nuevo — no recomendado por ahora | Evaluación, ver secciones arriba |

---

## Plan de ejecución progresiva sugerido (propuesta, no decisión)

Agrupación en tandas por afinidad técnica y esfuerzo, pensada para sesiones sucesivas de 1-2 tandas cada una. Es una sugerencia de orden, no un compromiso — Diego elige qué tanda(s) seguir, en qué orden, o si prefiere una combinación distinta.

- **Tanda A — Extender "Qué NEM necesito" a admisión completa** (ítems 1, 8, 9): la calculadora de ponderación PAES completa es la idea con más eco independiente en toda la investigación externa. Todo el trabajo cae sobre una pantalla que ya existe y datos ya cargados.
- **Tanda B — Costo real** (ítems 2, 3, 17 parcial): costo total + simulador CAE/FES. Cierra el círculo de "cuánto pago realmente" que hoy el sitio solo resuelve a medias con el arancel bruto.
- **Tanda C — Confianza del dato** (ítem 4 + parte de la Dirección 3 ya existente): barato, transversal a las 4 páginas, refuerza una regla de producto que Diego ya exige.
- **Tanda D — Comparación personalizada** (ítems 6, 10, 14): ranking ponderado, modo Versus, radar — mismo tipo de trabajo (UI de comparación + score en cliente), tiene sentido agruparlos.
- **Tanda E — Descubrimiento vocacional** (ítems 5, 19): la de mayor esfuerzo y mayor diferenciación estratégica frente al mercado chileno — probablemente su propia sesión o par de sesiones, dado el trabajo de curatoría del catálogo.
- **Tanda F — Series de tiempo y composición** (ítems 7, 11, 15, 16): agrupa todo lo que toca `queries.py`/`hecho_benchmark_nacional` en una sola pasada por ese archivo.
- **Housekeeping** (ítems 12, 13, 18): baratos, se pueden colar en cualquier sesión con espacio libre.

**Pregunta abierta para Diego, no resuelta en este documento:** si vale la pena reabrir la evaluación de integrar puntaje de corte histórico DEMRE, dado que salió como el gap más repetido de toda la investigación externa. No se resuelve acá porque cambia el alcance del proyecto (fuente externa nueva, no solo exponer datos ya cargados) — queda marcado en la sección aspiracional para que Diego lo decida cuando quiera.

`TAREA_27_PROMPT.md` (Ficha de institución) sigue en cola tal como estaba — este documento no lo reemplaza ni lo reordena, solo aporta contenido adicional para cuando se ejecute (ver Dirección 4).

---

## Próximo paso

Diego elige qué tanda(s) seguir (una, varias, en el orden sugerido o en otro). Con eso se redacta la siguiente `TAREA_N_PROMPT.md` de implementación y se marca T26 ✅ en `PLAN.md` con el resumen de qué dirección(es) quedaron priorizadas.
