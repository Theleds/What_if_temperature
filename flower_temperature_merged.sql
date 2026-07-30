CREATE OR REPLACE TABLE `Flowers_data.flower_temperature_merged` AS
SELECT 
    w.year,
    w.month,
    e.month_name,
    e.fob_usd_thousands AS miles_fob_monthly,
    e.net_tons_exported AS ton_monthly,
    w.avg_temperature AS temperature_monthly,
    w.frost_days_under_2 AS days_under_2,
    w.frost_days_under_0 AS days_under_0
FROM `Flowers_data.temperature_resume` w
INNER JOIN `Flowers_data.flower_resume` e
    ON w.year = e.year 
   AND w.month = e.month_num
WHERE w.department = 'BOGOTÁ'
ORDER BY w.year, w.month;