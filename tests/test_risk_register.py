import unittest

from src.risk_register import risk_level


class RiskLevelTests(unittest.TestCase):
    def test_critical_band(self):
        self.assertEqual(risk_level(20), "Critical")
        self.assertEqual(risk_level(25), "Critical")

    def test_high_band(self):
        self.assertEqual(risk_level(12), "High")
        self.assertEqual(risk_level(19), "High")

    def test_moderate_band(self):
        self.assertEqual(risk_level(6), "Moderate")
        self.assertEqual(risk_level(11), "Moderate")

    def test_low_band(self):
        self.assertEqual(risk_level(1), "Low")
        self.assertEqual(risk_level(5), "Low")


if __name__ == "__main__":
    unittest.main()
