import pandas as pd
import logging
from clickhouse_driver import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ORDERS_PATH = "/opt/airflow/dags/scripts/data/orders.parquet"
ORDER_ITEMS_PATH = "/opt/airflow/dags/scripts/data/order_items.parquet"

def load_to_clickhouse():
    logger.info("Memuat data ke ClickHouse Warehouse...")

    try:
        df_orders = pd.read_parquet(ORDERS_PATH)
        df_items = pd.read_parquet(ORDER_ITEMS_PATH)

        client = Client(
            host='clickhouse-server',
            user='admin',
            password='rahasia'
        )

        client.execute('CREATE DATABASE IF NOT EXISTS mci_db')

        client.execute('''
            CREATE TABLE IF NOT EXISTS mci_db.orders (
                order_id                Int32,
                user_id                 Int32,
                order_number            Int32,
                order_dow               Int8,
                order_hour_of_day       Int8,
                days_since_prior_order  Nullable(Float32),
                eval_set                String
            ) ENGINE = MergeTree()
            ORDER BY order_id
        ''')

        client.execute('''
            CREATE TABLE IF NOT EXISTS mci_db.order_items (
                order_id            Int32,
                product_id          Int32,
                product_name        String,
                aisle_id            Int32,
                aisle               Nullable(String),
                department_id       Int32,
                department          Nullable(String),
                add_to_cart_order   Int32,
                reordered           Int8
            ) ENGINE = MergeTree()
            ORDER BY (order_id, product_id)
        ''')

        client.execute('TRUNCATE TABLE mci_db.orders')
        client.execute('TRUNCATE TABLE mci_db.order_items')

        orders_tuples = list(df_orders.itertuples(index=False, name=None))
        if orders_tuples:
            client.execute('INSERT INTO mci_db.orders VALUES', orders_tuples)
            logger.info(f"✅ Berhasil insert {len(orders_tuples)} orders")

        items_tuples = list(df_items.itertuples(index=False, name=None))
        if items_tuples:
            client.execute('INSERT INTO mci_db.order_items VALUES', items_tuples)
            logger.info(f"✅ Berhasil insert {len(items_tuples)} order items")

        logger.info("✅ Pipeline Selesai! Data berhasil dimuat ke ClickHouse")

    except Exception as e:
        logger.error(f"❌ Gagal memuat data ke ClickHouse: {e}")
        raise

if __name__ == "__main__":
    load_to_clickhouse()
