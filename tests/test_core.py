from datetime import datetime, timezone
from app.schemas import NewsItem
from app.processors.normalizer import normalize_title
from app.processors.deduplicator import is_duplicate
from app.processors.classifier import classify
from app.processors.impact_analyzer import assess_importance
from app.services.asset_mapping import detect_assets
from app.collectors.mock_collector import mock_news
from app.processors.summarizer import MockSummaryProvider

def make(title): return NewsItem(title=title, url="https://x.test/a", published_at=datetime.now(timezone.utc))
def test_normalize_title(): assert normalize_title(" Fed: Rates!  ") == "fed rates"
def test_duplicate_url_and_title(): assert is_duplicate(make("Fed rates decision"), make("Fed rates decision"))
def test_classification(): assert "Central Bank" in classify(make("Fed announces interest rate decision")).market
def test_assets(): assert "XAUUSD" in detect_assets("Fed and CPI impact gold")
def test_importance(): assert assess_importance(make("FOMC statement released")).importance == "CRITICAL"
def test_mock_summary(): assert "Bitcoin ETF flows rise" in MockSummaryProvider().summarize(make("Bitcoin ETF flows rise")).short_summary
def test_mock_source(): assert len(mock_news()) == 3
