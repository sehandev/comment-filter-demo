import os

from dotenv import load_dotenv

load_dotenv()


class AI_Manager:
    available_models = [
        "gpt-4o",
        "o4-mini",
        "o3",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "claude-3-7-sonnet",
        "claude-sonnet-4",
        "claude-opus-4",
    ]
    model_name: str = "gemini-2.5-flash"
    api_key: dict[str, str] = {
        "openai": "",
        "gemini": "",
        "anthropic": "",
    }

    def __init__(self, model_name: str):
        if model_name not in self.available_models:
            raise ValueError(f"Invalid model: {model_name}")
        self.model_name = model_name
        self.api_key["openai"] = os.getenv("OPENAI_API_KEY", "")
        self.api_key["gemini"] = os.getenv("GEMINI_API_KEY", "")
        self.api_key["anthropic"] = os.getenv("ANTHROPIC_API_KEY", "")

    def validate_model(self, model_name: str) -> bool:
        match model_name:
            case "gpt-4o":
                return validate_openai_api_key()
            case "o4-mini":
                return validate_openai_api_key()
            case "o3":
                return validate_openai_api_key()
            case "gemini-2.5-pro":
                return validate_gemini_api_key()
            case "gemini-2.5-flash":
                return validate_gemini_api_key()
            case "claude-3-7-sonnet":
                return validate_anthropic_api_key()
            case "claude-sonnet-4":
                return validate_anthropic_api_key()
            case "claude-opus-4":
                return validate_anthropic_api_key()
            case _:
                raise ValueError(f"Invalid model: {model_name}")

    def get_response_openai(self, prompt: str) -> str:
        return "This is a response from OpenAI"

    def get_response_gemini(self, prompt: str) -> str:
        return "This is a response from Gemini"

    def get_response_anthropic(self, prompt: str) -> str:
        return "This is a response from Anthropic"

    def get_ai_response(self, prompt: str) -> str:
        if self.model_name.startswith("gpt") or self.model_name.startswith("o"):
            return self.get_response_openai(prompt)
        elif self.model_name.startswith("gemini"):
            return self.get_response_gemini(prompt)
        elif self.model_name.startswith("claude"):
            return self.get_response_anthropic(prompt)
        else:
            raise ValueError(f"No AI response method for model: {self.model_name}")


def validate_openai_api_key() -> bool:
    api_key = os.getenv("OPENAI_API_KEY")
    return bool(api_key)


def validate_gemini_api_key() -> bool:
    api_key = os.getenv("GEMINI_API_KEY")
    return bool(api_key)


def validate_anthropic_api_key() -> bool:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    return bool(api_key)
