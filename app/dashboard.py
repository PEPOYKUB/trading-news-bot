from datetime import datetime, timezone
import html
import streamlit as st
from app.database import list_source_status
from app.services.news_service import get_news, run_pipeline
from app.collectors.economic_calendar import EconomicCalendarProvider

st.set_page_config(page_title="Market Pulse", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Thai:wght@400;500;600;700&display=swap');
:root { --bg:#121316; --panel:#1A1C20; --line:#282A30; --text:#F0F2F5; --muted:#9A9FA8; --gold:#D4AF37; }
.stApp { background:var(--bg); color:var(--text); font-family:'Inter','Noto Sans Thai',sans-serif; }
[data-testid="stSidebar"] { background:#0F1012; border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:var(--text); }
.block-container { max-width:1440px; padding:42px 48px 64px; }
.eyebrow { color:var(--gold); font-size:12px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.hero { display:flex; justify-content:space-between; align-items:end; padding:18px 0 34px; border-bottom:1px solid var(--line); margin-bottom:28px; }
.hero h1 { font-size:38px; line-height:1.1; letter-spacing:-1.5px; margin:0; color:var(--text); }
.hero p { margin:12px 0 0; color:var(--muted); max-width:640px; font-size:15px; }
.live { color:#8FE3B2; font-size:13px; font-weight:600; white-space:nowrap; }
.metric { background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:18px 20px; min-height:96px; }
.metric-label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:1px; }
.metric-value { color:var(--text); font-size:28px; font-weight:700; margin-top:8px; }
.section-title { color:var(--text); font-size:21px; font-weight:700; margin:30px 0 14px; }
.news-card { background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:20px 22px; margin:10px 0; }
.news-card:hover { border-color:#5B4A1F; }
.news-top { display:flex; justify-content:space-between; gap:18px; align-items:center; }
.badge { font-size:11px; font-weight:700; letter-spacing:1px; padding:5px 9px; border-radius:999px; }
.critical { color:#FFB5B5; background:#3A2024; } .high { color:#FFD1A6; background:#3A2A1D; }
.news-title { color:var(--text); font-size:17px; font-weight:600; line-height:1.45; margin:14px 0 8px; }
.news-summary { color:#C6CAD1; font-size:14px; line-height:1.65; white-space:pre-line; }
.meta { color:var(--muted); font-size:12px; margin-top:14px; }
.asset { color:var(--gold); font-weight:600; }
.stButton > button { border-radius:10px; border:1px solid #66551E; background:#2A2412; color:#F7E6A2; font-weight:600; }
div[data-testid="stExpander"] { background:var(--panel); border:1px solid var(--line); border-radius:14px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='hero'><div><div class='eyebrow'>Market intelligence · live brief</div><h1>Market Pulse</h1><p>ข่าวสำคัญที่อาจกระทบกราฟ คัดมาให้อ่านเร็ว ตัดข้อมูลรบกวนออก และอ้างอิงจากแหล่งข่าวต้นฉบับ</p></div><div class='live'>● ระบบติดตามข่าวพร้อมใช้งาน</div></div>", unsafe_allow_html=True)
st.warning("ข้อมูลเพื่อการศึกษาเท่านั้น ไม่ใช่คำแนะนำการลงทุน ระบบนี้ไม่มีฟังก์ชันส่งคำสั่งซื้อขายจริง")

if st.button("↻  อัปเดตข่าว"):
    inserted = run_pipeline()
    st.success(f"อัปเดตแล้ว {inserted} ข่าวสำคัญใหม่")
    st.rerun()

items = [x for x in get_news() if x.importance in {"CRITICAL", "HIGH"}]
critical_count = sum(x.importance == "CRITICAL" for x in items)
high_count = sum(x.importance == "HIGH" for x in items)
sources = len({x.source for x in items})
cols = st.columns(4)
for col, label, value in zip(cols, ["ข่าวสำคัญ", "Critical", "High", "แหล่งข่าว"], [len(items), critical_count, high_count, sources]):
    col.markdown(f"<div class='metric'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ตัวกรองข่าว")
    markets = sorted({m for item in items for m in item.market})
    market = st.multiselect("ตลาด", markets)
    importance = st.multiselect("ระดับผลกระทบ", ["CRITICAL", "HIGH"], default=["CRITICAL", "HIGH"])
    asset = st.text_input("สินทรัพย์", placeholder="เช่น BTCUSD")
    query = st.text_input("ค้นหาคำ", placeholder="เช่น Fed, Bitcoin")
    st.caption("แสดงเฉพาะข่าวที่ระบบประเมินว่ามีโอกาสกระทบตลาด")

filtered = [x for x in items if (not market or any(m in x.market for m in market)) and x.importance in importance and (not asset or asset.upper() in ",".join(x.related_assets).upper()) and (not query or query.lower() in f"{x.title} {x.short_summary}".lower())]
st.markdown(f"<div class='section-title'>ข่าวที่ควรจับตา <span style='color:#9A9FA8;font-size:14px;font-weight:400'>· {len(filtered)} รายการ · อัปเดต {datetime.now(timezone.utc).strftime('%H:%M UTC')}</span></div>", unsafe_allow_html=True)

if not filtered: st.info("ยังไม่พบข่าวตามตัวกรอง กด ‘อัปเดตข่าว’ เพื่อโหลด Mock News")
for item in filtered:
    level_class = "critical" if item.importance == "CRITICAL" else "high"
    assets = ", ".join(item.related_assets) or "ไม่ทราบจากแหล่งข้อมูล"
    link = f"<a href='{html.escape(item.url)}' target='_blank' style='color:#D4AF37'>อ่านต้นฉบับ ↗</a>" if item.url else ""
    st.markdown(f"<div class='news-card'><div class='news-top'><span class='badge {level_class}'>{item.importance}</span><span class='meta'>{html.escape(item.source)} · {html.escape(item.local_published_at)}</span></div><div class='news-title'>{html.escape(item.title)}</div><div class='news-summary'>{html.escape(item.short_summary)}</div><div class='meta'>สินทรัพย์ที่อาจได้รับผลกระทบ: <span class='asset'>{html.escape(assets)}</span> · {link}</div></div>", unsafe_allow_html=True)
    with st.expander("ดูเหตุผลการประเมินและสิ่งที่ควรติดตาม"):
        st.write(item.impact_summary)
        st.caption(item.follow_up)

st.markdown("<div class='section-title'>Economic Calendar</div>", unsafe_allow_html=True)
for event in EconomicCalendarProvider().fetch(): st.markdown(f"**{event.importance}** · {event.event_name} · {event.currency} · {event.event_time.strftime('%Y-%m-%d %H:%M UTC')} · {', '.join(event.related_assets)}")
with st.expander("สถานะแหล่งข่าว"): st.dataframe(list_source_status(), use_container_width=True, hide_index=True)
