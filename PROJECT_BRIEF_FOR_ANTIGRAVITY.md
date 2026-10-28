# EV Market Performance & Insights — Authoritative Build Brief

**Deadline:** 28 October 2026  
**Required platform:** Native Tableau Public Desktop workbook, published to Tableau Public; Flask web integration is also required.

## Source of truth and workspace rules

- Work from the existing cleaned data and supporting project assets. The cleaned dataset is `ev_market_clean.csv` (199,999 rows, 37 columns in the current cleaned file); the original synthetic train/test CSVs must remain unchanged.
- Reuse the existing SQLite database, SQL query pack, data-preparation script and project documentation where valid. Inspect them before recreating anything.
- Keep the previous project folder intact as a backup. Build in a new clean final folder and copy only required assets into it.
- The data is synthetic/procedurally generated. State this clearly in the workbook/report and never present its values as real-world market facts.
- Do **not** generate or patch Tableau `.twb` XML by hand or with scripts. A prior generated workbook failed to open with Tableau XML schema errors. Build and validate the native workbook in the actual Tableau Public Desktop application. Programmatic utilities may inspect files but must not be treated as proof the workbook works.
- Do not claim work is complete because files exist or XML tests pass. Open the workbook in Tableau and visually test worksheets, dashboard, filters and story.
- Keep outputs and test evidence concise to conserve model quota. Avoid repeatedly scanning the full CSV or printing full rows; use targeted Python/SQL operations.

## Assignment requirements (from the college project page)

1. Define problem / problem understanding.
2. Data collection and extraction; collect/download the dataset.
3. Store data in a database.
4. Perform SQL operations.
5. Connect the database with Tableau (investigate actual supported connectors; do not falsely claim a connection if Tableau is using only a CSV).
6. Data preparation for visualization.
7. Data visualizations and count of unique visualizations.
8. Responsive dashboard design.
9. Tableau story with multiple scenes and count of scenes.
10. Performance testing: amount of data rendered, utilization of filters, number of calculated fields, and number of visualizations/graphs.
11. Publish dashboard and story to Tableau Public.
12. Embed dashboard and story with Flask.
13. Record a 5–7 minute end-to-end explanation video.
14. Write step-by-step project development documentation using the required college template if available.

### Visualization-count target and exact chart titles

The college portal is inconsistent: one rubric description says **9 unique visualizations**, while another page lists these **7 visualization titles**. To avoid under-delivering, create **at least 9 genuinely distinct chart worksheets**, not counting KPI cards alone. Cover all seven named analysis areas below. The title “EV Market Performance at a Glance” may be a KPI overview, but it does not replace the nine actual charts. Include the following seven topics and add at least two further distinct charts supported by real fields.

1. EV Market Performance at a Glance (KPI overview; useful for the dashboard but not counted among the nine chart worksheets if it only contains KPI cards).
2. EV Category Performance & Distribution.
3. Market Share by Manufacturer.
4. Customer Rating Records by EV Category.
5. Annual EV Sales Trend by Model Year.
6. Battery Technology Market Share.
7. Electric Vehicle Distribution by Manufacturing Country.
8. Driving Range vs Battery Capacity (or another valid range/efficiency comparison supported by the data).
9. Average Price by Vehicle Category (or another valid, non-duplicative analysis supported by the data).

The seven titles above are topics/views from the college page, not proof that the college requires exactly seven charts. The safest target is at least nine actual, distinct chart worksheets plus the KPI overview if built separately.

For each chart, verify the intended field aggregation and labels. Avoid misleading use of sums for ratings or averages where appropriate. Use only fields present in the actual dataset. Make a worksheet inventory listing every visualization and its purpose.

## Dashboard and story design

- Build one polished, responsive/readable Tableau dashboard using consistent formatting, clear titles, relevant tooltips and useful filters. Suggested filters: Manufacturer, Category, Manufacturing Country, Market Region, Model Year, and Battery Type where practical. Apply filters to relevant worksheets and test that they actually change the results.
- Do not cram every chart into one dashboard if readability suffers. The rubric asks for responsive/design quality and the count of visualizations; keep all unique chart worksheets in the workbook and place the main views on the dashboard in a readable layout.
- Make a Tableau Story with at least **3 scenes** based on the three stakeholder perspectives supplied in the project brief:
  1. Market strategy (sales, category demand, top manufacturers, customer ratings).
  2. Competitive/business intelligence (manufacturer comparisons, geography, battery technology).
  3. Sustainability research (range, efficiency, battery technology and satisfaction where supported).
- The underlying assignment’s Story section gives a scenario about global EV manufacturing footprint, production regions and supply-chain concentration. Include this geographic/manufacturing analysis where supported by available fields.

## SQL, database, and data quality

- Verify the SQLite database table schema and row count; execute all supplied SQL queries and capture valid results.
- Provide reproducible scripts for database load and SQL execution.
- Check duplicates, missing values, types and invalid ranges. Document exactly what cleaning was done; do not claim zero missing values unless verified in the final cleaned file.
- Since Tableau Public’s available local database connectors can be limited, investigate whether a genuine supported database connection is possible on this setup. If not, use the cleaned CSV for the native Tableau workbook, clearly document the SQLite SQL pipeline as a separate part, and explicitly flag the connector limitation instead of claiming Tableau is connected to SQLite. Do not let this block delivery of the required workbook.

## Flask web integration

- Reuse and test the existing Flask project.
- Provide separate, clearly labelled dashboard and story embed areas.
- Use the real Tableau Public published URL once the user publishes the workbook. Until then, use an obvious configurable placeholder. Never invent a live URL.
- Test the Flask endpoints locally, but distinguish local app testing from a real published Tableau embed test.

## Final deliverables checklist

- Native Tableau workbook that opens in Tableau Public Desktop, preferably saved/published as `.twbx` via the actual Tableau application.
- At least 9 distinct visualization worksheets, one readable interactive dashboard, and at least 3 story scenes.
- SQLite DB, SQL queries, execution results, data-quality report and preparation script.
- Tested Flask app with dashboard/story embedding configuration.
- Step-by-step project documentation, data dictionary, methodology, limitations and verified performance-test results.
- 5–7 minute demo-video script and a final manual submission checklist.
- Requirement-to-evidence matrix showing **Done / Partly done / Not done**, with evidence paths. Do not mark publishing or live embedding complete until the published links have been tested.

## Execution instructions

First inspect the source assets and actual field names. Then build the native Tableau workbook through the real Tableau GUI if reliable GUI automation is available. If GUI control is unavailable, say so immediately and give the user only the minimum precise manual actions needed; continue working on the SQL, Flask, documentation and validation in parallel. Prioritize a functioning deliverable over cosmetic extras. Never stop after writing a plan: execute what tools can genuinely perform, test it, and report concrete outcomes in under 200 words.
