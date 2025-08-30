from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"
# Make sure to set your API keys as environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENROUTER_API_KEY = "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"

openai_client = OpenAI(api_key=OPENAI_API_KEY)

class OpenAIAgent:
    def __init__(self, model):
        self.model = model

    def generate_answer(self, answer_context, retries=2):
        try:
            completion = openai_client.chat.completions.create(
                model=self.model,
                messages=answer_context)
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            if retries > 0:
                return self.generate_answer(answer_context, retries-1)
            return None

class GeminiAIAgent:
    def __init__(self, model="google/gemini-2.0-flash-lite-001"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY)
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
            api_key=OPENROUTER_API_KEY)
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
            api_key=OPENROUTER_API_KEY)
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