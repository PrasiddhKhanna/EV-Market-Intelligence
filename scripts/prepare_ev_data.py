#!/usr/bin/env python3
"""Rebuild the cleaned CSV and SQLite database from ev_market_train.csv.
Usage: python scripts/prepare_ev_data.py path/to/ev_market_train.csv --out data
Requires: pandas (pip install pandas).
"""
import argparse, sqlite3
from pathlib import Path
import pandas as pd

p = argparse.ArgumentParser()
p.add_argument('csv_path')
p.add_argument('--out', default='data')
args = p.parse_args()
out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(args.csv_path)
print('Loaded', len(df), 'rows and', len(df.columns), 'columns')
print('Missing values by column before cleaning:\n', df.isna().sum()[lambda s: s > 0])
print('Exact duplicate rows:', int(df.duplicated().sum()))
df = df.drop_duplicates().copy()
for col in df.select_dtypes(include='number').columns:
    if df[col].isna().any():
        med = df[col].median()
        print(f'Imputing {col} missing values with median {med}')
        df[col] = df[col].fillna(med)
df.to_csv(out / 'ev_market_clean.csv', index=False)
db = out / 'ev_market.db'
if db.exists(): db.unlink()
with sqlite3.connect(db) as con:
    df.to_sql('ev_market_clean', con, index=False, if_exists='replace', chunksize=10000)
    for col in ['market_region','model_year','manufacturer','category']:
        con.execute(f'CREATE INDEX idx_ev_{col} ON ev_market_clean({col})')
    con.commit()
print('Wrote', out/'ev_market_clean.csv', 'and', db)
