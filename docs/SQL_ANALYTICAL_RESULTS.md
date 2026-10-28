# EV Market Intelligence — Analytical SQL Results

This document captures the verified query execution results run against `data/ev_market.db` (Table: `ev_market_clean`, 199,999 records).

**Execution Timestamp:** 2026-10-27 | **Database:** SQLite 3 | **Dataset:** Cleaned Training Corpus

---

## Q1. Basic dataset / headline KPIs

```sql
SELECT COUNT(*) AS vehicle_records,
       COUNT(DISTINCT vehicle_id) AS unique_vehicles,
       ROUND(SUM(annual_sales_units), 0) AS total_recorded_sales_units,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(price_usd), 0) AS avg_price_usd,
       ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ev_market_clean
```

**Rows returned:** 1

|   vehicle_records |   unique_vehicles |   total_recorded_sales_units |   avg_range_km |   avg_price_usd |   avg_customer_rating |
|------------------:|------------------:|-----------------------------:|---------------:|----------------:|----------------------:|
|            199999 |            199999 |                   1.5587e+09 |          324.5 |           64921 |                  4.09 |

---

## Q2. Sales by market region

```sql
SELECT market_region, ROUND(SUM(annual_sales_units), 0) AS sales_units,
       ROUND(AVG(customer_rating), 2) AS avg_rating
FROM ev_market_clean
GROUP BY market_region ORDER BY sales_units DESC
```

**Rows returned:** 7

| market_region   |   sales_units |   avg_rating |
|:----------------|--------------:|-------------:|
| South Asia      |   2.25155e+08 |         4.09 |
| Latin America   |   2.2455e+08  |         4.09 |
| North America   |   2.23904e+08 |         4.09 |
| Middle East     |   2.2235e+08  |         4.09 |
| Asia Pacific    |   2.22185e+08 |         4.09 |
| Africa          |   2.218e+08   |         4.09 |
| Europe          |   2.1876e+08  |         4.09 |

---

## Q3. Annual model-year sales trend (interpret as model-year cohort, not calendar sales history)

```sql
SELECT model_year, ROUND(SUM(annual_sales_units), 0) AS sales_units,
       COUNT(*) AS vehicle_records
FROM ev_market_clean GROUP BY model_year ORDER BY model_year
```

**Rows returned:** 9

|   model_year |   sales_units |   vehicle_records |
|-------------:|--------------:|------------------:|
|         2018 |   1.72933e+08 |             22321 |
|         2019 |   1.77892e+08 |             22614 |
|         2020 |   1.72702e+08 |             21861 |
|         2021 |   1.66652e+08 |             22103 |
|         2022 |   1.71718e+08 |             21981 |
|         2023 |   1.73316e+08 |             22294 |
|         2024 |   1.77765e+08 |             22469 |
|         2025 |   1.74036e+08 |             22238 |
|         2026 |   1.71688e+08 |             22118 |

---

## Q4. Vehicle category performance

```sql
SELECT category, ROUND(SUM(annual_sales_units),0) AS sales_units,
       ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(price_usd),0) AS avg_price_usd,
       ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_market_clean GROUP BY category ORDER BY sales_units DESC
```

**Rows returned:** 15

| category            |   sales_units |   avg_range_km |   avg_price_usd |   avg_rating |
|:--------------------|--------------:|---------------:|----------------:|-------------:|
| Two-Wheeler Scooter |   1.7539e+08  |          105   |            2555 |         4.09 |
| Hatchback           |   1.55589e+08 |          279.7 |           23026 |         4.09 |
| Compact SUV         |   1.54154e+08 |          369.4 |           36472 |         4.09 |
| Sedan               |   1.53968e+08 |          429.6 |           42489 |         4.09 |
| Three-Wheeler       |   1.3377e+08  |          130.3 |            5504 |         4.09 |
| Crossover           |   1.32897e+08 |          395.1 |           41002 |         4.08 |
| Micro City Car      |   1.1597e+08  |          150.2 |           13009 |         4.09 |
| Luxury Sedan        |   1.15806e+08 |          550.6 |           90261 |         4.09 |
| Full-size SUV       |   1.1518e+08  |          474.6 |           85056 |         4.09 |
| Van / MPV           |   9.80693e+07 |          319.6 |           47554 |         4.09 |
| Luxury SUV          |   9.63199e+07 |          524.8 |          116295 |         4.09 |
| Sports Car          |   7.4315e+07  |          375.5 |          163593 |         4.09 |
| Electric Truck      |   1.33026e+07 |          225.6 |          167749 |         4.09 |
| Pickup Truck        |   1.3293e+07  |          390.7 |           68108 |         4.1  |
| Electric Bus        |   1.06809e+07 |          269.8 |          274543 |         4.08 |

---

## Q5. Battery technology comparison

```sql
SELECT battery_type, COUNT(*) AS vehicle_records,
       ROUND(AVG(battery_capacity_kwh),1) AS avg_capacity_kwh,
       ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(battery_degradation_pct_5yr),2) AS avg_5yr_degradation_pct,
       ROUND(SUM(annual_sales_units),0) AS sales_units
FROM ev_market_clean GROUP BY battery_type ORDER BY sales_units DESC
```

**Rows returned:** 5

| battery_type   |   vehicle_records |   avg_capacity_kwh |   avg_range_km |   avg_5yr_degradation_pct |   sales_units |
|:---------------|------------------:|-------------------:|---------------:|--------------------------:|--------------:|
| NMC            |             67672 |               78.3 |          324.3 |                     14.03 |   5.26947e+08 |
| LFP            |             64036 |               78.3 |          324.2 |                     10.13 |   4.98491e+08 |
| NCA            |             34099 |               77.9 |          325   |                     14.04 |   2.68497e+08 |
| Sodium-Ion     |             20089 |               78.1 |          325.9 |                     14.01 |   1.54157e+08 |
| Solid-State    |             14103 |               78.8 |          324.1 |                      7.44 |   1.10612e+08 |

---

## Q6. Top 10 manufacturers by recorded sales

```sql
SELECT manufacturer, ROUND(SUM(annual_sales_units),0) AS sales_units,
       COUNT(*) AS model_records, ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_market_clean GROUP BY manufacturer
ORDER BY sales_units DESC LIMIT 10
```

**Rows returned:** 10

| manufacturer     |   sales_units |   model_records |   avg_rating |
|:-----------------|--------------:|----------------:|-------------:|
| AmpereWorks      |   9.50455e+06 |            1067 |         4.09 |
| CircuitWorks     |   8.97446e+06 |            1054 |         4.1  |
| MomentumMobility |   8.82589e+06 |             995 |         4.11 |
| SurgeDynamics    |   8.8189e+06  |            1060 |         4.08 |
| TerraMotors      |   8.78561e+06 |            1048 |         4.08 |
| AmpereDynamics   |   8.76071e+06 |            1060 |         4.1  |
| VoltMobility     |   8.75809e+06 |            1039 |         4.08 |
| CurrentMotors    |   8.75106e+06 |            1031 |         4.1  |
| WattWheels       |   8.72123e+06 |            1058 |         4.1  |
| CircuitRides     |   8.68193e+06 |             992 |         4.07 |

---

## Q7. Manufacturing countries

```sql
SELECT manufacturing_country, COUNT(*) AS vehicle_records,
       ROUND(SUM(annual_sales_units),0) AS sales_units,
       ROUND(AVG(range_km),1) AS avg_range_km
FROM ev_market_clean GROUP BY manufacturing_country ORDER BY sales_units DESC
```

**Rows returned:** 10

| manufacturing_country   |   vehicle_records |   sales_units |   avg_range_km |
|:------------------------|------------------:|--------------:|---------------:|
| India                   |             20231 |   1.59958e+08 |          324.4 |
| China                   |             20052 |   1.59355e+08 |          326   |
| Vietnam                 |             19858 |   1.58067e+08 |          323.3 |
| UK                      |             20098 |   1.57558e+08 |          324.4 |
| South Korea             |             20138 |   1.56098e+08 |          325.5 |
| USA                     |             20086 |   1.56038e+08 |          324.5 |
| France                  |             19992 |   1.55783e+08 |          324.2 |
| Germany                 |             20009 |   1.5459e+08  |          323.9 |
| Sweden                  |             19921 |   1.52217e+08 |          325.9 |
| Japan                   |             19614 |   1.49039e+08 |          323.3 |

---

## Q8. Price vs range by category

```sql
SELECT category, ROUND(AVG(price_usd),0) AS avg_price_usd,
       ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(customer_rating),2) AS avg_rating
FROM ev_market_clean GROUP BY category
```

**Rows returned:** 15

| category            |   avg_price_usd |   avg_range_km |   avg_rating |
|:--------------------|----------------:|---------------:|-------------:|
| Compact SUV         |           36472 |          369.4 |         4.09 |
| Crossover           |           41002 |          395.1 |         4.08 |
| Electric Bus        |          274543 |          269.8 |         4.08 |
| Electric Truck      |          167749 |          225.6 |         4.09 |
| Full-size SUV       |           85056 |          474.6 |         4.09 |
| Hatchback           |           23026 |          279.7 |         4.09 |
| Luxury SUV          |          116295 |          524.8 |         4.09 |
| Luxury Sedan        |           90261 |          550.6 |         4.09 |
| Micro City Car      |           13009 |          150.2 |         4.09 |
| Pickup Truck        |           68108 |          390.7 |         4.1  |
| Sedan               |           42489 |          429.6 |         4.09 |
| Sports Car          |          163593 |          375.5 |         4.09 |
| Three-Wheeler       |            5504 |          130.3 |         4.09 |
| Two-Wheeler Scooter |            2555 |          105   |         4.09 |
| Van / MPV           |           47554 |          319.6 |         4.09 |

---

## Q9. Customer ratings by battery type and category

```sql
SELECT battery_type, category, ROUND(AVG(customer_rating),2) AS avg_rating,
       COUNT(customer_rating) AS rating_records
FROM ev_market_clean GROUP BY battery_type, category
ORDER BY avg_rating DESC
```

**Rows returned:** 75

| battery_type   | category            |   avg_rating |   rating_records |
|:---------------|:--------------------|-------------:|-----------------:|
| Solid-State    | Electric Bus        |         4.14 |              598 |
| Solid-State    | Sedan               |         4.12 |             1205 |
| NCA            | Micro City Car      |         4.11 |             2249 |
| Solid-State    | Compact SUV         |         4.11 |             1173 |
| Solid-State    | Van / MPV           |         4.11 |              787 |
| LFP            | Compact SUV         |         4.1  |             5446 |
| LFP            | Pickup Truck        |         4.1  |             3433 |
| LFP            | Van / MPV           |         4.1  |             3439 |
| NCA            | Compact SUV         |         4.1  |             2909 |
| NCA            | Full-size SUV       |         4.1  |             2180 |
| NCA            | Hatchback           |         4.1  |             2990 |
| NCA            | Sedan               |         4.1  |             2949 |
| NCA            | Sports Car          |         4.1  |             1374 |
| NCA            | Two-Wheeler Scooter |         4.1  |             3303 |
| NMC            | Luxury SUV          |         4.1  |             3547 |
| NMC            | Pickup Truck        |         4.1  |             3590 |
| NMC            | Sports Car          |         4.1  |             3023 |
| NMC            | Van / MPV           |         4.1  |             3602 |
| Sodium-Ion     | Electric Truck      |         4.1  |             1003 |
| Sodium-Ion     | Luxury Sedan        |         4.1  |             1331 |
| Solid-State    | Full-size SUV       |         4.1  |              890 |
| Solid-State    | Micro City Car      |         4.1  |              877 |
| Solid-State    | Pickup Truck        |         4.1  |              812 |
| Solid-State    | Three-Wheeler       |         4.1  |             1091 |
| LFP            | Full-size SUV       |         4.09 |             4122 |
| LFP            | Luxury SUV          |         4.09 |             3497 |
| LFP            | Luxury Sedan        |         4.09 |             4165 |
| LFP            | Micro City Car      |         4.09 |             4145 |
| LFP            | Sedan               |         4.09 |             5532 |
| LFP            | Sports Car          |         4.09 |             2696 |
| LFP            | Three-Wheeler       |         4.09 |             4734 |
| LFP            | Two-Wheeler Scooter |         4.09 |             6378 |
| NCA            | Electric Truck      |         4.09 |             1786 |
| NCA            | Pickup Truck        |         4.09 |             1828 |
| NCA            | Three-Wheeler       |         4.09 |             2572 |
| NMC            | Electric Truck      |         4.09 |             3610 |
| NMC            | Full-size SUV       |         4.09 |             4423 |
| NMC            | Luxury Sedan        |         4.09 |             4380 |
| Sodium-Ion     | Crossover           |         4.09 |             1476 |
| Sodium-Ion     | Full-size SUV       |         4.09 |             1299 |
| Sodium-Ion     | Hatchback           |         4.09 |             1700 |
| Sodium-Ion     | Pickup Truck        |         4.09 |             1122 |
| Sodium-Ion     | Sedan               |         4.09 |             1725 |
| Sodium-Ion     | Sports Car          |         4.09 |              894 |
| Sodium-Ion     | Three-Wheeler       |         4.09 |             1528 |
| Sodium-Ion     | Two-Wheeler Scooter |         4.09 |             1951 |
| Solid-State    | Crossover           |         4.09 |             1107 |
| Solid-State    | Electric Truck      |         4.09 |              764 |
| Solid-State    | Luxury Sedan        |         4.09 |              878 |
| Solid-State    | Two-Wheeler Scooter |         4.09 |             1354 |
| LFP            | Crossover           |         4.08 |             4696 |
| LFP            | Electric Bus        |         4.08 |             2776 |
| LFP            | Electric Truck      |         4.08 |             3456 |
| LFP            | Hatchback           |         4.08 |             5521 |
| NCA            | Crossover           |         4.08 |             2528 |
| NCA            | Electric Bus        |         4.08 |             1423 |
| NCA            | Van / MPV           |         4.08 |             1863 |
| NMC            | Compact SUV         |         4.08 |             5826 |
| NMC            | Crossover           |         4.08 |             5117 |
| NMC            | Electric Bus        |         4.08 |             2949 |
| NMC            | Hatchback           |         4.08 |             5714 |
| NMC            | Micro City Car      |         4.08 |             4271 |
| NMC            | Sedan               |         4.08 |             5823 |
| NMC            | Three-Wheeler       |         4.08 |             5131 |
| NMC            | Two-Wheeler Scooter |         4.08 |             6666 |
| Sodium-Ion     | Micro City Car      |         4.08 |             1266 |
| Solid-State    | Luxury SUV          |         4.08 |              762 |
| NCA            | Luxury SUV          |         4.07 |             1876 |
| NCA            | Luxury Sedan        |         4.07 |             2269 |
| Sodium-Ion     | Compact SUV         |         4.07 |             1783 |
| Sodium-Ion     | Electric Bus        |         4.07 |              872 |
| Solid-State    | Hatchback           |         4.07 |             1217 |
| Sodium-Ion     | Luxury SUV          |         4.06 |             1067 |
| Sodium-Ion     | Van / MPV           |         4.05 |             1072 |
| Solid-State    | Sports Car          |         4.04 |              588 |

---

## Query 11

```sql
SELECT COUNT(*) AS rows,
       COUNT(DISTINCT vehicle_id) AS distinct_ids,
       SUM(CASE WHEN annual_sales_units < 0 THEN 1 ELSE 0 END) AS negative_sales_rows,
       SUM(CASE WHEN range_km <= 0 THEN 1 ELSE 0 END) AS nonpositive_range_rows
FROM ev_market_clean
```

**Rows returned:** 1

|   rows |   distinct_ids |   negative_sales_rows |   nonpositive_range_rows |
|-------:|---------------:|----------------------:|-------------------------:|
| 199999 |         199999 |                     0 |                        0 |

---
