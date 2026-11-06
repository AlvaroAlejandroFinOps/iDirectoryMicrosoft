"""
iDirectoryFabric - Santolaya Chile Business Utilities
Módulo de utilitarios chilenos: validación de RUT con algoritmo Módulo 11
y normalización de valores UF / CLP para obras y contratos.
"""

from typing import Tuple, Optional
import re


def validate_chilean_rut(rut_str: str) -> bool:
    """Valida un RUT chileno usando el algoritmo Módulo 11."""
    if not rut_str:
        return False
    clean = re.sub(r"[^0-9kK]", "", rut_str.strip())
    if len(clean) < 2:
        return False
    body, dv = clean[:-1], clean[-1].upper()
    if not body.isdigit():
        return False

    # Algoritmo Módulo 11
    multiplier = 2
    total = 0
    for digit in reversed(body):
        total += int(digit) * multiplier
        multiplier = 2 if multiplier == 7 else multiplier + 1

    expected_mod = 11 - (total % 11)
    if expected_mod == 11:
        expected_dv = "0"
    elif expected_mod == 10:
        expected_dv = "K"
    else:
        expected_dv = str(expected_mod)

    return dv == expected_dv


def format_chilean_rut(rut_str: str) -> Optional[str]:
    """Formatea un RUT a estructura estándar: 12.345.678-K."""
    if not validate_chilean_rut(rut_str):
        return None
    clean = re.sub(r"[^0-9kK]", "", rut_str.strip())
    body, dv = clean[:-1], clean[-1].upper()
    # Formatear cuerpo con puntos
    rev_body = body[::-1]
    chunks = [rev_body[i:i + 3] for i in range(0, len(rev_body), 3)]
    formatted_body = ".".join(chunks)[::-1]
    return f"{formatted_body}-{dv}"

