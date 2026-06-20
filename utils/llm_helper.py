import os
import ollama


class LLMHelper:
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "qwen3:4b")
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.Client(host=self.host)

    def _load_prompt(self, filename: str, **replacements) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), f"../prompts/{filename}")
        with open(prompt_path) as f:
            text = f.read()
        for key, value in replacements.items():
            text = text.replace(f"{{{{{key}}}}}", value)
        return text

    def generate_test_cases(self, feature_description: str) -> str:
        prompt = self._load_prompt("test_case_generation.txt", feature=feature_description)
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]

    def analyze_failure(self, error_log: str) -> str:
        prompt = self._load_prompt("failure_analysis.txt", error_log=error_log)
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
