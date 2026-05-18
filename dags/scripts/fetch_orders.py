import requests
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://96.9.212.102:8000/orders"
OUTPUT_PATH = "/opt/airflow/dags/scripts/data/raw_orders.parquet"

def fetch_orders():
    logger.info("Membuka keran data: API Orders...")

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

        df = pd.DataFrame(data['orders'])
        df.to_parquet(OUTPUT_PATH, index=False)

        logger.info(f"✅ Sukses menyimpan {data['total_orders']} orders ke {OUTPUT_PATH}")

    except Exception as e:
        logger.error(f"❌ Gagal menarik data: {e}")
        raise

if __name__ == "__main__":
    fetch_orders()
