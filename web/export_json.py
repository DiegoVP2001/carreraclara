"""Exporta `mifuturo/queries.py` a JSON estatico para el comparador (Tarea 6 / Sesion 2).

Este script es la fuente de verdad; los JSON en `web/data/` son output
regenerable (mismo patron que `mifuturo/loader.py` con `comparador.db`).

Genera:
  - web/data/core.json: las 190 carreras genericas (slug, nombre, area,
    familia, benchmarks completos sin colapsar) + diagnostico_cobertura() +
    la lista de tipos de institucion vistos en los benchmarks (para el
    selector del toggle "filtro por tipo" en el cliente).
  - web/data/detalle/<slug>.json: un archivo por carrera generica con su
    oferta (hecho_oferta) e indicadores propios (hecho_indicadores), para
    lazy-load desde el cliente al abrir el panel "donde se imparte".

Slug: determinista, derivado de `nombre_carrera_generica` via NFKD (quitar
tildes) + lowercase + kebab-case. El JS del cliente debe generarlo con el
mismo algoritmo para pedir el archivo de detalle correcto (ver `slugify` en
`web/index.html`). Verificado sin colisiones sobre las 190 genericas reales.

Nota sobre el TODO `seleccionar_benchmark_destacado` de `queries.py`: se
resuelve como toggle de cliente en `web/index.html` (3 vistas: todo lado a
lado, priorizar Universidad, filtro por tipo) - no se colapsa nada aqui, se
exporta la lista completa de benchmarks por carrera.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mifuturo"))

from queries import (  # noqa: E402
    BenchmarkNacional,
    CarreraGenericaResumen,
    DiagnosticoCobertura,
    InstitucionInfo,
    detalle_carrera_generica,
    diagnostico_cobertura,
    get_connection,
    listar_carreras_genericas,
)

WEB_DIR = Path(__file__).parent
DATA_DIR = WEB_DIR / "data"
DETALLE_DIR = DATA_DIR / "detalle"


def slugify(nombre: str) -> str:
    """Normaliza un nombre de carrera generica a un slug kebab-case determinista.

    Debe coincidir exactamente con la funcion `slugify` de `index.html` -
    es el contrato que permite al cliente pedir `detalle/<slug>.json` sin
    tener que listar los 190 slugs de antemano.
    """
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFKD", nombre) if not unicodedata.combining(c)
    )
    slug = re.sub(r"[^a-z0-9]+", "-", sin_acentos.lower())
    return slug.strip("-")


def benchmark_a_dict(b: BenchmarkNacional) -> dict:
    return {
        "tipo_institucion": b.tipo_institucion,
        "ingreso_4to_anio_2024": b.ingreso_4to_anio_2024,
        "empleabilidad_1er_anio_2024": b.empleabilidad_1er_anio_2024,
        "empleabilidad_2do_anio_2024": b.empleabilidad_2do_anio_2024,
        "retencion_1er_anio": b.retencion_1er_anio,
        "retencion_2do_anio": b.retencion_2do_anio,
        "percentil_10_5to_anio": b.percentil_10_5to_anio,
        "percentil_50_5to_anio": b.percentil_50_5to_anio,
        "percentil_90_5to_anio": b.percentil_90_5to_anio,
    }


def institucion_a_dict(i: InstitucionInfo) -> dict:
    return {
        "codigo": i.codigo_institucion,
        "nombre": i.nombre_institucion,
        "tipo": i.tipo_institucion,
        "acreditacion": i.acreditacion,
        "tiene_ficha": i.tiene_ficha,
    }


def carrera_a_dict(c: CarreraGenericaResumen) -> dict:
    return {
        "slug": slugify(c.nombre_carrera_generica),
        "nombre": c.nombre_carrera_generica,
        "area": c.area,
        "familia": c.familia,
        "tiene_benchmark_nacional": c.tiene_benchmark_nacional,
        "benchmarks": [benchmark_a_dict(b) for b in c.benchmarks],
    }


def diagnostico_a_dict(d: DiagnosticoCobertura) -> dict:
    return {
        "total_carreras_genericas": d.total_carreras_genericas,
        "carreras_sin_benchmark_nacional": d.carreras_sin_benchmark_nacional,
        "filas_oferta_sin_carrera_generica": d.filas_oferta_sin_carrera_generica,
        "total_filas_oferta": d.total_filas_oferta,
        "filas_indicadores_con_institucion_colgante": d.filas_indicadores_con_institucion_colgante,
        "total_filas_indicadores": d.total_filas_indicadores,
    }


def main() -> None:
    DETALLE_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    try:
        carreras = listar_carreras_genericas(conn)
        diagnostico = diagnostico_cobertura(conn)

        tipos_institucion = sorted(
            {b.tipo_institucion for c in carreras for b in c.benchmarks if b.tipo_institucion}
        )

        core = {
            "carreras": [carrera_a_dict(c) for c in carreras],
            "diagnostico_cobertura": diagnostico_a_dict(diagnostico),
            "tipos_institucion": tipos_institucion,
        }
        (DATA_DIR / "core.json").write_text(
            json.dumps(core, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        slugs_vistos: dict[str, str] = {}
        for c in carreras:
            slug = slugify(c.nombre_carrera_generica)
            if slug in slugs_vistos:
                raise ValueError(
                    f"Colision de slug '{slug}' entre "
                    f"'{slugs_vistos[slug]}' y '{c.nombre_carrera_generica}'"
                )
            slugs_vistos[slug] = c.nombre_carrera_generica

            detalle = detalle_carrera_generica(conn, c.nombre_carrera_generica)
            assert detalle is not None  # viene de listar_carreras_genericas, existe por construccion

            detalle_dict = {
                "slug": slug,
                "nombre": detalle.resumen.nombre_carrera_generica,
                "ofertas": [
                    {
                        "codigo_unico_carrera": o.codigo_unico_carrera,
                        "institucion": institucion_a_dict(o.institucion),
                        "nombre_carrera_programa": o.nombre_carrera_programa,
                        "nivel_carrera": o.nivel_carrera,
                        "region": o.region,
                        "jornada": o.jornada,
                        "sede": o.sede,
                        "arancel_anual_2026": o.arancel_anual_2026,
                        "vacantes_1er_semestre": o.vacantes_1er_semestre,
                        "tiene_ponderacion_paes": o.tiene_ponderacion_paes,
                        "ponderacion_nem": o.ponderacion_nem,
                        "ponderacion_ranking": o.ponderacion_ranking,
                        "ponderacion_lenguaje": o.ponderacion_lenguaje,
                        "ponderacion_matematicas": o.ponderacion_matematicas,
                        "ponderacion_matematicas_2": o.ponderacion_matematicas_2,
                        "ponderacion_historia": o.ponderacion_historia,
                        "ponderacion_ciencias": o.ponderacion_ciencias,
                        "ponderacion_otros": o.ponderacion_otros,
                    }
                    for o in detalle.ofertas
                ],
                "indicadores": [
                    {
                        "institucion": institucion_a_dict(ind.institucion),
                        "nombre_carrera_titulo": ind.nombre_carrera_titulo,
                        "empleabilidad_1er_anio": ind.empleabilidad_1er_anio,
                        "empleabilidad_2do_anio": ind.empleabilidad_2do_anio,
                        "retencion_1er_anio": ind.retencion_1er_anio,
                        "continuidad_estudios_pct": ind.continuidad_estudios_pct,
                        "duracion_real_semestres": ind.duracion_real_semestres,
                        "ingreso_banda_texto": ind.ingreso_banda_texto,
                    }
                    for ind in detalle.indicadores
                ],
            }
            (DETALLE_DIR / f"{slug}.json").write_text(
                json.dumps(detalle_dict, ensure_ascii=False, indent=2), encoding="utf-8"
            )

        print(f"OK: {len(carreras)} carreras genericas exportadas a {DATA_DIR / 'core.json'}")
        print(f"OK: {len(slugs_vistos)} archivos de detalle exportados a {DETALLE_DIR}")
        print(f"Sin benchmark nacional: {diagnostico.carreras_sin_benchmark_nacional}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
