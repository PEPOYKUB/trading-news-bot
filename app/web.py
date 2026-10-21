from pathlib import Path
from threading import Thread
import time
import yaml
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import list_news, list_source_status
from app.collectors.economic_calendar import EconomicCalendarProvider
from app.services.news_service import run_pipeline
from app.config import get_settings

WEB_DIR = Path(__file__).resolve().parent.parent / "web"
app = FastAPI(title="Market Pulse API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"])

def live_fetch_loop():
    settings = get_settings()
    while True:
        try:
            run_pipeline()
        except Exception:
            pass
        time.sleep(max(1, settings.fetch_interval_minutes) * 60)

@app.on_event("startup")
def seed_demo_data():
    # Fetch immediately and keep refreshing in the background while the service runs.
    Thread(target=live_fetch_loop, name="market-pulse-fetch", daemon=True).start()

@app.get("/", include_in_schema=False)
def index(): return FileResponse(WEB_DIR / "index.html")

@app.get("/assets/{filename}", include_in_schema=False)
def assets(filename: str): return FileResponse(WEB_DIR / filename)

@app.get("/api/news")
def news(market: str | None = Query(default=None), importance: str | None = Query(default=None), asset: str | None = Query(default=None), q: str | None = Query(default=None)):
    items = [x for x in list_news() if x.importance in {"CRITICAL", "HIGH"}]
    if not get_settings().enable_mock_data:
        items = [x for x in items if not x.source.startswith("Mock ")]
    if market: items = [x for x in items if market in x.market]
    if importance: items = [x for x in items if x.importance == importance]
    if asset: items = [x for x in items if asset.upper() in [a.upper() for a in x.related_assets]]
    if q: items = [x for x in items if q.lower() in f"{x.title} {x.short_summary}".lower()]
    return {"items": [x.model_dump(mode="json") for x in items], "count": len(items)}

@app.get("/api/calendar")
def calendar(): return {"items": [x.model_dump(mode="json") for x in EconomicCalendarProvider().fetch()]}

@app.get("/api/sources")
def sources():
    config_path = Path(__file__).resolve().parent.parent / "config" / "sources.yaml"
    configured = {x["name"]: x for x in (yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}).get("sources", [])}
    now = time.time()
    result = []
    for item in list_source_status():
        if item["name"] not in configured:
            continue
        cfg = configured[item["name"]]
        try:
            fetched = __import__("datetime").datetime.fromisoformat(item["last_fetched_at"].replace("Z", "+00:00")).timestamp()
            item["freshness_minutes"] = max(0, round((now - fetched) / 60))
        except Exception:
            item["freshness_minutes"] = None
        item["trust_level"] = cfg.get("trust_level", "Publisher")
        item["website"] = cfg.get("website", "")
        result.append(item)
    return {"items": result}

@app.post("/api/refresh")
def refresh(): return {"inserted": run_pipeline()}
