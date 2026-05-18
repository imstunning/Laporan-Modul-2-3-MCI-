-- DDL: create database and tables in clickHouse

CREATE DATABASE IF NOT EXISTS mci_db;

-- tabel orders
CREATE TABLE IF NOT EXISTS mci_db.orders (
    order_id  Int32,
    user_id  Int32,
    order_number  Int32,
    order_dow  Int8,
    order_hour_of_day  Int8,
    days_since_prior_order  Nullable(Float32),
    eval_set  String
) ENGINE = MergeTree()
ORDER BY order_id;

-- tabel order_items
CREATE TABLE IF NOT EXISTS mci_db.order_items (
    order_id  Int32,
    product_id  Int32,
    product_name  String,
    aisle_id  Int32,
    aisle  Nullable(String),
    department_id  Int32,
    department  Nullable(String),
    add_to_cart_order  Int32,
    reordered  Int8
) ENGINE = MergeTree()
ORDER BY (order_id, product_id);