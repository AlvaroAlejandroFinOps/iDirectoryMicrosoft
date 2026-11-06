"""
iDirectoryFabric - Medallion Classifier & Workspace Item Detector
Analiza y clasifica artefactos de Microsoft Fabric Git Integration
en capas Medallón: Bronze, Silver, Gold, BI Semantic y Core Governance.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


class MedallionTier(str, Enum):
    CORE_GOVERNANCE = "core_governance"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    BI_SEMANTIC = "bi_semantic"
    UNKNOWN = "unknown"


# Extensiones canónicas de artefactos de Microsoft Fabric Git Integration
FABRIC_ITEM_EXTENSIONS = {
    ".Lakehouse": "Lakehouse",
    ".Notebook": "Notebook",
    ".DataPipeline": "DataPipeline",
    ".Warehouse": "Warehouse",
    ".SemanticModel": "SemanticModel",
    ".Report": "Report",
    ".Environment": "Environment",
    ".MirroredDatabase": "MirroredDatabase",
    ".KQLDatabase": "KQLDatabase",
    ".Eventstream": "Eventstream",
    ".MLModel": "MLModel",
    ".SQLDatabase": "SQLDatabase",
    ".GraphQLApi": "GraphQLApi",
}


def read_fabric_platform_metadata(item_dir: Path) -> Dict[str, Any]:
    """Lee el archivo .platform en la raíz del artefacto si existe."""
    platform_file = item_dir / ".platform"
    if platform_file.is_file():
        try:
            return json.loads(platform_file.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def detect_item_type(path: Path) -> Optional[str]:
    """Detecta el tipo de artefacto de Fabric a partir del sufijo de carpeta o metadatos."""
    name = path.name
    for ext, item_type in FABRIC_ITEM_EXTENSIONS.items():
        if name.endswith(ext):
            return item_type

    # Verificar si dentro hay un .platform que especifique el tipo
    meta = read_fabric_platform_metadata(path)
    if "metadata" in meta and "type" in meta["metadata"]:
        return str(meta["metadata"]["type"])

    # Detección por archivos internos estándar
    if (path / "notebook-content.py").is_file() or any(path.glob("*.ipynb")):
        return "Notebook"
    if (path / "pipeline-content.json").is_file():
        return "DataPipeline"
    if (path / "definition.pbir").is_file() or (path / "definition.pbip").is_file():
        return "Report"
    if (path / "definition.pbism").is_file() or (path / "definition" / "model.tmdl").is_file():
        return "SemanticModel"

    return None


def classify_fabric_item(item_path: Path) -> Dict[str, Any]:
    """
    Clasifica un artefacto de Microsoft Fabric en la arquitectura Medallón.
    Retorna un diccionario con:
      - item_name: Nombre del artefacto
      - item_type: Tipo de ítem en Fabric
      - tier: MedallionTier
      - confidence: "high" | "medium" | "inferred"
      - rationale: Motivo de la clasificación
    """
    path = item_path.resolve()
    name_lower = path.name.lower()
    path_str = str(path).lower().replace("\\", "/")

    item_type = detect_item_type(path) or "General"

    # 1. Clasificación por contexto de ruta (Folder Hierarchy)
    if any(k in path_str for k in ["/ws_core", "/core_governance", "/governance", "/shared_core"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.CORE_GOVERNANCE.value,
            "confidence": "high",
            "rationale": "Ubicado en directorio de gobernanza central / entorno compartido.",
        }

    if any(k in path_str for k in ["/ws_bronze", "/bronze", "/raw", "/ingest"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.BRONZE.value,
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Bronze.",
        }

    if any(k in path_str for k in ["/ws_silver", "/silver", "/curated", "/transform"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.SILVER.value,
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Silver.",
        }

    if any(k in path_str for k in ["/ws_gold", "/gold", "/analytics", "/dimensional"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.GOLD.value,
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Gold.",
        }

    if any(k in path_str for k in ["/ws_bi", "/bi_semantic", "/semantic", "/reporting", "/reports"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.BI_SEMANTIC.value,
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Semántica / BI.",
        }

    # 2. Clasificación por Tipo de Ítem y Nombres Nominales
    if item_type == "Environment":
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.CORE_GOVERNANCE.value,
            "confidence": "medium",
            "rationale": "Los artefactos Environment definen pools Spark y configuración de runtime.",
        }

    if item_type in ["SemanticModel", "Report"]:
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.BI_SEMANTIC.value,
            "confidence": "high",
            "rationale": "Modelos semánticos y reportes pertenecen a la capa de consumo BI Direct Lake.",
        }

    if item_type == "Warehouse":
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.GOLD.value,
            "confidence": "high",
            "rationale": "Fabric Warehouses normalmente alojan modelos analíticos dimensionales (Gold).",
        }

    # Heurística nominal para Notebooks, Pipelines y Lakehouses
    if any(k in name_lower for k in ["ingest", "raw", "landing", "copy", "source", "extrac", "bronze"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.BRONZE.value,
            "confidence": "medium",
            "rationale": "Patrón nominal de ingesta cruda o aterrizaje.",
        }

    if any(k in name_lower for k in ["curate", "clean", "transf", "normal", "silver", "dedup", "conformed"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.SILVER.value,
            "confidence": "medium",
            "rationale": "Patrón nominal de curación, limpieza y transformación con Delta.",
        }

    if any(k in name_lower for k in ["kimball", "star", "dim_", "fact_", "gold", "kpi", "mart", "analytics"]):
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": MedallionTier.GOLD.value,
            "confidence": "medium",
            "rationale": "Patrón nominal de modelo dimensional analítico (Star Schema).",
        }

    # Fallback predeterminado según tipo
    if item_type == "DataPipeline":
        tier = MedallionTier.BRONZE.value
        rat = "Pipeline de datos asignado por defecto a Bronze (Ingesta)."
    elif item_type == "Notebook":
        tier = MedallionTier.SILVER.value
        rat = "Notebook de PySpark asignado por defecto a Silver (Transformación)."
    elif item_type == "Lakehouse":
        tier = MedallionTier.SILVER.value
        rat = "Lakehouse asignado por defecto a Silver (Capa de persistencia Delta central)."
    else:
        tier = MedallionTier.UNKNOWN.value
        rat = "No se pudo determinar el nivel Medallón con certeza."

    return {
        "item_name": path.name,
        "item_type": item_type,
        "tier": tier,
        "confidence": "inferred",
        "rationale": rat,
    }


def scan_workspace_items(root_dir: Path) -> List[Dict[str, Any]]:
    """Escanea un directorio en busca de todos los artefactos de Microsoft Fabric."""
    root = root_dir.resolve()
    items: List[Dict[str, Any]] = []

    # Recorrido guiado que busca directorios de artefactos
    for p in root.rglob("*"):
        if not p.is_dir():
            continue
        # Ignorar directorios de sistema y runtime
        if any(part.startswith(".") and part not in [".platform", ".Environment", ".Notebook"] for part in p.parts):
            continue

        item_type = detect_item_type(p)
        if item_type is not None:
            classification = classify_fabric_item(p)
            classification["path"] = str(p.relative_to(root)).replace("\\", "/")
            items.append(classification)

    return items

