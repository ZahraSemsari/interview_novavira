
-- Section1
CREATE INDEX index_sum ON orders (created_at , total);
-- Section2 
CREATE INDEX index_sum_two_condition ON orders (user_id , created_at , total  )
-- Section3
