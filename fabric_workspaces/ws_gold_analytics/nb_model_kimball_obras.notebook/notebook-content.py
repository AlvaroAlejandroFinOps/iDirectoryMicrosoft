# Fabric notebook source
# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# ==============================================================================
# [iDirectoryFabric F8 Optimization Block - Santolaya]
# Configuración determinista para pool Spark de 16 vCores y lectura Direct Lake
# ==============================================================================
spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
spark.conf.set("spark.ms.autotune.optimizeWrite", "true")
spark.conf.set("spark.sql.shuffle.partitions", "8")
# ==============================================================================

from pyspark.sql import functions as F

# Carga de dimensiones y hechos desde Silver
curated_costos = spark.read.table("lakehouse_silver.curated_costos_obra")
dim_obras = spark.read.table("lakehouse_silver.dim_obras")

# Modelado dimensional Kimball
fact_costos_obra = (
    curated_costos.join(F.broadcast(dim_obras), on="id_obra", how="inner")
    .select(
        "id_obra",
        "id_transaccion",
        "fecha",
        "monto_pesos",
        "monto_uf",
        "centro_costo",
        "nombre_obra",
        "comuna",
        "region"
    )
)

# Escritura con V-Order para Direct Lake
(
    fact_costos_obra.write
    .format("delta")
    .mode("overwrite")
    .option("parquet.vorder.enabled", "true")
    .saveAsTable("lakehouse_gold.fact_costos_obra")
)

spark.sql("OPTIMIZE lakehouse_gold.fact_costos_obra")

