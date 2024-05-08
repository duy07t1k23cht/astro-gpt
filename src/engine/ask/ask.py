from typing import List
from datetime import datetime

from src.base import BaseAgent
from src.engine.search.entities.search_result import SearchResult


class Asker:
    def __init__(self, prompt_file: str, model: str) -> None:
        self.agent = BaseAgent(prompt_file, model=model)

    def ask(self, question: str, search_results: List[SearchResult] = [], current_time: bool = False, assistant_prompt: str = "") -> str:
        if search_results:
            search_results = search_results[:5]
            search_result_prompt = "\n".join([f"{i + 1}\n{result.summary()}" for i, result in enumerate(search_results)])
            search_result_prompt = f"Search results:\n```\n{search_result_prompt}\n```"
        else:
            search_result_prompt = ""

        if current_time:
            current_time_prompt = f"Today date: {datetime.now().strftime('%d %B %Y')}\n"
        else:
            current_time_prompt = ""

        question_prompt = f'The question: "{question}"\n'

        return self.agent.execute((question_prompt + current_time_prompt + search_result_prompt).strip(), assistant_prompt=assistant_prompt)
