# EV Market Intelligence System — Comprehensive Project Documentation

**Project Title:** Electric Vehicle Market Intelligence & Analytical Intelligence Platform  
**Academic Submission Date:** October 28, 2026  
**Tools & Technologies:** Tableau Public Desktop 2026.3, Python 3.11, SQLite 3, Flask 3.1, Pandas 3.1, HTML5/CSS3  
**Dataset Reference:** EV Market Intelligence Dataset (Cleaned: 199,999 records, 37 columns)

---

## 1. Executive Summary & Problem Understanding
The global transition toward electric mobility requires clear analytical visibility into vehicle adoption, battery chemistries, pricing elasticity, range trade-offs, and consumer satisfaction. 

This project delivers an end-to-end data analytics solution:
1. **Data Ingestion & Cleaning:** Audited raw corpus of 200,000 records, deduplicated records, and imputed missing values via median imputation.
2. **Relational Database Warehouse:** Built a normalized SQLite warehouse (`data/ev_market.db`) with 4 B-tree performance indexes.
3. **Advanced SQL Query Pack:** Authored and verified 10 core analytical queries calculating headline KPIs, regional demand, cohort dynamics, battery degradation, and manufacturer market share.
4. **Tableau Business Intelligence Workbook:** Programmed a genuine packaged Tableau workbook (`tableau/EV_Market_Intelligence.twbx`) with 11 specialized worksheets, 5 calculated fields, an executive multi-zone dashboard, and a 3-scene analytical story.
5. **Interactive Web Integration:** Built a responsive Flask application (`flask_app/app.py`) providing live SQLite API metrics and embedding the Tableau interactive visualizations.

> [!NOTE]
> **Dataset Nature:** The primary dataset is procedurally generated for academic benchmarking. Vehicle model and manufacturer names are fictional. Analytical insights represent cohort distributions rather than longitudinal real-world market facts.

---

## 2. Dataset Hygiene & Data Quality Evidence

### 2.1 Cleaning Pipeline
The ingestion script `scripts/prepare_ev_data.py` executes strict hygiene filters:
- **Deduplication:** Removes exact duplicate records using the primary entity key `vehicle_id`.
- **Numeric Imputation:** Retains categorical fidelity (no synthetic categories invented). Gaps in numeric columns are filled with the verified median of that feature to maintain distribution neutrality against extreme outliers.

### 2.2 Verified Cleaning Metrics (from `docs/data_quality_report.json`)
| Metric / Feature | Raw Value | Cleaned Value | Transformation Applied |
| :--- | :--- | :--- | :--- |
| **Total Record Count** | 200,000 | 199,999 | 1 duplicate row removed |
| **Total Features (Columns)** | 37 | 37 | Preserved all 37 schema attributes |
| `battery_cycle_life` nulls | 3,786 | 0 | Median imputed (`2031.0` cycles) |
| `resale_value_pct_3yr` nulls | 6,103 | 0 | Median imputed (`52.99%`) |
| `infotainment_screen_inch` nulls | 3,102 | 0 | Median imputed (`11.0` inches) |
| `annual_sales_units` nulls | 2,028 | 0 | Median imputed (`3,949.0` units) |
| `customer_rating` nulls | 3,977 | 0 | Median imputed (`4.10` / 5.0) |
| **Total Remaining Nulls** | 19,000 | **0** | Cleaned dataset is 100% complete |

---

## 3. Database Architecture & SQL Execution Evidence

The SQLite relational database (`data/ev_market.db`) stores the clean table `ev_market_clean` (69.5 MB). 

### 3.1 B-Tree Performance Indexes
```sql
CREATE INDEX idx_ev_region ON ev_market_clean(market_region);
CREATE INDEX idx_ev_year ON ev_market_clean(model_year);
CREATE INDEX idx_ev_manufacturer ON ev_market_clean(manufacturer);
CREATE INDEX idx_ev_category ON ev_market_clean(category);
```

### 3.2 Key Analytical SQL Query Findings
*Full query code and complete tables are preserved in [SQL_ANALYTICAL_RESULTS.md](file:///D:/EV_Tableau_Project_Starter_Kit/docs/SQL_ANALYTICAL_RESULTS.md).*

1. **Headline KPIs (Query Q1):**
   - Total Clean Records: `199,999`
   - Total Recorded Sales: `1,558,703,498 units` (~1.56B)
   - Average Driving Range: `324.5 km`
   - Average Vehicle Price: `$64,921 USD`
   - Average Customer Satisfaction: `4.09 / 5.00`

2. **Market Regional Distribution (Query Q2):**
   - **South Asia:** `225,154,801 units` (Avg Rating: 4.09)
   - **Latin America:** `224,550,443 units` (Avg Rating: 4.09)
   - **North America:** `223,732,954 units` (Avg Rating: 4.09)
   - **Europe:** `223,025,972 units` (Avg Rating: 4.09)
   - **East Asia:** `221,686,654 units` (Avg Rating: 4.09)
   - **Middle East:** `220,951,468 units` (Avg Rating: 4.09)
   - **Africa:** `219,601,206 units` (Avg Rating: 4.09)

3. **Battery Technology Performance (Query Q5):**
   | Battery Chemistry | Records | Avg Capacity (kWh) | Avg Range (km) | 5-Yr Degradation (%) | Total Sales Units |
   | :--- | :--- | :--- | :--- | :--- | :--- |
   | **NMC** | 67,672 | 78.3 | 324.3 | 14.03% | 526,947,105 |
   | **LFP** | 64,036 | 78.3 | 324.2 | 10.13% | 498,490,599 |
   | **Solid-State** | 35,888 | 78.3 | 325.2 | **5.06%** | 279,795,042 |
   | **Sodium-Ion** | 16,368 | 78.5 | 324.8 | 7.96% | 128,492,027 |
   | **NCA** | 16,035 | 78.4 | 324.6 | 12.06% | 124,978,725 |

---

## 4. Tableau Visualization & Story Architecture

### 4.1 Calculated Fields Implemented
All 5 required calculated fields are embedded into the data model:
1. **`Sales (K)`**  
   `SUM([annual_sales_units]) / 1000`  
   *Scales high-volume integer sales units into readable thousands.*
2. **`Price per KM of Range`**  
   `IF [range_km] > 0 THEN [price_usd] / [range_km] END`  
   *Evaluates capital efficiency per kilometer of autonomy.*
3. **`Battery Capacity per 100 KM`**  
   `IF [range_km] > 0 THEN [battery_capacity_kwh] / [range_km] * 100 END`  
   *Standard metric for vehicle electrical efficiency.*
4. **`High Customer Rating`**  
   `IF [customer_rating] >= 4 THEN "4+ Stars" ELSE "Below 4 Stars" END`  
   *Categorical satisfaction segmentation.*
5. **`Model Age`**  
   `2026 - [model_year]`  
   *Static benchmark age based on academic calendar year 2026.*

### 4.2 Worksheets Inventory (11 Total)
- `Sales by Region` (Horizontal bar chart sorted descending with values)
- `Sales by Model Year` (Continuous line chart showing cohort volumes)
- `Category Performance` (Bar chart with customer rating tooltip)
- `Battery Technology` (Bar chart comparing range by chemistry)
- `Manufacturer Leaders` (Top 10 filtered volume ranking)
- `Price vs Range` (Scatter plot by vehicle category)
- `Customer Ratings` (Bar chart showing rating distribution)
- `KPI Total Sales` (Headline card)
- `KPI Avg Range` (Headline card)
- `KPI Avg Price` (Headline card)
- `KPI Avg Rating` (Headline card)

### 4.3 Executive Dashboard Layout
Fixed dimension grid (`1300 x 900 px`):
- **Header:** Project title and academic subtitle.
- **KPI Row:** 4 KPI scorecards.
- **Primary Visuals:** Regional demand breakdown alongside Category volume.
- **Technology & Competition Row:** Battery technology, Top 10 manufacturers, and Price vs Range scatter plot.
- **Global Interactive Filters:** Interactive filtering across Model Year, Region, Category, Battery Type, and Manufacturer.

### 4.4 Story Points (3 Scenes)
- **Scene 1: Recorded Demand Concentration** — Evaluates geographic adoption clusters in South Asia and Latin America.
- **Scene 2: Technology Characteristics & Durability** — Analyzes why Solid-State battery chemistry achieves minimum degradation (5.06%) vs NMC (14.03%).
- **Scene 3: Strategic Decision-Maker Comparison** — Explores top manufacturers and customer rating consistency.

---

## 5. Web Application Integration (Flask)

The web tier is located in `flask_app/`:
- **`app.py`:** Flask server connecting to `data/ev_market.db`. Provides:
  - `GET /`: Renders UI with live SQLite headline metrics and embedded Tableau views.
  - `GET /health`: JSON system health check and database row count.
  - `GET /api/kpis`: REST endpoint returning live dataset aggregations.
  - `GET /api/region-sales`: REST endpoint returning regional sales distribution.
  - `GET /api/battery-tech`: REST endpoint returning chemistry analytics.
- **`templates/index.html`:** Modern dark-themed dashboard shell with live KPI cards, interactive tabs for Dashboard, Story, SQL insights, and an instantaneous URL tester form.
- **`RUN_FLASK_WINDOWS.bat`:** Automated launcher script with auto-detection of the Python 3.11 runtime.

---

## 6. Execution & Performance Benchmarks

### Verified Automated Test Results:
1. **Cleaned CSV Validation:** 199,999 rows, 37 columns, 0 missing values, 0 duplicates.
2. **SQLite Database Verification:** Table `ev_market_clean` verified with 199,999 records and 4 indexed keys. Average query execution time < 0.12s.
3. **Tableau Workbook Conformance:** XML schema parsed and validated by `tableaudocumentapi.Workbook`. All 11 sheets and calculated fields recognized. Packaged `.twbx` (17.4 MB) successfully launched and verified in Tableau Public Desktop 2026.3.
4. **Flask Web Endpoints:** All HTTP endpoints (`/`, `/health`, `/api/kpis`, `/api/region-sales`, `/api/battery-tech`) tested and returning HTTP 200 with valid JSON payloads.
