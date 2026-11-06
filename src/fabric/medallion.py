"""
iDirectoryFabric - Universal Base Schema, Medallion Classifier & Item Router
Gobierna el esquema de directorio base universal para Microsoft Fabric Git Integration
y clasifica/enruta artefactos en capas Medallón: Core Governance, Bronze, Silver, Gold y BI Semantic.
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
    ".CopyJob": "CopyJob",
    ".Dataflow": "Dataflow",
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

# Esquema de Directorio Base Universal para Workspaces de Microsoft Fabric
FABRIC_BASE_SCHEMA: Dict[str, Dict[str, Any]] = {
    "ws_core_governance": {
        "tier": MedallionTier.CORE_GOVERNANCE.value,
        "description": "Gobernanza central, Spark Environments, librerías compartidas y mantenimiento Delta",
        "containers": {
            "environments": ["Environment"],
            "libraries": ["Wheel", "PyModule"],
            "notebooks": ["Notebook"],
        },
    },
    "ws_bronze_ingest": {
        "tier": MedallionTier.BRONZE.value,
        "description": "Ingesta cruda inmutable, OneLake Shortcuts, Pipelines, Dataflows y Streaming",
        "containers": {
            "lakehouses": ["Lakehouse"],
            "pipelines": ["DataPipeline", "CopyJob"],
            "dataflows": ["Dataflow"],
            "eventstreams": ["Eventstream", "MirroredDatabase", "KQLDatabase"],
            "notebooks": ["Notebook"],
        },
    },
    "ws_silver_transform": {
        "tier": MedallionTier.SILVER.value,
        "description": "Curación, deduplicación, calidad de datos y conformación Delta Lake",
        "containers": {
            "lakehouses": ["Lakehouse"],
            "notebooks": ["Notebook"],
            "pipelines": ["DataPipeline"],
        },
    },
    "ws_gold_analytics": {
        "tier": MedallionTier.GOLD.value,
        "description": "Modelo dimensional Kimball Star Schema en Lakehouse Gold y Fabric Warehouse",
        "containers": {
            "lakehouses": ["Lakehouse"],
            "warehouses": ["Warehouse", "SQLDatabase", "GraphQLApi"],
            "notebooks": ["Notebook", "MLModel"],
            "pipelines": ["DataPipeline"],
        },
    },
    "ws_bi_semantic": {
        "tier": MedallionTier.BI_SEMANTIC.value,
        "description": "Modelos semánticos Direct Lake (TMDL) y reportes ejecutivos Power BI (PBIR/PBIP)",
        "containers": {
            "semantic_models": ["SemanticModel"],
            "reports": ["Report"],
        },
    },
}


def resolve_fabric_target_folder(item_name: str, item_type: Optional[str] = None, tier_hint: Optional[str] = None) -> str:
    """
    Determina la carpeta contenedora óptima dentro de fabric_workspaces/ para cualquier
    artefacto de Microsoft Fabric (Notebook, Lakehouse, Warehouse, Pipeline, SemanticModel, Report, etc.).
    """
    name_lower = item_name.lower()
    if item_type is None:
        for ext, itype in FABRIC_ITEM_EXTENSIONS.items():
            if name_lower.endswith(ext.lower()):
                item_type = itype
                break
        if item_type is None:
            if name_lower.endswith((".tmdl", ".pbism", ".bim")):
                item_type = "SemanticModel"
            elif name_lower.endswith((".pbir", ".pbip", ".pbix")):
                item_type = "Report"
            elif name_lower.endswith((".ipynb", ".py")):
                item_type = "Notebook"
            elif name_lower.endswith(".sql"):
                item_type = "Warehouse"
            elif name_lower.endswith(".whl"):
                item_type = "Wheel"

    inferred_tier = (tier_hint or "").lower()
    if not inferred_tier:
        if any(k in name_lower for k in ["maint", "vacuum", "audit", "gov", "admin", "shared", "core"]):
            inferred_tier = MedallionTier.CORE_GOVERNANCE.value
        elif any(k in name_lower for k in ["bronze", "raw", "ingest", "landing", "extract", "source", "copy"]):
            inferred_tier = MedallionTier.BRONZE.value
        elif any(k in name_lower for k in ["gold", "kimball", "star", "dim_", "fact_", "mart", "kpi", "analytics"]):
            inferred_tier = MedallionTier.GOLD.value
        elif any(k in name_lower for k in ["bi", "semantic", "report", "rpt_", "sm_"]):
            inferred_tier = MedallionTier.BI_SEMANTIC.value
        else:
            inferred_tier = MedallionTier.SILVER.value

    if item_type == "Environment":
        return "fabric_workspaces/ws_core_governance/environments"
    if item_type in ("Wheel", "PyModule"):
        return "fabric_workspaces/ws_core_governance/libraries"
    if item_type == "SemanticModel":
        return "fabric_workspaces/ws_bi_semantic/semantic_models"
    if item_type == "Report":
        return "fabric_workspaces/ws_bi_semantic/reports"
    if item_type in ("Warehouse", "SQLDatabase", "GraphQLApi"):
        return "fabric_workspaces/ws_gold_analytics/warehouses"
    if item_type == "Dataflow":
        return "fabric_workspaces/ws_bronze_ingest/dataflows"
    if item_type in ("Eventstream", "MirroredDatabase", "KQLDatabase"):
        return "fabric_workspaces/ws_bronze_ingest/eventstreams"

    if item_type in ("DataPipeline", "CopyJob"):
        if inferred_tier == MedallionTier.SILVER.value and any(k in name_lower for k in ["silver", "curate", "transf", "clean"]):
            return "fabric_workspaces/ws_silver_transform/pipelines"
        if inferred_tier == MedallionTier.GOLD.value:
            return "fabric_workspaces/ws_gold_analytics/pipelines"
        return "fabric_workspaces/ws_bronze_ingest/pipelines"

    if item_type == "Lakehouse":
        if inferred_tier == MedallionTier.BRONZE.value:
            return "fabric_workspaces/ws_bronze_ingest/lakehouses"
        if inferred_tier == MedallionTier.GOLD.value:
            return "fabric_workspaces/ws_gold_analytics/lakehouses"
        return "fabric_workspaces/ws_silver_transform/lakehouses"

    if item_type in ("Notebook", "MLModel"):
        if inferred_tier == MedallionTier.CORE_GOVERNANCE.value:
            return "fabric_workspaces/ws_core_governance/notebooks"
        if inferred_tier == MedallionTier.BRONZE.value:
            return "fabric_workspaces/ws_bronze_ingest/notebooks"
        if inferred_tier == MedallionTier.GOLD.value:
            return "fabric_workspaces/ws_gold_analytics/notebooks"
        return "fabric_workspaces/ws_silver_transform/notebooks"

    return "fabric_workspaces/ws_silver_transform/notebooks"


def validate_base_workspace_schema(root_dir: Path) -> Dict[str, Any]:
    """
    Verifica que el directorio base de Workspaces de Fabric posea las 5 capas Medallón
    y sus 17 carpetas contenedoras con sus respectivos beacons .context.yaml.
    """
    root = root_dir.resolve()
    ws_root = root / "fabric_workspaces" if (root / "fabric_workspaces").is_dir() else root

    containers_checked: List[Dict[str, Any]] = []
    missing_dirs: List[str] = []
    missing_beacons: List[str] = []

    for ws_name, ws_meta in FABRIC_BASE_SCHEMA.items():
        ws_dir = ws_root / ws_name
        ws_rel = f"fabric_workspaces/{ws_name}" if ws_root != root else ws_name
        if not ws_dir.is_dir():
            missing_dirs.append(ws_rel)
            continue
        if not (ws_dir / ".context.yaml").is_file():
            missing_beacons.append(f"{ws_rel}/.context.yaml")

        for container_name, accepted_types in ws_meta["containers"].items():
            c_dir = ws_dir / container_name
            c_rel = f"{ws_rel}/{container_name}"
            exists = c_dir.is_dir()
            has_beacon = (c_dir / ".context.yaml").is_file() if exists else False
            if not exists:
                missing_dirs.append(c_rel)
            elif not has_beacon:
                missing_beacons.append(f"{c_rel}/.context.yaml")

            containers_checked.append({
                "workspace": ws_name,
                "tier": ws_meta["tier"],
                "container": container_name,
                "path": c_rel,
                "accepted_types": accepted_types,
                "exists": exists,
                "has_beacon": has_beacon,
            })

    return {
        "valid": len(missing_dirs) == 0 and len(missing_beacons) == 0,
        "workspaces_count": len(FABRIC_BASE_SCHEMA),
        "containers_count": len(containers_checked),
        "containers": containers_checked,
        "missing_dirs": missing_dirs,
        "missing_beacons": missing_beacons,
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
    name_lower = name.lower()
    for ext, item_type in FABRIC_ITEM_EXTENSIONS.items():
        if name_lower.endswith(ext.lower()):
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
    Clasifica un artefacto de Microsoft Fabric en la arquitectura Medallón y
    sugiere su carpeta contenedora canónica dentro del esquema base.
    """
    path = item_path.resolve()
    name_lower = path.name.lower()
    path_str = str(path).lower().replace("\\", "/")

    item_type = detect_item_type(path) or "General"

    # 1. Clasificación por contexto de ruta (Folder Hierarchy)
    if any(k in path_str for k in ["/ws_core", "/core_governance", "/governance", "/shared_core"]):
        tier = MedallionTier.CORE_GOVERNANCE.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "high",
            "rationale": "Ubicado en directorio de gobernanza central / entorno compartido.",
        }

    if any(k in path_str for k in ["/ws_bronze", "/bronze", "/raw", "/ingest"]):
        tier = MedallionTier.BRONZE.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Bronze.",
        }

    if any(k in path_str for k in ["/ws_silver", "/silver", "/curated", "/transform"]):
        tier = MedallionTier.SILVER.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Silver.",
        }

    if any(k in path_str for k in ["/ws_gold", "/gold", "/analytics", "/dimensional"]):
        tier = MedallionTier.GOLD.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Gold.",
        }

    if any(k in path_str for k in ["/ws_bi", "/bi_semantic", "/semantic", "/reporting", "/reports"]):
        tier = MedallionTier.BI_SEMANTIC.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "high",
            "rationale": "Ubicado en workspace/directorio de capa Semántica / BI.",
        }

    # 2. Clasificación por Tipo de Ítem y Nombres Nominales
    if item_type == "Environment":
        tier = MedallionTier.CORE_GOVERNANCE.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "medium",
            "rationale": "Los artefactos Environment definen pools Spark y configuración de runtime.",
        }

    if item_type in ["SemanticModel", "Report"]:
        tier = MedallionTier.BI_SEMANTIC.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "high",
            "rationale": "Modelos semánticos y reportes pertenecen a la capa de consumo BI Direct Lake.",
        }

    if item_type in ["Warehouse", "SQLDatabase", "GraphQLApi"]:
        tier = MedallionTier.GOLD.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "high",
            "rationale": "Fabric Warehouses y SQL Databases alojan modelos analíticos dimensionales (Gold).",
        }

    # Heurística nominal para Notebooks, Pipelines y Lakehouses
    if any(k in name_lower for k in ["ingest", "raw", "landing", "copy", "source", "extrac", "bronze"]):
        tier = MedallionTier.BRONZE.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "medium",
            "rationale": "Patrón nominal de ingesta cruda o aterrizaje.",
        }

    if any(k in name_lower for k in ["curate", "clean", "transf", "normal", "silver", "dedup", "conformed"]):
        tier = MedallionTier.SILVER.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "medium",
            "rationale": "Patrón nominal de curación, limpieza y transformación con Delta.",
        }

    if any(k in name_lower for k in ["kimball", "star", "dim_", "fact_", "gold", "kpi", "mart", "analytics"]):
        tier = MedallionTier.GOLD.value
        return {
            "item_name": path.name,
            "item_type": item_type,
            "tier": tier,
            "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
            "confidence": "medium",
            "rationale": "Patrón nominal de modelo dimensional analítico (Star Schema).",
        }

    # Fallback predeterminado según tipo
    if item_type in ("DataPipeline", "CopyJob", "Dataflow", "Eventstream", "MirroredDatabase", "KQLDatabase"):
        tier = MedallionTier.BRONZE.value
        rat = "Artefacto de integración asignado por defecto a Bronze (Ingesta)."
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
        "target_folder": resolve_fabric_target_folder(path.name, item_type, tier),
        "confidence": "inferred",
        "rationale": rat,
    }


def scan_workspace_items(root_dir: Path) -> List[Dict[str, Any]]:
    """Escanea un directorio en busca de todos los artefactos de Microsoft Fabric."""
    root = root_dir.resolve()
    items: List[Dict[str, Any]] = []

    for p in root.rglob("*"):
        if not p.is_dir():
            continue
        if any(part.startswith(".") and part not in [".platform", ".Environment", ".Notebook"] for part in p.parts):
            continue

        item_type = detect_item_type(p)
        if item_type is not None:
            classification = classify_fabric_item(p)
            classification["path"] = str(p.relative_to(root)).replace("\\", "/")
            items.append(classification)

    return items
