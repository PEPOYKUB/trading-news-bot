from datetime import timezone
from zoneinfo import ZoneInfo
from app.config import get_settings
from app.database import save_news, save_source_status, list_news
from app.collectors.mock_collector import mock_news
from app.collectors.rss_collector import RSSCollector
from app.processors.classifier import classify
from app.processors.impact_analyzer import assess_importance
from app.processors.summarizer import MockSummaryProvider
from app.processors.deduplicator import is_duplicate
from app.services.asset_mapping import detect_assets

def process_item(item):
    item = classify(item); item.related_assets = detect_assets(f"{item.title} {item.raw_text}")
    item = assess_importance(item); item = MockSummaryProvider().summarize(item)
    item.utc_published_at = item.published_at.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    item.local_published_at = item.published_at.astimezone(ZoneInfo(get_settings().timezone)).strftime("%Y-%m-%d %H:%M %Z")
    item.processing_status = "processed"
    return item

def run_pipeline() -> int:
    count = 0
    items = mock_news()
    existing = list_news()
    for source in load_rss_sources():
        try:
            fetched = source.fetch(); items.extend(fetched); save_source_status(source.name, "ok", f"Fetched {len(fetched)} items")
        except Exception as exc:
            save_source_status(source.name, "error", str(exc)[:500])
    for item in items:
        try:
            if any(is_duplicate(item, old) and old.importance in {"CRITICAL", "HIGH"} and "เหตุการณ์:" not in old.short_summary for old in existing):
                continue
            save_source_status(item.source, "ok", "Mock source loaded")
            processed = process_item(item)
            # Store only actionable market-moving news for a focused dashboard.
            if processed.importance not in {"CRITICAL", "HIGH"}:
                continue
            if save_news(processed): count += 1; existing.append(processed)
        except Exception as exc:
            save_source_status(item.source, "error", str(exc)[:500])
    return count

def load_rss_sources():
    """Load enabled RSS sources from config/sources.yaml without hard-coding sources."""
    import yaml
    from pathlib import Path
    config_path = Path(__file__).resolve().parents[2] / "config" / "sources.yaml"
    if not config_path.exists(): return []
    payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return [RSSCollector(x["name"], x["url"]) for x in payload.get("sources", []) if x.get("enabled") and x.get("type") == "rss" and x.get("url")]

def get_news(): return list_news()
