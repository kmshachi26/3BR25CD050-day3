class CurrencyConverterError(Exception):
    """Base exception for currency converter errors."""
    pass


class CurrencyNotFoundError(CurrencyConverterError):
    """Raised when a specified currency is not found in the exchange rates."""
    pass


class CurrencyConverter:
    """A flexible currency converter supporting multiple currencies and custom exchange rates."""

    def __init__(self, base_currency: str = "USD"):
        self.base_currency = base_currency.strip().upper()
        # Exchange rates stored relative to base_currency (base_currency: 1.0)
        self.rates = {self.base_currency: 1.0}

    def add_rate(self, currency: str, rate: float) -> None:
        """
        Add or update the exchange rate for a currency relative to the base currency.

        :param currency: The currency code (e.g. 'EUR', 'GBP').
        :param rate: The exchange rate (1 base_currency = rate currency).
        """
        if not isinstance(currency, str) or not currency.strip():
            raise ValueError("Currency code must be a non-empty string.")
        if rate <= 0:
            raise ValueError("Exchange rate must be positive.")

        code = currency.strip().upper()
        self.rates[code] = float(rate)

    def set_rates(self, rates: dict) -> None:
        """
        Set multiple exchange rates at once.

        :param rates: A dictionary mapping currency codes to exchange rates relative to the base currency.
        """
        for currency, rate in rates.items():
            self.add_rate(currency, rate)

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert an amount from one currency to another.

        :param amount: The amount of money to convert.
        :param from_currency: The currency code to convert from.
        :param to_currency: The currency code to convert to.
        :return: The converted amount.
        """
        if amount < 0:
            raise ValueError("Amount to convert cannot be negative.")

        from_curr = from_currency.strip().upper()
        to_curr = to_currency.strip().upper()

        if from_curr not in self.rates:
            raise CurrencyNotFoundError(f"Exchange rate for currency '{from_curr}' is not available.")
        if to_curr not in self.rates:
            raise CurrencyNotFoundError(f"Exchange rate for currency '{to_curr}' is not available.")

        # Convert from_currency to base currency, then base currency to to_currency
        # amount_in_base = amount / rates[from_curr]
        # result = amount_in_base * rates[to_curr]
        amount_in_base = amount / self.rates[from_curr]
        converted_amount = amount_in_base * self.rates[to_curr]
        return round(converted_amount, 4)
