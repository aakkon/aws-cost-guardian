import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.services.aws_cost import run_ingest

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def ingest_job():
    db = SessionLocal()
    try:
        result = run_ingest(db)
        logger.info("Scheduled ingest completed: %s", result)
    except Exception as e:
        logger.error("Scheduled ingest failed: %s", e)
    finally:
        db.close()