
-- Section1
CREATE INDEX index_sum ON orders (created_at , total);
-- Section2 
CREATE INDEX index_sum_two_condition ON orders (user_id , created_at , total  )
-- Section3
WITH RECURSIVE

daily_orders AS (
    SELECT DATE(created_at) AS order_date, SUM(total) AS total_amount FROM orders
    GROUP BY DATE(created_at)
),

date_boundry AS (
    SELECT MIN(order_date) AS first_day, MAX(order_date) AS last_day
    FROM daily_orders
),

all_dates AS (
    SELECT first_day AS order_date, CAST(0 AS DECIMAL(10, 2)) AS total_amount, last_day
    FROM date_boundry
    WHERE first_day IS NOT NULL

    UNION ALL

    SELECT DATE_ADD(order_date, INTERVAL 1 DAY), CAST(0 AS DECIMAL(10, 2)), last_day
    FROM all_dates
    WHERE order_date < last_day
),

have_all_date AS (
    SELECT order_date, total_amount
    FROM all_dates

    UNION ALL

    SELECT order_date, total_amount
    FROM daily_orders
)

SELECT
    order_date, SUM(total_amount) AS total_amount
FROM have_all_date
GROUP BY order_date
ORDER BY order_date ASC;