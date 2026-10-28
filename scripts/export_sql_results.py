#!/usr/bin/env python3
"""Run all SQL queries against ev_market.db and generate markdown and json documentation."""
import sqlite3
import json
import re
from pathlib import Path
import pandas as pd

WORKSPACE = Path(r"D:\EV_Tableau_Project_Starter_Kit")
DB_PATH = WORKSPACE / "data" / "ev_market.db"
SQL_PATH = WORKSPACE / "sql" / "ev_market_queries.sql"
MD_OUT = WORKSPACE / "docs" / "SQL_ANALYTICAL_RESULTS.md"
JSON_OUT = WORKSPACE / "docs" / "sql_results.json"

with open(SQL_PATH, 'r', encoding='utf-8') as f:
    sql_text = f.read()

raw_blocks = [b.strip() for b in sql_text.split(';') if b.strip()]

results_dict = {}
md_lines = [
    "# EV Market Intelligence — Analytical SQL Results",
    "",
    "This document captures the verified query execution results run against `data/ev_market.db` (Table: `ev_market_clean`, 199,999 records).",
    "",
    f"**Execution Timestamp:** 2026-10-27 | **Database:** SQLite 3 | **Dataset:** Cleaned Training Corpus",
    "",
    "---",
    ""
]

with sqlite3.connect(DB_PATH) as con:
    for idx, block in enumerate(raw_blocks, 1):
        title_match = re.search(r'--\s*(Q\d+[^;\n]*)', block)
        title = title_match.group(1).strip() if title_match else f"Query {idx}"
        
        sql_lines = [line for line in block.splitlines() if not line.strip().startswith('--')]
        executable_sql = "\n".join(sql_lines).strip()
        if not executable_sql:
            continue
        
        df = pd.read_sql_query(executable_sql, con)
        results_dict[title] = {
            "query": executable_sql,
            "row_count": len(df),
            "columns": list(df.columns),
            "data": df.to_dict(orient="records")
        }
        
        md_lines.append(f"## {title}")
        md_lines.append("")
        md_lines.append("```sql")
        md_lines.append(executable_sql)
        md_lines.append("```")
        md_lines.append("")
        md_lines.append(f"**Rows returned:** {len(df):,}")
        md_lines.append("")
        md_lines.append(df.to_markdown(index=False))
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

with open(MD_OUT, 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))

with open(JSON_OUT, 'w', encoding='utf-8') as f:
    json.dump(results_dict, f, indent=2)

print(f"Generated {MD_OUT} and {JSON_OUT} successfully!")
