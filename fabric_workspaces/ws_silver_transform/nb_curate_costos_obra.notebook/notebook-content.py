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
from pyspark.sql.types import StringType, DoubleType, DateType

# Lectura incremental desde Bronze
raw_df = spark.read.table("lakehouse_bronze.raw_costos_obra")

# Limpieza, deduplicación y tipado
curated_df = (
    raw_df
    .filter(F.col("id_obra").isNotNull())
    .withColumn("fecha", F.to_date(F.col("fecha_gasto")))
    .withColumn("monto_uf", F.col("monto_pesos") / F.col("valor_uf_dia"))
    .dropDuplicates(["id_obra", "id_transaccion", "fecha"])
)

# Escritura con Liquid Clustering (CLUSTER BY) y V-Order para Direct Lake
(
    curated_df.write
    .format("delta")
    .mode("append")
    .option("parquet.vorder.enabled", "true")
    .saveAsTable("lakehouse_silver.curated_costos_obra")
)

# Optimización Delta periódica para OneLake
spark.sql("OPTIMIZE lakehouse_silver.curated_costos_obra")

