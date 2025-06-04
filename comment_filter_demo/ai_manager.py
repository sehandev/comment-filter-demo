import os

import anthropic
import openai
from dotenv import load_dotenv
from google import genai

load_dotenv()


class AI_Manager:
    available_model_dict = {
        "gpt-4o": {
            "api": "openai",
            "snapshot": "gpt-4o-2024-11-20",
        },
        "o4-mini": {
            "api": "openai",
            "snapshot": "o4-mini-2025-04-16",
        },
        "o3": {
            "api": "openai",
            "snapshot": "o3-2025-04-16",
        },
        "gemini-2.5-pro": {
            "api": "gemini",
            "snapshot": "gemini-2.5-pro-preview-05-06",
        },
        "gemini-2.5-flash": {
            "api": "gemini",
            "snapshot": "gemini-2.5-flash-preview-05-20",
        },
        "claude-3-7-sonnet": {
            "api": "anthropic",
            "snapshot": "claude-3-7-sonnet-20250219",
        },
        "claude-sonnet-4": {
            "api": "anthropic",
            "snapshot": "claude-sonnet-4-20250514",
        },
        "claude-opus-4": {
            "api": "anthropic",
            "snapshot": "claude-opus-4-20250514",
        },
    }
    model_name: str = "gemini-2.5-flash"
    api_key: dict[str, str] = {
        "openai": "",
        "gemini": "",
        "anthropic": "",
    }

    def __init__(self, model_name: str):
        if model_name not in self.available_model_dict:
            raise ValueError(f"Invalid model: {model_name}")
        self.model_name = model_name
        self.api_key["openai"] = os.getenv("OPENAI_API_KEY", "")
        self.api_key["gemini"] = os.getenv("GEMINI_API_KEY", "")
        self.api_key["anthropic"] = os.getenv("ANTHROPIC_API_KEY", "")

    def validate_model(self, model_name: str) -> bool:
        if model_name not in self.available_model_dict:
            return False
        api_provider = self.available_model_dict[model_name]["api"]

        match api_provider:
            case "openai":
                return validate_openai_api_key()
            case "gemini":
                return validate_gemini_api_key()
            case "anthropic":
                return validate_anthropic_api_key()
            case _:
                raise ValueError(f"Invalid API provider: {api_provider}")

    def get_response_openai(self, prompt: str) -> str:
        client = openai.OpenAI(api_key=self.api_key["openai"])
        response = client.chat.completions.create(
            model=self.available_model_dict[self.model_name]["snapshot"],
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def get_response_gemini(self, prompt: str) -> str:
        genai.configure(api_key=self.api_key["gemini"])
        client = genai.Client(api_key=self.api_key["gemini"])
        response = client.models.generate_content(
            model=self.available_model_dict[self.model_name]["snapshot"],
            contents=prompt,
        )
        return response.text

    def get_response_anthropic(self, prompt: str) -> str:
        client = anthropic.Anthropic(api_key=self.api_key["anthropic"])
        response = client.messages.create(
            model=self.available_model_dict[self.model_name]["snapshot"],
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        )
        return response.content[0].text

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
