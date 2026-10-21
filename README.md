# Trading News Intelligence Bot

ระบบติดตามข่าวการเงินสำหรับผู้เริ่มต้นใช้งาน Windows รองรับ Forex, Crypto, Gold/Commodities, Stocks/Indices และ Macro โดยเก็บเวลาใน UTC และแสดง Asia/Bangkok ได้ Dashboard จะแสดงเฉพาะข่าว CRITICAL/HIGH ที่มีโอกาสกระทบกราฟ เพื่อให้สแกนข่าวได้เร็ว ระบบนี้เป็น news intelligence เท่านั้น ไม่มีฟังก์ชันส่งคำสั่งซื้อขาย และข้อมูลไม่ใช่คำแนะนำการลงทุน

## ติดตั้งบน Windows

1. ติดตั้ง Python 3.11 ขึ้นไป และติ๊ก `Add Python to PATH`
2. เปิด PowerShell ในโฟลเดอร์โปรเจกต์
3. รัน `install.bat` เพื่อสร้าง virtual environment และติดตั้ง dependencies
4. ตรวจ `.env` ที่สร้างจาก `.env.example` ใส่ API key เฉพาะกรณีจะเพิ่ม provider จริง (ค่าเริ่มต้นใช้ Mock)
5. สร้างฐานข้อมูลด้วย `python -m app.main init-db`
6. ทดสอบ pipeline ด้วย `python -m app.main run-once`
7. เปิด Dashboard ด้วย `run_dashboard.bat`
8. เปิด Worker ด้วย `run_worker.bat` (ดึงทุก 5 นาทีตาม `.env`)
9. รัน tests ด้วย `test.bat`

## เปิดใช้งานเหมือนแอป

ดับเบิลคลิกไฟล์ `เปิด Trading News Bot.bat` ระบบจะเปิด Dashboard และเบราว์เซอร์ให้อัตโนมัติ

หากต้องการไอคอนบน Desktop ให้คลิกขวาไฟล์ `สร้าง Shortcut Trading News Bot.ps1` เลือก `Run with PowerShell` จากนั้นดับเบิลคลิก Shortcut ชื่อ `Trading News Bot` บน Desktop ได้เลย

หน้าต่างสีดำที่เปิดคู่กับ Dashboard คือเซิร์ฟเวอร์ของแอป ห้ามปิดหน้าต่างนี้ขณะใช้งาน หากต้องการหยุดแอปให้กด `Ctrl+C` ในหน้าต่างดังกล่าว

## เปิดเป็น Web App จากอุปกรณ์อื่นในเครือข่ายเดียวกัน

ดับเบิลคลิก `run_web.bat` แล้วเปิด `http://localhost:8000` บนเครื่องหลัก ระบบ Web App นี้แยกจาก Streamlit และรองรับมือถือ/แท็บเล็ตแบบ responsive

หากต้องการเปิดจากมือถือหรือคอมพิวเตอร์เครื่องอื่นที่อยู่ Wi-Fi เดียวกัน ให้รัน `ipconfig` บนเครื่องหลัก ดูค่า `IPv4 Address` เช่น `192.168.1.20` แล้วเปิด `http://192.168.1.20:8000` จากอุปกรณ์นั้น หาก Windows Firewall ถาม ให้ Allow access สำหรับ Private network เท่านั้น

API สำหรับต่อยอดอยู่ที่ `/docs` เช่น `http://localhost:8000/docs` ส่วนข้อมูลยังใช้ SQLite และ Mock Source ในเครื่องนี้ การเปิดใช้งานผ่านอินเทอร์เน็ตสาธารณะต้อง deploy Backend/Database ไปยัง Hosting ก่อน ไม่ควรเปิดพอร์ตบ้านตรง ๆ

## Deploy บน Render แบบทดลอง

1. สร้าง GitHub repository แบบ Private แล้วอัปโหลดโปรเจกต์นี้ขึ้นไป
2. ใน Render เลือก `New` → `Web Service`
3. เชื่อม GitHub และเลือก repository นี้
4. ใช้ค่า Build Command: `pip install -r requirements.txt`
5. ใช้ค่า Start Command: `uvicorn app.web:app --host 0.0.0.0 --port $PORT`
6. เลือกแผน `Free` แล้ว Deploy

ไฟล์ `render.yaml` มีค่าตั้งต้นให้แล้ว แต่เวอร์ชันทดลองนี้ยังใช้ SQLite ซึ่งข้อมูลอาจหายเมื่อ Render restart/redeploy เพื่อใช้งานจริงต้องย้ายฐานข้อมูลไป PostgreSQL เช่น Supabase ก่อน

## วิธีใช้ Dashboard

หน้า `Market Pulse` ใช้ธีมมืดและแสดงเฉพาะข่าวสำคัญที่อาจมีผลต่อกราฟ ข่าวแต่ละใบมีระดับ CRITICAL/HIGH, สรุปสั้น, สินทรัพย์ที่อาจได้รับผลกระทบ, เวลา และลิงก์ต้นฉบับ กด `อัปเดตข่าว` เพื่อดึงข้อมูลใหม่ ใช้ตัวกรองด้านซ้ายเพื่อเลือกตลาด/ระดับผลกระทบ/สินทรัพย์ หรือค้นหาคำ และกดส่วน `ดูเหตุผลการประเมินและสิ่งที่ควรติดตาม` เพื่อดูรายละเอียดเพิ่มเติม

## ใช้งาน RSS

เพิ่มรายการใน `config/sources.yaml` โดยใช้ RSS ที่อนุญาตตาม Terms of Use และมี attribution ชัดเจน โครงสร้างนี้เป็นจุดขยายสำหรับ collector; Mock เป็นค่าเริ่มต้นเพื่อให้ติดตั้งและทดสอบได้โดยไม่มี API key ห้าม bypass CAPTCHA/ระบบป้องกัน และเก็บเพียง metadata/summary ที่จำเป็น ไม่คัดลอกบทความเต็ม

## Provider และแจ้งเตือน

`MockSummaryProvider` ทำงานได้ทันทีและมี interface สำหรับ OpenAI/ผู้ให้บริการอื่นในอนาคต ควรเพิ่ม OpenAI adapter โดยอ่าน `OPENAI_API_KEY` จาก environment เท่านั้น ห้าม hard-code key

Notification providers มี Console และ Telegram (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) เป็น extension point; Email ยังต้องผูก SMTP ที่ได้รับอนุญาตก่อนเปิดใช้ Watchlist ตั้งผ่าน `WATCHLIST=EURUSD,GBPUSD,XAUUSD,BTCUSD,NAS100`

## ตัวอย่างผลลัพธ์

ข่าว Mock เช่น `Fed officials signal rates may remain restrictive...` จะถูกจัดเป็น Central Bank/Forex/Macro, ระดับ CRITICAL, สินทรัพย์ที่อาจเกี่ยวข้องคือ USD/XAUUSD/US Indices และแสดงเวลา UTC กับ Asia/Bangkok พร้อมลิงก์ต้นฉบับตัวอย่าง

## แก้ปัญหาที่พบบ่อย

- `python is not recognized`: ติดตั้ง Python ใหม่โดยเลือก Add to PATH หรือใช้ `py -3.11`
- `streamlit is not recognized`: ใช้ `run_dashboard.bat` หรือ activate `.venv` ก่อน
- RSS ล้มเหลว: ตรวจ URL, timeout, Terms of Use และดูสถานะ source ใน Dashboard; ระบบยังทำงานต่อด้วย source อื่น
- ไม่มีข่าว: รัน `python -m app.main run-once` เพื่อเติม Mock News
- ภาษา/เวลาไม่ตรง: ตั้ง `TIMEZONE` ใน `.env` เป็น IANA timezone เช่น `Asia/Bangkok`

## สถานะฟีเจอร์

พร้อมใช้งานใน MVP: SQLite, Mock news/calendar/summary, classification, asset mapping, importance, duplicate URL/title check, timezone display, Streamlit dashboard, scheduler, console notification, Telegram adapter, tests และ Windows batch files

เป็นโครงสร้างต่อยอด: licensed News API, Economic Calendar API จริง, OpenAI adapter เต็มรูปแบบ, similarity clustering หลายแหล่ง, SMTP email และการแจ้งเตือนแบบ persistent deduplication
