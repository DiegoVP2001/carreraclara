"""Exporta un indice plano institucion+carrera-titulo para el comparador (Tarea 7).

Este script es la fuente de verdad; `web/data/instituciones.json` es output
regenerable (mismo patron que `export_json.py` con `core.json`/`detalle/`).

Decision de grano (ver PLAN.md, Tarea 7): se usa `hecho_indicadores`
(`IndicadorTitulo` en `queries.py` - institucion x carrera-titulo), no
`hecho_oferta`, porque viene directo del ancla sin el fuzzy-match de
`Area Carrera Generica` que `hecho_oferta` necesita para unirse a carrera
generica (peor cobertura, ver Tarea 1/4).

Decision de forma del indice: un unico JSON plano (`instituciones.json`) con
las ~1690 combinaciones institucion+carrera-titulo validas. El dataset es
chico, asi que no se indexa por institucion ni se pagina - el cliente filtra
en memoria con `normalizar()` (mismo patron que el combobox de carreras).

Decision de reuso de `queries.py` (no se modifica, ver CLAUDE.md/PLAN.md):
no existe una consulta que liste TODAS las filas de `hecho_indicadores` de
una sola vez, asi que este script itera `listar_carreras_genericas()` +
`detalle_carrera_generica()` (ya expuestas) y junta los `.indicadores` de
cada generica. Se verifico que esto cubre el 100% de las filas validas:
de las 1692 filas de `hecho_indicadores`, 2 son filas totalmente vacias
(codigo_institucion, nombre_carrera_titulo y nombre_carrera_generica los
3 NULL - mismo patron de fila fantasma que el ya documentado en Tarea 4 para
`hecho_oferta`) y por eso no tienen `nombre_carrera_generica` para que
`detalle_carrera_generica` las traiga; las 1690 filas restantes SI tienen
`nombre_carrera_generica` no nulo, asi que iterar las 190 genericas las
captura completas (verificado contra `comparador.db` directo via sqlite3,
no solo confiando en la cobertura logica).

Identificador de combinacion: `f"{codigo_institucion}--{slugify(carrera_titulo)}"`.
Es determinista y se verifico sin colisiones sobre las 1690 filas reales
(codigo_institucion + nombre_carrera_titulo ya es una clave unica natural en
el dataset real; el slug del titulo no colisiona entre titulos distintos del
mismo codigo). Las 2 filas totalmente vacias no tienen codigo_institucion
(NULL) y se excluyen del indice - no representan una combinacion valida que
se pueda buscar ni seleccionar.

Estado "institucion sin ficha": el codigo_institucion SI existe en estas 16
filas (FK colgante a `dim_institucion`, no fila vacia) - se identifican en
el selector por codigo + carrera-titulo, ya que no tienen nombre propio
(ver `institucion.tiene_ficha=False` en `web/index.html`, mismo patron).

Ingreso como rango numerico (iteracion 2, feedback de Diego tras probar el
MVP v1): `ingreso_banda_texto` es una banda de texto ("De $900 mil a $1
millon"), no un numero continuo (`ingreso_numerico` existe en el schema pero
esta 100% NULL en el dataset real - confirmado via sqlite3 directo). En vez
de tratarla como categoria ordinal (v1: escala Chart.js `category`), se
parsea el texto a un RANGO numerico real `[min, max]` en CLP (helper
`parse_rango_banda`) - el cliente grafica una "floating bar" (Chart.js
soporta datasets `[min, max]` por punto en un grafico de barras normal) con
el eje de sueldo como eje lineal continuo, mostrando solo los extremos de
la banda (no un boxplot real con cuartiles, solo el rango). Se probo el
parser contra las 22 bandas reales: el limite superior de cada banda calza
exactamente con el limite inferior de la banda siguiente (continuidad sin
huecos ni superposicion), confirmando que el regex separa bien los 2
montos de texto como "De $2 millones 500 mil a $3 millones".

Banda abierta: "Sobre $3 millones 500 mil" no tiene techo reportado por
SIES - `max` queda en `None` explicitamente (`ingreso_banda_abierta=True`
en el combo) en vez de inventarse un techo. El cliente decide como
visualizarla (ver `instituciones.html`); este modulo nunca rellena un
numero que SIES no reporto.

`continuidad_estudios_pct` se deja fuera del export (Diego: "no es
relevante para el estudiante que esta postulando" - feedback de iteracion
2). Sigue disponible en `queries.py`/`comparador.db` si una tarea futura
lo necesita; no se borra del modelo de datos, solo no se expone aqui.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mifuturo"))

from queries import (  # noqa: E402
    IndicadorTitulo,
    InstitucionInfo,
    detalle_carrera_generica,
    get_connection,
    listar_carreras_genericas,
)

WEB_DIR = Path(__file__).parent
DATA_DIR = WEB_DIR / "data"


def slugify(nombre: str) -> str:
    """Identico a `slugify()` de `export_json.py`/`index.html` - mismo contrato NFKD+kebab-case."""
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFKD", nombre) if not unicodedata.combining(c)
    )
    slug = re.sub(r"[^a-z0-9]+", "-", sin_acentos.lower())
    return slug.strip("-")


_RE_MONEY = re.compile(r"\$(\d+)\s*(?:(mill\w*)\s*(?:(\d+)\s*mil)?|mil)\b")


def _valor_monto(m: re.Match) -> int:
    base = int(m.group(1))
    if m.group(2):
        extra = int(m.group(3)) if m.group(3) else 0
        return base * 1_000_000 + extra * 1000
    return base * 1000


def parse_rango_banda(texto: str) -> tuple[int | None, int | None]:
    """Parsea una banda de texto a `(minimo, maximo)` en CLP.

    Cada banda tiene 1 o 2 montos en dinero ("De $X a $Y" o, para la unica
    banda abierta, solo "Sobre $X"). Se toma el primer monto encontrado como
    minimo y el ultimo como maximo (`None` si solo hay 1 monto - banda
    abierta). Maneja los 3 formatos vistos en las 22 bandas reales: "$D
    mil", "$D millon(es)" y "$D millon(es) E mil".

    Probado contra las 22 bandas reales de `comparador.db`: produce 22
    rangos donde el maximo de cada banda calza exactamente con el minimo de
    la banda siguiente (sin huecos, sin superposicion), salvo la ultima
    banda (abierta, maximo=None).
    """
    montos = list(_RE_MONEY.finditer(texto))
    if not montos:
        return None, None
    minimo = _valor_monto(montos[0])
    maximo = _valor_monto(montos[-1]) if len(montos) >= 2 else None
    return minimo, maximo


_RE_ARANCEL_CLP = re.compile(r"^\$\s*([\d.]+)$")
_RE_ARANCEL_UF = re.compile(r"^UF\s*([\d.]+)$")


def parse_arancel(texto: str) -> tuple[str, int] | None:
    """Parsea un valor de `hecho_oferta.arancel_anual_2026` a `(moneda, monto)`.

    Dos formatos reales vistos en la columna: pesos ("$ 3.407.000", 9785/9900
    filas) y UF ("UF 152", 113/9900 filas) - **no se convierte UF a CLP**
    (necesitaria un valor de UF del dia, dato externo que este proyecto no
    tiene y que ademas varia diario; convertir igual inventaria precision que
    SIES no reporto). Se devuelve la moneda explicita para que el cliente
    etiquete correctamente ("UF 152" vs "$3.407.000"), nunca mezclados como
    si fueran la misma unidad. Verificado: ningun combo institucion+generica
    mezcla ambas monedas entre sus filas de `hecho_oferta` (0 casos sobre el
    diagnostico real, ver diagnostico_arancel.py) - si eso cambiara con datos
    nuevos, este parser seguiria devolviendo cada fila con su moneda propia,
    es la logica de agregacion en `resolver_arancel` la que asumiria
    homogeneidad (assert explicito ahi, no aqui).
    """
    m_clp = _RE_ARANCEL_CLP.match(texto)
    if m_clp:
        return "CLP", int(m_clp.group(1).replace(".", ""))
    m_uf = _RE_ARANCEL_UF.match(texto)
    if m_uf:
        return "UF", int(m_uf.group(1).replace(".", ""))
    return None


def resolver_arancel(cur, codigo_institucion: int, nombre_carrera_generica: str) -> dict:
    """Resuelve el arancel cruzado de un combo, escalonado por nivel de certeza.

    Decision de la sesion (Tarea 7, Iteracion 4 - ver diagnostico_arancel.py):
    el join confiable institucion+generica (mismo que usa "donde se imparte"
    en index.html) llega a `hecho_oferta` a nivel de carrera GENERICA, no de
    carrera-titulo (el grano real de esta pestana). El diagnostico real sobre
    los 1690 combos dio:
      - Nivel 1 (sin ambiguedad - 0 filas o 1 valor unico): 1196 combos (70.77%)
      - Nivel 2 (ambiguo - 2+ valores distintos): 494 combos (29.23%)
    494 es "de orden cientos", no decenas - el umbral que la sesion de scoping
    fijo para intentar el fuzzy-match manual con Diego en la misma sesion. Por
    eso esta funcion NO implementa el Paso 2 (fuzzy-match nombre_carrera_programa
    vs nombre_carrera_titulo): cae directo a Nivel 3 (rango aproximado) para
    todo combo ambiguo, dejando el fuzzy-match como TODO explicito documentado
    en PLAN.md para una sesion futura dedicada solo a eso.

    Devuelve dict con:
      - `arancel_moneda`: "CLP" | "UF" | None (None si no hay ninguna fila)
      - `arancel_exacto`: int | None (Nivel 1 con 1+ filas, todas el mismo valor)
      - `arancel_min` / `arancel_max`: int | None (Nivel 3: rango entre filas
        distintas - se usa tanto para el Nivel 2 real como, trivialmente,
        cuando `arancel_exacto` ya esta poblado min=max=exacto no se duplica)
      - `arancel_aproximado`: bool - True solo si el valor mostrado es un rango
        (Nivel 2 sin resolver), nunca junto con `arancel_exacto` poblado.
    """
    cur.execute(
        "SELECT DISTINCT arancel_anual_2026 FROM hecho_oferta"
        " WHERE codigo_institucion = ? AND nombre_carrera_generica = ?"
        " AND arancel_anual_2026 IS NOT NULL",
        (codigo_institucion, nombre_carrera_generica),
    )
    textos = [r[0] for r in cur.fetchall()]
    if not textos:
        return {
            "arancel_moneda": None,
            "arancel_exacto": None,
            "arancel_min": None,
            "arancel_max": None,
            "arancel_aproximado": False,
        }

    parsed = [parse_arancel(t) for t in textos]
    if any(p is None for p in parsed):
        raise AssertionError(f"arancel_anual_2026 con formato no reconocido entre {textos!r}")
    monedas = {p[0] for p in parsed}
    if len(monedas) > 1:
        raise AssertionError(
            f"Combo institucion={codigo_institucion} generica={nombre_carrera_generica!r} "
            f"mezcla monedas distintas en hecho_oferta: {textos!r} - revisar dataset, "
            "el diagnostico de la sesion asumio 0 casos mixtos"
        )
    moneda = monedas.pop()
    montos = sorted({p[1] for p in parsed})

    if len(montos) == 1:
        return {
            "arancel_moneda": moneda,
            "arancel_exacto": montos[0],
            "arancel_min": None,
            "arancel_max": None,
            "arancel_aproximado": False,
        }

    return {
        "arancel_moneda": moneda,
        "arancel_exacto": None,
        "arancel_min": montos[0],
        "arancel_max": montos[-1],
        "arancel_aproximado": True,
    }


_POND_COLS = [
    ("ponderacion_nem", "nem"),
    ("ponderacion_ranking", "ranking"),
    ("ponderacion_lenguaje", "paes_lenguaje"),
    ("ponderacion_matematicas", "paes_matematicas"),
    ("ponderacion_matematicas_2", "paes_matematicas_2"),
    ("ponderacion_historia", "paes_historia"),
    ("ponderacion_ciencias", "paes_ciencias"),
    ("ponderacion_otros", "ponderacion_otros"),
]


def resolver_ponderaciones(cur, codigo_institucion: int, nombre_carrera_generica: str) -> dict:
    """Resuelve las ponderaciones PAES de un combo desde hecho_oferta.

    El join es identico al de resolver_arancel (institucion+generica, no titulo)
    porque hecho_oferta vive a nivel institucion x sede x jornada, no titulo.

    Si todas las filas del combo tienen las mismas 8 ponderaciones: perfil
    unico, se expone directamente. Si varían entre sedes/jornadas: se marca
    `ponderacion_varía=True` y se devuelve el primer perfil (para tener siempre
    algo que mostrar sin inventar datos). Si ninguna fila tiene ponderacion > 0:
    `tiene_ponderacion_paes=False` (ausencia legitima, no error).
    """
    sel_cols = ", ".join(f"o.{db_col}" for _, db_col in _POND_COLS)
    cur.execute(
        f"SELECT DISTINCT {sel_cols} FROM hecho_oferta o"
        " WHERE o.codigo_institucion = ? AND o.nombre_carrera_generica = ?",
        (codigo_institucion, nombre_carrera_generica),
    )
    rows = cur.fetchall()

    def row_tiene_datos(row: tuple) -> bool:
        return any(v is not None and v > 0 for v in row)

    rows_con_datos = [r for r in rows if row_tiene_datos(r)]
    if not rows_con_datos:
        base = {"tiene_ponderacion_paes": False, "ponderacion_varia": False}
        base.update({key: None for key, _ in _POND_COLS})
        return base

    primer_perfil = {key: rows_con_datos[0][i] for i, (key, _) in enumerate(_POND_COLS)}
    varia = len(rows_con_datos) > 1
    return {"tiene_ponderacion_paes": True, "ponderacion_varia": varia, **primer_perfil}


def institucion_a_dict(i: InstitucionInfo) -> dict:
    return {
        "codigo": i.codigo_institucion,
        "nombre": i.nombre_institucion,
        "tipo": i.tipo_institucion,
        "acreditacion": i.acreditacion,
        "anios_acreditacion": i.anios_acreditacion,
        "vigencia_acreditacion": i.vigencia_acreditacion,
        "areas_acreditadas": i.areas_acreditadas,
        "direccion_sede_central": i.direccion_sede_central,
        "pagina_web": i.pagina_web,
        "tipo_sociedad": i.tipo_sociedad,
        "tiene_ficha": i.tiene_ficha,
    }


def combo_a_dict(
    indicador: IndicadorTitulo,
    nombre_carrera_generica: str,
    area: str | None,
    familia: str | None,
) -> dict:
    codigo = indicador.institucion.codigo_institucion
    assert codigo is not None  # filtrado antes de llamar a esta funcion

    ingreso_min: int | None = None
    ingreso_max: int | None = None
    ingreso_abierta = False
    if indicador.ingreso_banda_texto:
        ingreso_min, ingreso_max = parse_rango_banda(indicador.ingreso_banda_texto)
        ingreso_abierta = ingreso_min is not None and ingreso_max is None

    return {
        "id": f"{codigo}--{slugify(indicador.nombre_carrera_titulo or '')}",
        "institucion": institucion_a_dict(indicador.institucion),
        "carrera_titulo": indicador.nombre_carrera_titulo,
        "carrera_generica": nombre_carrera_generica,
        "area": area,
        "familia": familia,
        "empleabilidad_1er_anio": indicador.empleabilidad_1er_anio,
        "empleabilidad_2do_anio": indicador.empleabilidad_2do_anio,
        "retencion_1er_anio": indicador.retencion_1er_anio,
        "duracion_real_semestres": indicador.duracion_real_semestres,
        "ingreso_banda_texto": indicador.ingreso_banda_texto,
        "ingreso_banda_min": ingreso_min,
        "ingreso_banda_max": ingreso_max,
        "ingreso_banda_abierta": ingreso_abierta,
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    try:
        cur_arancel = conn.cursor()
        cur_pond = conn.cursor()
        genericas = listar_carreras_genericas(conn)

        combos: list[dict] = []
        ids_vistos: dict[str, tuple[int, str]] = {}

        for generica in genericas:
            detalle = detalle_carrera_generica(conn, generica.nombre_carrera_generica)
            assert detalle is not None  # viene de listar_carreras_genericas, existe por construccion

            for indicador in detalle.indicadores:
                codigo = indicador.institucion.codigo_institucion
                if codigo is None:
                    # No deberia ocurrir: las unicas filas de hecho_indicadores
                    # sin codigo_institucion tampoco tienen
                    # nombre_carrera_generica (fila fantasma, ver docstring),
                    # asi que detalle_carrera_generica nunca las trae. Falla
                    # fuerte si esa premisa cambia con datos nuevos.
                    raise AssertionError(
                        f"Indicador sin codigo_institucion bajo generica "
                        f"'{generica.nombre_carrera_generica}' - revisar dataset"
                    )

                combo = combo_a_dict(
                    indicador, generica.nombre_carrera_generica, generica.area, generica.familia
                )
                combo.update(resolver_arancel(cur_arancel, codigo, generica.nombre_carrera_generica))
                combo.update(resolver_ponderaciones(cur_pond, codigo, generica.nombre_carrera_generica))
                clave = (codigo, indicador.nombre_carrera_titulo or "")
                if combo["id"] in ids_vistos and ids_vistos[combo["id"]] != clave:
                    raise ValueError(
                        f"Colision de id '{combo['id']}' entre {ids_vistos[combo['id']]} y {clave}"
                    )
                ids_vistos[combo["id"]] = clave
                combos.append(combo)

        sin_ficha = sum(1 for c in combos if not c["institucion"]["tiene_ficha"])
        sin_ingreso = sum(1 for c in combos if not c["ingreso_banda_texto"])
        banda_abierta = sum(1 for c in combos if c["ingreso_banda_abierta"])
        sin_arancel = sum(1 for c in combos if c["arancel_moneda"] is None)
        arancel_exacto = sum(1 for c in combos if c["arancel_exacto"] is not None)
        arancel_aproximado = sum(1 for c in combos if c["arancel_aproximado"])
        con_ponderacion = sum(1 for c in combos if c["tiene_ponderacion_paes"])
        ponderacion_varia = sum(1 for c in combos if c.get("ponderacion_varia"))

        # Ningun combo puede quedar sin clasificar entre exacto/aproximado/sin-dato.
        if sin_arancel + arancel_exacto + arancel_aproximado != len(combos):
            raise AssertionError(
                "Combos de arancel sin clasificar: "
                f"sin_dato={sin_arancel} exacto={arancel_exacto} aproximado={arancel_aproximado} "
                f"total={len(combos)}"
            )

        # Sanity check del parser de rango: cada banda distinta con techo
        # (max no nulo) debe calzar su techo con el piso de la banda
        # siguiente en la cadena ordinal real (continuidad sin huecos,
        # verificada manualmente en la sesion contra las 22 bandas reales -
        # aqui solo se reconfirma que el dataset completo no introdujo una
        # banda de texto nueva que rompa esa cadena).
        rangos_unicos = sorted(
            {
                (c["ingreso_banda_min"], c["ingreso_banda_max"])
                for c in combos
                if c["ingreso_banda_min"] is not None
            }
        )
        for (lo_actual, hi_actual), (lo_siguiente, _hi_siguiente) in zip(
            rangos_unicos, rangos_unicos[1:]
        ):
            if hi_actual is not None and hi_actual != lo_siguiente:
                raise AssertionError(
                    f"Discontinuidad en bandas de ingreso: techo {hi_actual} no calza "
                    f"con el piso de la siguiente banda {lo_siguiente}"
                )

        # Sanity check de cobertura completa contra la tabla cruda: toda fila
        # de hecho_indicadores con codigo_institucion no nulo debe terminar
        # como un combo (las 2 filas restantes son la fila fantasma sin
        # generica/institucion/titulo, documentada en el docstring, que no
        # representa una combinacion seleccionable).
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hecho_indicadores WHERE codigo_institucion IS NOT NULL")
        total_filas_validas = cur.fetchone()[0]
        if total_filas_validas != len(combos):
            raise AssertionError(
                f"Cobertura incompleta: {total_filas_validas} filas validas en "
                f"hecho_indicadores vs. {len(combos)} combos exportados"
            )

        data = {
            "combos": combos,
            "diagnostico": {
                "total_combos": len(combos),
                "combos_institucion_sin_ficha": sin_ficha,
                "combos_sin_banda_ingreso": sin_ingreso,
                "combos_banda_ingreso_abierta": banda_abierta,
                "combos_arancel_exacto": arancel_exacto,
                "combos_arancel_aproximado": arancel_aproximado,
                "combos_sin_arancel": sin_arancel,
                "combos_con_ponderacion_paes": con_ponderacion,
                "combos_sin_ponderacion_paes": len(combos) - con_ponderacion,
                "combos_ponderacion_varia_por_sede": ponderacion_varia,
            },
        }

        (DATA_DIR / "instituciones.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        print(f"OK: {len(combos)} combinaciones institucion+carrera-titulo exportadas")
        print(f"  institucion sin ficha: {sin_ficha}")
        print(f"  sin banda de ingreso: {sin_ingreso}")
        print(f"  banda de ingreso abierta (sin techo reportado): {banda_abierta}")
        print(f"  arancel exacto (Nivel 1): {arancel_exacto}")
        print(f"  arancel aproximado/rango (Nivel 2 sin fuzzy-match, ver TODO en PLAN.md): {arancel_aproximado}")
        print(f"  sin dato de arancel (0 filas en hecho_oferta): {sin_arancel}")
        print(f"  bandas de ingreso distintas (rangos unicos): {len(rangos_unicos)}")
        print(f"  con ponderacion PAES (al menos 1 componente > 0): {con_ponderacion}")
        print(f"  sin ponderacion PAES reportada: {len(combos) - con_ponderacion}")
        print(f"  ponderacion varia por sede/jornada: {ponderacion_varia}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
