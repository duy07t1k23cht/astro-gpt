from src.base import BaseAgent


class Translator:
    def __init__(self, prompt_file: str, model: str) -> None:
        self.agent = BaseAgent(prompt_file, model=model)

    def translate(self, input: str, assistant_prompt: str = "") -> str:
        return self.agent.execute(input, assistant_prompt=assistant_prompt)


if __name__ == "__main__":
    translator = Translator()
    translator.translate("Giải thích thuyết Big Bang")
    translator.translate("Explain the Big Bang theory")
