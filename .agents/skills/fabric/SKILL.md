---
name: Fabric
description: "Gobernanza de Esquema de Directorio Base Universal, optimización para capacidad F8, mapeo a Arquitectura Medallón y remediación de código en repositorios y workspaces de Microsoft Fabric. Usar /fabric en Antigravity o $fabric en Codex."
metadata:
  version: "6.0.0"
---

# Fabric: Universal Base Directory Schema, F8 Optimization & Medallion Governance Engine

Skill especializada para gobernanza agéntica, ruteo y validación de repositorios basados en el **Esquema de Directorio Base Universal (`iDirectoryFabric`)** vinculados a workspaces de **Microsoft Fabric Git Integration**.

## Cuándo activar esta Skill
- Cuando el usuario mencione **Microsoft Fabric**, **OneLake**, **Lakehouse**, **Warehouse**, **Data Pipelines**, **Notebooks de PySpark en Fabric**, **Modelos Semánticos Direct Lake (TMDL)**, **Reportes Power BI (PBIR)** o la capacidad **F8**.
- Cuando se requiera validar o estructurar el **Esquema de Directorio Base** (5 Workspaces Medallón y 17 carpetas contenedoras gobernadas) o enrutar nuevos artefactos de Fabric hacia su carpeta correspondiente.
- Cuando se necesite **auditar o remediar código** para evitar *throttling*, *Interactive Delay* o *Background Rejection* por sobreconsumo de CUs en Fabric F8.

## Esquema de Directorio Base (`fabric_workspaces/`)

```text
fabric_workspaces/
├── ws_core_governance/                # environments/, libraries/, notebooks/
├── ws_bronze_ingest/                  # lakehouses/, pipelines/, dataflows/, eventstreams/, notebooks/
├── ws_silver_transform/               # lakehouses/, notebooks/, pipelines/
├── ws_gold_analytics/                 # lakehouses/, warehouses/, notebooks/, pipelines/
└── ws_bi_semantic/                    # semantic_models/ (TMDL), reports/ (PBIR/PBIP)
```

## Comandos Operacionales

Ejecuta desde la raíz del repositorio:

```powershell
# 1. Validar las 17 carpetas del esquema base y clasificar artefactos depositados
python FWengine.py fabric --classify [ruta]

# 2. Auditar código contra las 7 reglas de optimización de Capacidad F8
python FWengine.py fabric --audit [ruta]

# 3. Aplicar remediación automática a notebooks PySpark (V-Order, 8 shuffle partitions)
python FWengine.py fabric --remediate [ruta]

# 4. Enrutar automáticamente un nuevo artefacto Fabric a su carpeta contenedora base
python FWengine.py route <ruta_artefacto> --move

# 5. Empaquetar contexto focalizado Tier 1A (<220 tokens) de un contenedor o artefacto Fabric
python FWengine.py context --pack <ruta_objetivo> --tier 1a

# 6. Reconciliar topología y sincronizar satélite tras cambios en workspaces
python FWengine.py reconcile
```

## Catálogo de Reglas y Directivas de Ingeniería para F8

1. **`[RULE-F8-01]` V-Order Parquet:** Asegurar siempre `spark.conf.set("spark.sql.parquet.vorder.enabled", "true")` y `.option("parquet.vorder.enabled", "true")` en escrituras Delta para posibilitar lectura directa sub-segundo en Direct Lake.
2. **`[RULE-F8-02]` Liquid Clustering:** En OneLake, prohibir `partitionBy()` con alta cardinalidad (>100 particiones) que genera tormentas de archivos pequeños (<1 MB). Reemplazar por Liquid Clustering (`CLUSTER BY`).
3. **`[RULE-F8-03]` Collect Guard:** Prohibido usar `df.collect()` o `.toPandas()` en notebooks productivos; satura los 16 vCores del pool F8 y causa OOM en el driver.
4. **`[RULE-F8-04]` Shuffle Partitions (4 a 8):** El valor por defecto de Spark (200) genera miles de micro-tareas que colapsan el scheduler en 16 vCores. Configurar `spark.conf.set("spark.sql.shuffle.partitions", "8")`.
5. **`[RULE-F8-05]` Mantenimiento Delta:** Programar `OPTIMIZE` y `VACUUM ... RETAIN 168 HOURS` semanalmente en `ws_core_governance/notebooks/`.
6. **`[RULE-F8-06]` Blindaje Direct Lake:** En `ws_bi_semantic/semantic_models/` (TMDL), prohibir columnas calculadas en DAX que causen degradación a *DirectQuery*. Pre-calcular en Silver/Gold.
7. **`[RULE-F8-07]` Suavizado de Pipelines:** En `pipelines/`, secuenciar actividades para no ejecutar más de 2 notebooks pesados concurrentemente, distribuyendo el cómputo en la ventana de suavizado de 24 horas.
