<SEED_ARCHITECTURAL_VECTOR version="6.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: iDirectoryFabric — Microsoft Fabric F8 (Santolaya)

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — GEMINI / ANTIGRAVITY / CLAUDE / CODEX]:**
> 1. **Naturaleza del Artefacto:** Este documento es el **Vector Arquitectónico y Memoria Técnica Primaria (ThinkingSeed Master v6.0)** con `contains_source_code="false"`. **NO es el repositorio completo de código fuente**. La ausencia deliberada de código crudo es una invariante de Context Engineering para concentrar densidad semántica y preservar la ventana de contexto del agente.
> 2. **Perfil de Cómputo Objetivo:** **Microsoft Fabric Capacidad F8** (8 Capacity Units = 16 vCores equivalentes). Aplica smoothing de 24h para background jobs (PySpark, Pipelines) y 5min para operaciones interactivas (Power BI Direct Lake). Se deben respetar los límites de throttling para prevenir *Interactive Delay* y *Background Rejection*.
> 3. **Dominio Corporativo:** **Santolaya** (Constructora e Inmobiliaria Santolaya, Chile). Operaciones de proyectos de edificación, desarrollo inmobiliario, control de costos, gestión de compras y subcontratos, y flujos financieros (UF / CLP / RUT chileno).
> 4. **Modo de Razonamiento:** Opera como **Arquitecto Principal de Datos y Gobernador de Capacidad Fabric**. Utiliza las firmas simbólicas (Sección 4), el catálogo de reglas F8 (Sección 5) y la superficie de tensión (Sección 7) para auditar código, detectar cuellos de botella de CUs y aplicar remediaciones deterministas.

## Seed Changelog
- `2026-11-06 (v6.0-Fabric)`: Reingeniería integral de iDirectory orientada al gobierno de repositorios y workspaces de Microsoft Fabric (Capacidad F8) para la compañía chilena Santolaya. Incorporación de: (1) Mapeo nativo a Arquitectura Medallón (Bronze, Silver, Gold, Direct Lake); (2) Motor de optimización y remediación de código PySpark/T-SQL/DAX; (3) Gobernanza multi-workspace con soporte para Microsoft Fabric Git Integration (`.platform`, `.Lakehouse`, `.Notebook`, `.DataPipeline`, `.Warehouse`, `.SemanticModel`, `.Report`, `.Environment`); (4) Guardrails de memoria para Direct Lake (<8 GB) y Liquid Clustering en Delta Lake; (5) Skill especializada `Fabric` para agentes de IA en Antigravity.
- `2026-10-31 (v6.0)`: Runtime versionado, evidencia incremental por contenido, skills portables, consultas sin escritura y actualización semántica por el agente actual.
- `2026-10-28 (v5.0)`: Protocolo de federación de contexto L0-L3, bus federado `icontext_bus.json` e índice AST en `contracts_ast.json`.

---

## 0. IDENTIDAD, METADATOS Y CONTRATO DEL RECEPTOR

```yaml
seed_schema_version: "6.0"
project_name: "iDirectoryFabric"
target_platform: "Microsoft Fabric"
target_capacity: "F8 (8 Capacity Units / ~16 vCores Spark Burst)"
client: "Santolaya (Constructora e Inmobiliaria Santolaya — Chile)"
project_type: "fabric_context_engineering_and_governance_framework"
repository_mode: "fabric_multi_workspace_monorepo"
generated_at: "2026-11-06T08:35:00.000000+00:00"
generated_by: "Antigravity / iDirectoryFabric v6.0 Reengineering"
repository_root: "./"
git_branch: "master"
analysis_mode: "static+fabric_git+validated"
coverage_level: "high"
compliance_frameworks:
  - "Microsoft Fabric Git Integration Standard"
  - "Delta Lake Liquid Clustering Protocol"
  - "Power BI Direct Lake Memory Guardrails"
  - "Chilean Commercial & Tax Standards (SII, RUT, UF/CLP)"
```

### 0.1 Instrucciones para el modelo receptor
1. **Contexto Pasivo y Quirúrgico:** No generes código no solicitado ni modifiques archivos fuera del ámbito de la tarea activa. Utiliza este documento como fuente canónica de verdad (*Ground Truth*).
2. **Invariante de Cómputo F8:** Toda propuesta de ingeniería debe diseñarse para operar dentro del presupuesto estricto de 8 CUs. Prohibido sugerir pipelines con más de 2 notebooks paralelos pesados o escaneos completos no particionados en PySpark.
3. **Respeto a la Arquitectura Medallón:** Los datos crudos residen exclusivamente en Bronze (Lakehouse append-only); la lógica de negocio y curación en Silver (Delta Lake con Liquid Clustering y V-Order); los modelos analíticos dimensionales (Kimball) en Gold (Warehouse o Delta Tables); y la explotación semántica en Direct Lake.
4. **Portabilidad de Rutas POSIX:** Cita siempre rutas relativas normalizadas (`./fabric_workspaces/...`) con separador `/`. Prohibidas rutas absolutas con `file:///` o barras invertidas `\`.

---

## 1. RESUMEN EJECUTIVO Y ALCANCE

**iDirectoryFabric v6.0**, concebido por **Gravity HyperScale Thinking** y adaptado para **Santolaya**, provee un plano de control unificado y determinista para gobernar el ecosistema de workspaces y repositorios sincronizados con **Microsoft Fabric**.

En organizaciones con capacidades elásticas pero acotadas como **Fabric F8** (8 CUs = $8 \times 2 = 16\text{ vCores}$), el desarrollo descuidado de pipelines y notebooks induce picos instantáneos de consumo que activan el *smoothing penalty* de 24 horas. Esto causa la degradación progresiva de la capacidad:
1. *Interactive Delay:* Retraso en la renderización de informes Power BI corporativos para gerentes de proyectos y ejecutivos de Santolaya.
2. *Interactive Rejection:* Fallas críticas de visuales en Power BI por agotamiento de CUs interactivos.
3. *Background Rejection:* Aborto automático de pipelines de ingesta (Data Factory) y jobs de procesamiento (PySpark).

**iDirectoryFabric v6.0** erradica este riesgo mediante:
- **Clasificador Medallón Inteligente:** Detecta y asigna automáticamente artefactos de Fabric (Lakehouses, Warehouses, Notebooks, Pipelines, Modelos Semánticos) a sus respectivas capas (Bronze -> Silver -> Gold -> Direct Lake).
- **Motor de Remediación F8:** Linter estático y parcheo automático de código PySpark, T-SQL y DAX para asegurar compresión V-Order, Liquid Clustering (`CLUSTER BY`), ajuste de particiones de shuffle (4 a 8 en lugar de las 200 por defecto) y eliminación de llamadas letales a `.collect()`.
- **Topología Multi-Workspace Git:** Estructura modular `fabric_workspaces/` que permite vincular workspaces independientes o repositorios unificados de GitHub con Microsoft Fabric Git Integration.
- **Plano de Contexto para Agentes de IA (Antigravity):** Micro-balizas contextuales (`.context.yaml`) que permiten a los agentes de Antigravity operar con presupuestos atómicos ultra-bajos (<220 tokens en Tier 1A).

---

## 2. MAPA DE DOMINIOS Y LINAJE MEDALLÓN FABRIC

```text
+----------------------------------------------------------------------------------------------------+
|                                    SISTEMAS FUENTE SANTOLAYA                                       |
|                  (Compras / Subcontratos / ERP Contable / Ventas Inmobiliarias / Obras)            |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA BRONZE: ws_bronze_ingest (Lakehouse Bronze / Data Pipelines / Shortcuts)                      |
| - Ingesta raw inmutable, append-only, schema-on-read.                                              |
| - Metadatos de auditoría obligatorios: _ingested_at, _source_system, _batch_id.                    |
| - Cómputo: Copy Activity optimizada sin levantar clusters Spark innecesarios.                      |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA SILVER: ws_silver_transform (Lakehouse Silver / Curated PySpark Notebooks)                    |
| - Limpieza, deduplicación, validación de RUT chileno con algoritmo Módulo 11.                     |
| - Conversión y normalización de montos en UF (Unidad de Fomento) y CLP según fecha contable.       |
| - Tablas Delta Lake optimizadas con V-Order = True y Liquid Clustering (CLUSTER BY id_obra, fecha).|
| - Particiones de shuffle acotadas a 4-8 para evitar desbordar los 16 vCores de F8.                 |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA GOLD: ws_gold_analytics (Fabric Warehouse / Lakehouse Gold / Kimball Star Schema)             |
| - Modelo dimensional de alta performance: Fact_Costos_Obra, Fact_Avance_Fisico,                   |
|   Fact_Ventas_Inmobiliarias, Dim_Proyecto, Dim_Obra, Dim_Contratista, Dim_Tiempo.                 |
| - Pre-agregaciones deterministas para garantizar consultas analíticas sub-segundo.                 |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA BI SEMANTIC: ws_bi_semantic (Semantic Models Direct Lake / Power BI Reports PBIR)             |
| - Modelos semánticos en modo DIRECT LAKE puro contra OneLake Delta tables.                         |
| - Salvaguarda estricta: Memoria de modelo < 8 GB (Límite F8).                                      |
| - Prohibidas columnas calculadas en DAX que fuercen degradación a DirectQuery.                     |
| - Reportes de avance y márgenes de proyectos en formato PBIR con control de versiones Git.         |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 3. ESPECIFICACIÓN DE CAPACIDAD F8 Y GOBERNANZA DE CÓMPUTO

### 3.1 Presupuesto de CUs y Concurrencia
| Dimensión | Límite Capacidad F8 | Política iDirectoryFabric |
|---|---|---|
| **Capacity Units (CUs)** | 8 CUs | Techo operacional estricto |
| **vCores Spark (Pool)** | ~16 vCores máximos | 1 Pool mediano (4 nodos) ó 2 pools pequeños (2 nodos c/u) |
| **Smoothing Interactivo** | 5 minutos | Monitoreo de visuales DAX para evitar queries DirectQuery |
| **Smoothing Background** | 24 horas | Secuenciación escalonada de notebooks y pipelines nocturnos |
| **Memoria Direct Lake** | 8 GB - 10 GB | Verificación previa de cardinalidad y tamaño de tablas Delta |
| **Auto-pause de Spark** | 2 minutos por defecto | Inyección en `.Environment/Setting/Spark/compute.json` |

---

## 4. CONTRATOS SIMBÓLICOS Y FIRMAS DE GOBERNANZA

### 4.1 Núcleo de Gobernanza: FWengine.py y src/fabric/

El motor central opera con **100% Python Standard Library** (`Zero-Dependency`), exponiendo la suite de métodos de inspección, ruteo, reconciliación y remediación:

```python
# SEED SECTION: 4.1 FWengine.py Core Symbolic Contracts
class FWengine:
    @staticmethod
    def reconcile_repository(root_path: Path, check_only: bool = False) -> List[str]:
        """Ejecuta la reconciliación integral de topología, balizas, satélite y bus federado."""
        ...

    @staticmethod
    def audit_repository(root_path: Path, fix: bool = False) -> bool:
        """Audita el cumplimiento de normas de nomenclatura, micro-balizas y contratos AST."""
        ...

    @staticmethod
    def build_context_pack(root_path: Path, target_dir: str, tier: str = "1a") -> Dict[str, Any]:
        """Genera el paquete de contexto atómico (<220 tokens en Tier 1A) para agentes de IA."""
        ...

    @staticmethod
    def manage_checkpoint(root_path: Path, action: str, **kwargs) -> Dict[str, Any]:
        """Administra el estado de continuidad atencional en .context/checkpoint.json."""
        ...

class FabricGovernor:
    @staticmethod
    def classify_fabric_item(item_path: Path) -> str:
        """Analiza la estructura .platform y determina la capa Medallón (Bronze/Silver/Gold/BI)."""
        ...

    @staticmethod
    def audit_f8_compliance(workspace_path: Path) -> List[Dict[str, Any]]:
        """Verifica el cumplimiento de las 7 reglas de optimización de capacidad F8."""
        ...

    @staticmethod
    def remediate_pyspark_notebook(notebook_path: Path) -> bool:
        """Aplica remediaciones automáticas de V-Order, liquid clustering y shuffle partitions."""
        ...
```

---

## 5. CATÁLOGO DE REGLAS DE OPTIMIZACIÓN Y REMEDIACIÓN F8

- **`[RULE-F8-01]` V-Order Parquet Optimization:** Toda escritura de tabla Delta en PySpark debe incluir compresión V-Order (`spark.conf.set("spark.sql.parquet.vorder.enabled", "true")` y `parquet.vorder.enabled=true`) para posibilitar lectura directa en Direct Lake sin recodificación.
- **`[RULE-F8-02]` Liquid Clustering Obligatorio:** Se prohíbe el particionamiento jerárquico tradicional (`partitionBy`) con alta cardinalidad (>100 particiones) que genera tormentas de archivos pequeños (<1 MB) en OneLake. Debe utilizarse `CLUSTER BY (id_obra, fecha)`.
- **`[RULE-F8-03]` Guardián de Memoria de Driver (`Collect Guard`):** Se bloquea el uso de `df.collect()`, `.toPandas()` y llamadas desmedidas en notebooks productivos, reemplazándolos por agregaciones distribuidas o escritura directa en Delta.
- **`[RULE-F8-04]` Redimensión de Shuffle Partitions:** El parámetro `spark.sql.shuffle.partitions` debe reducirse de su valor por defecto (200) a un rango entre 4 y 8, proporcional a los 16 vCores disponibles en F8, eliminando la sobrecarga de scheduling.
- **`[RULE-F8-05]` Mantenimiento Preventivo Delta:** Todo Lakehouse productivo debe contar con jobs programados de `OPTIMIZE` y `VACUUM` (retención de 7 días) para impedir la degradación del log de transacciones Delta.
- **`[RULE-F8-06]` Blindaje Direct Lake (No DirectQuery Fallback):** Prohibidas las columnas calculadas complejas en DAX dentro de modelos semánticos en Direct Lake. Toda lógica derivativa debe pre-calcularse en la capa Silver o Gold.
- **`[RULE-F8-07]` Orquestación Suavizada de Pipelines:** En Data Factory, se prohíbe disparar más de 2 actividades de notebooks pesados en paralelo sobre la capacidad F8. Se deben usar dependencias secuenciales para distribuir el consumo de CUs en la ventana de suavizado de 24 horas.

---

## 6. TOPOLOGÍA DE WORKSPACES Y CONTROL GIT

El estándar de directorios para repositorios vinculados a Microsoft Fabric Git Integration se organiza de la siguiente manera:

```text
fabric_workspaces/
├── ws_core_governance/           # Entornos Spark F8, librerías compartidas (validación RUT/UF)
├── ws_bronze_ingest/             # Ingesta cruda inmutable (Lakehouse Bronze, Data Pipelines)
├── ws_silver_transform/          # Curación PySpark, Liquid Clustering, V-Order (Lakehouse Silver)
├── ws_gold_analytics/            # Almacén analítico dimensional Kimball (Fabric Warehouse)
└── ws_bi_semantic/               # Modelos semánticos Direct Lake (TMDL) y Reportes (PBIR)
```

Cada artefacto de Fabric se compone de su carpeta tipada (ej. `*.Lakehouse`, `*.Notebook`, `*.DataPipeline`, `*.Warehouse`, `*.SemanticModel`, `*.Report`) y su archivo descriptor `.platform`.

---

## 7. SUPERFICIE DE TENSIÓN Y RIESGOS DE CAPACIDAD

1. **Riesgo de Degradación a DirectQuery:** Si un modelo semántico excede los 8 GB o contiene DAX no soportado, Fabric conmuta a DirectQuery, saturando los 8 CUs en minutos. *Mitigación:* Auditar TMDL con `FabricGovernor.audit_f8_compliance()`.
2. **Tormenta de Archivos Pequeños en OneLake:** Ingestas frecuentes de archivos CSV/JSON en Bronze generan latencia extrema de metadatos. *Mitigación:* Aplicar `OPTIMIZE` y compactación automática en Silver.
3. **Pico de Concurrencia Matutino:** Inicio simultáneo de pipelines a las 08:00 AM activando throttling interactivo durante el horario comercial de Santolaya. *Mitigación:* Escalonar triggers nocturnos entre las 02:00 y las 05:00 AM.
4. **Discrepancias en Conversión de UF:** Cálculos de costos desfasados por variación diaria del valor de la UF. *Mitigación:* Centralizar tabla de tipo de cambio oficial en Silver con linaje verificado.

---

## 8. INVARIANTES ARQUITECTÓNICOS

- **`[INV-01]` Zero-Dependency Kernel:** El motor `FWengine.py` opera exclusivamente sobre la librería estándar de Python 3.10+.
- **`[INV-02]` Prohibición de Escaneo Ciego:** Los agentes de IA nunca exploran el repositorio mediante barridos recursivos descontrolados; emplean `context --pack` o `map --slice`.
- **`[INV-03]` Poda Estricta (`crawl: false`):** Las ramas de datos pesados (`data/raw`, `data/processed`, `logs`) están completamente vetadas para la ingesta en contexto de LLM.
- **`[INV-04]` Sincronización Determinista por SHA-256:** Todo cambio en balizas o topología debe cerrarse mediante `python FWengine.py reconcile`.
- **`[INV-05]` Aislamiento Medallón:** Los pipelines de ingesta nunca escriben directamente en Silver o Gold sin transitar por Bronze.
- **`[INV-06]` Topología All-Lowercase:** Los directorios del repositorio de gobernanza deben mantener nomenclatura en minúsculas.
- **`[INV-07]` Presupuesto Atómico Tier 1A:** La vista focalizada de cualquier directorio o archivo no debe exceder 220 tokens.
- **`[INV-08]` Portabilidad de Rutas POSIX:** Se prohíben rutas absolutas locales o separadores invertidos en contratos y documentación.
- **`[INV-09]` V-Order Obligatorio en OneLake:** Ningún archivo Parquet/Delta puede generarse en Silver/Gold sin el flag de V-Order activo.
- **`[INV-10]` Direct Lake Non-Fallback:** Los modelos semánticos en `ws_bi_semantic` no deben contener expresiones que fuercen DirectQuery.

</SEED_ARCHITECTURAL_VECTOR>

