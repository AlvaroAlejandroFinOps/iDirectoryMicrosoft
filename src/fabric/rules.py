"""
iDirectoryFabric - Fabric F8 Optimization & Throttling Linter Rules
Reglas de análisis estático para código PySpark, T-SQL, Pipelines y TMDL en Microsoft Fabric F8.
"""

from pathlib import Path
from typing import Any, Dict, List, Set
import re
import json


FABRIC_F8_RULES = {
    "RULE-F8-01": {
        "id": "RULE-F8-01",
        "name": "V-Order Parquet Optimization",
        "severity": "HIGH",
        "description": "Las escrituras Delta/Parquet deben tener activo V-Order para lectura directa sub-segundo en Direct Lake.",
        "remediation": "Configurar spark.conf.set('spark.sql.parquet.vorder.enabled', 'true') al inicio del notebook.",
    },
    "RULE-F8-02": {
        "id": "RULE-F8-02",
        "name": "Liquid Clustering vs Hive Partitioning",
        "severity": "HIGH",
        "description": "Evitar partitionBy() en columnas de alta cardinalidad en OneLake (genera tormentas de archivos pequeños). Usar Liquid Clustering (CLUSTER BY).",
        "remediation": "Reemplazar .partitionBy(cols) por Liquid Clustering con .clusterBy(cols) o Delta ALTER TABLE CLUSTER BY.",
    },
    "RULE-F8-03": {
        "id": "RULE-F8-03",
        "name": "Collect & Driver OOM Protection",
        "severity": "CRITICAL",
        "description": "Uso peligroso de .collect() o .toPandas() en PySpark que puede provocar OOM en el driver y saturar los 16 vCores de F8.",
        "remediation": "Evitar descargar DataFrames enteros al driver; usar escrituras directas a OneLake o .limit() controlado.",
    },
    "RULE-F8-04": {
        "id": "RULE-F8-04",
        "name": "Shuffle Partition Sizing for 16 vCores",
        "severity": "MEDIUM",
        "description": "El valor por defecto de 200 shuffle partitions sobrecarga el planificador en capacidades F8 (~16 vCores).",
        "remediation": "Configurar spark.conf.set('spark.sql.shuffle.partitions', '8') para cargas de volumen medio.",
    },
    "RULE-F8-05": {
        "id": "RULE-F8-05",
        "name": "Delta Maintenance Automation",
        "severity": "MEDIUM",
        "description": "Falta de mantenimiento Delta programado (OPTIMIZE / VACUUM) para prevenir acumulación de metadatos.",
        "remediation": "Incluir comando OPTIMIZE table_name y VACUUM table_name RETAIN 168 HOURS en pipelines semanales.",
    },
    "RULE-F8-06": {
        "id": "RULE-F8-06",
        "name": "Direct Lake DAX Fallback Prevention",
        "severity": "CRITICAL",
        "description": "Columnas calculadas en DAX en modelos Direct Lake que provocan conmutación a DirectQuery y saturación de 8 CUs.",
        "remediation": "Pre-calcular columnas derivadas en PySpark o SQL en la capa Silver/Gold y removerlas del modelo semántico.",
    },
    "RULE-F8-07": {
        "id": "RULE-F8-07",
        "name": "Pipeline Concurrency Smoothing",
        "severity": "HIGH",
        "description": "Más de 2 notebooks pesados ejecutándose concurrentemente en un pipeline sobre F8 saturan la capacidad.",
        "remediation": "Secuenciar actividades pesadas con dependencias en el pipeline para suavizar el consumo sobre 24h.",
    },
}

# Directorios internos del motor de gobernanza excluidos del escaneo de artefactos Fabric cuando se audita la raíz
FRAMEWORK_INTERNAL_DIRS: Set[str] = {
    "src/core",
    "src/fabric",
    "tools",
    "tests",
    "scripts",
    "schemas",
    "config",
    "docs",
    "01_seed",
    "artifacts",
    "skills",
}


def audit_pyspark_content(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analiza código PySpark en busca de violaciones a las reglas F8."""
    violations: List[Dict[str, Any]] = []

    # Verificar si el archivo es realmente un notebook o job PySpark
    has_spark_import = bool(re.search(r"^\s*(?:from|import)\s+pyspark\b", content, re.MULTILINE))
    has_spark_api = bool(re.search(r"\bspark\.(?:read|sql|table|conf|createDataFrame)\b", content))
    is_fabric_nb = "notebook-content.py" in file_path or "# Fabric notebook source" in content

    if not (has_spark_import or has_spark_api or is_fabric_nb):
        return violations

    # 1. Verificar V-Order en escrituras de DataFrame Spark
    has_writes = bool(re.search(r"\.write\b\s*\.(?:format|mode|option|save|parquet|delta)|\.(?:saveAsTable|toTable)\s*\(", content))
    has_vorder = "vorder.enabled" in content.lower()
    if has_writes and not has_vorder:
        violations.append({
            "rule_id": "RULE-F8-01",
            "file": file_path,
            "severity": FABRIC_F8_RULES["RULE-F8-01"]["severity"],
            "message": "Escritura de datos detectada sin compresión V-Order explícita.",
            "suggestion": FABRIC_F8_RULES["RULE-F8-01"]["remediation"]
        })

    # 2. Verificar partitionBy de alta cardinalidad
    partition_match = re.search(r"\.partitionBy\(([^)]+)\)", content)
    if partition_match:
        cols = partition_match.group(1)
        violations.append({
            "rule_id": "RULE-F8-02",
            "file": file_path,
            "severity": FABRIC_F8_RULES["RULE-F8-02"]["severity"],
            "message": f"Uso de partitionBy({cols}). En Microsoft Fabric se recomienda Liquid Clustering (CLUSTER BY) para OneLake.",
            "suggestion": FABRIC_F8_RULES["RULE-F8-02"]["remediation"]
        })

    # 3. Verificar .collect() o .toPandas() en DataFrame de PySpark
    collect_match = re.search(r"(?:df|sdf|data|dataset|table|result)\.(collect\(\)|toPandas\(\))", content, re.IGNORECASE)
    if collect_match:
        violations.append({
            "rule_id": "RULE-F8-03",
            "file": file_path,
            "severity": FABRIC_F8_RULES["RULE-F8-03"]["severity"],
            "message": f"Llamada riesgosa '{collect_match.group(0)}' que descarga datos masivos a la memoria del driver.",
            "suggestion": FABRIC_F8_RULES["RULE-F8-03"]["remediation"]
        })

    # 4. Verificar shuffle partitions
    has_shuffle_config = "shuffle.partitions" in content.lower()
    if has_writes and not has_shuffle_config:
        violations.append({
            "rule_id": "RULE-F8-04",
            "file": file_path,
            "severity": FABRIC_F8_RULES["RULE-F8-04"]["severity"],
            "message": "spark.sql.shuffle.partitions no configurado (usará 200 por defecto en pool de 16 vCores).",
            "suggestion": FABRIC_F8_RULES["RULE-F8-04"]["remediation"]
        })

    return violations


def audit_pipeline_content(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analiza la definición JSON de un pipeline de Data Factory para detectar sobreconcurrencia."""
    violations: List[Dict[str, Any]] = []
    try:
        data = json.loads(content)
        properties = data.get("properties", data)
        activities = properties.get("activities", [])

        # Contar actividades de Notebook sin dependencias (ejecutan en paralelo al inicio)
        root_notebooks = 0
        for act in activities:
            act_type = act.get("type", "")
            depends = act.get("dependsOn", [])
            if "TridentNotebook" in act_type or "SparkJob" in act_type or act_type == "Notebook":
                if not depends:
                    root_notebooks += 1

        if root_notebooks > 2:
            violations.append({
                "rule_id": "RULE-F8-07",
                "file": file_path,
                "severity": FABRIC_F8_RULES["RULE-F8-07"]["severity"],
                "message": f"Pipeline inicia {root_notebooks} actividades de Spark en paralelo sin escalonamiento.",
                "suggestion": FABRIC_F8_RULES["RULE-F8-07"]["remediation"]
            })
    except Exception:
        pass

    return violations


def audit_tmdl_content(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Analiza archivos de modelo semántico TMDL buscando columnas calculadas en DAX."""
    violations: List[Dict[str, Any]] = []
    calc_col_matches = re.findall(r"column\s+[\w\s]+\s*=\s*(.+)", content)
    if calc_col_matches:
        violations.append({
            "rule_id": "RULE-F8-06",
            "file": file_path,
            "severity": FABRIC_F8_RULES["RULE-F8-06"]["severity"],
            "message": f"Detectadas {len(calc_col_matches)} columnas calculadas en DAX. En Direct Lake causan conmutación a DirectQuery.",
            "suggestion": FABRIC_F8_RULES["RULE-F8-06"]["remediation"]
        })
    return violations


def _is_framework_internal_file(file_path: Path, scan_root: Path) -> bool:
    """Verifica si un archivo pertenece al motor interno de iDirectory cuando se escanea desde la raíz."""
    if not (scan_root / "FWengine.py").is_file():
        return False
    try:
        rel = file_path.resolve().relative_to(scan_root.resolve()).as_posix().lower()
    except ValueError:
        return False
    if rel == "fwengine.py":
        return True
    for internal_prefix in FRAMEWORK_INTERNAL_DIRS:
        if rel == internal_prefix or rel.startswith(internal_prefix + "/"):
            return True
    return False


def audit_fabric_path(target_path: Path) -> List[Dict[str, Any]]:
    """Audita un archivo o directorio completo de Fabric contra las reglas F8."""
    target = target_path.resolve()
    all_violations: List[Dict[str, Any]] = []

    files_to_check: List[Path] = []
    if target.is_file():
        files_to_check.append(target)
    elif target.is_dir():
        for p in target.rglob("*"):
            if not p.is_file():
                continue
            if any(part.startswith(".") and part not in [".platform", ".Environment", ".Notebook"] for part in p.parts):
                continue
            if _is_framework_internal_file(p, target):
                continue
            files_to_check.append(p)

    for f in files_to_check:
        ext = f.suffix.lower()
        rel_str = str(f).replace("\\", "/")
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        if ext == ".py" or f.name == "notebook-content.py":
            all_violations.extend(audit_pyspark_content(content, rel_str))
        elif ext == ".json" and ("pipeline" in f.name.lower() or "pipeline-content" in f.name.lower()):
            all_violations.extend(audit_pipeline_content(content, rel_str))
        elif ext == ".tmdl":
            all_violations.extend(audit_tmdl_content(content, rel_str))

    return all_violations
