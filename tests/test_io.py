import json
import unittest

from ecmof_pipeline.io import strip_error_comments


class StripErrorCommentsTests(unittest.TestCase):
    def test_removes_legacy_comment(self):
        source = '{"value": 1, //error\n "next": 2}'
        self.assertEqual(json.loads(strip_error_comments(source)), {"value": 1, "next": 2})

    def test_preserves_comment_text_inside_string(self):
        source = '{"value": "https://example.test//error"}'
        self.assertEqual(json.loads(strip_error_comments(source))["value"], "https://example.test//error")


if __name__ == "__main__":
    unittest.main()
