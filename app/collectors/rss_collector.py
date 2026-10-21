from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import feedparser
import httpx
import re
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
            image_url = ""
            for media_key in ("media_content", "media_thumbnail", "enclosures"):
                media = entry.get(media_key) or []
                if media and isinstance(media, list):
                    image_url = media[0].get("url", "") if isinstance(media[0], dict) else ""
                    if image_url: break
            if not image_url:
                image_match = re.search(r'<img[^>]+src=["\']([^"\']+)', entry.get("summary", ""), re.I)
                image_url = image_match.group(1) if image_match else ""
            out.append(NewsItem(id=hashlib.sha256((url or title).encode()).hexdigest()[:16], title=title, source=self.name, url=url, image_url=image_url, published_at=published, fetched_at=datetime.now(timezone.utc), raw_text=entry.get("summary", "")[:1000]))
        return out
