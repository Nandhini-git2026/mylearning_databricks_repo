from pyspark import pipelines as dp
from pyspark.sql import functions as f


# ------------------------------------------------------------------------------
# customers -> SCD Type 1 (we only need current state for this dimension)
# ------------------------------------------------------------------------------

@dp.temporary_view(name="customers_clean")
@dp.expect_or_fail("pk_not_null", "customer_id IS NOT NULL")
@dp.expect_all_or_drop(
    {
        "valid_email": r"email RLIKE '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'",
        "non_blank_name": "first_name IS NOT NULL AND length(trim(first_name)) > 0",
    }
)
def customers_clean():
    return spark.read.table("retail.bronze.customers_snapshot").select(
        "customer_id", "first_name", "last_name", "email", "city", "country", "updated_at"
    )


dp.create_streaming_table(
    name="retail.silver.customers",
    comment="SCD Type 1 (current state) customer dimension, governed by Unity Catalog.",
)

dp.create_auto_cdc_from_snapshot_flow(
    target="retail.silver.customers",
    source="customers_clean",
    keys=["customer_id"],
    stored_as_scd_type=1,
)


# ------------------------------------------------------------------------------
# orders -> SCD Type 2 (we want full order-status history, e.g. PLACED -> PAID
# -> SHIPPED -> DELIVERED, for lifecycle/funnel analysis in gold)
# ------------------------------------------------------------------------------

@dp.temporary_view(name="orders_clean")
@dp.expect_or_fail("pk_not_null", "order_id IS NOT NULL")
@dp.expect_all_or_drop(
    {
        "valid_status": "order_status IN ('PLACED','PAID','SHIPPED','DELIVERED','CANCELLED')",
        "non_negative_amount": "order_amount >= 0",
        "fk_customer_exists": "customer_id IS NOT NULL",
    }
)
def orders_clean():
    orders_df = spark.read.table("retail.bronze.orders_snapshot").select(
        "order_id", "customer_id", "order_status", "order_amount", "order_ts", "updated_at")
    return orders_df


dp.create_streaming_table (
    name="retail.silver.orders",
    comment="SCD Type 2 order history (status changes tracked over time), governed by Unity Catalog."
)

dp.create_auto_cdc_from_snapshot_flow(
     target="retail.silver.orders",
    source="orders_clean",
    keys=["order_id"],
    stored_as_scd_type=2,
    track_history_column_list=["order_status", "order_amount"]
)
