# api/services.py

import requests
from decimal import Decimal
from django.conf import settings
from decouple import config


class ExchangeRateService:
    @staticmethod
    def get_exchange_rate(currency_code):
        """
        Get exchange rate for a given currency code against UAH.
        Returns a Decimal rate or raises an exception.
        """
        api_key = config('EXCHANGE_RATE_API_KEY')
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency_code}"

        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or data.get('result') != 'success':
            error_message = data.get('error', 'Unknown error')
            raise Exception(f"Exchange rate API error: {error_message}")

        # Get the UAH rate (if not available, raise exception)
        conversion_rates = data.get('conversion_rates', {})
        if 'UAH' not in conversion_rates:
            raise Exception("UAH exchange rate not available")

        return Decimal(str(conversion_rates['UAH']))
