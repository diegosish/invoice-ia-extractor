"""Tests para utilidades del cliente OpenAI."""

from src.clients.openai_client import _clean_markdown_json, _supports_json_mode


class TestCleanMarkdownJson:
    def test_strips_json_fence(self):
        text = '```json\n{"a": 1}\n```'
        assert _clean_markdown_json(text) == '{"a": 1}'

    def test_strips_plain_fence(self):
        text = '```\n{"a": 1}\n```'
        assert _clean_markdown_json(text) == '{"a": 1}'

    def test_no_fence_unchanged(self):
        text = '{"a": 1}'
        assert _clean_markdown_json(text) == '{"a": 1}'

    def test_handles_empty(self):
        assert _clean_markdown_json("") == ""


class TestSupportsJsonMode:
    def test_gpt_4o_mini_supports(self):
        assert _supports_json_mode("gpt-4o-mini") is True

    def test_gpt_4o_supports(self):
        assert _supports_json_mode("gpt-4o") is True

    def test_reasoning_models_dont_support(self):
        assert _supports_json_mode("o1-mini") is False
        assert _supports_json_mode("o4-mini") is False

    def test_old_models_dont_support(self):
        assert _supports_json_mode("gpt-3.5-turbo") is False
