from datetime import datetime
from pydantic import BaseModel, Field

class NewsItem(BaseModel):
    id: str = ""
    title: str
    source: str = "Unknown"
    url: str = ""
    published_at: datetime
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    language: str = "en"
    market: list[str] = Field(default_factory=list)
    region: str = "Global"
    related_assets: list[str] = Field(default_factory=list)
    importance: str = "LOW"
    importance_reason: str = "ประเมินเบื้องต้นจากประเภทข่าวและคำสำคัญ"
    sentiment: str = "MIXED"
    impact_summary: str = "ไม่ทราบจากแหล่งข้อมูล"
    short_summary: str = "ไม่ทราบจากแหล่งข้อมูล"
    keywords: list[str] = Field(default_factory=list)
    duplicate_group: str = ""
    raw_text: str = ""
    processing_status: str = "new"
    follow_up: str = "ติดตามข้อมูลเพิ่มเติมจากแหล่งข่าวต้นฉบับ"
    local_published_at: str = ""
    utc_published_at: str = ""
    related_count: int = 1

class EconomicEvent(BaseModel):
    event_name: str
    country: str
    currency: str
    previous: str | None = None
    forecast: str | None = None
    actual: str | None = None
    event_time: datetime
    importance: str = "MEDIUM"
    related_assets: list[str] = Field(default_factory=list)
