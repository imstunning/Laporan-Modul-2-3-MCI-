import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_PATH = "/opt/airflow/dags/scripts/data/raw_orders.parquet"
ORDERS_OUTPUT_PATH = "/opt/airflow/dags/scripts/data/orders.parquet"
ORDER_ITEMS_OUTPUT_PATH = "/opt/airflow/dags/scripts/data/order_items.parquet"

def transform_orders():
    logger.info("Membaca data mentah dari Data Lake...")

    try:
        df = pd.read_parquet(INPUT_PATH)
        orders = df.to_dict('records')

        logger.info("Transformasi data: flatten nested + handle missing values...")

        flat_orders = []
        flat_order_items = []

        for order in orders:
            flat_orders.append({
                'order_id': order['order_id'],
                'user_id': order['user_id'],
                'order_number': order['order_number'],
                'order_dow': order['order_dow'],
                'order_hour_of_day': order['order_hour_of_day'],
                'days_since_prior_order': order['days_since_prior_order'],
                'eval_set': order['eval_set']
            })

            for product in order['products']:
                flat_order_items.append({
                    'order_id': order['order_id'],
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'aisle_id': product['aisle_id'],
                    'aisle': None if product['aisle'] == 'missing' else product['aisle'],
                    'department_id': product['department_id'],
                    'department': None if product['department'] == 'missing' else product['department'],
                    'add_to_cart_order': product['add_to_cart_order'],
                    'reordered': product['reordered']
                })

        os.makedirs(os.path.dirname(ORDERS_OUTPUT_PATH), exist_ok=True)

        pd.DataFrame(flat_orders).to_parquet(ORDERS_OUTPUT_PATH, index=False)
        pd.DataFrame(flat_order_items).to_parquet(ORDER_ITEMS_OUTPUT_PATH, index=False)

        logger.info(f"✅ Sukses transformasi {len(flat_orders)} orders, {len(flat_order_items)} order items ke {ORDERS_OUTPUT_PATH}")

    except Exception as e:
        logger.error(f"❌ Gagal transformasi data: {e}")
        raise

if __name__ == "__main__":
    transform_orders()
