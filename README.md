# EV Market Intelligence

> **College Data Analytics Project — EV Insights Dashboard & Web Integration**
> Synthetic EV market dataset · 199,999 records · 37 features · Tableau Public + Flask + SQLite

[![Live Dashboard](https://img.shields.io/badge/Tableau-Dashboard-blue)](https://public.tableau.com/shared/Q27K39PSC)
[![Live Story](https://img.shields.io/badge/Tableau-Story-green)](https://public.tableau.com/views/EV_Market_Intelligence/Story1)
![Live WebPage](https://ev-market-intelligence.onrender.com/)

---

## 📋 Project Overview

This project performs end-to-end analysis of a synthetic Electric Vehicle market dataset through:

- **9 Tableau visualizations** across market share, sales trends, battery technology, geography, pricing, and range.
- **3-scene Tableau Story** covering Commercial Strategy, Competitive Intelligence, and Sustainability Research.
- **SQLite database** with 10 analytical SQL queries.
- **Flask web application** embedding the live Tableau Public views and serving live KPI data from SQLite.

> **Dataset Notice**: All data is synthetically/procedurally generated for educational purposes. Values do not represent real-world market facts.

---

## 📁 Project Structure

```
EV-Market-Intelligence/
├── flask_app/
│   ├── app.py              # Flask routes and SQLite API
│   ├── requirements.txt    # Python dependencies
│   └── templates/
│       └── index.html      # Single-page web app with Tableau embeds
├── sql/
│   └── ev_market_queries.sql  # 10 analytical SQL queries
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   ├── DEMO_VIDEO_SCRIPT.md
│   ├── COLLEGE_REQUIREMENTS_CHECKLIST.md
│   └── SQL_ANALYTICAL_RESULTS.md
├── scripts/
│   ├── prepare_ev_data.py     # Data cleaning and DB loader
│   └── verify_data_and_db.py  # Data/DB integrity verification
├── data/                   # ⚠ Large files — not committed to Git
│   ├── ev_market_clean.csv # (199,999 rows, 37 cols) — regenerate with prepare_ev_data.py
│   └── ev_market.db        # SQLite database — regenerate with prepare_ev_data.py
├── .env.example            # Environment variable template
├── .gitignore
├── render.yaml             # Render.com deployment config
└── TABLEAU_CHART_PLAN.md   # Chart-by-chart build specification
```

---

## 🚀 Quick Start (Local)

### 1. Clone and set up environment

```bash
git clone https://github.com/YOUR_USERNAME/EV-Market-Intelligence.git
cd EV-Market-Intelligence
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r flask_app/requirements.txt
```

### 2. Prepare the database

The SQLite database and CSV are not committed (too large). Regenerate them:

```bash
python scripts/prepare_ev_data.py
python scripts/verify_data_and_db.py
```

### 3. Configure environment variables

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Edit `.env` — the Tableau URLs are already set to the live published views.

### 4. Run Flask locally

```bash
cd flask_app
flask --app app run --port 5000
```

Or from the root:

```bash
python flask_app/app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔗 Tableau Public Links

| View | URL |
|------|-----|
| **Dashboard** | https://public.tableau.com/shared/Q27K39PSC |
| **Story (3 scenes)** | https://public.tableau.com/views/EV_Market_Intelligence/Story1 |

---

## 🌐 Deployment (Render)

1. Push this repository to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service** → Connect your GitHub repo.
3. Render will detect `render.yaml` automatically and configure the build.
4. Set any extra environment variables in the Render dashboard if needed.
5. The app will be live at `https://ev-market-intelligence.onrender.com` (or similar).

**Production start command** (also in `render.yaml`):

```bash
gunicorn --chdir flask_app app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

---

## 🛠 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Main web app with Tableau embeds and KPI cards |
| `GET /health` | Health check — returns DB connection status and record count |
| `GET /api/kpis` | JSON: total records, sales, avg range, avg price, avg rating |
| `GET /api/region-sales` | JSON: sales and rating aggregated by market region |
| `GET /api/battery-tech` | JSON: battery chemistry comparison data |

---

## 📊 Visualizations (9 Charts + KPI Overview)

1. EV Category Performance & Distribution (Horizontal Bar)
2. Market Share by Manufacturer — Top 10 (Sorted Bar)
3. Customer Rating Records by EV Category (Column Chart)
4. Annual EV Sales Trend by Model Year (Line Chart)
5. Battery Technology Market Share (Treemap)
6. EV Distribution by Manufacturing Country (Map / Bar)
7. Driving Range vs Battery Capacity (Scatter Plot)
8. Average Price by Vehicle Category (Lollipop / Bar)
9. Battery Degradation & Efficiency Matrix (Highlight Table)

**Dashboard filters**: Market Region · Category · Model Year · Battery Type

---

## 📋 Assignment Requirements Coverage

| Requirement | Status |
|-------------|--------|
| Problem definition | ✅ |
| Data collection & extraction | ✅ |
| Database (SQLite) | ✅ |
| SQL operations (10 queries) | ✅ |
| Tableau connection (CSV data source) | ✅ Documented |
| Data preparation | ✅ |
| 9+ unique visualizations | ✅ |
| Responsive dashboard | ✅ |
| Tableau story (3 scenes) | ✅ |
| Performance testing evidence | ✅ Docs |
| Published to Tableau Public | ✅ |
| Flask web integration with embeds | ✅ |
| Demo video script | ✅ |
| Project documentation | ✅ |

---

## 📄 License

Educational use only. Dataset is synthetic and procedurally generated.


[https://ev-market-intelligence.onrender.com/]: https://ev-market-intelligence.onrender.com/