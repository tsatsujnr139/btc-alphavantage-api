from rest_framework import serializers
from .models import BtcRate


class BtcRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BtcRate
        fields = ('exchange_rate', 'last_refreshed')