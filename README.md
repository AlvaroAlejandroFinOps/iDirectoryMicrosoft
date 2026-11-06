![iDirectoryFabric Architecture](iDirectory.png)

**iDirectoryFabric v6.0.0.** Enterprise Governance, Context Engineering & Automated Remediation Framework for Microsoft Fabric (Capacity F8) — Santolaya (Chile).
<!-- ICONTEXT-V6:RELEASE -->

# iDirectoryFabric: The Microsoft Fabric Context Engineering & Governance Standard by Gravity HyperScale Thinking

**Language:** [English](README.md) | [Español](README_ES.md)

[![Standard](https://img.shields.io/badge/Standard-Enterprise%20Paper--Grade%20v6.0-2b2b2b?style=flat-square)](#)
[![Fabric Capacity](https://img.shields.io/badge/Fabric%20Capacity-F8%20%288%20CUs%20%7C%2016%20vCores%29-0078d4?style=flat-square)](#3-microsoft-fabric-capacity-f8-governance--cu-economics)
[![Client](https://img.shields.io/badge/Enterprise-Santolaya%20%28Chile%29-107c41?style=flat-square)](#1-executive-abstract)
[![Architecture](https://img.shields.io/badge/Architecture-OneLake%20Medallion-008272?style=flat-square)](#2-system-architecture--medallion-lineage)
[![Direct Lake](https://img.shields.io/badge/Power%20BI-Direct%20Lake%20Guardrails-f2c811?style=flat-square)](#4-f8-optimization--remediation-engine)
[![Engine](https://img.shields.io/badge/Engine-FWengine.py-1a1a1a?style=flat-square)](#5-cli-interface--operational-commands)
[![License](https://img.shields.io/badge/License-MIT-1a1a1a?style=flat-square)](LICENSE)

---

## 1. Executive Abstract

**iDirectoryFabric**, originated and engineered by **Gravity HyperScale Thinking** and custom-calibrated for **Santolaya** (Constructora e Inmobiliaria Santolaya, Santiago, Chile), establishes a deterministic control-plane and context engineering architecture to govern enterprise workloads across **Microsoft Fabric**.

Modern real estate and civil engineering enterprises operate highly interconnected data flows spanning on-premise transactional systems, cloud ERPs, procurement platforms (Iconstruye), financial accounting (SAP / Softland), CRM sales funnels (PlanOK / Salesforce), and construction site progress metrics. Operating these workloads on an elastic but constrained cloud capacity such as **Microsoft Fabric F8** (providing 8 Capacity Units, equivalent to a ~16 vCore Spark burst pool) introduces acute operational risks:
1. **Interactive Delay & Rejection:** Unoptimized DAX measures or semantic models that exceed F8 memory thresholds (~8–10 GB) involuntarily fall back from Direct Lake to DirectQuery, translating visual clicks into hundreds of T-SQL queries against the SQL Analytics Endpoint and instantly exhausting the 8 CUs.
2. **Background Throttling:** Simultaneous execution of uncurated PySpark notebooks or unpartitioned copy activities triggers Fabric's 24-hour background smoothing mechanism. When usage exceeds 100% of capacity over the smoothing window, Fabric initiates *Background Rejection*, summarily terminating production pipelines.
3. **Small File Storms in OneLake:** Hive-style multi-column partitioning (`partitionBy`) across high-cardinality keys generates millions of sub-megabyte Parquet files, overwhelming driver metadata caches and inducing severe driver Out-of-Memory (OOM) failures.

To eliminate these vulnerabilities, **iDirectoryFabric v6.0** introduces a zero-dependency governance kernel (`FWengine.py`), an automated **Medallion Architecture Classifier**, an **F8 Static & Dynamic Remediation Engine**, and an **Adaptive Context Engineering Plane** that enables autonomous coding agents (Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex) to inspect, repair, and deploy Fabric items with bounded token consumption ($< 220\text{ tokens}$ in Tier 1A).

---

## 2. System Architecture & Medallion Lineage

iDirectoryFabric organizes repositories connected via **Microsoft Fabric Git Integration** into a multi-workspace structure respecting strict Medallion separation of concerns:

```text
+----------------------------------------------------------------------------------------------------+
|                                    SANTOLAYA SOURCE SYSTEMS                                        |
|              (Procurement / Subcontracts / ERP / Real Estate Sales / Construction Works)           |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| BRONZE LAYER: ws_bronze_ingest (Lakehouse Bronze / Data Pipelines / Shortcuts)                     |
| - Immutable, append-only, schema-on-read raw ingestion in OneLake.                                 |
| - Mandatory audit lineage: _ingested_at, _source_system, _batch_id.                                |
| - Compute: Lightweight Copy Activities avoiding redundant Spark cluster initialization.            |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| SILVER LAYER: ws_silver_transform (Lakehouse Silver / Curated PySpark Notebooks)                   |
| - Deduplication, entity resolution, Chilean RUT validation (Modulo 11 verification).               |
| - Currency normalization (UF - Unidad de Fomento and CLP daily conversion).                        |
| - Delta Lake storage optimized with V-Order = True and Liquid Clustering (CLUSTER BY id_obra).     |
| - Shuffle partitions capped at 8 to eliminate scheduler thrashing across 16 vCores.                |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| GOLD LAYER: ws_gold_analytics (Fabric Warehouse / Lakehouse Gold / Kimball Star Schema)            |
| - Dimensional analytics star schema: fact_costos_obra, fact_avance_fisico,                          |
|   fact_ventas_inmobiliarias, dim_proyecto, dim_obra, dim_contratista, dim_tiempo.                  |
| - Pre-aggregated Delta tables ensuring sub-second analytical response times.                       |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| BI SEMANTIC LAYER: ws_bi_semantic (Direct Lake Semantic Models TMDL / Power BI PBIR)              |
| - Pure DIRECT LAKE semantic models bound directly to OneLake Delta tables.                         |
| - Strict memory ceiling: Model memory < 8 GB (F8 physical guardrail).                              |
| - Zero calculated DAX columns: All derived metrics pre-computed upstream in Silver/Gold.           |
| - Executive project dashboards stored in human-readable Power BI Enhanced Report format (PBIR).    |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
```

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

iDirectoryFabric injects deterministic Spark pool configurations into `.Environment/Setting/Spark/compute.json`:
- **Node Allocation:** Min 1 node, Max 2 nodes (prevents runaway autoscale charges).
- **Auto-pause Delay:** 2 minutes (eliminates idle cluster burn).
- **Dynamic Optimization:** Auto-tune and `optimizeWrite` enabled by default.

---

## 4. F8 Optimization & Remediation Engine

The remediation engine detects and resolves 7 systemic performance anti-patterns:

```text
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
| Rule ID     | Anti-Pattern Detected                | Severity | Automated Remediation                   |
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
| RULE-F8-01  | Parquet write without V-Order        | HIGH     | Injects parquet.vorder.enabled = true    |
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
# 1. Audit repository or workspace against F8 capacity rules
python FWengine.py fabric --audit fabric_workspaces/

# 2. Classify all Fabric Git items into Medallion tiers
python FWengine.py fabric --classify fabric_workspaces/

# 3. Apply automated F8 code remediation to PySpark notebooks
python FWengine.py fabric --remediate fabric_workspaces/

# 4. Compile atomic context pack (<220 tokens) for AI agent pair programming
python FWengine.py context --pack fabric_workspaces/ws_silver_transform --tier 1a

# 5. Full idempotent repository reconciliation (topology, beacons, satellite)
python FWengine.py reconcile
python FWengine.py reconcile --check
```

---

## 6. Antigravity AI Agent Protocol

iDirectoryFabric integrates seamlessly with **Antigravity** through specialized skills and context engineering profiles:

- **Skill Activation:** Invoke `/fabric` in Antigravity chat to trigger Fabric governance, CU audits, and Medallion classification.
- **Context Preservation:** Atomic context packs (`Tier 1A`) ensure agents edit complex PySpark notebooks or TMDL files without loading extraneous datasets or burning context window tokens.
- **DNA Vector:** The architectural vector `01_seed/seed-idirectory-master.md` serves as the infallible reference for system design, business rules, and capacity limits.

---

## 7. Mathematical Formulation & Token Bounds

Context compilation latency $T_{\text{pack}}$ and token consumption $\Theta$ satisfy:

$$\Theta(\text{Tier 1A}) \le 220\text{ tokens}, \quad \Theta(\text{Tier 1B}) \le 800\text{ tokens}$$

Topological integrity is verified by the cryptographic SHA-256 fingerprint:

$$\text{topology\_hash} = \mathcal{H}_{\text{SHA256}}\left(\bigoplus_{i=1}^{N} \text{node\_path}_i \parallel \text{node\_mtime}_i \parallel \text{beacon\_hash}_i\right)$$

---

## 8. License & Authorship

- **Architecture & Origin:** Designed by **Gravity HyperScale Thinking**.
- **Enterprise Calibration:** Tailored for **Santolaya** (Constructora e Inmobiliaria, Chile).
- **License:** MIT License. See [LICENSE](LICENSE) for terms.
