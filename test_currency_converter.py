import unittest
from currency_converter import CurrencyConverter, CurrencyNotFoundError

class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CurrencyConverter(base_currency="USD")
        self.converter.set_rates({
            "EUR": 0.85,
            "GBP": 0.75,
            "JPY": 110.0,
        })

    def test_initialization(self):
        converter = CurrencyConverter("eur")
        self.assertEqual(converter.base_currency, "EUR")
        self.assertIn("EUR", converter.rates)
        self.assertEqual(converter.rates["EUR"], 1.0)

    def test_add_rate(self):
        self.converter.add_rate("CAD", 1.25)
        self.assertEqual(self.converter.rates["CAD"], 1.25)

        # Updating existing rate
        self.converter.add_rate("EUR", 0.90)
        self.assertEqual(self.converter.rates["EUR"], 0.90)

    def test_invalid_add_rate(self):
        with self.assertRaises(ValueError):
            self.converter.add_rate("", 1.5)
        with self.assertRaises(ValueError):
            self.converter.add_rate("AUD", -1.0)
        with self.assertRaises(ValueError):
            self.converter.add_rate("AUD", 0)

    def test_convert_same_currency(self):
        result = self.converter.convert(100, "USD", "USD")
        self.assertEqual(result, 100)

    def test_convert_from_base(self):
        # 100 USD to EUR (0.85 rate) -> 85 EUR
        result = self.converter.convert(100, "USD", "EUR")
        self.assertEqual(result, 85.0)

    def test_convert_to_base(self):
        # 85 EUR to USD -> 85 / 0.85 = 100 USD
        result = self.converter.convert(85, "EUR", "USD")
        self.assertEqual(result, 100.0)

    def test_convert_cross_currency(self):
        # 85 EUR to GBP: (85 / 0.85) * 0.75 = 100 * 0.75 = 75 GBP
        result = self.converter.convert(85, "EUR", "GBP")
        self.assertEqual(result, 75.0)

    def test_convert_case_insensitive(self):
        result = self.converter.convert(100, "usd", "eur")
        self.assertEqual(result, 85.0)

    def test_convert_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.converter.convert(-10, "USD", "EUR")

    def test_convert_unknown_currency(self):
        with self.assertRaises(CurrencyNotFoundError):
            self.converter.convert(100, "USD", "XYZ")
        with self.assertRaises(CurrencyNotFoundError):
            self.converter.convert(100, "ABC", "EUR")


if __name__ == "__main__":
    unittest.main()
