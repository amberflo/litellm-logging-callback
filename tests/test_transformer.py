import unittest
import pathlib
import json

from amberflo.transformer import extract_events_from_log

_resources_path = pathlib.Path(__file__).parent.resolve() / "resources"


def _load_resource(name, ext):
    path = _resources_path / f"{name}.{ext}"
    with open(path, "r") as f:
        return json.load(f)


def _load_log(name):
    return _load_resource(name, "slo.json")


def _load_expected(name):
    return _load_resource(name, "expected.json")


def _write_resource(name, ext, data):
    path = _resources_path / f"{name}.{ext}"
    with open(path, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)


def _write_expected(name, data):
    _write_resource(name, "expected.json", data)


class TestTransformer(unittest.TestCase):
    def test_transformer_produces_events(self):
        cases = [
            "bedrock-anthropic-claude-haiku.completion",
            "openai-gpt-4o.completion",
            "openai-text-embedding-ada-002.embedding",
            "openai-team-key-a.completion",
            "openai-team-key-b.completion",
        ]

        for case in cases:
            with self.subTest(case=case):
                log = _load_log(case)

                events = extract_events_from_log(log)
                self.assertIsNotNone(events)

                expected = _load_expected(case)
                self.assertEqual(events, expected)

    def test_transformer_does_not_produce_events(self):
        cases = [
            "disabled-model.completion",
        ]

        for case in cases:
            with self.subTest(case=case):
                log = _load_log(case)

                events = extract_events_from_log(log)
                self.assertIsNone(events)
