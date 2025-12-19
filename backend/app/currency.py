import httpx
from decimal import Decimal
from typing import Optional
from .config import settings

API_BASE_URL = "https://v6.exchangerate-api.com/v6"

async def get_exchange_rate(base_currency: str, target_currency: str) -> Optional[Decimal]:
    """
    Fetches the exchange rate from base_currency to target_currency.

    :param base_currency: The currency of the expense (e.g., "EUR").
    :param target_currency: The user's base currency (e.g., "USD").
    :return: The exchange rate as a Decimal, or None if an error occurs.
    """
    if base_currency == target_currency:
        return Decimal("1.0")

    if not settings.EXCHANGE_RATE_API_KEY:
        print("Warning: EXCHANGE_RATE_API_KEY is not set. Cannot perform currency conversion.")
        return None

    url = f"{API_BASE_URL}/{settings.EXCHANGE_RATE_API_KEY}/latest/{base_currency}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
            
            data = response.json()
            
            if data.get("result") == "success":
                rate = data.get("conversion_rates", {}).get(target_currency)
                if rate:
                    return Decimal(str(rate))
                else:
                    print(f"Error: Target currency '{target_currency}' not found in API response.")
                    return None
            else:
                print(f"Error from currency API: {data.get('error-type')}")
                return None

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during currency conversion: {e}")
        return None