<SEED_ARCHITECTURAL_VECTOR version="6.0" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: iDirectoryFabric — Microsoft Fabric F8 (Santolaya)

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — GEMINI / ANTIGRAVITY / CLAUDE / CODEX]:**
> 1. **Naturaleza del Artefacto:** Este documento es el **Vector Arquitectónico y Memoria Técnica Primaria (ThinkingSeed Master v6.0)** con `contains_source_code="false"`. La ausencia deliberada de código crudo es una invariante para concentrar densidad semántica y preservar la ventana de contexto del agente.
> 2. **Perfil de Cómputo Objetivo:** **Microsoft Fabric Capacidad F8** (8 Capacity Units = ~16 vCores Spark Pool). Aplica smoothing de 24h para background jobs (PySpark, Pipelines) y 5min para operaciones interactivas (Power BI Direct Lake).
> 3. **Dominio Corporativo:** **Santolaya** (Constructora e Inmobiliaria Santolaya — Chile). Control de costos de edificación, desarrollo inmobiliario, compras y subcontratación, y flujos financieros en UF y CLP con RUT chileno.

## Seed Changelog
- `2026-11-06 (v6.0-Fabric)`: Reingeniería integral orientada al gobierno de repositorios y workspaces de Microsoft Fabric (Capacidad F8) para la compañía chilena Santolaya. Mapeo Medallón, motor de optimización/remediación F8, estructura multi-workspace Git Integration y skill Fabric para Antigravity.
- `2026-10-31 (v6.0)`: Runtime versionado, evidencia incremental por contenido, skills portables, consultas sin escritura y actualización semántica por el agente actual.

---

## 0. IDENTIDAD, METADATOS Y CONTRATO DEL RECEPTOR

```yaml
seed_schema_version: "6.0"
project_name: "iDirectoryFabric"
target_platform: "Microsoft Fabric"
target_capacity: "F8 (8 Capacity Units / 16 vCores Spark Burst)"
client: "Santolaya (Constructora e Inmobiliaria Santolaya — Chile)"
project_type: "fabric_context_engineering_and_governance_framework"
repository_mode: "fabric_multi_workspace_monorepo"
generated_at: "2026-11-06T09:20:00+00:00"
generated_by: "Antigravity / iDirectoryFabric v6.0 Reengineering"
repository_root: "./"
analysis_mode: "static+fabric_git+validated"
coverage_level: "high"
```

### 0.1 Instrucciones para el modelo receptor
1. **Contexto Pasivo y Quirúrgico:** No generes código no solicitado ni modifiques archivos fuera del ámbito de la tarea activa. Utiliza este documento como fuente canónica de verdad (*Ground Truth*).
2. **Invariante de Cómputo F8:** Toda propuesta de ingeniería debe diseñarse para operar dentro del presupuesto estricto de 8 CUs. Prohibido sugerir pipelines con más de 2 notebooks paralelos pesados o escaneos completos no particionados en PySpark.
3. **Respeto a la Arquitectura Medallón:** Los datos crudos residen exclusivamente en Bronze (OneLake append-only); la lógica de negocio y curación en Silver (Delta Lake con Liquid Clustering y V-Order); los modelos analíticos dimensionales (Kimball) en Gold; y la explotación en Direct Lake.
4. **Portabilidad de Rutas POSIX:** Cita siempre rutas relativas normalizadas (`./fabric_workspaces/...`) con separador `/`. Prohibidas rutas absolutas o esquemas locales.

---

## 1. RESUMEN EJECUTIVO Y ALCANCE

**iDirectoryFabric v6.0**, concebido por **Gravity HyperScale Thinking** y adaptado para **Santolaya**, provee un plano de control unificado y determinista para gobernar el ecosistema de workspaces y repositorios sincronizados con **Microsoft Fabric**.
En organizaciones con capacidades elásticas pero acotadas como **Fabric F8** (8 CUs), el desarrollo descuidado de pipelines induce picos instantáneos que activan el *smoothing penalty* de 24 horas, provocando *Interactive Delay*, *Interactive Rejection* y *Background Rejection*.

iDirectoryFabric erradica este riesgo mediante:
- Clasificador Medallón Inteligente de artefactos de Fabric (Bronze, Silver, Gold, BI Semantic, Core Governance).
- Motor de Remediación F8 (Linter estático y parcheo de V-Order, Liquid Clustering y shuffle partitions).
- Topología Multi-Workspace Git Integration (`fabric_workspaces/`).
- Plano de Contexto para Agentes de IA en Antigravity con paquetes atómicos Tier 1A ($< 220\text{ tokens}$).

---

## 2. ARQUITECTURA, TOPOLOGÍA Y FRONTERAS MODULARES

El repositorio se organiza en fronteras modulares de alta ingeniería:

```text
fabric_workspaces/
├── ws_core_governance/  # Entornos Spark F8, librerías chilenas (RUT/UF)
├── ws_bronze_ingest/    # Ingesta cruda append-only (Lakehouse Bronze, Pipelines)
├── ws_silver_transform/ # Curación Delta, Liquid Clustering, V-Order (Lakehouse Silver)
├── ws_gold_analytics/   # Modelo dimensional Kimball Star Schema (Warehouse)
└── ws_bi_semantic/      # Modelos semánticos Direct Lake TMDL y reportes PBIR
```

Los módulos de gobernanza residen en `./src/core/` (motor central) y `./src/fabric/` (clasificador, linter y remediador).

---

## 3. FLUJOS DE EJECUCIÓN, ENTRY POINTS Y CICLO DE VIDA

1. **Flujo de Reconciliación e Idempotencia:** `python FWengine.py reconcile` audita la topología, normaliza nombres en minúsculas, aprovisiona balizas `.context.yaml` y sincroniza el satélite `.context/tree.json`.
2. **Flujo de Inspección Fabric:** `python FWengine.py fabric --classify` detecta artefactos y `python FWengine.py fabric --audit` evalúa las 7 reglas de capacidad F8.
3. **Flujo de Remediación:** `python FWengine.py fabric --remediate` aplica optimizaciones directas a notebooks.
4. **Ciclo de Vida Agéntico:** `python FWengine.py context --pack <dir> --tier 1a` compila el paquete de contexto atómico ($< 220\text{ tokens}$).

---

## 4. CONTRATOS SIMBÓLICOS, MODELO DE DATOS Y PERSISTENCIA

### 4.1 FWengine.py y contratos públicos

El plano de control expone los siguientes contratos simbólicos y métodos públicos verificados por el índice AST:

- **Contratos Core FWengine:**
  - `FWengine.py`: Script lanzador y punto de entrada compatible.
  - `MiniYAML`: Parser determinista zero-dependency para micro-balizas `.context.yaml`.
  - `atomic_write(path, data)`: Escritura atómica protegida contra corrupción en bloqueos I/O.
  - `audit_repository(root, fix)`: Audita violaciones topológicas, balizas y derivas satelitales.
  - `bounded(value, min_val, max_val)`: Acota valores numéricos dentro de presupuestos estrictos.
  - `build_ast_contracts_index(root, write_to_disk)`: Compila el índice de firmas AST de símbolos públicos.
  - `build_context_capsule(root, target)`: Compila cápsula autocontenida de contexto.
  - `build_context_pack(root, target_dir, tier)`: Genera el paquete de contexto Tier 1A / 1B.
  - `build_ecosystem_pack(root)`: Empaqueta telemetría unificada del ecosistema en $<650$ tokens.
  - `check_satellite_freshness(root)`: Detecta desincronizaciones entre el satélite y el sistema de archivos.
  - `compute_context_budget(root, include_pruned)`: Calcula el presupuesto de tokens por directorio gobernado.
  - `compute_node_fingerprint(dir_path)`: Calcula hash determinista O(delta) de 16 caracteres hexadecimales.
  - `compute_topology_hash(root)`: Calcula la huella SHA-256 inmutable de la topología del proyecto.
  - `contracts_index(root)`: Resuelve y retorna el catálogo consolidado de contratos.
  - `crawl_allowed(dir_path, meta)`: Determina si un directorio es explorable por agentes.
  - `digest(content)`: Genera hash criptográfico determinista de contenido textual.
  - `discover_unbeaconed_directories(root)`: Detecta carpetas huérfanas sin baliza `.context.yaml`.
  - `ensure_beacon_chain(path)`: Asegura la cadena jerárquica ininterrumpida de balizas.
  - `estimate_tokens_v4(item)`: Estimador multimodal determinista ($\sim 4$ caracteres por token).
  - `estimated_tokens(text)`: Heurística estándar para estimación de tokens.
  - `extract_preserved_comments(beacon_path)`: Preserva comentarios y enriquecimiento semántico local.
  - `extract_seed_section(root, section_id)`: Extrae quirúrgicamente una sección de la semilla.
  - `format_compact_tree_json(data)`: Serializa `.context/tree.json` manteniéndolo en $\le 1000$ tokens.
  - `format_sliced_tree(slice_data)`: Formatea la vista recortada del subgrafo topológico.
  - `generate_beacon_content(meta)`: Genera contenido estándar para balizas contextuales.
  - `generate_sliced_tree(root, target)`: Genera subgrafo focalizado en $<150$ tokens.
  - `generate_tree_json(root)`: Compila el mapa satelital completo del repositorio.
  - `get_seed_sections(root)`: Parsea y devuelve el índice seccional de la semilla activa.
  - `ignore_patterns(root)`: Resuelve la lista activa de exclusiones `.agentignore`.
  - `ignored(path)`: Evalúa si una ruta se encuentra excluida de la navegación.
  - `infer_beacon_meta(dir_path, root)`: Infiere metadatos contextuales para carpetas nuevas.
  - `init_project(target_dir)`: Inicializa la estructura determinista de gobernanza.
  - `input_hash(files)`: Calcula el hash de entrada para capas de sincronización.
  - `inspect_python_header(file_path)`: Inspecciona encabezados e imports en archivos Python.
  - `inventory(root)`: Genera el inventario persistente de evidencias y firmas.
  - `is_ignored_path(path, root, patterns)`: Valida rutas contra reglas de exclusión.
  - `iter_beacon_files(root)`: Generador determinista de balizas en el árbol gobernado.
  - `iter_files(root)`: Itera archivos elegibles excluyendo ramas podadas (`crawl: false`).
  - `load_ignore_patterns(root)`: Carga patrones desde `.agentignore` y `.gitignore`.
  - `main()`: Punto de entrada CLI del motor.
  - `manage_checkpoint(root, action, **kwargs)`: Administra la máquina de estados en `.context/checkpoint.json`.
  - `matches_version(path)`: Verifica correspondencia con el runtime fijado.
  - `publish_layer(root, layer, data)`: Publica telemetría de capa en `.context/layers/`.
  - `put(path, raw, check)`: Escribe archivos de distribución verificando integridad.
  - `python_contracts(path)`: Extrae contratos y símbolos de archivos Python vía AST.
  - `query_orientation(root)`: Consulta el estado de orientación rápida desde la caché.
  - `read_json(path)`: Lectura segura de documentos JSON en UTF-8.
  - `reconcile_plans_lifecycle(root, check_only)`: Garbage collector de planes activos obsoletos.
  - `reconcile_repository(root, check_only)`: Cierre unificado e idempotente del repositorio.
  - `repository_lock(root, name)`: Bloqueo de concurrencia a nivel de sistema operativo.
  - `resolve_beacon(dir_path, root)`: Resuelve la baliza efectiva con herencia topológica.
  - `resolve_seed_key_files(root)`: Localiza y resuelve archivos de semilla físicos.
  - `route_file(file_path, base_path, move, overwrite)`: Enruta y normaliza archivos a su destino canónico.
  - `safe_io_retry(func, retries, delay)`: Reintento resiliente contra bloqueos I/O en Windows NTFS.
  - `safe_rename_casing(src, dst)`: Renombrado atómico bidireccional inmune a colisiones de casing.
  - `scaffold_beacon_for_dir(dir_path, root)`: Aprovisiona baliza `.context.yaml` adaptativa.
  - `sync_beacons(root, auto_discover, force_defaults)`: Sincroniza balizas en todo el árbol.
  - `sync_icontext_bus(root, ast_index, write_to_disk)`: Sincroniza el bus de federación cognitivo.
  - `sync_tree(root)`: Escribe y compacta el satélite `.context/tree.json`.
  - `upsert_segmented_block(path, tag, content)`: Inserción no destructiva de bloques segmentados.
  - `validate_backlog_data(data)`: Valida la estructura formal de `queue.json`.
  - `validate_backlog_queue(root, check_only)`: Valida la cola formal de intenciones en backlog.
  - `validate_beacon_data(data)`: Valida balizas contra el esquema formal Draft-07.
  - `validate_dependency_dag(root)`: Cortafuegos arquitectónico que impide ciclos e imports cruzados.
  - `validate_readmes(root)`: Valida consistencia bilingüe de `README.md` y `README_ES.md`.
  - `validate_seed(path, index)`: Valida formalmente el vector arquitectónico ThinkingSeed.
  - `validate_tree_data(data)`: Valida la integridad estructural de `tree.json`.
  - `write_json(path, data)`: Escritura determinista de JSON con indentación y orden de claves.

- **Contratos Fabric & Santolaya:**
  - `MedallionTier`: Enumerador canónico de capas (`BRONZE`, `SILVER`, `GOLD`, `BI_SEMANTIC`, `CORE_GOVERNANCE`).
  - `classify_fabric_item(item_path)`: Clasifica un artefacto de Fabric en su capa Medallón correspondiente.
  - `detect_item_type(path)`: Identifica el tipo de artefacto Fabric (`Notebook`, `Lakehouse`, `Warehouse`, etc.).
  - `read_fabric_platform_metadata(item_dir)`: Parsea el descriptor `.platform` de Microsoft Fabric Git Integration.
  - `scan_workspace_items(root_dir)`: Descubre y cataloga todos los ítems de Fabric en el workspace.
  - `audit_fabric_path(target_path)`: Audita un directorio o archivo contra las 7 reglas F8.
  - `audit_pyspark_content(content, file_path)`: Detecta antipatrones en scripts y notebooks PySpark.
  - `audit_pipeline_content(content, file_path)`: Detecta sobreconcurrencia de notebooks en Data Pipelines.
  - `audit_tmdl_content(content, file_path)`: Detecta columnas calculadas en DAX dentro de modelos TMDL.
  - `remediate_pyspark_code(code)`: Inyecta encabezados F8 (V-Order, Liquid Clustering, 8 particiones).
  - `remediate_file(file_path, dry_run)`: Parchea archivos físicos en el workspace.
  - `run_fabric_cli(argv, repo_root)`: Controlador del subcomando `fabric`.
  - `validate_chilean_rut(rut_str)`: Valida RUT de empresas y subcontratistas chilenos con Módulo 11.
  - `format_chilean_rut(rut_str)`: Formatea RUT chileno a estructura canónica con puntos y guion.
  - `build(check)`: Genera distribuciones independientes de runtime.

---

## 5. CONFIGURACIÓN, ENTORNOS Y DEPENDENCIAS

- **Kernel:** Python 3.10+ Standard Library pura (`Zero-Dependency`).
- **Política de Contexto:** `./config/context_policy.json` (perfiles Tier 1A $\le 220$t, Tier 1B $\le 800$t, Tier 2 $\le 16000$t).
- **Entornos Fabric:** `./fabric_workspaces/ws_core_governance/env_santolaya_prod.environment/` define el pool Spark con 1 a 2 nodos medianos (16 vCores max) y auto-pause en 2 minutos.

---

## 6. PRUEBAS, CI/CD, DESPLIEGUE Y OPERACIÓN

- **Suite Unitaria:** 69 pruebas en `tests/test_fwengine.py` (100% éxito) cubriendo resiliencia I/O, casing atómico en NTFS, cortafuegos DAG y contratos AST.
- **Suite de Presupuestos:** 8 benchmarks en `tests/test_token_budget.py` validando que `.context/tree.json` ocupe $\le 1000$ tokens (valor actual: 692 tokens, 97.0% de ahorro).
- **Verificación de Gobernanza:** `python FWengine.py reconcile --check`.

---

## 7. SUPERFICIE DE TENSIÓN, CONTRADICCIONES Y MODOS DE FALLA (AUDITORÍA ADVERSARIAL)

1. **Riesgo de Fallback a DirectQuery:** Si una tabla de Direct Lake supera 8 GB o contiene DAX no soportado, Fabric conmuta a DirectQuery saturando los 8 CUs. *Mitigación:* Validación previa en `audit_tmdl_content`.
2. **Tormentas de Archivos Pequeños:** `partitionBy` tradicional genera latencia masiva de metadatos en OneLake. *Mitigación:* Forzar Liquid Clustering (`CLUSTER BY`).
3. **Pico de Concurrencia Matutina:** Disparo simultáneo de pipelines satura la ventana de 24h de suavizado. *Mitigación:* Secuenciación en Data Factory.
4. **Desfase de UF:** Variación diaria del valor UF en contratos de edificación. *Mitigación:* Centralización en Silver con linaje estricto.

---

## 8. SEGURIDAD, PRIVACIDAD Y GUARDRAILS

- **Zero-Trust:** Prohibido almacenar credenciales o secretos en balizas o código; utilizar Azure Key Vault y Managed Identity de Fabric.
- **Poda Absorbente (`crawl: false`):** Carpetas de datos masivos o archivos compilados quedan estrictamente excluidas de la ventana de contexto.
- **Restricción de Rutas:** Prohibidas rutas absolutas del host en documentación y contratos.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y DECISIONES (ADRs)

- `[CONFIRMADO]` Eliminación de 8 carpetas esqueleto no funcionales (`02_foundation`, `03_research`, `data`, `infrastructure`, `logs`, `src/cloud_jobs`, `src/dashboards`, `src/data_generation`).
- `[CONFIRMADO]` Reducción del satélite topológico a 18 nodos y 692 tokens.
- `[CONFIRMADO]` Implementación de la Skill `Fabric` para Antigravity.
- `[CONFIRMADO]` Compatibilidad plena con Microsoft Fabric Git Integration.

---

## 10. REGLAS DE MODIFICACIÓN, GLOSARIO E ÍNDICE DE EVIDENCIAS

1. **Glosario:**
   - **CU:** Capacity Unit de Microsoft Fabric (F8 = 8 CUs $\approx$ 16 vCores Spark).
   - **Direct Lake:** Modo de acceso nativo de Power BI a Delta Lake en OneLake sin importar datos.
   - **Liquid Clustering:** Esquema flexible de agrupamiento que reemplaza al particionamiento rígido Hive.
   - **V-Order:** Formato optimizado de ordenamiento Parquet para lecturas de alto rendimiento.
2. **Índice de Evidencias:** Telemetría registrada en `.context/inventory.json`, `.context/contracts_ast.json` y `.context/tree.json`.

---

## 📌 CONTEXT HANDOFF & PROTOCOLO DE ASISTENCIA

Al retomar este repositorio, el agente de IA receptor debe:
1. Inspeccionar `.context/checkpoint.json` y ejecutar `python FWengine.py reconcile --check`.
2. Para tareas atómicas en Fabric, compilar contexto con `python FWengine.py context --pack <ruta> --tier 1a`.
3. Para auditar código de workspaces, invocar `python FWengine.py fabric --audit <ruta>`.
4. Finalizar cualquier cambio ejecutando `python FWengine.py reconcile`.

</SEED_ARCHITECTURAL_VECTOR>

