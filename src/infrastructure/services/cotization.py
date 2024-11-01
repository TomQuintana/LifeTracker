import requests


class Cotization:
    """
    Service for Cotization.
    """

    def __init__(self, crypto_currency):
        self.crypto_currency = crypto_currency

    async def _obtain(self) -> float | None:
        url = "https://min-api.cryptocompare.com/data/pricemultifull"
        params = {"fsyms": self.crypto_currency, "tsyms": "ARS"}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            print(data)
            return data["RAW"]["USDT"]["ARS"]["PRICE"]

    async def calculate_cotization(self, buy_price: float) -> float:
        print(self.crypto_currency)
        cotization_value: float | None = await self._obtain()
        cotization_market_int = int(cotization_value or 0)
        total_cotization: int | float = round((buy_price / cotization_market_int), 2)

        return total_cotization
