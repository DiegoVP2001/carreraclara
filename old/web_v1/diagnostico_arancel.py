"""Diagnostico de Paso 1 (Tarea 7, Iteracion 4): cuantos combos institucion+
carrera-titulo de `instituciones.json` resuelven a un arancel sin ambiguedad.

Para cada uno de los ~1690 combos, busca las filas de `hecho_oferta` con el
mismo `codigo_institucion` y la misma `nombre_carrera_generica` (ya resuelta
en el loader via `Area Carrera Generica`, ver MODELO_DATOS.md seccion 6 -
no hace falta repetir el join de texto aqui, la columna ya esta en la tabla).
Clasifica:
  - Nivel 1 (sin ambiguedad): 0 filas encontradas, o todas comparten el mismo
    `arancel_anual_2026`.
  - Nivel 2 (ambiguo): 2+ filas con `arancel_anual_2026` distintos.

No escribe nada a disco - solo imprime los conteos que deciden el resto de
la sesion (ver TAREA_7_ITERACION_4_PROMPT.md).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mifuturo"))

from queries import detalle_carrera_generica, get_connection, listar_carreras_genericas  # noqa: E402


def main() -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()

        nivel1 = 0
        nivel1_cero_filas = 0
        nivel1_una_o_mas_iguales = 0
        nivel2 = 0
        nivel2_ejemplos: list[tuple[int, str, list[str]]] = []
        total = 0

        genericas = listar_carreras_genericas(conn)
        for generica in genericas:
            detalle = detalle_carrera_generica(conn, generica.nombre_carrera_generica)
            assert detalle is not None

            for indicador in detalle.indicadores:
                codigo = indicador.institucion.codigo_institucion
                if codigo is None:
                    continue  # filas fantasma, ya excluidas del export (ver export_instituciones.py)
                total += 1

                cur.execute(
                    "SELECT arancel_anual_2026 FROM hecho_oferta"
                    " WHERE codigo_institucion = ? AND nombre_carrera_generica = ?"
                    " AND arancel_anual_2026 IS NOT NULL",
                    (codigo, generica.nombre_carrera_generica),
                )
                aranceles = sorted({r[0] for r in cur.fetchall()})

                if len(aranceles) <= 1:
                    nivel1 += 1
                    if len(aranceles) == 0:
                        nivel1_cero_filas += 1
                    else:
                        nivel1_una_o_mas_iguales += 1
                else:
                    nivel2 += 1
                    if len(nivel2_ejemplos) < 15:
                        nivel2_ejemplos.append(
                            (codigo, indicador.nombre_carrera_titulo or "", aranceles)
                        )

        print(f"Total combos clasificados: {total}")
        print(f"Nivel 1 (sin ambiguedad): {nivel1} ({100 * nivel1 / total:.2f}%)")
        print(f"  - de los cuales 0 filas en hecho_oferta: {nivel1_cero_filas}")
        print(f"  - de los cuales 1+ filas con arancel igual: {nivel1_una_o_mas_iguales}")
        print(f"Nivel 2 (ambiguo, 2+ aranceles distintos): {nivel2} ({100 * nivel2 / total:.2f}%)")
        print()
        print("Ejemplos de Nivel 2 (hasta 15):")
        for codigo, titulo, aranceles in nivel2_ejemplos:
            print(f"  codigo={codigo} titulo={titulo!r} aranceles={aranceles}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
