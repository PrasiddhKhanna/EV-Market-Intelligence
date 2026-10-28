# EV Market Intelligence — Demonstration Video Script (3–5 Minutes)

**Presenter Target Duration:** 3 minutes 30 seconds to 4 minutes 30 seconds  
**Objective:** Present the end-to-end data pipeline, SQL database operations, Tableau interactive dashboard, visual story points, and web integration for college grading.

---

## Video Scene Breakdown & Timings

### [00:00 – 00:45] Scene 1: Introduction & Problem Scope
- **Visual on Screen:** Title slide or Flask web application header showing "EV Market Intelligence".
- **Speaker:**
  > "Hello everyone. Today I am presenting my College Data Analytics Project: the **EV Market Intelligence Platform**.
  > With electric vehicle adoption accelerating globally, automotive stakeholders need rapid visibility into consumer demand, battery durability, and price elasticity across categories and regions.
  > For this project, we processed a comprehensive dataset of 200,000 vehicle records across 37 attributes. 
  > Before diving into the numbers, it is important to note that the dataset is procedurally generated for academic benchmarking, so our findings represent cohort patterns rather than real-world commercial rankings."

---

### [00:45 – 01:30] Scene 2: Data Cleaning & SQLite Database Architecture
- **Visual on Screen:** Split screen or code editor showing `scripts/prepare_ev_data.py`, `docs/data_quality_report.json`, and terminal running SQL queries.
- **Speaker:**
  > "We established a disciplined data preparation pipeline using Python and Pandas.
  > During data hygiene checks, we identified and eliminated duplicate records, reducing the corpus to exactly 199,999 valid vehicle entries.
  > Five numeric columns contained missing data—including battery cycle life, 3-year resale percentage, screen size, sales units, and customer rating. Rather than introducing artificial bias, we applied median imputation to preserve distribution stability.
  > We then loaded the clean data into a high-performance SQLite database (`ev_market.db`) and constructed B-tree indexes across market regions, model years, manufacturers, and categories to optimize query response times."

---

### [01:30 – 02:15] Scene 3: Analytical SQL Queries
- **Visual on Screen:** SQLite query tool (or the 'Live SQL Queries' tab in the Flask web app) highlighting Query Q1, Q2, and Q5.
- **Speaker:**
  > "Against our SQLite warehouse, we authored 10 dedicated analytical SQL queries.
  > First, Query 1 computes our headline KPIs: nearly 1.56 billion recorded vehicle cohort sales, an average driving range of 324.5 kilometers, and an average price of approximately \$64,920 USD.
  > Next, Query 2 analyzes geographic demand, showing strong volume distribution in South Asia and Latin America, driven largely by high-density urban transit and two-wheeler adoption.
  > In Query 5, we compare battery chemistries. While NMC and LFP represent the highest sales volumes, Solid-State battery technology demonstrated exceptional long-term durability, exhibiting only a 5.06% five-year degradation rate compared to over 14% for NMC."

---

### [02:15 – 03:15] Scene 4: Tableau Interactive Dashboard & 3-Scene Story
- **Visual on Screen:** Tableau Public Desktop opening `tableau/EV_Market_Intelligence.twbx`, clicking filters, and advancing through the 3 story points.
- **Speaker:**
  > "Now moving to our visual analytics in Tableau Public Desktop.
  > We developed 11 individual worksheets and 5 custom calculated fields—including Price per Kilometer of Range, Battery Capacity per 100 KM, and rating thresholds.
  > Here is the executive dashboard:
  > At the top, KPI cards present instant totals. In the center, regional demand is paired with Category Performance. At the bottom, battery technology comparisons and manufacturer rankings give an executive overview.
  > Global filters allow us to drill down seamlessly by model year, category, and battery type.
  > In addition, we built a 3-Scene Story:
  > - **Scene 1** isolates geographic demand concentration.
  > - **Scene 2** unpacks battery technology performance versus price.
  > - **Scene 3** provides a competitive benchmark of top manufacturers against consumer satisfaction ratings."

---

### [03:15 – 04:00] Scene 5: Flask Web Embedding & Conclusion
- **Visual on Screen:** Web browser navigating `http://127.0.0.1:5000`, showing live SQLite KPI cards, tab switching between Dashboard, Story, and SQL queries.
- **Speaker:**
  > "Finally, we wrapped the entire project in a modern Python Flask web application.
  > The web app queries our SQLite database live through REST endpoints to populate headline cards, while providing an embedded iframe container for the Tableau dashboard and story.
  > Users can also test and embed any published Tableau Public URL directly on the fly.
  > In summary, this project demonstrates a complete, professional data lifecycle: from raw data extraction and automated cleaning, to relational database querying, interactive Tableau visual storytelling, and full-stack web integration.
  > Thank you for watching!"

---

## Presentation Checklist for the Recording:
1. Ensure microphone is tested and clear.
2. Have Tableau Public Desktop pre-opened with `tableau/EV_Market_Intelligence.twbx`.
3. Have Flask web application running at `http://127.0.0.1:5000`.
4. Keep `docs/SQL_ANALYTICAL_RESULTS.md` or DB Browser for SQLite ready in a side window.
