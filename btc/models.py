from django.db import models


class BtcRate(models.Model):
    """Model definition for Current BTC Rate"""
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=9, blank=False)
    last_refreshed = models.DateTimeField()

    def __str__(self):
        return f"Most Recently Retrieved BTC/USD Exchange Rate Is {self.exchange_rate} " \
               f"Last Refreshed at {self.last_refreshed}"
