from datetime import datetime, timezone, timedelta
from app.schemas import NewsItem, EconomicEvent
def mock_news() -> list[NewsItem]:
    now = datetime.now(timezone.utc)
    return [NewsItem(id="mock-fed-001", title="Fed officials signal rates may remain restrictive as inflation stays elevated", source="Mock Financial Desk", url="https://example.com/mock-fed", published_at=now - timedelta(minutes=5), fetched_at=now), NewsItem(id="mock-btc-001", title="Bitcoin ETF flows rise as institutional interest continues", source="Mock Crypto Wire", url="https://example.com/mock-btc", published_at=now - timedelta(minutes=18), fetched_at=now), NewsItem(id="mock-oil-001", title="OPEC discusses supply outlook amid geopolitical uncertainty", source="Mock Commodities News", url="https://example.com/mock-oil", published_at=now - timedelta(hours=1), fetched_at=now)]
def mock_calendar() -> list[EconomicEvent]:
    now = datetime.now(timezone.utc)
    return [EconomicEvent(event_name="US CPI (Mock)", country="United States", currency="USD", previous="3.1%", forecast="3.0%", event_time=now + timedelta(hours=4), importance="CRITICAL", related_assets=["USD", "XAUUSD", "NAS100"])]
