from pathlib import Path
from threading import Thread
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import list_news, list_source_status
from app.collectors.economic_calendar import EconomicCalendarProvider
from app.services.news_service import run_pipeline

WEB_DIR = Path(__file__).resolve().parent.parent / "web"
app = FastAPI(title="Market Pulse API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"])

@app.on_event("startup")
def seed_demo_data():
    # Fetch fresh sources in the background so the hosted page opens immediately.
    Thread(target=run_pipeline, name="market-pulse-fetch", daemon=True).start()

@app.get("/", include_in_schema=False)
def index(): return FileResponse(WEB_DIR / "index.html")

@app.get("/assets/{filename}", include_in_schema=False)
def assets(filename: str): return FileResponse(WEB_DIR / filename)

@app.get("/api/news")
def news(market: str | None = Query(default=None), importance: str | None = Query(default=None), asset: str | None = Query(default=None), q: str | None = Query(default=None)):
    items = [x for x in list_news() if x.importance in {"CRITICAL", "HIGH"}]
    if market: items = [x for x in items if market in x.market]
    if importance: items = [x for x in items if x.importance == importance]
    if asset: items = [x for x in items if asset.upper() in [a.upper() for a in x.related_assets]]
    if q: items = [x for x in items if q.lower() in f"{x.title} {x.short_summary}".lower()]
    return {"items": [x.model_dump(mode="json") for x in items], "count": len(items)}

@app.get("/api/calendar")
def calendar(): return {"items": [x.model_dump(mode="json") for x in EconomicCalendarProvider().fetch()]}

@app.get("/api/sources")
def sources(): return {"items": list_source_status()}

@app.post("/api/refresh")
def refresh(): return {"inserted": run_pipeline()}
