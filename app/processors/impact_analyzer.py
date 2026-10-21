from app.schemas import NewsItem
CRITICAL = ["fomc", "cpi", "nfp", "war", "flash crash", "default", "regulation", "exchange halt"]
HIGH = ["interest rate", "central bank", "fed", "opec", "etf", "earnings", "guidance", "sanction"]
def assess_importance(item: NewsItem) -> NewsItem:
    text = f"{item.title} {item.raw_text}".lower()
    if any(x in text for x in CRITICAL): item.importance, item.importance_reason = "CRITICAL", "พบคำสำคัญที่อาจทำให้ตลาดผันผวนมาก; เป็นการประเมินเบื้องต้น ไม่รับประกันทิศทางราคา"
    elif any(x in text for x in HIGH): item.importance, item.importance_reason = "HIGH", "เป็นข่าวเศรษฐกิจ/ตลาดที่ควรติดตามทันที; เป็นการประเมินเบื้องต้น"
    else: item.importance, item.importance_reason = "LOW", "ไม่พบสัญญาณผลกระทบวงกว้างจากข้อมูลที่มี; เป็นการประเมินเบื้องต้น"
    item.sentiment = "NEGATIVE" if any(x in text for x in ["war", "crash", "fall", "risk", "restrictive"]) else "POSITIVE" if any(x in text for x in ["rise", "growth", "strong", "inflow"]) else "MIXED"
    return item
