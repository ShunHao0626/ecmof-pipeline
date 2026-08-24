import unittest

from ecmof_pipeline.validate import best_evidence, validate_records


class ValidationTests(unittest.TestCase):
    def test_exact_match(self):
        score, chunk_index = best_evidence("Cu3(HHTP)2", ["The material Cu3(HHTP)2 was synthesized."])
        self.assertEqual(score, 1.0)
        self.assertEqual(chunk_index, 0)

    def test_report_counts_matches(self):
        records = [{"MOF_name": "Cu-HHTP", "application": "sensor"}]
        report = validate_records(records, ["Cu-HHTP was used as a sensor."], threshold=0.8)
        self.assertEqual(report["summary"]["fields_checked"], 2)
        self.assertEqual(report["summary"]["fields_matched"], 2)


if __name__ == "__main__":
    unittest.main()
