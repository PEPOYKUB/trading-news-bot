from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import feedparser
import httpx
from app.schemas import NewsItem

class RSSCollector:
    def __init__(self, name: str, url: str, timeout: float = 15): self.name, self.url, self.timeout = name, url, timeout
    def fetch(self) -> list[NewsItem]:
        response = httpx.get(self.url, timeout=self.timeout, follow_redirects=True, headers={"User-Agent": "TradingNewsBot/1.0"})
        response.raise_for_status(); parsed = feedparser.parse(response.content); out = []
        for entry in parsed.entries:
            published = datetime.now(timezone.utc)
            for key in ("published", "updated"):
                if entry.get(key):
                    try: published = parsedate_to_datetime(entry[key]).astimezone(timezone.utc); break
                    except (TypeError, ValueError, IndexError): pass
            title = entry.get("title", "Untitled").strip(); url = entry.get("link", "")
            out.append(NewsItem(id=hashlib.sha256((url or title).encode()).hexdigest()[:16], title=title, source=self.name, url=url, published_at=published, fetched_at=datetime.now(timezone.utc), raw_text=entry.get("summary", "")[:1000]))
        return out
