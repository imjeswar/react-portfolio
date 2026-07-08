from typing import List, Dict, Any, Generator
from openai import OpenAI
from backend.core.interfaces import LLMProvider
from backend.core.config import settings

class OpenAILLMProvider(LLMProvider):
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured in environment variables.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o"  # fallback to gpt-4o

    def _prepare_messages(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if history:
            for message in history:
                messages.append({
                    "role": message.get("sender", "user").replace("assistant", "assistant").replace("user", "user"),
                    "content": message.get("text", "")
                })

        messages.append({"role": "user", "content": prompt})
        return messages

    def generate(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        messages = self._prepare_messages(prompt, system_prompt, history)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2
            )
            return {
                "answer": response.choices[0].message.content,
                "confidence": 0.9
            }
        except Exception as e:
            # Gracefully handle API errors (e.g. Quota Exceeded 429)
            from backend.rag.chat.openai_llm import MockLLMProvider
            mock_res = MockLLMProvider().generate(prompt, system_prompt, history)
            return {
                "answer": f"⚠️ **[OpenAI API Error: {str(e)}]**\n\nYour OpenAI API key has exceeded its quota or is invalid. Switching dynamically to RAG grounding with Mock LLM response:\n\n{mock_res['answer']}",
                "confidence": 0.5
            }

    def generate_stream(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        messages = self._prepare_messages(prompt, system_prompt, history)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            # Stream out the error callout and fall back to streaming mock content
            yield f"⚠️ **[OpenAI API Error: {str(e)}]**\n\nYour OpenAI API key has exceeded its quota or is invalid. Switching dynamically to RAG grounding with Mock LLM response:\n\n"
            
            from backend.rag.chat.openai_llm import MockLLMProvider
            mock_llm = MockLLMProvider()
            for chunk in mock_llm.generate_stream(prompt, system_prompt, history):
                yield chunk


class MockLLMProvider(LLMProvider):
    def generate(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        return {
            "answer": f"This is a mock RAG response for prompt: '{prompt}'. Overriding LLM answer to save API tokens.\n\nCitation check: [Employee Handbook, Page 12, Section 2.1].",
            "confidence": 0.95
        }

    def generate_stream(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        full_text = f"This is a streamed mock response for prompt: '{prompt}'. It is grounded in the retrieved document context. According to the policies, employee leave is 20 days per year [Employee Handbook, Page 18, Section 4.2]. If you have any further questions, please ask."
        for word in full_text.split(" "):
            yield word + " "
