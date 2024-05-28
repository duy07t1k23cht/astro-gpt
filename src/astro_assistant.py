from src.base import BaseAgent
from src.engine.ask.ask import Asker
from src.engine.question_eval.question_eval import Evaluator
from src.engine.search import serper
from src.engine.translate.language_detector import LanguageDetector
from src.engine.translate.translate import Translator
from src.views.custom_logger import logger


class Assistant:
    def __init__(
        self,
        en_translate_prompt_file: str,
        vi_translate_prompt_file: str,
        question_eval_prompt_file: str,
        ask_prompt_file: str,
        language_detector_prompt_file: str,
        base_model: str,
    ) -> None:
        """Initialize the AI assistant.

        Args:
            en_translate_prompt_file (str): Path to the YAML file containing the configuration of prompts for translation to English.
            vi_translate_prompt_file (str): Path to the YAML file containing the configuration of prompts for translation to Vietnamese.
            question_eval_prompt_file (str): Path to the YAML file containing the configuration of prompts for evaluating input questions.
            ask_prompt_file (str): Path to the YAML file containing the configuration of prompts for answering input questions.
            language_detector_prompt_file (str): Path to the YAML file containing the configuration of prompts for language detection of input questions.
            base_model (str): Name of the GPT base model or ClaudeAI base model.
        """
        logger.i(f"Initializing agents:\n\ten_translate_prompt_file: '{en_translate_prompt_file}'")

        self.en_translator = Translator(prompt_file=en_translate_prompt_file, model=base_model)
        self.vi_translator = Translator(prompt_file=vi_translate_prompt_file, model="gpt-3.5-turbo-0125")
        self.asker = Asker(prompt_file=ask_prompt_file, model=base_model)
        self.evaluator = Evaluator(prompt_file=question_eval_prompt_file, model=base_model)
        self.language_detector = LanguageDetector(prompt_file=language_detector_prompt_file, model="gpt-3.5-turbo-0125")

    def execute(self, question: str) -> str:
        """Perform assistance for the input question.

        Args:
            question (str): The input question.

        Returns:
            str: The response of the assistant.
        """
        # Determine the language of the input question.
        language = self.language_detector.detect(question)

        # Translate it to English if necessary.
        if language == "vi":
            english_question = self.en_translator.translate(
                question,
                assistant_prompt="Here is the translation:",
            ).strip()
        else:
            english_question = question.strip()

        # Evaluate the question if it is related to astronomy.
        eval_result = self.evaluator.eval(english_question)

        # Provide assistance if the question is related to astronomy; refuse to assist otherwise.
        if "yes" in eval_result.lower() and len(eval_result.strip()) < 5:
            search_results = serper.simplify_search(query=english_question)
            
            english_response = self.asker.ask(
                english_question,
                search_results,
                current_time=True,
                assistant_prompt="Based on the provided information and my knowledge, here is my answer:",
            )
        else:
            english_response = eval_result

        # Translate the answer to the original language and return it.
        if language == "vi":
            return self.vi_translator.translate(english_response)
        else:
            return english_response

    def ask(self, input: str):
        return self.default_assistant.ask_gpt(input)


if __name__ == "__main__":
    assistant = Assistant(
        en_translate_prompt_file="prompts/translate-en.yaml",
        vi_translate_prompt_file="prompts/translate-vi.yaml",
        ask_prompt_file="prompts/ask.yaml",
        question_eval_prompt_file="prompts/eval.yaml",
        language_detector_prompt_file="prompts/language_detector.yaml",
        base_model="claude-3-sonnet-20240229",
    )
    # question = "Ronaldo có mấy quả bóng vàng?"
    # question = "Giải thích chi tiết thuyết Big Bang"
    # question = "Explain the big bang theory"
    # question = "lần nhật thực tiếp theo là vào khi nào?"
    # question = "Lần nguyệt thực tiếp theo là vào khi nào?"
    question = "Hành tinh nào có nhiều mặt trăng nhất trong hệ mặt trời và nó có bao nhiêu mặt trăng?"
    # question = "Nhật quyển là gì?"

    response1 = assistant.execute(question)
