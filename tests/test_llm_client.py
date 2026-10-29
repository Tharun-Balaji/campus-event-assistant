import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from main import LLMClient, answer_student_query
from utils.config import SYSTEM_PROMPT


def make_client():
    """Create an LLMClient without requiring a real Gemini API key."""
    with patch("main.genai.Client") as mocked_genai_client:
        client = LLMClient(api_key="test-api-key")
    return client, mocked_genai_client


def test_prompt_replaces_only_user_query_and_preserves_json_braces():
    query = "When is the Tech Fest?"

    prompt = SYSTEM_PROMPT.replace("{user_query}", query)

    assert "{user_query}" not in prompt
    assert query in prompt
    assert '"event_name": "Tech Fest"' in prompt
    assert '"date": "2025-09-15"' in prompt
    assert '"location": "Main Auditorium"' in prompt
    # The JSON example's braces should still be present.
    assert "{" in prompt
    assert "}" in prompt


def test_call_api_sends_correct_model_and_prompt():
    client, _ = make_client()
    client.client.models.generate_content = MagicMock(
        return_value=SimpleNamespace(text='{"event_name": "Tech Fest"}')
    )
    query = "When is the Tech Fest?"
    expected_prompt = SYSTEM_PROMPT.replace("{user_query}", query)

    result = client.call_api(query)

    assert result == '{"event_name": "Tech Fest"}'
    client.client.models.generate_content.assert_called_once_with(
        model="gemini-2.5-flash",
        contents=expected_prompt,
    )


@pytest.mark.parametrize(
    "response",
    [
        None,
        SimpleNamespace(text=None),
        SimpleNamespace(text=""),
        SimpleNamespace(text="   \n\t  "),
    ],
    ids=["response-is-none", "text-is-none", "empty-text", "whitespace-text"],
)
def test_empty_api_response_returns_friendly_message(response):
    client, _ = make_client()
    client.client.models.generate_content = MagicMock(return_value=response)

    result = client.call_api("When is the Tech Fest?")

    assert result == "I didn't receive a valid response. Please try again."


def test_call_api_strips_response_whitespace():
    client, _ = make_client()
    client.client.models.generate_content = MagicMock(
        return_value=SimpleNamespace(text="  Hello student! \n")
    )

    assert client.call_api("Hello") == "Hello student!"


def test_answer_student_query_returns_api_error_message_when_client_raises():
    with patch("main.LLMClient", side_effect=RuntimeError("test failure")):
        result = answer_student_query("When is the Tech Fest?")

    assert result == "Sorry, I encountered an error: test failure"


def test_prompt_replacement_does_not_format_json_braces():
    """Regression test for the original KeyError caused by str.format()."""
    query = "Tell me about the Hackathon"
    prompt = SYSTEM_PROMPT.replace("{user_query}", query)

    # A JSON object in the prompt should not be treated as a format field.
    assert '"event_name"' in prompt
    assert query in prompt
