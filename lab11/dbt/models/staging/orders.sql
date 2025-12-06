-- models/staging/orders.sql

SELECT
    order_id,
    customer_id,
    order_date,
    amount
FROM
   {{ ref('raw_orders') }} -- raw_data.orders -- Asume que tienes una tabla 'orders' en un esquema 'raw_data'
WHERE
    order_date >= '2023-01-01'
