from fastapi import APIRouter

from src.celery.celery_worker import assist
from src.redis.db import database
from src.utils.app_utils import export_status
from src.const import status
from uuid import uuid4

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "File Upload Example. Please use `/docs` for enter to Swagger UI and test the API"}


@router.get("/hello/")
async def get_users():
    return "Hello"


@router.get("/ask")
async def ask(query: str):
    request_id = str(uuid4())

    response = assist.apply_async(args=(query,), task_id=request_id, serializer="json")

    database.set(request_id, export_status(id=request_id, status=status.IN_PROGRESS, prompt=query, response=None))

    return response.get()
