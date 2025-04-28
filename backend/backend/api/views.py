import json
from datetime import timedelta, datetime
import base64
import io
from rest_framework_simplejwt.tokens import AccessToken
import matplotlib.pyplot as plt
import matplotlib
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import yfinance as yf
import numpy as np
import pandas as pd
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import LoginSerializer, RegisterSerializer, CryptoSymbolSerializer
from django.contrib.auth import authenticate
from django.core.cache import cache

from newsapi import NewsApiClient

import os
from dotenv import load_dotenv

from django.http import JsonResponse
from django.db import connection, OperationalError

from api.prediction_analysis import price_prediction_analysis
from api.sentiment_analysis import sentiment_and_prediction_analysis
from api.models import CryptoSymbols

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import CustomUser

load_dotenv()


# Create your views here.

matplotlib.use('Agg')

# Authentications


def health_check(request):
    db_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            one = cursor.fetchone()
            if one is None or one[0] != 1:
                db_status = "error"
    except OperationalError as e:
        db_status = f"error: {str(e)}"

    return JsonResponse({
        "api": "ok",
        "database": db_status,
        "status": "ok" if db_status == "ok" else "error"
    })


class RegisterView(APIView):
    def post(self, request):
        # Validasi apakah format email benar
        email = request.data.get('email')
        try:
            validate_email(email)  # Validasi format email
        except ValidationError:
            return Response({"email": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        # Cek apakah email sudah ada
        if CustomUser.objects.filter(email=email).exists():
            return Response({"email": "Email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user:
                # Issue access token
                access_token = AccessToken.for_user(user)
                response = Response({
                    "access": str(access_token),
                    "role": user.role.name,
                    "username": user.username,
                    "email": user.email,
                })

                return response

            return Response({
                "error": "Invalid Credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Since we're not using refresh tokens or cookies, just return a success message
            response = Response(
                {"message": "User logged out successfully"}, status=status.HTTP_200_OK)
            return response

        except Exception as e:
            return Response({
                "error": "Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)


# fetch crypto historical api

class FetchCryptoData(APIView):
    def post(self, request):
        try:
            coin = request.data.get("coin")
            if not coin:
                return Response({"error": "Coin parameter is required"}, status=400)

            cache_key = f"crypto_{coin}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=200)

            url = f"https://api.coingecko.com/api/v3/coins/{coin}"
            response = requests.get(url)
            if response.status_code != 200:
                return Response({"error": "Failed to fetch data from API"}, status=response.status_code)

            data = response.json()
            coin_data = {
                "Price": data["market_data"]["current_price"]["usd"],
                "MarketCap": data["market_data"]["market_cap"]["usd"],
                "Volume24h": data["market_data"]["total_volume"]["usd"],
                "FDV": data["market_data"].get("fully_diluted_valuation", {}).get("usd"),
                "TotalSupply": data["market_data"].get("total_supply"),
                "MaxSupply": data["market_data"].get("max_supply"),
                "CirculatingSupply": data["market_data"].get("circulating_supply"),
                "MarketCapChangePercentage": data["market_data"].get("market_cap_change_percentage_24h"),
                "Description": data["description"].get("en", "")
            }

            cache.set(cache_key, coin_data, timeout=600)
            return Response(coin_data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class FetchCryptoChart(APIView):
    def post(self, request):
        try:
            coin = request.data.get("coin")
            period = request.data.get("period", "week")

            if not coin:
                return Response({"error": "Coin parameter is required"}, status=400)

            period_mapping = {"week": 7, "month": 30, "all": "max"}
            if period not in period_mapping:
                return Response({"error": "Invalid period"}, status=400)

            days = period_mapping[period]
            cache_key_chart = f"crypto_history_{coin}_{days}"
            cached_chart = cache.get(cache_key_chart)

            if cached_chart:
                return Response({"chart": cached_chart}, status=200)

            url_history = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}&interval=daily"
            response = requests.get(url_history)
            if response.status_code != 200:
                return Response({"error": "Failed to fetch historical data from API"}, status=response.status_code)

            data = response.json()
            prices = data.get("prices", [])
            if not prices:
                return Response({"error": "No historical data available"}, status=404)

            cache.set(cache_key_chart, prices, timeout=600)
            return Response({"chart": prices}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

 # Get the full path
model = load_model(
    'D:/Documents/Haikal Politeknik Negeri Batam/Semester 6/PBL/crypto_price_prediction/backend/backend/api/lstm_model.keras')  # Load the model

# helper function to convert matplotlib plots


def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    buf.close()
    return f"data:image/png;base64,{data}"


class fetchCryptoPrediction(APIView):
    def post(self, request):
        try:
            coin = request.data.get("coin")
            no_of_days = request.data.get("no_of_days", 2)

            # cache key
            cache_key = f"{coin}_{no_of_days}_prediction"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=200)

            # fetch crypto data
            end = datetime.now()
            start = datetime(end.year - 10, end.month, end.day)
            coin_data = yf.download(coin, start=start, end=end)

            # data preparation
            splitting_len = int(len(coin_data) * 0.8)
            x_test = coin_data[['Close']][splitting_len:]
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(x_test)

            x_data = []
            y_data = []
            base_days = 100
            for i in range(base_days, len(scaled_data)):
                x_data.append(scaled_data[i-base_days: i])
                y_data.append(scaled_data[i])

            x_data = np.array(x_data)
            y_data = np.array(y_data)

            # Predictions
            predictions = model.predict(x_data)
            inv_predictions = scaler.inverse_transform(predictions)
            inv_y_test = scaler.inverse_transform(y_data)

            x_data = np.array(x_data)
            y_data = np.array(y_data)

            # prepare data for plotting
            plotting_data = pd.DataFrame({
                'Original Test Data': inv_y_test.flatten(),
                'Predicted Test Data': inv_predictions.flatten()
            }, index=x_test.index[base_days:])


            # General Plot
            # Plot 1: Original Closing Prices
            fig1 = plt.figure(figsize=(15, 6))
            plt.plot(coin_data['Close'], 'b', label='Close Price')
            plt.title('Closing Price Over Time')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.legend()
            original_plot = plot_to_base64(fig1)
            plt.close(fig1)

            # plot 2: Original vs Predicted Data
            fig2 = plt.figure(figsize=(15, 6))
            plt.plot(plotting_data['Original Test Data'],
                     label='Original Test Data', color='blue', linewidth=2)
            plt.plot(plotting_data['Predicted Test Data'],
                     label='Predicted Test Data', color='red', linewidth=2)
            plt.legend()
            plt.title('Original vs Predicted Test Data')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            predicted_plot = plot_to_base64(fig2)
            plt.close(fig2)

            # plot 3 : Future Predictions
            last_100 = coin_data[['Close']].tail(100)
            last_100_scaled = scaler.transform(last_100)

            future_predictions = []
            last_100_scaled = last_100_scaled.reshape(1, -1, 1)
            for _ in range(no_of_days):
                next_day = model.predict(last_100_scaled)
                future_predictions.append(scaler.inverse_transform(next_day))
                last_100_scaled = np.append(
                    last_100_scaled[:, 1:, :], next_day.reshape(1, 1, -1), axis=1)

            future_predictions = np.array(future_predictions).flatten()

            # price prediction analysis
            price_analysis_data = price_prediction_analysis(coin, future_predictions)

            # sentiment analysis
            sentiment_label, recommendation, final_score, summarize = sentiment_and_prediction_analysis(coin, future_predictions)

            result = {
                "original_plot": original_plot,
                "predicted_plot": predicted_plot,
                "future_plot": future_predictions,
                "predict_price_analysis": price_analysis_data,
                "sentiment_label": sentiment_label,
                "recommendation": recommendation,
                "final_score": final_score,
                "summarize": summarize,
            }

            # cache the result
            cache.set(cache_key, result, timeout=60 * 60)

            return Response(result, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)



# Top Volume Coins
class TopVolumeCoinView(APIView):
    def get(self, request):
        cached_data = cache.get('top_volume_coins')
        if cached_data:
            return Response(cached_data)

        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {'vs_currency': 'usd', 'order': 'volume_desc', 'per_page': 10, 'page': 1}
        response = requests.get(url, params=params).json()

        cache.set('top_volume_coins', response, timeout=300)

        return Response(response)
    

# Crypto List
class CryptoListView(APIView):
    def get(self, request):
        
        cached_data = cache.get('crypto_symbol_list')
        if cached_data:
            return Response(cached_data)

        crypto_symbols = CryptoSymbols.objects.all()
        serializer = CryptoSymbolSerializer(crypto_symbols, many=True)

        cache.set('crypto_symbol_list', serializer.data, 86400)

        return Response(serializer.data)

# Trending Coins
class TrendingCoinView(APIView):
    def get(self, request):

        cached_data = cache.get('trending_coins')
        if cached_data:
            return Response(cached_data)

        # Ambil trending coins
        trending_url = 'https://api.coingecko.com/api/v3/search/trending'
        trending_data = requests.get(trending_url).json()

        # Ambil harga 1 BTC dalam USD
        btc_price_url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {'ids': 'bitcoin', 'vs_currencies': 'usd'}
        btc_price_data = requests.get(btc_price_url, params=params).json()
        btc_to_usd = btc_price_data.get('bitcoin', {}).get('usd', 0)

        coins = trending_data.get('coins', [])[:10]
        
        simplified = []
        for coin in coins:
            price_btc = coin['item']['price_btc']
            price_usd = price_btc * btc_to_usd if btc_to_usd else None

            simplified.append({
                'name': coin['item']['name'],
                'symbol': coin['item']['symbol'],
                'market_cap_rank': coin['item']['market_cap_rank'],
                'price_btc': price_btc,
                'price_usd': price_usd,
            })

        cache.set('trending_coins', simplified, timeout=300)

        return Response(simplified)
    
# market cap
class MarketCapRankingView(APIView):
    def get(self, request):
        
        cached_data = cache.get('market_cap_rankings')
        if cached_data:
            return Response(cached_data)

        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 10, 'page': 1}
        response = requests.get(url, params=params).json()

        cache.set('market_cap_rankings', response, timeout=300)

        return Response(response)

# top exchanges 
class TopExchangesView(APIView):
    def get(self, request):
        
        cached_data = cache.get('top_exchanges')
        if cached_data:
            return Response(cached_data)

        url = 'https://api.coingecko.com/api/v3/exchanges'
        data = requests.get(url).json()
        top_exchanges = data[:10]  # ini baru aman kalau data itu list

        cache.set('top_exchanges', top_exchanges, timeout=300)

        return Response(top_exchanges)
    


class CryptoNewsListView(APIView):
    def get(self, request):
        cached_data = cache.get('crypto_news_list')
        if cached_data:
            return Response(cached_data)
        
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        all_articles = newsapi.get_everything(
            q='cryptocurrency',
            language='en',
            sort_by='publishedAt',
            page_size=50
        )

        news_data = []
        for article in all_articles.get('articles', []):
            news_data.append({
                'title': article.get('title'),
                'image': article.get('urlToImage'),
                'link': article.get('url')
            })

        cache.set('crypto_news_list', news_data, 3600)

        return Response(news_data)