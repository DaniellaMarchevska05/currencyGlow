# api/views.py
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import CurrencyExchangeSerializer
from .services import ExchangeRateService
from django.contrib.auth.models import User
from .models import UserBalance, CurrencyExchange
from django.db import transaction
from decimal import Decimal
from .serializers import UserRegistrationSerializer, UserBalanceSerializer

def frontend_view(request):
    return render(request, 'api/index.html')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully",
        }, status=status.HTTP_201_CREATED)


class UserBalanceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_balance = UserBalance.objects.get(user=request.user)
        serializer = UserBalanceSerializer(user_balance)
        return Response(serializer.data)


class CurrencyExchangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Get exchange rate for a currency, charge the user's balance,
        and store the result in the database.
        """
        currency_code = request.data.get('currency_code', '').upper()

        if not currency_code:
            return Response(
                {"error": "Currency code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user balance
        try:
            user_balance = UserBalance.objects.get(user=request.user)
        except UserBalance.DoesNotExist:
            return Response(
                {"error": "User balance not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user has balance
        if user_balance.balance <= 0:
            return Response(
                {"error": "Insufficient balance"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get exchange rate from external API
        try:
            rate = ExchangeRateService.get_exchange_rate(currency_code)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Update user balance and store exchange rate in atomic transaction
        try:
            with transaction.atomic():
                # Deduct 1 coin from user's balance
                user_balance.balance -= 1
                user_balance.save()

                # Create exchange rate record
                exchange = CurrencyExchange.objects.create(
                    user=request.user,
                    currency_code=currency_code,
                    rate=rate
                )

                serializer = CurrencyExchangeSerializer(exchange)

                # Add balance to response
                response_data = serializer.data
                response_data['balance_remaining'] = user_balance.balance

                return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"Transaction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR

            )


# api/views.py
# Add to existing file along with other views

class ExchangeHistoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Return the request history with optional filtering by currency and date.
        """
        queryset = CurrencyExchange.objects.filter(user=request.user)

        # Apply filters if provided
        currency = request.query_params.get('currency')
        if currency:
            queryset = queryset.filter(currency_code__iexact=currency)

        date = request.query_params.get('date')
        if date:
            queryset = queryset.filter(created_at__date=date)

        # Order by most recent first
        queryset = queryset.order_by('-created_at')

        # Serialize and return
        serializer = CurrencyExchangeSerializer(queryset, many=True)
        return Response(serializer.data)

