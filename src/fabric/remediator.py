"""
iDirectoryFabric - Fabric Code Remediator
Aplica parches y optimizaciones automáticas a código PySpark,
pipelines y configuraciones de capacidad F8 en Microsoft Fabric.
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
import re

F8_PYSPARK_HEADER = """# ==============================================================================
# [iDirectoryFabric F8 Optimization Block - Santolaya]
# Configuración determinista para pool Spark de 16 vCores y lectura Direct Lake
# ==============================================================================
spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
spark.conf.set("spark.ms.autotune.optimizeWrite", "true")
spark.conf.set("spark.sql.shuffle.partitions", "8")
# ==============================================================================
"""


def remediate_pyspark_code(code: str) -> Tuple[str, List[str]]:
    """
    Parchea código PySpark inyectando configuraciones recomendadas para Fabric F8
    y remediando antipatrones conocidos.
    """
    actions: List[str] = []
    new_code = code

    # 1. Inyectar encabezado V-Order y Shuffle Partitions si falta
    if "vorder.enabled" not in new_code.lower() and ("spark." in new_code or "from pyspark" in new_code):
        # Insertar después de imports o al inicio
        import_blocks = list(re.finditer(r"^(?:from\s+\S+\s+import\s+.*|import\s+.*)$", new_code, re.MULTILINE))
        if import_blocks:
            last_import = import_blocks[-1]
            insert_pos = last_import.end()
            new_code = new_code[:insert_pos] + "\n\n" + F8_PYSPARK_HEADER + new_code[insert_pos:]
        else:
            new_code = F8_PYSPARK_HEADER + "\n" + new_code
        actions.append("Inyectado bloque de optimización F8 (V-Order=True, Shuffle Partitions=8, OptimizeWrite=True).")

    # 2. Alertar / Comentar sobre llamadas peligrosas a collect()
    if re.search(r"\b\w+\.collect\(\)", new_code):
        actions.append("ALERTA: Se detectó llamada a .collect(). Se recomienda reemplazar por .take(10) o agregaciones.")

    return new_code, actions


def remediate_file(file_path: Path, dry_run: bool = False) -> Dict[str, Any]:
    """Aplica remediación sobre un archivo específico si aplica."""
    path = file_path.resolve()
    if not path.is_file():
        return {"file": str(path), "modified": False, "actions": ["Archivo no encontrado."]}

    ext = path.suffix.lower()
    if ext != ".py" and path.name != "notebook-content.py":
        return {"file": str(path), "modified": False, "actions": ["Tipo de archivo no remediable automáticamente."]}

    original = path.read_text(encoding="utf-8", errors="replace")
    remediated, actions = remediate_pyspark_code(original)

    modified = False
    if remediated != original:
        modified = True
        if not dry_run:
            path.write_text(remediated, encoding="utf-8")

    return {
        "file": str(path).replace("\\", "/"),
        "modified": modified,
        "actions": actions
    }

