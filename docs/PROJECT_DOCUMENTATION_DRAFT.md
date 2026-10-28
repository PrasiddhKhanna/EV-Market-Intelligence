# EV Market Intelligence Dashboard — Project Documentation (Draft)

## 1. Problem Understanding
The project demonstrates how structured electric-vehicle market attributes can be stored, queried, cleaned and visualized to help stakeholders compare the vehicle categories, regions, manufacturers and battery technologies represented in a dataset. The objective is to make comparisons accessible through KPIs, charts, filters and a short visual story.

## 2. Dataset and limitations
The provided source contains `ev_market_train.csv` (200,000 rows before cleaning) and `ev_market_test.csv` (100,000 rows). Each has 37 columns. The source page explicitly labels the rows as procedurally generated and the maker/model names as fictional. Consequently, results are illustrative and must not be used as real-world EV market facts. This draft uses the training file for descriptive analysis and leaves the test file separate.

## 3. Data collection and extraction
The dataset was downloaded from the course-linked dataset page. The original CSV is retained separately. The cleaned analysis file is `data/ev_market_clean.csv`.

## 4. Data preparation
The initial training file has one exact duplicate row / duplicate vehicle identifier. The cleaning script removes exact duplicate rows. Five numeric columns contain missing values: `battery_cycle_life`, `resale_value_pct_3yr`, `infotainment_screen_inch`, `annual_sales_units`, and `customer_rating`. For the ready-to-use analysis file, missing numeric values in columns with gaps are filled using that column's median; categorical fields are not invented or filled. This imputation choice should be mentioned as a limitation, and a future version could compare results with missing rows excluded. See `data_quality_report.json` for the actual counts and medians.

## 5. Database and SQL operations
The supplied SQLite database is `data/ev_market.db` and contains table `ev_market_clean`. SQL query examples in `sql/ev_market_queries.sql` calculate KPIs, region totals, model-year comparisons, category performance, battery-type comparisons, manufacturer leaders, country distribution, customer ratings, and data checks. Indexes are created on market region, model year, manufacturer and category.

### Tableau Public connector constraint
Tableau Desktop Public Edition supports file-based connectors such as CSV and Excel, but its connector list is limited and does not include direct local SQLite connections. The recommended workflow for this setup is to execute database operations in SQLite and connect Tableau Public to the prepared CSV file that contains the same cleaned records. This is a file-based handoff, not a direct database connection. If the evaluator specifically demands a direct live DB connector, confirm whether the college provides a full Tableau Desktop license / approved connector. Tableau Public itself uses extracts rather than live database connections.

## 6. Visualization plan
- Sales by market region (bar chart)
- Sales by model year (line chart; represents model-year cohorts, not longitudinal calendar sales)
- Sales by vehicle category (bar chart)
- Average driving range by battery technology (bar chart)
- Top 10 manufacturers by recorded sales (bar chart)
- Category average price versus range (scatter plot)
- Customer rating by category (bar chart)

## 7. Dashboard design
Use a clear title, four headline KPIs, a primary comparison row, a technology / manufacturer row, and filters for model year, market region, category, battery technology and manufacturer. Prefer readable typography, consistent color use and minimal gridlines. The project is described as an analysis of a synthetic dataset in its title or subtitle.

## 8. Story
Three story scenes: (1) regional and category distribution; (2) battery technology and range/price comparisons; (3) manufacturer and customer-rating comparisons. Each scene should use cautious descriptive language and avoid causal claims.

## 9. Performance testing
Record row count, render time for each dashboard sheet, filter interaction results and whether all worksheets update as expected. Use Tableau's performance recording feature if available; otherwise use a stopwatch and log repeated trials. Do not claim performance metrics until they are actually measured.

## 10. Web integration
Publish the dashboard and story to Tableau Public, copy the Share/embed URL, and paste it into the Flask app's environment variable `TABLEAU_EMBED_URL`. Run Flask locally and test that the iframe loads. Tableau Public content is public.

## 11. Demonstration video outline (3–5 minutes)
1. Introduce the problem and synthetic dataset.
2. Explain cleaning choices and SQLite storage.
3. Show 2–3 SQL queries and their outputs.
4. Walk through KPIs, worksheets, filters and story scenes.
5. Show the Flask page embedding the published Tableau view.
6. State limitations: synthetic data, imputation, sample-based observations, and the Tableau Public connector constraint.

## 12. Conclusion
This project demonstrates a reproducible data workflow from collection and cleaning through SQL queries, visualization, storytelling and web embedding. Any conclusions refer only to the provided synthetic dataset.
