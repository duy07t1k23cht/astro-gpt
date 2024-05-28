import os
import sys

sys.path.append(".")

import anthropic
from openai import OpenAI

from src.utils.file_utils import load_yaml
from src.views.custom_logger import logger

CLAUDE_MODELS = ["claude-2.1", "claude-3-opus-20240229", "claude-3-haiku-20240307", "claude-3-sonnet-20240229"]

OPENAI_MODELS = ["gpt-3.5-turbo-0125", "gpt-4o", "gpt-4-turbo"]


class BaseAgent:
    def __init__(self, prompt_file: str = None, model: str = "gpt-4o") -> None:
        self.model = model
        if model in CLAUDE_MODELS:
            self.client = anthropic.Anthropic(
                api_key=os.getenv("CLAUDE_API_KEY"),
            )
        elif model in OPENAI_MODELS:
            self.client = OpenAI()
        else:
            raise ValueError(f"The model {model} does not in either CLAUDE_MODELS or OPENAI_MODELS")

        if prompt_file:
            prompt = load_yaml(prompt_file)
        else:
            prompt = {}

        self.system_prompt = prompt.get("system", "")
        self.user_prompt = prompt.get("user", "{}")

    def execute(self, *args, **kwargs) -> str:
        question = self.user_prompt.format(*args)
        if "assistant_prompt" in kwargs:
            assistant_prompt = kwargs["assistant_prompt"]
        else:
            assistant_prompt = ""
            
        if isinstance(self.client, OpenAI):
            return self.ask_gpt(question, assistant_prompt=assistant_prompt)
        else:
            return self.ask_claude(question, assistant_prompt=assistant_prompt)

    def ask_gpt(self, question: str, assistant_prompt: str = "") -> str:
        question = question.strip()

        if not question:
            logger.w("The prompt cannot be empty!")
            return

        try:
            logger.i(f"New prompt: Model {self.model}\n\tSystem: {self.system_prompt}\n\tUser: {question}")

            if self.system_prompt:
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": question},
                ]
            else:
                logger.w("Asking without system prompt.")
                messages = [{"role": "user", "content": question}]

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )

            response = completion.choices[0].message.content

            logger.i(f"\n\tAssistant: {response}")
            logger.i("=" * 120 + "Finish request")

            return response

        except Exception as e:
            logger.e(f"Oops! Something went wrong: {e}")
            return ""

    def ask_claude(self, question: str, assistant_prompt: str = "") -> str:
        question = question.strip()

        if not question:
            logger.w("The prompt cannot be empty!")
            return

        try:
            logger.i(f"New prompt: Model {self.model}\n\tSystem: {self.system_prompt}\n\tUser: {question}")

            messages = [{"role": "user", "content": question}]
            if assistant_prompt:
                messages.append({"role": "assistant", "content": assistant_prompt})

            if self.system_prompt:
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    system=self.system_prompt,  # <-- system prompt
                    messages=messages,  # <-- user prompt
                )
            else:
                logger.w("Asking without system prompt.")
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=messages,  # <-- user prompt
                )

            response = message.content
            if response:
                response = response[0].text
                logger.i(f"\n\tAssistant: {response}")
                logger.i("=" * 120 + "Finish request")
            else:
                response = ""

            return response

        except Exception as e:
            logger.e(f"Oops! Something went wrong: {e}")
            return ""


def main():
    client = BaseAgent("prompts/default.yaml", model="gpt-4-turbo")
    client.execute("Which planet has the most moons?")


if __name__ == "__main__":
    main()
