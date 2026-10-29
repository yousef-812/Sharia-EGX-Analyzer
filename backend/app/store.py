from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(os.getenv("DATABASE_PATH", "./data/analysis_runs.sqlite3"))


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, symbol TEXT NOT NULL, result_json TEXT NOT NULL)")
    return conn


def save_run(symbol: str, result: dict) -> int:
    with connect() as conn:
        cur = conn.execute("INSERT INTO runs(created_at, symbol, result_json) VALUES (?, ?, ?)", (datetime.now(timezone.utc).isoformat(), symbol.upper(), json.dumps(result)))
        return int(cur.lastrowid)


def latest_runs(limit: int = 20) -> list[dict]:
    with connect() as conn:
        rows = conn.execute("SELECT id, created_at, symbol, result_json FROM runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"id": r[0], "created_at": r[1], "symbol": r[2], "result": json.loads(r[3])} for r in rows]
