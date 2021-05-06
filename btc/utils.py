from alpha_vantage.cryptocurrencies import CryptoCurrencies
from django.conf import settings

import logging
from .models import BtcRate

logger = logging.getLogger(__name__)
cc = CryptoCurrencies(key=settings.ALPHAVANTAGE_API_KEY)


def get_current_btc_exchange_rate():
    data = cc.get_digital_currency_exchange_rate(from_currency='BTC', to_currency='USD')
    logger.info(f"ALPHAVANTAGE API RESPONSE {data}")
    return data[0]


def save_or_update_current_exchange_rate(data):
    existing_exchange_rate = BtcRate.objects.filter(pk=1)
    if len(existing_exchange_rate) > 0:
        existing_exchange_rate[0].exchange_rate = data["5. Exchange Rate"]
        existing_exchange_rate[0].last_refreshed = data["6. Last Refreshed"]
        existing_exchange_rate[0].save()
        return existing_exchange_rate[0]
    return BtcRate.objects.create(
        exchange_rate=data["5. Exchange Rate"],
        last_refreshed=data["6. Last Refreshed"]
    )
