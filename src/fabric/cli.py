"""
iDirectoryFabric - Fabric CLI Subcommand Controller
Integra la validación del Esquema de Directorio Base Universal, clasificación Medallón,
auditoría de Capacidad F8 y remediación automática en el CLI.
"""

from pathlib import Path
from typing import List
from .medallion import (
    scan_workspace_items,
    classify_fabric_item,
    validate_base_workspace_schema,
)
from .rules import audit_fabric_path
from .remediator import remediate_file


def run_fabric_cli(argv: List[str], repo_root: Path) -> int:
    """Ejecuta los subcomandos de Fabric."""
    if not argv or "--help" in argv or "-h" in argv:
        print("[iDirectoryFabric - Motor de Gobernanza y Esquema Base para Microsoft Fabric]")
        print("Uso: python FWengine.py fabric [opciones]")
        print("  --classify [ruta]    Valida el esquema de directorio base y clasifica artefactos Fabric en capas Medallón.")
        print("  --audit [ruta]       Audita código PySpark/Pipelines/TMDL contra reglas de Capacidad F8.")
        print("  --remediate [ruta]   Aplica parches automáticos de optimización F8 a notebooks.")
        return 0

    mode = "audit"
    default_workspace = repo_root / "fabric_workspaces"
    target_path = default_workspace if default_workspace.exists() else repo_root

    idx = 0
    while idx < len(argv):
        arg = argv[idx]
        if arg in ["--audit", "audit"]:
            mode = "audit"
            if idx + 1 < len(argv) and not argv[idx + 1].startswith("-"):
                target_path = Path(argv[idx + 1])
                idx += 1
        elif arg in ["--classify", "classify"]:
            mode = "classify"
            if idx + 1 < len(argv) and not argv[idx + 1].startswith("-"):
                target_path = Path(argv[idx + 1])
                idx += 1
        elif arg in ["--remediate", "remediate"]:
            mode = "remediate"
            if idx + 1 < len(argv) and not argv[idx + 1].startswith("-"):
                target_path = Path(argv[idx + 1])
                idx += 1
        idx += 1

    target = target_path.resolve()
    if not target.is_absolute():
        target = (repo_root / target_path).resolve()

    if mode == "classify":
        print(f"[*] Analizando Esquema de Directorio Base y Artefactos Fabric en: {target}")
        if (target / "fabric_workspaces").is_dir() or target.name.lower() == "fabric_workspaces":
            schema_report = validate_base_workspace_schema(target)
            status_str = "VALIDADO (100%)" if schema_report["valid"] else "INCOMPLETO"
            print(
                f"[+] Esquema Base Universal: {status_str} — "
                f"{schema_report['workspaces_count']} Workspaces Medallón | "
                f"{schema_report['containers_count']} Carpetas Contenedoras Gobernadas:"
            )
            for c in schema_report["containers"]:
                tier_badge = f"[{c['tier'].upper():<15}]"
                types_str = ", ".join(c["accepted_types"])
                state_icon = "OK" if (c["exists"] and c["has_beacon"]) else "MISSING"
                print(f"  {tier_badge} {c['path']:<52} ({state_icon}) <- [{types_str}]")

        items = scan_workspace_items(target)
        if not items:
            if not ((target / "fabric_workspaces").is_dir() or target.name.lower() == "fabric_workspaces"):
                direct = classify_fabric_item(target)
                print(f"  -> Clasificación de ruta: {direct['tier'].upper()} ({direct['item_type']}) -> Destino base: {direct['target_folder']}")
            else:
                print("[i] Directorio base limpio (0 artefactos acoplados). Listo para recibir artefactos de cualquier Workspace.")
            return 0

        print(f"\n[+] Se detectaron {len(items)} artefactos Fabric depositados:")
        for it in items:
            tier_badge = f"[{it['tier'].upper():<15}]"
            print(f"  {tier_badge} {it['item_name']:<35} ({it['item_type']:<13}) -> Destino base: {it['target_folder']}")
        return 0

    elif mode == "audit":
        print(f"[*] Auditando conformidad de Capacidad F8 en: {target}")
        violations = audit_fabric_path(target)
        if not violations:
            print("[PASS] 0 violaciones detectadas. Todo el código analizado cumple los estándares de Fabric F8.")
            return 0

        print(f"[!] Se encontraron {len(violations)} advertencias/violaciones de Capacidad F8:")
        for v in violations:
            sev_badge = f"[{v['severity']:<8}]"
            print(f"  {sev_badge} {v['rule_id']}: {v['message']}")
            print(f"             Archivo: {v['file']}")
            print(f"             Sugerencia: {v['suggestion']}")
        return 1 if any(v["severity"] == "CRITICAL" for v in violations) else 0

    elif mode == "remediate":
        print(f"[*] Aplicando remediaciones automáticas de optimización F8 en: {target}")
        files_to_remediate: List[Path] = []
        if target.is_file():
            files_to_remediate.append(target)
        else:
            for p in target.rglob("*.py"):
                if not any(part.startswith(".") for part in p.parts):
                    files_to_remediate.append(p)

        total_modified = 0
        for f in files_to_remediate:
            res = remediate_file(f, dry_run=False)
            if res["modified"]:
                total_modified += 1
                print(f"  [FIX] Modificado: {res['file']}")
                for act in res["actions"]:
                    print(f"        -> {act}")

        print(f"[+] Remediación finalizada: {total_modified} archivos actualizados con optimizaciones F8.")
        return 0

    return 0
