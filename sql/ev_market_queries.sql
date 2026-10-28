-- EV Market Intelligence: SQLite query pack
-- Run these in DB Browser for SQLite, SQLiteStudio, or sqlite3 against data/ev_market.db.
-- Main table: ev_market_clean

-- Q1. Basic dataset / headline KPIs
SELECT COUNT(*) AS vehicle_records,
       COUNT(DISTINCT vehicle_id) AS unique_vehicles,
       ROUND(SUM(annual_sales_units), 0) AS total_recorded_sales_units,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(price_usd), 0) AS avg_price_usd,
       ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ev_market_clean;

-- Q2. Sales by market region
SELECT market_region, ROUND(SUM(annual_sales_units), 0) AS sales_units,
       ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ev_market_clean
GROUP BY market_region ORDER BY sales_units DESC;

-- Q3. Annual model-year sales trend (interpret as model-year cohort, not calendar sales history)
SELECT model_year, ROUND(SUM(annual_sales_units), 0) AS sales_units,
       COUNT(*) AS vehicle_records
FROM ev_market_clean GROUP BY model_year ORDER BY model_year;

-- Q4. Vehicle category performance
SELECT category, ROUND(SUM(annual_sales_units),0) AS sales_units,
       ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(price_usd),0) AS avg_price_usd,
       ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_market_clean GROUP BY category ORDER BY sales_units DESC;

-- Q5. Battery technology comparison
SELECT battery_type, COUNT(*) AS vehicle_records,
       ROUND(AVG(battery_capacity_kwh),1) AS avg_capacity_kwh,
       ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(battery_degradation_pct_5yr),2) AS avg_5yr_degradation_pct,
       ROUND(SUM(annual_sales_units),0) AS sales_units
FROM ev_market_clean GROUP BY battery_type ORDER BY sales_units DESC;

-- Q6. Top 10 manufacturers by recorded sales
SELECT manufacturer, ROUND(SUM(annual_sales_units),0) AS sales_units,
       COUNT(*) AS model_records, ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_market_clean GROUP BY manufacturer
ORDER BY sales_units DESC LIMIT 10;

-- Q7. Manufacturing countries
SELECT manufacturing_country, COUNT(*) AS vehicle_records,
       ROUND(SUM(annual_sales_units),0) AS sales_units,
       ROUND(AVG(range_km),1) AS avg_range_km
FROM ev_market_clean GROUP BY manufacturing_country ORDER BY sales_units DESC;

-- Q8. Price vs range by category
SELECT category, ROUND(AVG(price_usd),0) AS avg_price_usd,
       ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_market_clean GROUP BY category;

-- Q9. Customer ratings by battery type and category
SELECT battery_type, category, ROUND(AVG(customer_rating),2) AS avg_rating,
       COUNT(customer_rating) AS rating_records
FROM ev_market_clean GROUP BY battery_type, category
ORDER BY avg_rating DESC;

-- Q10. Quality checks: missingness in source values is addressed in the cleaned output;
-- source file has synthetic data and has one exact duplicate row removed.
SELECT COUNT(*) AS rows,
       COUNT(DISTINCT vehicle_id) AS distinct_ids,
       SUM(CASE WHEN annual_sales_units < 0 THEN 1 ELSE 0 END) AS negative_sales_rows,
       SUM(CASE WHEN range_km <= 0 THEN 1 ELSE 0 END) AS nonpositive_range_rows
FROM ev_market_clean;
