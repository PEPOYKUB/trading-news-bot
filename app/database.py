import json
import sqlite3
from pathlib import Path
from .config import get_settings
from .schemas import NewsItem

SCHEMA = """
CREATE TABLE IF NOT EXISTS news (
 id TEXT PRIMARY KEY, title TEXT NOT NULL, source TEXT, url TEXT UNIQUE,
 published_at TEXT, fetched_at TEXT, language TEXT, market TEXT, region TEXT,
 related_assets TEXT, importance TEXT, importance_reason TEXT, sentiment TEXT,
 impact_summary TEXT, short_summary TEXT, keywords TEXT, duplicate_group TEXT,
 raw_text TEXT, processing_status TEXT, follow_up TEXT, local_published_at TEXT,
 utc_published_at TEXT, related_count INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS source_status (name TEXT PRIMARY KEY, enabled INTEGER, status TEXT, message TEXT, last_fetched_at TEXT);
"""

def get_connection(db_path: Path | None = None):
    path = db_path or get_settings().database_path
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con

def init_db() -> None:
    with get_connection() as con: con.executescript(SCHEMA)

def save_news(item: NewsItem) -> bool:
    init_db(); data = item.model_dump()
    fields = ["id", "title", "source", "url", "published_at", "fetched_at", "language", "market", "region", "related_assets", "importance", "importance_reason", "sentiment", "impact_summary", "short_summary", "keywords", "duplicate_group", "raw_text", "processing_status", "follow_up", "local_published_at", "utc_published_at", "related_count"]
    vals = [data[f].isoformat() if hasattr(data[f], "isoformat") else json.dumps(data[f], ensure_ascii=False) if isinstance(data[f], list) else data[f] for f in fields]
    updates = ",".join(f"{field}=excluded.{field}" for field in fields if field != "id")
    with get_connection() as con:
        cur = con.execute(f"INSERT INTO news ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)}) ON CONFLICT(id) DO UPDATE SET {updates}", vals)
        return cur.rowcount > 0

def list_news(limit: int = 200) -> list[NewsItem]:
    init_db()
    with get_connection() as con: rows = con.execute("SELECT * FROM news ORDER BY published_at DESC LIMIT ?", (limit,)).fetchall()
    output = []
    for row in rows:
        d = dict(row)
        for key in ("market", "related_assets", "keywords"): d[key] = json.loads(d[key] or "[]")
        output.append(NewsItem.model_validate(d))
    return output

def save_source_status(name: str, status: str, message: str = "", enabled: bool = True) -> None:
    from datetime import datetime, timezone
    init_db()
    with get_connection() as con: con.execute("INSERT OR REPLACE INTO source_status VALUES (?,?,?,?,?)", (name, int(enabled), status, message, datetime.now(timezone.utc).isoformat()))

def list_source_status() -> list[dict]:
    init_db()
    with get_connection() as con: return [dict(x) for x in con.execute("SELECT * FROM source_status ORDER BY name").fetchall()]
