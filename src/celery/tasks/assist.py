from celery import Celery, Task

from src.astro_assistant import Assistant
from src.config import config
from src.views.custom_logger import logger
from src.redis.db import database
from src.utils.app_utils import export_status
from src.const import status


class AssistTask(Task):
    _assistant = None

    @property
    def assistant(self):
        if self._assistant is None:
            logger.i("Creating a new Assistant...")
            self._assistant = Assistant(
                en_translate_prompt_file=config["astro_gpt"]["en_translate_prompt_file"],
                vi_translate_prompt_file=config["astro_gpt"]["vi_translate_prompt_file"],
                question_eval_prompt_file=config["astro_gpt"]["question_eval_prompt_file"],
                ask_prompt_file=config["astro_gpt"]["ask_prompt_file"],
                language_detector_prompt_file=config["astro_gpt"]["language_detector_prompt_file"],
                base_model=config["astro_gpt"]["base_model"],
            )
        return self._assistant

    def on_success(self, retval, task_id, args, kwargs):
        query = args[0]
        database.set(task_id, export_status(id=task_id, status=status.SUCCESS, prompt=query, response=retval))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        query = args[0]
        database.set(task_id, export_status(id=task_id, status=status.FAILED, prompt=query, response=exc))
