import os
from typing import Optional
from dotenv import load_dotenv
from google import genai
from utils.config import SYSTEM_PROMPT

load_dotenv()


class LLMClient:
    """Client for interacting with Gemini API for campus event Q&A."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        self.client = genai.Client(api_key=self.api_key)

    def call_api(self, user_query: str) -> str:
        """Call Gemini API with system prompt and user query."""
        full_prompt = SYSTEM_PROMPT.format(user_query=user_query)

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )

        text = getattr(response, "text", None) if response is not None else None
        if text is None or not text.strip():
            return "I didn't receive a valid response. Please try again."

        return text.strip()


def answer_student_query(query: str) -> str:
    """Answer a student's query about campus events."""
    try:
        client = LLMClient()
        return client.call_api(query)
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"


def main():
    """Main function to demonstrate the API calling functionality."""
    test_queries = [
        "When is the Tech Fest happening?",
        "Where is the Career Fair located?",
        "Tell me about the Hackathon",
        "What's the schedule for the Music Concert?",
        "Tell me a joke",
        "What's the weather like?"
    ]

    print("Campus Event Q&A Assistant")
    print("=" * 40)

    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {answer_student_query(query)}")
        print("-" * 40)


if __name__ == "__main__":
    main()