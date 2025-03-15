from django.urls import path
from api.views import RegisterView, LoginView, LogoutView, FetchCryptoData

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # fetch crypto data
    path('fetchCryptoData/', FetchCryptoData.as_view(), name='fetch-crypto-data')
]