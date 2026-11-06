---
name: Fabric
description: "Gobernanza, optimización para capacidad F8, mapeo a Arquitectura Medallón y remediación de código en repositorios y workspaces de Microsoft Fabric. Usar /fabric en Antigravity o $fabric en Codex."
metadata:
  version: "6.0.0"
---

# Fabric: Microsoft Fabric Governance, F8 Optimization & Medallion Engine

Skill especializada para pair programming y gobernanza agéntica de repositorios vinculados a workspaces de **Microsoft Fabric**, con calibración prioritaria para la **Capacidad F8** (8 CUs / 16 vCores) de **Santolaya** (Chile).

## Cuándo activar esta Skill
- Cuando el usuario mencione **Microsoft Fabric**, **OneLake**, **Lakehouse**, **Warehouse**, **Data Pipelines**, **Notebooks de PySpark en Fabric**, **Modelos Semánticos Direct Lake**, o la capacidad **F8**.
- Cuando se requiera clasificar un repositorio o carpeta en la **Arquitectura Medallón** (Bronze -> Silver -> Gold -> Direct Lake BI).
- Cuando se necesite **auditar o remediar código** para evitar *throttling*, *Interactive Delay* o *Background Rejection* por sobreconsumo de CUs en Fabric F8.
- Para inspeccionar o estructurar repositorios compatibles con **Microsoft Fabric Git Integration** (`.platform`, `.Lakehouse`, `.Notebook`, `.DataPipeline`, `.Warehouse`, `.SemanticModel`, `.Report`, `.Environment`).

## Comandos Operacionales

Ejecuta desde la raíz del repositorio:

```powershell
# 1. Auditar código contra las 7 reglas de optimización de Capacidad F8
python FWengine.py fabric --audit [ruta]

# 2. Clasificar artefactos de Fabric en capas Medallón
python FWengine.py fabric --classify [ruta]

# 3. Aplicar remediación automática a notebooks PySpark (V-Order, 8 shuffle partitions)
python FWengine.py fabric --remediate [ruta]

# 4. Empaquetar contexto focalizado Tier 1A (<220 tokens) de un artefacto Fabric
python FWengine.py context --pack <ruta_artefacto> --tier 1a

# 5. Reconciliar topología y sincronizar satélite tras cambios en workspaces
python FWengine.py reconcile
```

## Catálogo de Reglas y Directivas de Ingeniería para F8

1. **`[RULE-F8-01]` V-Order Parquet:** Asegurar siempre `spark.conf.set("spark.sql.parquet.vorder.enabled", "true")` y `.option("parquet.vorder.enabled", "true")` en escrituras Delta para posibilitar lectura directa sub-segundo en Direct Lake.
2. **`[RULE-F8-02]` Liquid Clustering:** En OneLake, prohibir `partitionBy()` con alta cardinalidad (>100 particiones) que genera tormentas de archivos pequeños (<1 MB). Reemplazar por Liquid Clustering: `CLUSTER BY (id_obra, fecha)`.
3. **`[RULE-F8-03]` Collect Guard:** Prohibido usar `df.collect()` o `.toPandas()` en notebooks productivos; satura los 16 vCores del pool F8 y causa OOM en el driver.
4. **`[RULE-F8-04]` Shuffle Partitions (4 a 8):** El valor por defecto de Spark (200) genera miles de micro-tareas que colapsan el scheduler en 16 vCores. Configurar `spark.conf.set("spark.sql.shuffle.partitions", "8")`.
5. **`[RULE-F8-05]` Mantenimiento Delta:** Programar `OPTIMIZE` y `VACUUM ... RETAIN 168 HOURS` semanalmente en cada Lakehouse.
6. **`[RULE-F8-06]` Blindaje Direct Lake:** En modelos semánticos TMDL, prohibir columnas calculadas en DAX que causen degradación a *DirectQuery* (lo cual saturaría de inmediato los 8 CUs). Pre-calcular en Silver/Gold.
7. **`[RULE-F8-07]` Suavizado de Pipelines:** En Data Factory, secuenciar actividades para no ejecutar más de 2 notebooks pesados concurrentemente, distribuyendo el cómputo en la ventana de suavizado de 24 horas.

## Flujo de Trabajo Agéntico Recomendado
1. **Inspección Mínima:** Inicia con `python FWengine.py context --pack <target> --tier 1a` para cargar solo el beacon y firmas esenciales.
2. **Auditoría Previa:** Corre `python FWengine.py fabric --audit <target>` para identificar violaciones de CUs antes de editar.
3. **Edición Quirúrgica:** Modifica el código preservando los comentarios y el bloque de optimización F8.
4. **Remediación / Verificación:** Ejecuta `python FWengine.py fabric --audit <target>` y finaliza con `python FWengine.py reconcile`.

