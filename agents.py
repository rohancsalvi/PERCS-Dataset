from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

class OpenAIAgent:
    def __init__(self, model):
        self.model = model

    def generate_answer(self, answer_context, retries=2):
        try:
            completion = openai_client.chat.completions.create(
                model=self.model,
                messages=answer_context
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            if retries > 0:
                return self.generate_answer(answer_context, retries - 1)
            return None


class GeminiAIAgent:
    def __init__(self, model="google/gemini-2.0-flash-lite-001"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
        self.model = model

    def generate_answer(self, messages):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None


class MistralAIAgent:
    def __init__(self, model="mistralai/mixtral-8x7b-instruct"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
        self.model = model

    def generate_answer(self, messages):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None


class LlamaAgent:
    def __init__(self, model="meta-llama/llama-3.3-70b-instruct"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
        self.model = model

    def generate_answer(self, user_input):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=user_input
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None
