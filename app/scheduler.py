import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from app.config import get_settings
from app.services.news_service import run_pipeline
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
def run_once():
    count = run_pipeline(); logging.info("Processed %s new mock news items", count)
def run_forever():
    settings = get_settings(); scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(run_once, "interval", minutes=settings.fetch_interval_minutes, max_instances=1, coalesce=True, id="news-pipeline")
    run_once(); logging.info("Worker started; interval=%s minutes", settings.fetch_interval_minutes); scheduler.start()
if __name__ == "__main__": run_forever()
