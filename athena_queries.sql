-- Athena Query Examples for Weather Data
-- Replace DATABASE_NAME and TABLE_NAME with your actual database and table names

-- 1. Get latest weather data
SELECT *
FROM weather_db_weatherpipelinestack.weather_data
ORDER BY timestamp DESC
LIMIT 10;

-- 2. Get average temperature by hour for today
SELECT 
    hour,
    AVG(temperature) as avg_temperature,
    MIN(temperature) as min_temperature,
    MAX(temperature) as max_temperature,
    COUNT(*) as record_count
FROM weather_db_weatherpipelinestack.weather_data
WHERE year = CAST(YEAR(CURRENT_DATE) AS VARCHAR)
  AND month = LPAD(CAST(MONTH(CURRENT_DATE) AS VARCHAR), 2, '0')
  AND day = LPAD(CAST(DAY(CURRENT_DATE) AS VARCHAR), 2, '0')
GROUP BY hour
ORDER BY hour;

-- 3. Get weather statistics by day
SELECT 
    year,
    month,
    day,
    AVG(temperature) as avg_temp,
    AVG(humidity) as avg_humidity,
    AVG(pressure) as avg_pressure,
    AVG(wind_speed) as avg_wind_speed,
    COUNT(*) as record_count
FROM weather_db_weatherpipelinestack.weather_data
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 30;

-- 4. Find hottest and coldest days
SELECT 
    year,
    month,
    day,
    MAX(temperature) as max_temp,
    MIN(temperature) as min_temp,
    AVG(temperature) as avg_temp
FROM weather_db_weatherpipelinestack.weather_data
WHERE year = CAST(YEAR(CURRENT_DATE) AS VARCHAR)
GROUP BY year, month, day
ORDER BY max_temp DESC
LIMIT 10;

-- 5. Weather conditions distribution
SELECT 
    weather_main,
    weather_description,
    COUNT(*) as occurrence_count,
    AVG(temperature) as avg_temp,
    AVG(humidity) as avg_humidity
FROM weather_db_weatherpipelinestack.weather_data
GROUP BY weather_main, weather_description
ORDER BY occurrence_count DESC;

-- 6. Wind analysis
SELECT 
    hour,
    AVG(wind_speed) as avg_wind_speed,
    AVG(wind_deg) as avg_wind_direction,
    MAX(wind_speed) as max_wind_speed
FROM weather_db_weatherpipelinestack.weather_data
WHERE year = CAST(YEAR(CURRENT_DATE) AS VARCHAR)
  AND month = LPAD(CAST(MONTH(CURRENT_DATE) AS VARCHAR), 2, '0')
GROUP BY hour
ORDER BY hour;

-- 7. Time series data for specific date range
SELECT 
    timestamp,
    temperature,
    humidity,
    pressure,
    wind_speed,
    weather_description
FROM weather_db_weatherpipelinestack.weather_data
WHERE year = '2024'
  AND month = '01'
  AND day BETWEEN '01' AND '07'
ORDER BY timestamp;

-- 8. Partition information (verify partitions are working)
SHOW PARTITIONS weather_db_weatherpipelinestack.weather_data;

-- 9. Table schema verification
DESCRIBE weather_db_weatherpipelinestack.weather_data;

-- 10. Count records by partition
SELECT 
    year,
    month,
    day,
    hour,
    COUNT(*) as record_count
FROM weather_db_weatherpipelinestack.weather_data
GROUP BY year, month, day, hour
ORDER BY year DESC, month DESC, day DESC, hour DESC
LIMIT 100;

