
-- Section1
CREATE INDEX index_sum ON orders (created_at , total);
-- Section2 
CREATE INDEX index_sum_two_condition ON orders (user_id , created_at , total  )
-- Section3
CREATE TEMPORARY TABLE daily_orders AS
SELECT
    DATE(created_at) AS order_date,
    SUM(total) AS total_amount
FROM orders
GROUP BY DATE(created_at);
CREATE TEMPORARY TABLE all_dates (
    order_date DATE,
    total_amount DECIMAL(10, 2)
);
DELIMITER //
CREATE PROCEDURE have_all_date()
BEGIN
    DECLARE first_day DATE;
    DECLARE last_day DATE;
    SELECT
        MIN(order_date),
        MAX(order_date)
    INTO
        first_day,
        last_day
    FROM daily_orders;
    WHILE first_day <= last_day DO
        INSERT INTO all_dates (order_date, total_amount)
        VALUES (first_day, 0);
        SET first_day = DATE_ADD(first_day, INTERVAL 1 DAY);
    END WHILE;
END //
DELIMITER ;
CALL have_all_date();
SELECT
    order_date,
    SUM(total_amount) AS total_amount
FROM
(
    SELECT order_date, total_amount
    FROM all_dates
    UNION ALL
    SELECT order_date, total_amount
    FROM daily_orders
) AS result
GROUP BY order_date
ORDER BY order_date ASC;

DROP PROCEDURE have_all_date;