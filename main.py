import os
from typing import Optional
from dotenv import load_dotenv
from google import genai
from utils.config import SYSTEM_PROMPT

# Load environment variables
load_dotenv()


class LLMClient:
    """Client for interacting with Gemini API for campus event Q&A."""

    def __init__(self, api_key: Optional[str] = None):
        # Initialize the API key
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        # Raise ValueError if no API key found
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        # Initialize the genai Client
        self.client = genai.Client(api_key=self.api_key)

    def call_api(self, user_query: str) -> str:
        """Call Gemini API with system prompt and user query."""
        # Format the prompt with user query
        full_prompt = SYSTEM_PROMPT.format(user_query=user_query)
        # Make API call to llm
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )

        # Handle empty, None, or whitespace-only response
        text = getattr(response, "text", None) if response is not None else None
        if text is None or not text.strip():
            return "I didn't receive a valid response. Please try again."

        # Return the response text
        return text.strip()

def answer_student_query(query: str) -> str:
    """Answer a student's query about campus events."""
    try:
        # Create llmClient instance
        client = LLMClient()

        # Call the API
        return client.call_api(query)

    except Exception as e:
        # Handle exceptions and return error message if needed
        return f"Sorry, I encountered an error: {e}"

def main():
    """Main function to demonstrate the API calling functionality."""
    test_queries = [
        "When is the Tech Fest happening?",
        "Where is the Career Fair located?",
        "Tell me about the Hackathon",
        "What's the schedule for the Music Concert?",
        "Tell me a joke",  # Non-event query
        "What's the weather like?"  # Non-event query
    ]

    print("Campus Event Q&A Assistant")
    print("=" * 40)

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = answer_student_query(query)
        print(f"Response: {result}")
        print("-" * 40)


if __name__ == "__main__":
    main()