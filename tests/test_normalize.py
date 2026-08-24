import unittest

from ecmof_pipeline.normalize import flatten_records, normalize_record
from ecmof_pipeline.schema import EXPECTED_FIELDS


class NormalizeTests(unittest.TestCase):
    def test_flattens_accidentally_nested_arrays(self):
        value = [{"MOF_name": "A"}, [{"MOF_name": "B"}, {"MOF_name": "C"}]]
        self.assertEqual([item["MOF_name"] for item in flatten_records(value)], ["A", "B", "C"])

    def test_orders_expected_fields_and_preserves_extra_fields(self):
        result = normalize_record({"MOF_name": "A", "review_note": "check"})
        self.assertEqual(list(result)[: len(EXPECTED_FIELDS)], list(EXPECTED_FIELDS))
        self.assertEqual(result["review_note"], "check")


if __name__ == "__main__":
    unittest.main()
