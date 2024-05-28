from datetime import datetime
from typing import List

from src.base import BaseAgent
from src.engine.search.entities.search_result import SearchResult


class Asker:
    def __init__(self, prompt_file: str, model: str) -> None:
        self.agent = BaseAgent(prompt_file, model=model)

    def ask(self, question: str, search_results, current_time: bool = False, assistant_prompt: str = "") -> str:
        if search_results:
            search_result_prompt = f"\n```\n{search_results}\n```"
        else:
            search_result_prompt = ""

        if current_time:
            current_time_prompt = f"\nCurrent date: {datetime.now().strftime('%d %B %Y')}\n"
        else:
            current_time_prompt = ""

        question_prompt = f"{question}"

        return self.agent.execute((question_prompt + current_time_prompt + search_result_prompt).strip(), assistant_prompt=assistant_prompt)


if __name__ == "__main__":
    asker = Asker(prompt_file="prompts/ask.yaml", model="claude-3-sonnet-20240229")
    asker.ask("Which planet has the most moons?")
