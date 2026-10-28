import os
from typing import Optional
from dotenv import load_dotenv
from google import genai
from utils.config import SYSTEM_PROMPT

# TODO: Load environment variables

class LLMClient:
    """Client for interacting with Gemini API for campus event Q&A."""
    
    def __init__(self, api_key: Optional[str] = None):
        # TODO: Initialize the API key
        # TODO: Raise ValueError if no API key found
        # TODO: Initialize the genai Client
        
        pass
    
    def call_api(self, user_query: str) -> str:
        """Call Gemini API with system prompt and user query."""
        # TODO: Format the prompt with user query
        
        # TODO: Make API call to llm
        
        # TODO: Handle empty or None response
        
        # TODO: Return the response text
        
        pass


def answer_student_query(query: str) -> str:
    """Answer a student's query about campus events."""
    # TODO: Create llmClient instance
    # TODO: Call the API
    # TODO: Handle exceptions and return error message if needed
    
    pass


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
