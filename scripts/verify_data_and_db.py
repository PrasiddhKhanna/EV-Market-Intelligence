#!/usr/bin/env python3
"""Verification of cleaned dataset, SQLite database, and SQL queries."""
import sqlite3
import re
import pandas as pd
from pathlib import Path

WORKSPACE = Path(r"D:\EV_Tableau_Project_Starter_Kit")
CSV_PATH = WORKSPACE / "data" / "ev_market_clean.csv"
DB_PATH = WORKSPACE / "data" / "ev_market.db"
SQL_PATH = WORKSPACE / "sql" / "ev_market_queries.sql"

print("--- 1. Verifying CSV Dataset ---")
df = pd.read_csv(CSV_PATH)
print(f"Rows: {len(df):,}, Columns: {len(df.columns)}")
null_counts = df.isna().sum()
total_nulls = null_counts.sum()
print(f"Total nulls in cleaned CSV: {total_nulls}")
print(f"Duplicates: {df.duplicated().sum()}")
print("Columns:", list(df.columns)[:10], f"... (+ {len(df.columns)-10} more)")

print("\n--- 2. Verifying SQLite Database ---")
with sqlite3.connect(DB_PATH) as con:
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Tables:", tables)
    cur.execute("SELECT COUNT(*) FROM ev_market_clean;")
    db_rows = cur.fetchone()[0]
    print(f"Row count in ev_market_clean: {db_rows:,}")
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indexes = [idx[0] for idx in cur.fetchall()]
    print("Indexes:", indexes)

print("\n--- 3. Verifying SQL Queries ---")
with open(SQL_PATH, 'r', encoding='utf-8') as f:
    sql_text = f.read()

# Split into distinct queries by semicolon while ignoring comments
queries = []
# Find query blocks starting with -- Q... or SELECT
raw_blocks = [b.strip() for b in sql_text.split(';') if b.strip()]

with sqlite3.connect(DB_PATH) as con:
    for idx, block in enumerate(raw_blocks, 1):
        # Extract title from comment if present
        title_match = re.search(r'--\s*(Q\d+[^;\n]*)', block)
        title = title_match.group(1) if title_match else f"Query {idx}"
        
        # Strip comments to get executable SQL
        sql_lines = [line for line in block.splitlines() if not line.strip().startswith('--')]
        executable_sql = "\n".join(sql_lines).strip()
        if not executable_sql:
            continue
        try:
            res = pd.read_sql_query(executable_sql, con)
            print(f"[OK] {title}: returned {len(res)} rows, {len(res.columns)} cols")
            # print top 2 rows
            print("     Preview:\n", res.head(2).to_string(index=False))
        except Exception as e:
            print(f"[ERROR] {title}: {e}")
