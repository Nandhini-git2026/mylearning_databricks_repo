from pyspark import pipelines as dp
from pyspark.sql import functions as F

FOREIGN_CATALOG ="mysql_connection_catalog"
FOREIGN_SCHEMA = "salesdb"

@dp.table(
    name="retail.bronze.customers_snapshot",
    comment="Raw live snapshot of MySQL salesdb.customers via Lakehouse Federation.",
)
@dp.expect("valid_customer_id", "customer_id IS NOT NULL")

def customer_sanpshot():
    cust_df = spark.read.table(f"{FOREIGN_CATALOG}.{FOREIGN_SCHEMA}.customers").\
    withColumn("_ingested_at", F.current_timestamp()).\
    withColumn("_source_system", F.lit("mysql_salesdb"))

    return cust_df

@dp.table(
    name="retail.bronze.orders_snapshot",
    comment="Raw live snapshot of MySQL salesdb.orders via Lakehouse Federation.",
)

@dp.expect_all(
    {
        "valid_order_id": "order_id IS NOT NULL",
        "non_negative_amount": "order_amount >= 0",
    }
)

def orders_snapshot():
    ord_df = spark.read.table(f"{FOREIGN_CATALOG}.{FOREIGN_SCHEMA}.orders").\
    withColumn("_ingested_at", F.current_timestamp()).\
    withColumn("_source_system", F.lit("mysql_salesdb"))

    return ord_df

