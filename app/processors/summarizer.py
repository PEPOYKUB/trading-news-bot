from app.schemas import NewsItem
class SummaryProvider:
    def summarize(self, item: NewsItem) -> NewsItem: raise NotImplementedError
class MockSummaryProvider(SummaryProvider):
    def summarize(self, item: NewsItem) -> NewsItem:
        assets = ", ".join(item.related_assets) or "สินทรัพย์ที่เกี่ยวข้อง"
        tone = {"POSITIVE": "มีโอกาสหนุน", "NEGATIVE": "มีโอกาสกดดัน", "MIXED": "อาจผันผวน"}.get(item.sentiment, "อาจผันผวน")
        item.short_summary = f"{item.title}.\n{tone} {assets} — ควรติดตามปฏิกิริยาของตลาดและรายละเอียดจากต้นฉบับ"
        item.impact_summary = f"ประเมินเบื้องต้นว่า {tone} {assets} จากประเภทข่าวและคำสำคัญในหัวข้อเท่านั้น ไม่ใช่คำแนะนำการลงทุน"
        item.follow_up = "ติดตามตัวเลขจริง แถลงการณ์ฉบับเต็ม และการยืนยันจากแหล่งข่าวต้นฉบับ"
        return item

class OpenAISummaryProvider(SummaryProvider):
    """Optional adapter; requires OPENAI_API_KEY and the openai package."""
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key, self.model = api_key, model
    def summarize(self, item: NewsItem) -> NewsItem:
        if not self.api_key: return MockSummaryProvider().summarize(item)
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        response = client.responses.create(model=self.model, input=f"Summarize only this source-backed news in Thai. Do not invent facts. Title: {item.title}\nSource: {item.source}\nText: {item.raw_text[:2000]}")
        item.short_summary = response.output_text[:2000]
        item.impact_summary = "ประเมินจากข้อมูลข่าวต้นฉบับโดยผู้ให้บริการ AI; ไม่ใช่คำแนะนำการลงทุน"
        return item
