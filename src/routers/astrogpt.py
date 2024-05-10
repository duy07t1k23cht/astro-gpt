from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from src.celery.celery_worker import assist
from src.redis.db import database
from src.utils.app_utils import export_status
from src.const import status
from src.views.custom_logger import logger

router = APIRouter()


class AskResponse(BaseModel):
    request_id: str
    user: str
    assistant: str


@router.get("/")
async def root():
    return {"message": "File Upload Example. Please use `/docs` for enter to Swagger UI and test the API"}


@router.get("/hello/")
async def introduction():
    return {
        "message": "Astro GPT is an innovative project designed to provide a seamless experience for natural language processing tasks for astronomy topic. Its main features include robust API integration and efficient task monitoring."
    }
    return


@router.get("/ask")
async def ask(query: str):
    try:
        request_id = str(uuid4())

        response = assist.apply_async(args=(query,), task_id=request_id, serializer="json")

        database.set(request_id, export_status(id=request_id, status=status.IN_PROGRESS, prompt=query, response=None))

        return AskResponse(request_id=request_id, user=query, assistant=response.get().strip())
    except Exception as e:
        logger.e(f"An error occurs: {e}")
        return {"error": "An unexpected error occurred"}
