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
    backend="s3",
    s3_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    s3_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    s3_bucket="duynm98-demo-s3",
    s3_base_path="celery-backend-result/astrogpt-",
    s3_region="ap-southeast-1",
)


app.conf.update(
    enable_utc=True,
    timezone="Asia/Saigon",
    broker_connection_retry_on_startup=True,
)


@app.task(name="assist", base=AssistTask, bind=True)
def assist(self, query: str):
    return self.assistant.execute(query).strip()
