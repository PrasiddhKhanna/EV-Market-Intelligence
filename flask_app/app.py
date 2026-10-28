from flask import Flask, render_template, request, jsonify
import os
import sqlite3
from pathlib import Path

# Load .env if python-dotenv is installed (optional — env vars can be set directly)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

app = Flask(__name__)
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

WORKSPACE = Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE / "data" / "ev_market.db"

# Real published Tableau Public URLs (override via env vars if needed)
DEFAULT_DASHBOARD_URL = (
    "https://public.tableau.com/shared/Q27K39PSC"
    "?:showVizHome=no&:embed=true&:toolbar=yes&:display_count=n"
)
DEFAULT_STORY_URL = (
    "https://public.tableau.com/views/EV_Market_Intelligence/Story1"
    "?:showVizHome=no&:embed=true&:toolbar=yes&:display_count=n&:language=en-US"
)

@app.route('/')
def home():
    dashboard_url = (
        request.args.get('dashboard_url')
        or os.environ.get('TABLEAU_DASHBOARD_URL', '').strip()
        or DEFAULT_DASHBOARD_URL
    )
    story_url = (
        request.args.get('story_url')
        or os.environ.get('TABLEAU_STORY_URL', '').strip()
        or DEFAULT_STORY_URL
    )
    
    # Query live headline KPIs from SQLite
    kpis = {}
    try:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("""
                SELECT COUNT(*),
                       ROUND(SUM(annual_sales_units), 0),
                       ROUND(AVG(range_km), 1),
                       ROUND(AVG(price_usd), 0),
                       ROUND(AVG(customer_rating), 2)
                FROM ev_market_clean;
            """)
            row = cur.fetchone()
            if row:
                kpis = {
                    "total_records": f"{row[0]:,}",
                    "total_sales": f"{int(row[1]):,}",
                    "avg_range": f"{row[2]:.1f} km",
                    "avg_price": f"${int(row[3]):,}",
                    "avg_rating": f"{row[4]:.2f} / 5.0"
                }
    except Exception as e:
        kpis = {"error": str(e)}

    return render_template(
        'index.html',
        dashboard_url=dashboard_url,
        story_url=story_url,
        kpis=kpis
    )

@app.route('/health')
def health():
    db_exists = DB_PATH.exists()
    row_count = 0
    if db_exists:
        try:
            with sqlite3.connect(DB_PATH) as con:
                row_count = con.cursor().execute("SELECT COUNT(*) FROM ev_market_clean;").fetchone()[0]
        except Exception:
            pass
    return jsonify({
        'status': 'ok',
        'database_connected': db_exists,
        'records_loaded': row_count,
        'database_path': str(DB_PATH)
    })

@app.route('/api/kpis')
def get_kpis():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT COUNT(*) AS total_records,
                   ROUND(SUM(annual_sales_units), 0) AS total_sales,
                   ROUND(AVG(range_km), 1) AS avg_range,
                   ROUND(AVG(price_usd), 0) AS avg_price,
                   ROUND(AVG(customer_rating), 2) AS avg_rating
            FROM ev_market_clean;
        """)
        row = cur.fetchone()
        return jsonify({
            "total_records": row[0],
            "total_sales": row[1],
            "avg_range": row[2],
            "avg_price": row[3],
            "avg_rating": row[4]
        })

@app.route('/api/region-sales')
def region_sales():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT market_region, ROUND(SUM(annual_sales_units), 0) AS sales_units, ROUND(AVG(customer_rating), 2) AS avg_rating
            FROM ev_market_clean
            GROUP BY market_region ORDER BY sales_units DESC;
        """)
        rows = [{"region": r[0], "sales": r[1], "rating": r[2]} for r in cur.fetchall()]
        return jsonify(rows)

@app.route('/api/battery-tech')
def battery_tech():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT battery_type, COUNT(*) AS vehicle_records,
                   ROUND(AVG(battery_capacity_kwh),1) AS avg_capacity_kwh,
                   ROUND(AVG(range_km),1) AS avg_range_km,
                   ROUND(AVG(battery_degradation_pct_5yr),2) AS avg_5yr_degradation_pct,
                   ROUND(SUM(annual_sales_units),0) AS sales_units
            FROM ev_market_clean GROUP BY battery_type ORDER BY sales_units DESC;
        """)
        rows = [{"battery_type": r[0], "records": r[1], "capacity_kwh": r[2], "range_km": r[3], "degradation_pct": r[4], "sales": r[5]} for r in cur.fetchall()]
        return jsonify(rows)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
