import os
import json

from celery import Celery, Task
from dotenv import load_dotenv

from src.astro_assistant import Assistant
from src.celery.tasks import AssistTask
from src.views.custom_logger import logger

RESULT_EXPIRE_TIME = 60 * 60 * 10  # keep tasks around for ten hours

load_dotenv()
app = Celery(
    "astro",
    broker_url=os.environ.get("CELERY_BROKER_URL"),
    backend_url=os.environ.get("CELERY_RESULT_BACKEND"),
    # result_expires=RESULT_EXPIRE_TIME,
)


app.conf.update(
    worker_max_tasks_per_child=1,
    worker_prefetch_multiplier=1,
    enable_utc=True,
    timezone="Asia/Saigon",
    broker_connection_retry_on_startup=True,
)


@app.task(name="assist", base=AssistTask, bind=True)
def assist(self, query: str):
    return self.assistant.execute(query)
