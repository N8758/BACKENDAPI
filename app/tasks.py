from celery import Celery
from .ai_handler import rewrite_text
from .cache import set_cache
from .config import REDIS_URL

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(name="rewrite_task")
def rewrite_task(text: str, tone: str):
    result = rewrite_text(text, tone)
    set_cache(f"{text}_{tone}", result)
    return str(result)  # Ensure result is string
