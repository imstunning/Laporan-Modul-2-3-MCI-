-- query untuk visualisasi di metabase

-- Orders by Day of Week
SELECT 
    CASE order_dow
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_name,
    COUNT(*) AS total_orders
FROM mci_db.orders
GROUP BY order_dow, day_name
ORDER BY order_dow;

-- Orders by Hour of Day
SELECT 
    order_hour_of_day AS hour,
    COUNT(*) AS total_orders
FROM mci_db.orders
GROUP BY order_hour_of_day
ORDER BY order_hour_of_day;

-- Top 10 Most Ordered Products
SELECT 
    product_name,
    COUNT(*) AS total_ordered
FROM mci_db.order_items
GROUP BY product_name
ORDER BY total_ordered DESC
LIMIT 10;

-- Top 5 Departments by Orders
SELECT 
    department,
    COUNT(*) AS total_orders
FROM mci_db.order_items
WHERE department IS NOT NULL
GROUP BY department
ORDER BY total_orders DESC
LIMIT 5;

-- Top 10 Products by Reorder Rate
SELECT 
    product_name,
    COUNT(*) AS total_ordered,
    SUM(reordered) AS total_reordered,
    ROUND(SUM(reordered) / COUNT(*) * 100, 2) AS reorder_rate
FROM mci_db.order_items
GROUP BY product_name
HAVING total_ordered > 1
ORDER BY reorder_rate DESC
LIMIT 10;

-- Average Items per Order by Day
SELECT 
    o.order_dow,
    CASE o.order_dow
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_name,
    ROUND(AVG(item_count), 2) AS avg_items_per_order
FROM mci_db.orders o
JOIN (
    SELECT order_id, COUNT(*) AS item_count
    FROM mci_db.order_items
    GROUP BY order_id
) i ON o.order_id = i.order_id
GROUP BY o.order_dow, day_name
ORDER BY o.order_dow;