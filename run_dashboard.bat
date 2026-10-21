@echo off
call .venv\Scripts\activate
python -m app.main init-db
streamlit run app\dashboard.py
