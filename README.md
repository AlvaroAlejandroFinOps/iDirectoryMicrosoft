![iDirectoryFabric Architecture](iDirectory.png)

**iDirectoryFabric v6.0.0.** Universal Base Directory Schema, Enterprise Governance, Context Engineering & Automated Remediation Framework for Microsoft Fabric (Capacity F8+).
<!-- ICONTEXT-V6:RELEASE -->

# iDirectoryFabric: The Universal Microsoft Fabric Base Directory Schema & Governance Standard by Gravity HyperScale Thinking

**Language:** [English](README.md) | [Español](README_ES.md)

[![Standard](https://img.shields.io/badge/Standard-Enterprise%20Paper--Grade%20v6.0-2b2b2b?style=flat-square)](#)
[![Blueprint](https://img.shields.io/badge/Blueprint-Universal%20Fabric%20Base%20Schema-107c41?style=flat-square)](#2-system-architecture--medallion-lineage)
[![Fabric Capacity](https://img.shields.io/badge/Fabric%20Capacity-F8%2B%20%288%20CUs%20%7C%2016%20vCores%29-0078d4?style=flat-square)](#3-microsoft-fabric-capacity-f8-governance--cu-economics)
[![Architecture](https://img.shields.io/badge/Architecture-OneLake%20Medallion-008272?style=flat-square)](#2-system-architecture--medallion-lineage)
[![Direct Lake](https://img.shields.io/badge/Power%20BI-Direct%20Lake%20Guardrails-f2c811?style=flat-square)](#4-f8-optimization--remediation-engine)
[![Engine](https://img.shields.io/badge/Engine-FWengine.py-1a1a1a?style=flat-square)](#5-cli-interface--operational-commands)
[![License](https://img.shields.io/badge/License-MIT-1a1a1a?style=flat-square)](LICENSE)

---

## 1. Executive Abstract

**iDirectoryFabric**, originated and engineered by **Gravity HyperScale Thinking**, establishes the **Universal Base Directory Schema (Blueprint/Template)** and deterministic context engineering control-plane to structure, govern, and scale any enterprise repository across **Microsoft Fabric Git Integration** on GitHub.

Modern data engineering teams operating across multiple Microsoft Fabric Workspaces face two structural challenges when adopting GitHub version control:
1. **Repository & Workspace Sprawl:** Without a standardized base folder schema, Notebooks (`.Notebook`), Lakehouse references (`.Lakehouse`), Warehouses (`.Warehouse`), Data Pipelines (`.DataPipeline`), Semantic Models (`.SemanticModel` in TMDL), and Power BI Reports (`.Report` in PBIR) are dumped flatly into workspace roots, breaking lineage visibility and governance.
2. **Capacity Throttling & DirectQuery Fallback (F8+ Baseline):** Operating workloads on elastic capacities such as **Microsoft Fabric F8** (8 Capacity Units $\approx$ 16 vCore Spark burst pool) requires strict guardrails against *Interactive Rejection*, *Background Rejection* (24-hour smoothing window), and *Small File Storms* in OneLake.

To solve both challenges simultaneously, **iDirectoryFabric v6.0** provides a clean, client-agnostic **5-Workspace / 17-Container Base Directory Schema** anchored by `.context.yaml` beacons, paired with a zero-dependency governance kernel (`FWengine.py`), an **Automated Medallion Router & Classifier**, and an **F8 Static & Dynamic Remediation Engine** with bounded AI token consumption ($< 220\text{ tokens}$ in Tier 1A).

---

## 2. System Architecture & Medallion Lineage

iDirectoryFabric provides a clean, ready-to-clone multi-workspace base structure compatible with **Microsoft Fabric Git Integration** (*Subfolder-per-Workspace* and native *Workspace Folders*):

```text
fabric_workspaces/
├── ws_core_governance/                # Central Governance, Spark Compute & Shared Libraries
│   ├── environments/                  # Target folder for *.Environment (Spark pools, runtime)
│   ├── libraries/                     # Target folder for shared Python wheels (.whl) & modules (.py)
│   └── notebooks/                     # Target folder for maintenance *.Notebook (OPTIMIZE / VACUUM)
│
├── ws_bronze_ingest/                  # Bronze Layer Workspace (Immutable Raw Ingestion)
│   ├── lakehouses/                    # Target folder for Bronze *.Lakehouse references & Shortcuts
│   ├── pipelines/                     # Target folder for ingestion *.DataPipeline & *.CopyJob
│   ├── dataflows/                     # Target folder for *.Dataflow Gen2 items
│   ├── eventstreams/                  # Target folder for *.Eventstream, *.MirroredDatabase, *.KQLDatabase
│   └── notebooks/                     # Target folder for complex API/raw ingestion *.Notebook
│
├── ws_silver_transform/               # Silver Layer Workspace (Curation, Quality & Conformed Delta)
│   ├── lakehouses/                    # Target folder for Silver *.Lakehouse references
│   ├── notebooks/                     # Target folder for PySpark/SQL transformation & SCD2 *.Notebook
│   └── pipelines/                     # Target folder for Silver orchestration *.DataPipeline
│
├── ws_gold_analytics/                 # Gold Layer Workspace (Kimball Dimensional Star Schema)
│   ├── lakehouses/                    # Target folder for V-Order optimized Gold *.Lakehouse
│   ├── warehouses/                    # Target folder for *.Warehouse & *.SQLDatabase (T-SQL DDL/Views)
│   ├── notebooks/                     # Target folder for Kimball Facts & Dimensions *.Notebook
│   └── pipelines/                     # Target folder for Gold analytical refresh *.DataPipeline
│
└── ws_bi_semantic/                    # BI Semantic & Consumption Layer Workspace (Direct Lake)
    ├── semantic_models/               # Target folder for *.SemanticModel (TMDL & .pbism definitions)
    └── reports/                       # Target folder for Power BI *.Report (PBIR / PBIP text format)
```

Each of the 17 container folders is anchored in Git by its own `.context.yaml` beacon—preserving the empty base folder hierarchy in GitHub without polluting workspaces with `.gitkeep` files that Fabric Git Integration rejects, while automatically injecting layer-specific engineering rules into AI coding agents.

---

## 3. Microsoft Fabric Capacity F8 Governance & CU Economics

Fabric F8 compute capacity allocates 8 Capacity Units (CUs), operating under deterministic smoothing algorithms:

$$\text{Available Compute Pool} = 8\text{ CUs} \approx 16\text{ vCores Spark (Starter Pool: 1–2 Medium Nodes)}$$

### Smoothing & Throttling Parameters
| Operation Type | Smoothing Window | Throttling Impact on Capacity Exceeded |
|---|---|---|
| **Interactive (Direct Lake / Reports)** | 5 Minutes | Delay $\to$ Interactive Rejection (Visual failure in Power BI) |
| **Background (PySpark / Pipelines)** | 24 Hours | Queueing $\to$ Background Rejection (Pipeline aborted) |
| **Direct Lake Model Memory** | Hard Limit | Fallback to DirectQuery $\implies$ Immediate 8 CU saturation |

iDirectoryFabric governs Spark pool configurations inside `ws_core_governance/environments/*.Environment/Setting/Spark/compute.json`:
- **Node Allocation:** Min 1 node, Max 2 nodes (prevents runaway autoscale charges).
- **Auto-pause Delay:** 2 minutes (eliminates idle cluster burn).
- **Dynamic Optimization:** Auto-tune and `optimizeWrite` enabled by default.

---

## 4. F8 Optimization & Remediation Engine

The remediation engine detects and resolves 7 systemic performance anti-patterns across any artifact dropped into the base schema:

```text
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
| Rule ID     | Anti-Pattern Detected                | Severity | Automated Remediation                   |
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
| RULE-F8-01  | Parquet write without V-Order        | HIGH     | Injects parquet.vorder.enabled = true   |
| RULE-F8-02  | partitionBy on high-cardinality keys | HIGH     | Replaces with Liquid Clustering         |
| RULE-F8-03  | df.collect() / .toPandas() on driver | CRITICAL | Flags/refactors to distributed sink     |
| RULE-F8-04  | Default shuffle.partitions = 200     | MEDIUM   | Downscales partitions to 8              |
| RULE-F8-05  | Missing Delta OPTIMIZE & VACUUM      | MEDIUM   | Appends automated maintenance commands  |
| RULE-F8-06  | DAX calculated columns in DirectLake | CRITICAL | Pushes calculation upstream to Silver   |
| RULE-F8-07  | Pipeline starting >2 parallel jobs   | HIGH     | Enforces sequential dependency chains   |
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
```

---

## 5. CLI Interface & Operational Commands

The entire governance kernel is invoked via `FWengine.py`:

```powershell
# 1. Validate the 5-Workspace / 17-Container base schema and classify deposited Fabric items
python FWengine.py fabric --classify fabric_workspaces/

# 2. Audit repository or workspace against F8 capacity rules
python FWengine.py fabric --audit fabric_workspaces/

# 3. Apply automated F8 code remediation to PySpark notebooks
python FWengine.py fabric --remediate fabric_workspaces/

# 4. Automatically route any Fabric item or file into its canonical base container folder
python FWengine.py route <item_path> --move

# 5. Compile atomic context pack (<220 tokens) for AI agent pair programming
python FWengine.py context --pack fabric_workspaces/ws_silver_transform/notebooks --tier 1a

# 6. Full idempotent repository reconciliation (topology, beacons, satellite)
python FWengine.py reconcile
python FWengine.py reconcile --check
```

---

## 6. Antigravity AI Agent Protocol

iDirectoryFabric integrates seamlessly with **Antigravity** through specialized skills and context engineering profiles:

- **Skill Activation:** Invoke `/fabric` in Antigravity chat to trigger base schema validation, CU audits, and Medallion routing.
- **Context Preservation:** Atomic context packs (`Tier 1A`) ensure agents edit complex PySpark notebooks or TMDL files without loading extraneous datasets or burning context window tokens.
- **DNA Vector:** The architectural vector `01_seed/seed-idirectoryfabric-master.md` serves as the infallible reference for system design, folder contracts, and capacity limits.

---

## 7. Mathematical Formulation & Token Bounds

Context compilation latency $T_{\text{pack}}$ and token consumption $\Theta$ satisfy:

$$\Theta(\text{Tier 1A}) \le 220\text{ tokens}, \quad \Theta(\text{Tier 1B}) \le 800\text{ tokens}$$

Topological integrity is verified by the cryptographic SHA-256 fingerprint:

$$\text{topology\_hash} = \mathcal{H}_{\text{SHA256}}\left(\bigoplus_{i=1}^{N} \text{node\_path}_i \parallel \text{node\_mtime}_i \parallel \text{beacon\_hash}_i\right)$$

---

## 8. License & Authorship

- **Architecture & Origin:** Designed by **Gravity HyperScale Thinking**.
- **Blueprint Scope:** Universal Base Directory Schema for **Microsoft Fabric Git Integration**.
- **License:** MIT License. See [LICENSE](LICENSE) for terms.
