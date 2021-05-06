import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .utils import get_current_btc_exchange_rate, save_or_update_current_exchange_rate
from .models import BtcRate
from .serializers import BtcRateSerializer


class GetCurrentBTCRate(APIView):
    """
    Get current BTC rate from DB
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get Current BTC Exchange Rate
        """
        exchange_rate = list(BtcRate.objects.all())
        return Response(BtcRateSerializer(exchange_rate, many=True).data)

    def post(self, request):
        """
        Get & Save Current BTC Exchange Rate
        """
        data = get_current_btc_exchange_rate()
        updated_exchange_rate = save_or_update_current_exchange_rate(data)
        return Response(BtcRateSerializer(updated_exchange_rate).data)
