from src.base import BaseAgent


class LanguageDetector:
    def __init__(self, prompt_file: str, model: str) -> None:
        self.agent = BaseAgent(prompt_file, model=model)

    def detect(self, input: str, assistant_prompt: str = "", default: str = "vi") -> str:
        detection = self.agent.execute(input, assistant_prompt=assistant_prompt).lower().strip()
        return detection if detection in ["en", "vi"] else default


if __name__ == "__main__":
    language_detector = LanguageDetector("prompts/language_detector.yaml", model="gpt-3.5-turbo-0125")
    # language_detector.detect("Giải thích thuyết Big Bang")
    language_detector.detect("Explain the big bang theory")
