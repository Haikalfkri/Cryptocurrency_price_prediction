from django.urls import path
from api.views import *

urlpatterns = [
    path('health', health_check, name='health_check'),

    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # fetch crypto data
    path('fetchCryptoData/', FetchCryptoData.as_view(), name='fetch-crypto-data'),
    path('fetchCryptoChart/', FetchCryptoChart.as_view(), name='fetch-crypto-chart'),
    path('predictedCryptoData/', fetchCryptoPrediction.as_view(), name='predicted-crypto-data'),
    path('cryptoList/', CryptoListView.as_view(), name='crypto-list'),

    # news
    path('cryptoNewsList/', CryptoNewsListView.as_view(), name='crypto-news-list'),
    path('cryptoInsightList/', CryptoInsightNewsListView.as_view(), name='crypto-insight-list'),

    # Coins
    path('topVolumeCoin/', TopVolumeCoinView.as_view(), name='top-volume-coin'),
    path('trendingCoin/', TrendingCoinView.as_view(), name='trending-coin-view'),
    path('marketCapRankings/', MarketCapRankingView.as_view(), name='market-cap'),
    path('topExchangesRankings/', TopExchangesView.as_view(), name='top-exchanges'),
    
    # user
    path('userFeedback/', UserFeedbackView.as_view(), name='user-feedback'),
]