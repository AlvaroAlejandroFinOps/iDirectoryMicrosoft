![Arquitectura iDirectoryFabric](iDirectory.png)

**iDirectoryFabric v6.0.0.** Framework de Gobernanza, Ingeniería de Contexto y Remediación Automatizada para Microsoft Fabric (Capacidad F8) — Santolaya (Chile).
<!-- ICONTEXT-V6:RELEASE -->

# iDirectoryFabric: Estándar de Ingeniería de Contexto y Gobernanza para Microsoft Fabric por Gravity HyperScale Thinking

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Estándar](https://img.shields.io/badge/Est%C3%A1ndar-Enterprise%20Paper--Grade%20v6.0-2b2b2b?style=flat-square)](#)
[![Capacidad Fabric](https://img.shields.io/badge/Capacidad%20Fabric-F8%20%288%20CUs%20%7C%2016%20vCores%29-0078d4?style=flat-square)](#3-gobernanza-de-capacidad-f8-y-economía-de-cus)
[![Cliente](https://img.shields.io/badge/Empresa-Santolaya%20%28Chile%29-107c41?style=flat-square)](#1-resumen-ejecutivo)
[![Arquitectura](https://img.shields.io/badge/Arquitectura-OneLake%20Medallion-008272?style=flat-square)](#2-arquitectura-del-sistema-y-linaje-medallón)
[![Direct Lake](https://img.shields.io/badge/Power%20BI-Direct%20Lake%20Guardrails-f2c811?style=flat-square)](#4-motor-de-optimización-y-remediación-f8)
[![Motor](https://img.shields.io/badge/Motor-FWengine.py-1a1a1a?style=flat-square)](#5-interfaz-cli-y-comandos-operacionales)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-1a1a1a?style=flat-square)](LICENSE)

---

## 1. Resumen Ejecutivo

**iDirectoryFabric**, concebido y desarrollado por **Gravity HyperScale Thinking** y calibrado específicamente para **Santolaya** (Constructora e Inmobiliaria Santolaya, Santiago de Chile), establece un plano de control determinista y una arquitectura de ingeniería de contexto para gobernar cargas de trabajo corporativas sobre **Microsoft Fabric**.

En empresas de edificación e inmobiliarias de alta envergadura, los flujos de datos integran sistemas transaccionales locales, ERPs en la nube, portales de abastecimiento y subcontratación (Iconstruye), contabilidad financiera (SAP / Softland), CRM comercial y promesas (PlanOK / Salesforce) y seguimiento de avance físico en obra. Al desplegar estas cargas sobre una capacidad elástica pero acotada como **Microsoft Fabric F8** (que provee 8 Capacity Units, equivalentes a un pool de ráfaga de ~16 vCores Spark), surgen riesgos operacionales críticos:
1. **Interactive Delay y Rejection:** Modelos semánticos o medidas DAX descuidadas que exceden los límites de memoria de F8 (~8–10 GB) conmutan forzosamente de Direct Lake a DirectQuery, traduciendo cada interacción visual en decenas de consultas T-SQL contra el SQL Analytics Endpoint y saturando de inmediato los 8 CUs.
2. **Throttling en Segundo Plano (Background Throttling):** La ejecución simultánea de notebooks de PySpark sin escalonar o actividades de copia desmedidas activa el mecanismo de suavizado de 24 horas de Fabric. Cuando el consumo excede el 100% de la capacidad en la ventana de suavizado, Fabric aplica *Background Rejection*, cancelando de forma forzosa los pipelines productivos.
3. **Tormenta de Archivos Pequeños en OneLake:** El particionamiento tradicional tipo Hive (`partitionBy`) sobre columnas de alta cardinalidad genera millones de archivos Parquet de pocos kilobytes, colapsando la memoria de metadatos del driver Spark y provocando fallos por Out-of-Memory (OOM).

Para erradicar estas fallas, **iDirectoryFabric v6.0** introduce un núcleo de gobernanza sin dependencias externas (`FWengine.py`), un **Clasificador Medallón Inteligente**, un **Motor de Optimización y Remediación Estática/Dinámica F8**, y un **Plano de Ingeniería de Contexto Adaptativo** que permite a los agentes autónomos de IA (Google Gemini/Antigravity, Anthropic Claude Code, OpenAI/Codex) auditar, reparar y estructurar artefactos de Fabric con un consumo acotado de tokens ($< 220\text{ tokens}$ en Tier 1A).

---

## 2. Arquitectura del Sistema y Linaje Medallón

iDirectoryFabric organiza los repositorios vinculados mediante **Microsoft Fabric Git Integration** en una estructura multi-workspace que respeta el aislamiento estricto de capas Medallón:

```text
+----------------------------------------------------------------------------------------------------+
|                                    SISTEMAS ORIGEN SANTOLAYA                                       |
|             (Compras / Subcontratos / ERP Contable / Ventas Inmobiliarias / Avance Obra)           |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA BRONZE: ws_bronze_ingest (Lakehouse Bronze / Data Pipelines / Shortcuts)                      |
| - Ingesta raw inmutable, append-only, schema-on-read en OneLake.                                   |
| - Metadatos de auditoría obligatorios: _ingested_at, _source_system, _batch_id.                    |
| - Cómputo: Copy Activities ligeras sin inicialización innecesaria de clusters Spark.               |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA SILVER: ws_silver_transform (Lakehouse Silver / Curated PySpark Notebooks)                    |
| - Limpieza, deduplicación, validación de RUT chileno con algoritmo Módulo 11.                     |
| - Normalización monetaria (conversión diaria de UF - Unidad de Fomento y CLP).                     |
| - Almacenamiento Delta Lake optimizado con V-Order = True y Liquid Clustering (CLUSTER BY id_obra).|
| - Particiones de shuffle acotadas a 8 para eliminar sobrecarga en los 16 vCores.                  |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA GOLD: ws_gold_analytics (Fabric Warehouse / Lakehouse Gold / Kimball Star Schema)             |
| - Modelo dimensional analítico en estrella: fact_costos_obra, fact_avance_fisico,                   |
|   fact_ventas_inmobiliarias, dim_proyecto, dim_obra, dim_contratista, dim_tiempo.                 |
| - Tablas Delta pre-agregadas que aseguran respuestas analíticas en sub-segundos.                   |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+────────────────────────────────────────────────────────────────────────────────────────────────────+
| CAPA BI SEMANTIC: ws_bi_semantic (Modelos Semánticos Direct Lake TMDL / Power BI PBIR)             |
| - Modelos semánticos en modo DIRECT LAKE puro conectados directamente a Delta OneLake.             |
| - Límite estricto de memoria: Modelo semántico < 8 GB (salvaguarda física F8).                     |
| - Cero columnas calculadas DAX: Toda métrica derivada se pre-calcula aguas arriba en Silver/Gold.  |
| - Reportes ejecutivos de obras e inmobiliaria en formato PBIR con trazabilidad Git.               |
+────────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Gobernanza de Capacidad F8 y Economía de CUs

La capacidad Microsoft Fabric F8 asigna 8 Capacity Units (CUs), operando bajo algoritmos de suavizado (*smoothing*):

$$\text{Pool de Cómputo Disponible} = 8\text{ CUs} \approx 16\text{ vCores Spark (Starter Pool: 1–2 Nodos Medianos)}$$

### Parámetros de Suavizado y Throttling
| Tipo de Operación | Ventana de Suavizado | Impacto de Throttling ante Sobrecarga |
|---|---|---|
| **Interactiva (Direct Lake / Reportes)** | 5 Minutos | Retraso $\to$ Interactive Rejection (Falla de visuales en Power BI) |
| **Segundo Plano (PySpark / Pipelines)** | 24 Horas | Encolado $\to$ Background Rejection (Cancelación forzosa de pipeline) |
| **Memoria de Modelo Direct Lake** | Límite Físico | Degradación a DirectQuery $\implies$ Saturación inmediata de 8 CUs |

iDirectoryFabric inyecta configuraciones deterministas en `.Environment/Setting/Spark/compute.json`:
- **Asignación de Nodos:** Mínimo 1 nodo, Máximo 2 nodos (previene sobrecostes de autoescala).
- **Auto-pause Delay:** 2 minutos (elimina cobro por clusters ociosos).
- **Optimización Dinámica:** Auto-tune y `optimizeWrite` activos por defecto.

---

## 4. Motor de Optimización y Remediación F8

El motor de remediación analiza y soluciona 7 antipatrones de rendimiento:

```text
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
| Regla ID    | Antipatrón Detectado                 | Severidad| Remediación Automatizada                |
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
| RULE-F8-01  | Escritura Parquet sin V-Order        | ALTA     | Inyecta parquet.vorder.enabled = true   |
| RULE-F8-02  | partitionBy en alta cardinalidad     | ALTA     | Reemplaza por Liquid Clustering (Delta) |
| RULE-F8-03  | df.collect() / .toPandas() en driver | CRÍTICA  | Bloquea y refactoriza a escritura Delta |
| RULE-F8-04  | shuffle.partitions por defecto (200) | MEDIA    | Reduce particiones de shuffle a 8       |
| RULE-F8-05  | Ausencia de OPTIMIZE y VACUUM Delta  | MEDIA    | Inyecta sentencias de mantenimiento     |
| RULE-F8-06  | Columnas calculadas DAX (DirectLake) | CRÍTICA  | Mueve el cálculo aguas arriba a Silver  |
| RULE-F8-07  | Pipeline con >2 jobs concurrentes    | ALTA     | Aplica dependencias secuenciales        |
+─────────────+──────────────────────────────────────+──────────+─────────────────────────────────────────+
```

---

## 5. Interfaz CLI y Comandos Operacionales

El plano de control se invoca a través de `FWengine.py`:

```powershell
# 1. Auditar repositorio o workspace contra las reglas de capacidad F8
python FWengine.py fabric --audit fabric_workspaces/

# 2. Clasificar artefactos de Fabric Git en capas Medallón
python FWengine.py fabric --classify fabric_workspaces/

# 3. Aplicar remediación automática F8 a notebooks de PySpark
python FWengine.py fabric --remediate fabric_workspaces/

# 4. Compilar paquete de contexto atómico (<220 tokens) para agentes de IA
python FWengine.py context --pack fabric_workspaces/ws_silver_transform --tier 1a

# 5. Reconciliación completa e idempotente del repositorio (topología, balizas, satélite)
python FWengine.py reconcile
python FWengine.py reconcile --check
```

---

## 6. Protocolo de Agentes de IA en Antigravity

iDirectoryFabric se acopla con **Antigravity** mediante skills especializadas y perfiles de contexto adaptativo:

- **Activación de Skill:** Invoca `/fabric` en el chat de Antigravity para iniciar auditorías de CUs, remediación y clasificación Medallón.
- **Preservación de Ventana de Contexto:** Los paquetes atómicos (`Tier 1A`) permiten a los agentes editar notebooks o definiciones TMDL complejas sin sobrecargar la ventana de contexto.
- **Vector ADN Arquitectónico:** El archivo `01_seed/seed-idirectoryfabric-master.md` actúa como la referencia canónica para diseño de sistemas, reglas de negocio y límites de capacidad.

---

## 7. Formulación Matemática y Presupuestos de Tokens

La latencia de compilación $T_{\text{pack}}$ y el consumo de tokens $\Theta$ satisfacen:

$$\Theta(\text{Tier 1A}) \le 220\text{ tokens}, \quad \Theta(\text{Tier 1B}) \le 800\text{ tokens}$$

La integridad topológica se valida mediante el fingerprint criptográfico SHA-256:

$$\text{topology\_hash} = \mathcal{H}_{\text{SHA256}}\left(\bigoplus_{i=1}^{N} \text{node\_path}_i \parallel \text{node\_mtime}_i \parallel \text{beacon\_hash}_i\right)$$

---

## 8. Licencia y Autoría

- **Arquitectura y Concepción:** Diseñado por **Gravity HyperScale Thinking**.
- **Calibración Corporativa:** Adaptado para **Santolaya** (Constructora e Inmobiliaria, Chile).
- **Licencia:** Licencia MIT. Consulta [LICENSE](LICENSE) para más detalles.
