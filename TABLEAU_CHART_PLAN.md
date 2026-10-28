# Tableau Chart & Workbook Plan: EV Market Performance & Intelligence

## 1. Verified Data Schema & Source Fields
- **Data Source**: `ev_market_clean.csv` (199,999 records, 37 columns, synthetic/procedurally generated benchmark dataset).
- **Core Validated Columns**:
  - Dimensions: `vehicle_id`, `model_name`, `manufacturer`, `model_year`, `manufacturing_country`, `market_region`, `category`, `battery_type`, `drivetrain`, `recommended_use_case`
  - Metrics: `annual_sales_units`, `price_usd`, `range_km`, `battery_capacity_kwh`, `battery_degradation_pct_5yr`, `customer_rating`, `efficiency_wh_per_km`, `top_speed_kmph`, `acceleration_0_100_sec`, `co2_saved_tons_per_year`

---

## 2. Global Interactive Filters (Dashboard-Level)
Configure these 4 interactive filters with **Apply to Worksheets > All Using This Data Source**:
1. `market_region` (Multiple Values dropdown / list)
2. `category` (Multiple Values dropdown)
3. `model_year` (Range of values / discrete slider: 2018–2026)
4. `battery_type` (Multiple Values list: LFP, NMC, NCA, LTO, Solid-State)

---

## 3. Recommended Tableau Calculated Fields
Only include calculations directly supported by verified numeric columns:
1. **`[Price per Km Range]`**
   - Formula: `SUM([price_usd]) / SUM([range_km])`
   - Purpose: Economic efficiency indicator per vehicle model/category.
2. **`[Energy Consumption kWh/100km]`**
   - Formula: `AVG([efficiency_wh_per_km]) / 10`
   - Purpose: Standard automotive metric for battery consumption efficiency.
3. **`[Customer Rating Sentiment Group]`**
   - Formula: `IF [customer_rating] >= 4.5 THEN "Top Tier (>=4.5)" ELSEIF [customer_rating] >= 4.0 THEN "Standard (4.0-4.4)" ELSE "Below Average (<4.0)" END`
   - Purpose: Categorizing customer satisfaction segments.

---

## 4. Visualizations Inventory (9 Required Charts + Variety of Types)

| # | Worksheet Title | Status | Chart Type | Dimensions & Shelves | Aggregation & Measure | Analytical Purpose |
|---|---|---|---|---|---|---|
| **1** | **EV Category Performance & Distribution** | **Already Built Manually** | Horizontal Bar Chart | Rows: `category`<br>Columns: `SUM(annual_sales_units)` | `SUM(annual_sales_units)` | Compare total adoption volume across 15 vehicle categories. |
| **2** | **Market Share by Manufacturer** | **Already Built Manually** | Horizontal Bar Chart (Sorted Top 10) | Rows: `manufacturer` (Top 10 filter by sales)<br>Columns: `SUM(annual_sales_units)` | `SUM(annual_sales_units)` | Identify top sales volume leaders and enterprise market concentration. |
| **3** | **Customer Rating Records by EV Category** | **Already Built Manually** | Column / Bar Chart | Columns: `category`<br>Rows: `COUNT(customer_rating)` | `COUNT(customer_rating)` / Record Count | Quantify review submission volume across vehicle classes. |
| **4** | **Annual EV Sales Trend by Model Year** | *To Build* | Line Chart with Trend Markers | Columns: `model_year` (Discrete)<br>Rows: `SUM(annual_sales_units)` | `SUM(annual_sales_units)` | Track sales trajectory across model years (cohort-level progression). |
| **5** | **Battery Technology Market Share** | *To Build* | Treemap (or Donut/Pie) | Detail / Label: `battery_type`<br>Size / Color: `SUM(annual_sales_units)` | `SUM(annual_sales_units)`, `% of Total` | Show market dominance among battery chemistries (NMC, LFP, NCA, LTO, Solid-State). |
| **6** | **Electric Vehicle Distribution by Manufacturing Country** | *To Build* | Filled Map / Geographic Symbol Map | Detail: `manufacturing_country`<br>Color / Size: `SUM(annual_sales_units)` | `SUM(annual_sales_units)`, `COUNT(vehicle_id)` | Visualize geographic manufacturing footprint and global production hubs. |
| **7** | **Driving Range vs Battery Capacity** | *To Build* | Scatter Plot with Trend Line | Columns: `battery_capacity_kwh`<br>Rows: `range_km`<br>Detail: `category`<br>Color: `battery_type` | `AVG(battery_capacity_kwh)`, `AVG(range_km)` | Assess pack energy density vs driving distance efficiency. |
| **8** | **Average Price by Vehicle Category** | *To Build* | Ordered Lollipop / Horizontal Bar Chart | Rows: `category`<br>Columns: `AVG(price_usd)`<br>Color: `AVG(price_usd)` | `AVG(price_usd)` | Benchmark average market price positioning across categories. |
| **9** | **Battery Degradation & Efficiency Matrix** | *To Build* | Heatmap / Highlight Table | Columns: `battery_type`<br>Rows: `category`<br>Color / Label: `AVG(battery_degradation_pct_5yr)` | `AVG(battery_degradation_pct_5yr)`, `AVG(efficiency_wh_per_km)` | Multi-variable engineering comparison of long-term battery health and energy efficiency. |

*(Optional Dashboard KPI Header: Single-value KPI cards for Total Sales `SUM(annual_sales_units)`, Average Price `AVG(price_usd)`, Average Range `AVG(range_km)`, and Average Rating `AVG(customer_rating)`).*

---

## 5. Tableau Story Plan (3 Stakeholder Scenarios)

### Scene 1: Commercial Market Strategy
- **Target Audience**: Chief Commercial Officer, Sales & Product Planning Directors.
- **Narrative Focus**: Volume drivers, category consumer demand, top 10 brand distribution, and overall market adoption.
- **Included Views**:
  - `EV Category Performance & Distribution`
  - `Market Share by Manufacturer`
  - `Annual EV Sales Trend by Model Year`
- **Key Takeaways**: Commercial volume is spearheaded by top manufacturers; commuter categories (e.g. Scooters, Hatchbacks) dominate unit volumes, requiring tailored regional pricing strategies.

### Scene 2: Competitive & Global Supply Chain Intelligence
- **Target Audience**: Strategy Executives, Procurement & Supply Chain Analysts.
- **Narrative Focus**: Geographic concentration of assembly, market region absorption, and battery chemistry adoption.
- **Included Views**:
  - `Electric Vehicle Distribution by Manufacturing Country`
  - `Battery Technology Market Share`
  - Global filters for `market_region` and `manufacturing_country`
- **Key Takeaways**: Manufacturing capacity is heavily centered across key global hubs; NMC and LFP chemistries control majority volume, while next-gen chemistries remain niche.

### Scene 3: Sustainable Engineering & Customer Experience
- **Target Audience**: Chief Technology Officer, R&D Leads, Fleet Sustainability Managers.
- **Narrative Focus**: Technical efficiency trade-offs, real-world range capability relative to pack size, degradation risks, and consumer satisfaction.
- **Included Views**:
  - `Driving Range vs Battery Capacity`
  - `Battery Degradation & Efficiency Matrix`
  - `Customer Rating Records by EV Category`
- **Key Takeaways**: Solid-state and LFP chemistries show lower 5-year degradation profiles; driving range scales reliably with pack capacity across commercial categories with consistent customer satisfaction.
