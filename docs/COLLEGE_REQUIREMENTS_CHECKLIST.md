# College Data Analytics Requirements & Rubric Checklist

**Project Title:** EV Market Intelligence Platform  
**Target Deadline:** October 28, 2026  
**Status:** 100% Implemented, Verified, and Ready for Submission

---

## Academic Rubric Mapping & Verification Matrix

| College Requirement / Rubric Item | Project Implementation | Location / File Path | Verification Status |
| :--- | :--- | :--- | :--- |
| **1. Problem Formulation & Scope** | Problem statement, objectives, stakeholder value, and synthetic dataset disclosures documented. | `docs/PROJECT_DOCUMENTATION.md` (Section 1) | **VERIFIED** |
| **2. Data Extraction & Cleaning** | Automated duplicate row removal and median imputation on 5 numeric columns with gaps. | `scripts/prepare_ev_data.py`<br>`data/ev_market_clean.csv` | **VERIFIED** (199,999 rows, 0 nulls) |
| **3. Data Quality Documentation** | Evidence of before/after null counts, medians, and duplicate counts recorded. | `docs/data_quality_report.json` | **VERIFIED** (Exact duplicate: 1, 0 remaining nulls) |
| **4. Relational Database & SQL** | Normalized SQLite database with 4 B-tree performance indexes. | `data/ev_market.db`<br>`sql/ev_market_queries.sql` | **VERIFIED** (All 10 queries executed with 0 errors) |
| **5. SQL Query Evidence** | Output tables, row counts, and SQL code documented for evaluator inspection. | `docs/SQL_ANALYTICAL_RESULTS.md`<br>`docs/sql_results.json` | **VERIFIED** (Full markdown & JSON export) |
| **6. Calculated Fields (Minimum 3-5)** | 5 distinct calculated fields (`Sales (K)`, `Price per KM`, `Battery Capacity per 100 KM`, `High Customer Rating`, `Model Age`). | `tableau/EV_Market_Intelligence.twbx`<br>`scripts/build_tableau_workbook.py` | **VERIFIED** (Parsed by `tableaudocumentapi`) |
| **7. Specialized Visualizations** | 11 worksheets covering bar charts, continuous cohort line charts, scatter plots, and KPI cards. | `tableau/EV_Market_Intelligence.twbx` | **VERIFIED** (11 sheets built & tested) |
| **8. Interactive Dashboard** | Multi-zone grid layout with title, KPI metrics row, visual charts, and global interactive filters. | `tableau/EV_Market_Intelligence.twbx` | **VERIFIED** (Tested in Tableau Public Desktop 2026.3) |
| **9. Analytical Story (Multi-Scene)** | 3-Scene Story narrative exploring demand distribution, battery technology degradation, and manufacturer benchmarks. | `tableau/EV_Market_Intelligence.twbx` | **VERIFIED** (Scene 1, Scene 2, Scene 3 created) |
| **10. Web Application Embedding** | Flask web app providing live SQLite REST API and responsive Tableau embedding iframe. | `flask_app/app.py`<br>`flask_app/templates/index.html` | **VERIFIED** (Tested HTTP 200 on all endpoints) |
| **11. Demonstration Video Script** | Minute-by-minute speaking and visual guide designed for a 3–5 minute presentation recording. | `docs/DEMO_VIDEO_SCRIPT.md` | **VERIFIED** (Complete script with timestamps) |
| **12. Automated Regression Tests** | End-to-end Python test suite validating dataset, database, SQL, workbook XML, and Flask app. | `tests/test_pipeline_and_app.py` | **VERIFIED** (Automated test suite passing) |

---

## Detailed Component Status

### 1. Data Pipeline
- Original source files preserved untouched in root / `D:\ev cars data set\`.
- Cleaned CSV: `data/ev_market_clean.csv` (199,999 rows, 37 columns, 0 null values).
- Database: `data/ev_market.db` (Table: `ev_market_clean`, indexed on `market_region`, `model_year`, `manufacturer`, `category`).

### 2. Tableau Deliverables
- `tableau/EV_Market_Intelligence.twbx`: Authentic packaged Tableau workbook with embedded data.
- `tableau/EV_Market_Intelligence.twb`: Standalone XML workbook with relative link to `../data/ev_market_clean.csv`.
- `tableau/TABLEAU_BUILD_GUIDE.md`: Step-by-step instruction manual for manual reconstruction or modifications.

### 3. Web Application (Flask)
- Run launcher: `RUN_FLASK_WINDOWS.bat` (automatically locates Python 3.11).
- Endpoints verified:
  - `GET /` (Renders dashboard shell with live SQLite KPIs)
  - `GET /health` (Database status & record count)
  - `GET /api/kpis` (JSON KPI aggregations)
  - `GET /api/region-sales` (JSON regional demand data)
  - `GET /api/battery-tech` (JSON battery technology data)

### 4. Evaluator / Instructor Notes
- Connector transparency: As documented in Section 5 of `docs/PROJECT_DOCUMENTATION.md`, Tableau Public Desktop Edition uses file-based extracts and does not expose a native local SQLite live connector. Data was transformed and loaded into SQLite for relational queries, and packaged into the Tableau workbook for visualization handoff.
