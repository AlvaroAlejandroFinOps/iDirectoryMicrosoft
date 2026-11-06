![Arquitectura iDirectoryFabric](iDirectory.png)

**iDirectoryFabric v6.0.0.** Esquema de Directorio Base Universal, Gobernanza Corporativa, Ingeniería de Contexto y Remediación Automatizada para Microsoft Fabric (Capacidad F8+).
<!-- ICONTEXT-V6:RELEASE -->

# iDirectoryFabric: El Esquema de Directorio Base Universal y Estándar de Gobernanza para Microsoft Fabric por Gravity HyperScale Thinking

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Estándar](https://img.shields.io/badge/Est%C3%A1ndar-Enterprise%20Paper--Grade%20v6.0-2b2b2b?style=flat-square)](#)
[![Blueprint](https://img.shields.io/badge/Blueprint-Esquema%20Base%20Universal%20Fabric-107c41?style=flat-square)](#2-arquitectura-del-sistema-y-linaje-medallón)
[![Capacidad Fabric](https://img.shields.io/badge/Capacidad%20Fabric-F8%2B%20%288%20CUs%20%7C%2016%20vCores%29-0078d4?style=flat-square)](#3-gobernanza-de-capacidad-f8-y-economía-de-cus)
[![Arquitectura](https://img.shields.io/badge/Arquitectura-OneLake%20Medallion-008272?style=flat-square)](#2-arquitectura-del-sistema-y-linaje-medallón)
[![Direct Lake](https://img.shields.io/badge/Power%20BI-Direct%20Lake%20Guardrails-f2c811?style=flat-square)](#4-motor-de-optimización-y-remediación-f8)
[![Motor](https://img.shields.io/badge/Motor-FWengine.py-1a1a1a?style=flat-square)](#5-interfaz-cli-y-comandos-operacionales)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-1a1a1a?style=flat-square)](LICENSE)

---

## 1. Resumen Ejecutivo

**iDirectoryFabric**, concebido y desarrollado por **Gravity HyperScale Thinking**, establece el **Esquema de Directorio Base Universal (Blueprint/Template Agnóstico)** y el plano de control determinista de ingeniería de contexto para estructurar, gobernar y escalar cualquier repositorio corporativo conectado a **Microsoft Fabric Git Integration** en GitHub.

Los equipos de alta ingeniería de datos que operan múltiples Workspaces en Microsoft Fabric enfrentan dos desafíos críticos al llevar sus proyectos a GitHub:
1. **Desorden Topológico de Artefactos:** Sin un esquema de carpetas base estandarizado, los Notebooks (`.Notebook`), referencias de Lakehouse (`.Lakehouse`), Warehouses (`.Warehouse`), Pipelines (`.DataPipeline`), Modelos Semánticos (`.SemanticModel` en TMDL) y Reportes Power BI (`.Report` en PBIR) caen mezclados en la raíz del workspace, degradando la trazabilidad y el mantenimiento.
2. **Throttling de Capacidad y Caída a DirectQuery (Base F8+):** Operar cargas analíticas sobre capacidades como **Microsoft Fabric F8** (8 Capacity Units $\approx$ pool de ráfaga de 16 vCores Spark) exige barreras estrictas contra *Interactive Rejection*, *Background Rejection* (ventana de suavizado de 24 horas) y tormentas de archivos pequeños en OneLake.

Para resolver ambos retos de raíz, **iDirectoryFabric v6.0** entrega un **Esquema de Directorio Base limpio y agnóstico de 5 Workspaces Medallón y 17 Carpetas Contenedoras** gobernadas por balizas `.context.yaml`, acompañado de un kernel sin dependencias externas (`FWengine.py`), un **Ruteador y Clasificador Medallón Automático**, y un **Motor de Remediación F8** con consumo acotado de tokens ($< 220\text{ tokens}$ en Tier 1A).

---

## 2. Arquitectura del Sistema y Linaje Medallón

iDirectoryFabric provee una estructura base limpia, lista para clonar y adaptar a cualquier proyecto, 100% compatible con **Microsoft Fabric Git Integration** (*Subfolder-per-Workspace* y *Workspace Folders* nativos):

```text
fabric_workspaces/
├── ws_core_governance/                # Gobernanza Central, Cómputo Spark y Librerías Comunes
│   ├── environments/                  # Carpeta donde caen *.Environment (Spark pools, runtime)
│   ├── libraries/                     # Carpeta donde caen paquetes Python (.whl) y utilitarios (.py)
│   └── notebooks/                     # Carpeta donde caen *.Notebook de mantenimiento (OPTIMIZE/VACUUM)
│
├── ws_bronze_ingest/                  # Workspace Capa Bronze (Ingesta Cruda Inmutable)
│   ├── lakehouses/                    # Carpeta donde caen referencias *.Lakehouse Bronze y Shortcuts
│   ├── pipelines/                     # Carpeta donde caen *.DataPipeline y *.CopyJob de ingesta
│   ├── dataflows/                     # Carpeta donde caen *.Dataflow Gen2
│   ├── eventstreams/                  # Carpeta donde caen *.Eventstream, *.MirroredDatabase, *.KQLDatabase
│   └── notebooks/                     # Carpeta donde caen *.Notebook de ingesta vía APIs o fuentes complejas
│
├── ws_silver_transform/               # Workspace Capa Silver (Curación, Calidad y Conformación Delta)
│   ├── lakehouses/                    # Carpeta donde caen referencias *.Lakehouse Silver
│   ├── notebooks/                     # Carpeta donde caen *.Notebook PySpark/SQL de limpieza y SCD2
│   └── pipelines/                     # Carpeta donde caen *.DataPipeline de orquestación Silver
│
├── ws_gold_analytics/                 # Workspace Capa Gold (Modelo Dimensional Kimball Star Schema)
│   ├── lakehouses/                    # Carpeta donde caen referencias *.Lakehouse Gold con V-Order
│   ├── warehouses/                    # Carpeta donde caen *.Warehouse y *.SQLDatabase (T-SQL DDL/Vistas)
│   ├── notebooks/                     # Carpeta donde caen *.Notebook de tablas de Hechos y Dimensiones
│   └── pipelines/                     # Carpeta donde caen *.DataPipeline de refresco analítico Gold
│
└── ws_bi_semantic/                    # Workspace Capa Semántica y Consumo BI (Direct Lake)
    ├── semantic_models/               # Carpeta donde caen *.SemanticModel (definiciones TMDL y .pbism)
    └── reports/                       # Carpeta donde caen archivos Power BI *.Report (formato PBIR / PBIP)
```

Cada una de las 17 carpetas contenedoras está anclada en Git mediante su propio archivo `.context.yaml`, lo que permite que GitHub versione la estructura de directorios base limpia sin archivos `.gitkeep` (que Fabric Git Integration rechaza) e inyecte directivas específicas de ingeniería de datos en los agentes de IA.

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

iDirectoryFabric gobierna las configuraciones de pools Spark dentro de `ws_core_governance/environments/*.Environment/Setting/Spark/compute.json`:
- **Asignación de Nodos:** Mínimo 1 nodo, Máximo 2 nodos (previene sobrecostes de autoescala).
- **Auto-pause Delay:** 2 minutos (elimina cobro por clusters ociosos).
- **Optimización Dinámica:** Auto-tune y `optimizeWrite` activos por defecto.

---

## 4. Motor de Optimización y Remediación F8

El motor de remediación analiza y soluciona 7 antipatrones de rendimiento sobre cualquier artefacto que se deposite en el esquema base:

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
# 1. Validar el esquema base de 5 Workspaces / 17 Contenedores y clasificar artefactos depositados
python FWengine.py fabric --classify fabric_workspaces/

# 2. Auditar repositorio o workspace contra las reglas de capacidad F8
python FWengine.py fabric --audit fabric_workspaces/

# 3. Aplicar remediación automática F8 a notebooks de PySpark
python FWengine.py fabric --remediate fabric_workspaces/

# 4. Enrutar automáticamente cualquier artefacto o archivo de Fabric a su carpeta contenedora base
python FWengine.py route <ruta_artefacto> --move

# 5. Compilar paquete de contexto atómico (<220 tokens) para agentes de IA
python FWengine.py context --pack fabric_workspaces/ws_silver_transform/notebooks --tier 1a

# 6. Reconciliación completa e idempotente del repositorio (topología, balizas, satélite)
python FWengine.py reconcile
python FWengine.py reconcile --check
```

---

## 6. Protocolo de Agentes de IA en Antigravity

iDirectoryFabric se acopla con **Antigravity** mediante skills especializadas y perfiles de contexto adaptativo:

- **Activación de Skill:** Invoca `/fabric` en el chat de Antigravity para validar el esquema base, auditar CUs y clasificar artefactos Medallón.
- **Preservación de Ventana de Contexto:** Los paquetes atómicos (`Tier 1A`) permiten a los agentes editar notebooks o definiciones TMDL complejas sin sobrecargar la ventana de contexto.
- **Vector ADN Arquitectónico:** El archivo `01_seed/seed-idirectoryfabric-master.md` actúa como la referencia canónica para diseño de sistemas, contratos de carpetas y límites de capacidad.

---

## 7. Formulación Matemática y Presupuestos de Tokens

La latencia de compilación $T_{\text{pack}}$ y el consumo de tokens $\Theta$ satisfacen:

$$\Theta(\text{Tier 1A}) \le 220\text{ tokens}, \quad \Theta(\text{Tier 1B}) \le 800\text{ tokens}$$

La integridad topológica se valida mediante el fingerprint criptográfico SHA-256:

$$\text{topology\_hash} = \mathcal{H}_{\text{SHA256}}\left(\bigoplus_{i=1}^{N} \text{node\_path}_i \parallel \text{node\_mtime}_i \parallel \text{beacon\_hash}_i\right)$$

---

## 8. Licencia y Autoría

- **Arquitectura y Concepción:** Diseñado por **Gravity HyperScale Thinking**.
- **Alcance del Blueprint:** Esquema de Directorio Base Universal para **Microsoft Fabric Git Integration**.
- **Licencia:** Licencia MIT. Consulta [LICENSE](LICENSE) para más detalles.
