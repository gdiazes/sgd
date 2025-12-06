
  
    

  create  table "db_dbt"."public"."my_first_model__dbt_tmp"
  
  
    as
  
  (
    -- models/example/my_first_model.sql



SELECT
    1 as id,
    'hello dbt' as message,
    NOW() as created_at
  );
  