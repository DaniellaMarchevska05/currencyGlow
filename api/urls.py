# api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserBalanceView, CurrencyExchangeView, ExchangeHistoryView, home_view, register_view, balance_view, currency_view, history_view

urlpatterns = [
    # Frontend views
    path('', home_view, name='home'),
    path('app/', home_view, name='app_home'),
    path('register/', register_view, name='register_page'),
    path('balance/', balance_view, name='balance_page'),
    path('currency/', currency_view, name='currency_page'),
    path('history/', history_view, name='history_page'),

    # API endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/balance/', UserBalanceView.as_view(), name='balance'),
    path('api/currency/', CurrencyExchangeView.as_view(), name='currency'),
    path('api/history/', ExchangeHistoryView.as_view(), name='history'),
]
