#!/usr/bin/env python3
"""End-to-end regression test suite for EV Market Intelligence Project."""
import unittest
import sqlite3
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
from tableaudocumentapi import Workbook

WORKSPACE = Path(__file__).resolve().parent.parent
CSV_PATH = WORKSPACE / "data" / "ev_market_clean.csv"
DB_PATH = WORKSPACE / "data" / "ev_market.db"
SQL_PATH = WORKSPACE / "sql" / "ev_market_queries.sql"
TWB_PATH = WORKSPACE / "tableau" / "EV_Market_Intelligence.twb"
TWBX_PATH = WORKSPACE / "tableau" / "EV_Market_Intelligence.twbx"

# Import Flask app
import sys
sys.path.insert(0, str(WORKSPACE / "flask_app"))
from app import app

class TestEVProjectPipeline(unittest.TestCase):

    def test_01_cleaned_csv_integrity(self):
        """Verify cleaned CSV row count, schema, nulls, and duplicates."""
        self.assertTrue(CSV_PATH.exists(), "Cleaned CSV does not exist")
        df = pd.read_csv(CSV_PATH)
        self.assertEqual(len(df), 199999, f"Expected 199,999 rows, found {len(df)}")
        self.assertEqual(len(df.columns), 37, f"Expected 37 columns, found {len(df.columns)}")
        self.assertEqual(int(df.isna().sum().sum()), 0, "Found unexpected null values in clean dataset")
        self.assertEqual(int(df.duplicated().sum()), 0, "Found unexpected duplicate rows in clean dataset")

    def test_02_sqlite_database_integrity(self):
        """Verify SQLite table, record count, and index structure."""
        self.assertTrue(DB_PATH.exists(), "SQLite database does not exist")
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [r[0] for r in cur.fetchall()]
            self.assertIn("ev_market_clean", tables, "Table 'ev_market_clean' missing from SQLite DB")
            
            cur.execute("SELECT COUNT(*) FROM ev_market_clean;")
            count = cur.fetchone()[0]
            self.assertEqual(count, 199999, f"DB row count mismatch: {count}")

            cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_ev_%';")
            indexes = [r[0] for r in cur.fetchall()]
            self.assertGreaterEqual(len(indexes), 4, f"Expected at least 4 indexes, found {indexes}")

    def test_03_sql_queries_execution(self):
        """Execute all queries from sql/ev_market_queries.sql and verify results."""
        self.assertTrue(SQL_PATH.exists(), "SQL script does not exist")
        with open(SQL_PATH, 'r', encoding='utf-8') as f:
            sql_text = f.read()
        
        blocks = [b.strip() for b in sql_text.split(';') if b.strip()]
        self.assertGreaterEqual(len(blocks), 10, "Expected at least 10 SQL queries")
        
        with sqlite3.connect(DB_PATH) as con:
            for idx, block in enumerate(blocks, 1):
                clean_lines = [l for l in block.splitlines() if not l.strip().startswith('--')]
                query = "\n".join(clean_lines).strip()
                if not query:
                    continue
                df = pd.read_sql_query(query, con)
                self.assertGreater(len(df), 0, f"Query {idx} returned 0 rows: {query[:60]}")
                self.assertGreater(len(df.columns), 0, f"Query {idx} returned 0 columns")

    def test_04_tableau_twb_structure(self):
        """Verify Tableau .twb XML schema and document API introspection."""
        self.assertTrue(TWB_PATH.exists(), "Tableau .twb file does not exist")
        
        # XML Parse check
        tree = ET.parse(TWB_PATH)
        root = tree.getroot()
        self.assertEqual(root.tag, "workbook", "Root XML tag is not 'workbook'")
        
        # Document API check
        wb = Workbook(str(TWB_PATH))
        self.assertEqual(len(wb.worksheets), 11, f"Expected 11 worksheets, found {len(wb.worksheets)}")
        self.assertEqual(len(wb.dashboards), 1, f"Expected 1 dashboard, found {len(wb.dashboards)}")
        self.assertEqual(len(wb.datasources), 1, f"Expected 1 datasource, found {len(wb.datasources)}")
        
        # Verify 5 calculated fields
        ds = wb.datasources[0]
        calc_fields = [f.name for f in ds.fields.values() if f.calculation is not None]
        expected_calcs = [
            'Sales (K)',
            'Price per KM of Range',
            'Battery Capacity per 100 KM',
            'High Customer Rating',
            'Model Age'
        ]
        for ec in expected_calcs:
            self.assertIn(ec, calc_fields, f"Calculated field '{ec}' missing from Tableau datasource")

    def test_05_tableau_twbx_packaged_workbook(self):
        """Verify packaged .twbx ZIP container and internal files."""
        self.assertTrue(TWBX_PATH.exists(), "Tableau .twbx file does not exist")
        self.assertGreater(TWBX_PATH.stat().st_size, 10_000_000, "Packaged workbook size unusually small")
        
        with zipfile.ZipFile(TWBX_PATH, 'r') as zf:
            file_list = zf.namelist()
            self.assertIn("EV_Market_Intelligence.twb", file_list, ".twb missing from .twbx root")
            self.assertIn("Data/ev_market_clean.csv", file_list, "Packaged CSV missing from .twbx Data/")
        
        # Document API check on twbx
        wb_pkg = Workbook(str(TWBX_PATH))
        self.assertEqual(len(wb_pkg.worksheets), 11)
        self.assertEqual(len(wb_pkg.dashboards), 1)

    def test_06_flask_app_endpoints(self):
        """Verify Flask web server routes and live database integrations."""
        client = app.test_client()
        
        # /health
        res_health = client.get('/health')
        self.assertEqual(res_health.status_code, 200)
        data_health = res_health.get_json()
        self.assertEqual(data_health.get('status'), 'ok')
        self.assertTrue(data_health.get('database_connected'))
        self.assertEqual(data_health.get('records_loaded'), 199999)

        # / (Home page)
        res_home = client.get('/')
        self.assertEqual(res_home.status_code, 200)
        self.assertIn(b"EV Market Intelligence", res_home.data)
        self.assertIn(b"199,999", res_home.data)

        # / with embed param
        test_url = "https://public.tableau.com/views/Test/View"
        res_embed = client.get(f'/?dashboard_url={test_url}')
        self.assertEqual(res_embed.status_code, 200)
        self.assertIn(test_url.encode('utf-8'), res_embed.data)

        # /api/kpis
        res_kpi = client.get('/api/kpis')
        self.assertEqual(res_kpi.status_code, 200)
        kpi_json = res_kpi.get_json()
        self.assertEqual(kpi_json['total_records'], 199999)
        self.assertEqual(int(kpi_json['total_sales']), 1558703498)

        # /api/region-sales
        res_region = client.get('/api/region-sales')
        self.assertEqual(res_region.status_code, 200)
        self.assertEqual(len(res_region.get_json()), 7)

        # /api/battery-tech
        res_battery = client.get('/api/battery-tech')
        self.assertEqual(res_battery.status_code, 200)
        self.assertEqual(len(res_battery.get_json()), 5)

if __name__ == '__main__':
    unittest.main()
