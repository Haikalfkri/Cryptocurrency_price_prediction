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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import LoginSerializer, RegisterSerializer, CryptoSymbolSerializer, UserFeedbackSerializer
from django.contrib.auth import authenticate
from django.core.cache import cache

from concurrent.futures import ThreadPoolExecutor

from newsapi import NewsApiClient

import os
from dotenv import load_dotenv

from django.http import JsonResponse
from django.db import connection, OperationalError

from api.prediction_analysis import price_prediction_analysis
from api.sentiment_analysis import sentiment_and_prediction_analysis, news_analyze
from api.models import CryptoSymbols

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import CustomUser

from pycoingecko import CoinGeckoAPI

load_dotenv()


# Create your views here.

matplotlib.use('Agg')

# Authentications

cg = CoinGeckoAPI()


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
                "PriceChangePercentage": data["market_data"].get("price_change_percentage_24h"),
                "MarketCap": data["market_data"]["market_cap"]["usd"],
                "MarketCapChangePercentage": data["market_data"].get("market_cap_change_percentage_24h"),
                "Volume24h": data["market_data"]["total_volume"]["usd"],
                "FDV": data["market_data"].get("fully_diluted_valuation", {}).get("usd"),
                "TotalSupply": data["market_data"].get("total_supply"),
                "MaxSupply": data["market_data"].get("max_supply"),
                "CirculatingSupply": data["market_data"].get("circulating_supply"),
                "Rank": data.get("market_cap_rank"),
                "ATH": data["market_data"]["ath"]["usd"],
                "ATHChangePercentage": data["market_data"]["ath_change_percentage"]["usd"],
                "ATHDate": data["market_data"]["ath_date"]["usd"],
                "ATL": data["market_data"]["atl"]["usd"],
                "ATLChangePercentage": data["market_data"]["atl_change_percentage"]["usd"],
                "ATLDate": data["market_data"]["atl_date"]["usd"],
                "Homepage": data["links"]["homepage"][0] if data["links"]["homepage"] else None,
                "Explorer": data["links"]["blockchain_site"][0] if data["links"]["blockchain_site"] else None,
                "Description": data["description"].get("en", ""),
            }


            cache.set(cache_key, coin_data, timeout=7200)
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

            period_mapping = {"week": 7, "month": 30,}
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


# image
def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    buf.close()
    return f"data:image/png;base64,{data}"


# Crypto Prediction
class fetchCryptoPrediction(APIView):
    def post(self, request):
        try:
            symbol = request.data.get("coin")  # Contoh: 'BTCUSDT'
            no_of_days = int(request.data.get("no_of_days", 2))

            if not symbol:
                return Response({"error": "Missing coin parameter."}, status=400)

            cache_key = f"{symbol}_{no_of_days}_prediction"
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data, status=200)

            # Get Binance Kline data (daily candles)
            end_time = int(datetime.now().timestamp() * 1000)
            start_time = int((datetime.now() - timedelta(days=365 * 10)).timestamp() * 1000)

            all_data = []
            while start_time < end_time:
                url = "https://api.binance.com/api/v3/klines"
                params = {
                    "symbol": symbol.upper(),
                    "interval": "1d",
                    "startTime": start_time,
                    "limit": 1000
                }
                response = requests.get(url, params=params)
                data = response.json()

                if isinstance(data, dict) and data.get("code"):
                    return Response({"error": data.get("msg", "Failed to fetch Binance data.")}, status=400)

                if not data:
                    break

                all_data.extend(data)
                last_time = data[-1][0]
                start_time = last_time + 24 * 60 * 60 * 1000  # Next day

            # Parse data
            df = pd.DataFrame(all_data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'num_trades',
                'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
            ])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df['Close'] = df['close'].astype(float)

            if df.empty:
                return Response({"error": "No historical data found for this coin."}, status=400)

            coin_data = df[['Close']]
            splitting_len = int(len(coin_data) * 0.8)
            x_test = coin_data[["Close"]][splitting_len:]

            if x_test.empty:
                return Response({"error": "Not enough data to make a prediction."}, status=400)

            # Scale data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(x_test)

            base_days = 100
            x_data, y_data = [], []
            for i in range(base_days, len(scaled_data)):
                x_data.append(scaled_data[i-base_days: i])
                y_data.append(scaled_data[i])

            if not x_data or not y_data:
                return Response({"error": "Not enough data after scaling to make prediction."}, status=400)

            x_data = np.array(x_data)
            y_data = np.array(y_data)

            # Predictions
            predictions = model.predict(x_data)
            inv_predictions = scaler.inverse_transform(predictions)
            inv_y_test = scaler.inverse_transform(y_data)

            plotting_data = pd.DataFrame({
                'Original Test Data': inv_y_test.flatten(),
                'Predicted Test Data': inv_predictions.flatten()
            }, index=x_test.index[base_days:])

            # Plot 1
            fig1 = plt.figure(figsize=(15, 6))
            plt.plot(coin_data['Close'], label='Close Price')
            plt.title(f'{symbol.upper()} Closing Price Over Time')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.legend()
            original_plot = plot_to_base64(fig1)
            plt.close(fig1)

            # Plot 2
            fig2 = plt.figure(figsize=(15, 6))
            plt.plot(plotting_data['Original Test Data'], label='Original Test Data', color='blue')
            plt.plot(plotting_data['Predicted Test Data'], label='Predicted Test Data', color='red')
            plt.legend()
            plt.title('Original vs Predicted')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            predicted_plot = plot_to_base64(fig2)
            plt.close(fig2)

            # Predict future prices
            last_100 = coin_data.tail(100)
            last_100_scaled = scaler.transform(last_100)
            last_100_scaled = last_100_scaled.reshape(1, -1, 1)

            future_predictions = []
            for _ in range(no_of_days):
                next_day = model.predict(last_100_scaled)
                future_predictions.append(scaler.inverse_transform(next_day))
                last_100_scaled = np.append(last_100_scaled[:, 1:, :], next_day.reshape(1, 1, -1), axis=1)

            future_predictions = np.array(future_predictions).flatten()

            # Analysis
            price_analysis_data = price_prediction_analysis(symbol, future_predictions)
            sentiment_label, recommendation, final_score, summarize = sentiment_and_prediction_analysis(
                symbol, future_predictions)

            result = {
                "original_plot": original_plot,
                "predicted_plot": predicted_plot,
                "future_plot": future_predictions.tolist(),
                "predict_price_analysis": price_analysis_data,
                "sentiment_label": sentiment_label,
                "recommendation": recommendation,
                "final_score": final_score,
                "summarize": summarize,
            }

            # Cache result
            cache.set(cache_key, result, timeout=3600)
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


# Trending Coins
class TrendingCoinView(APIView):
    def get(self, request):
        cached_data = cache.get('trending_coins')
        if cached_data:
            return Response(cached_data)

        # Ambil trending coins
        trending_url = 'https://api.coingecko.com/api/v3/search/trending'
        trending_data = requests.get(trending_url).json()

        coins = trending_data.get('coins', [])[:10]
        
        simplified = []
        for coin in coins:
            price_btc = coin['item']['price_btc']

            simplified.append({
                'name': coin['item']['name'],
                'symbol': coin['item']['symbol'],
                'market_cap_rank': coin['item']['market_cap_rank'],
                'price_btc': price_btc,
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

# User Feedback
class UserFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'message': 'Feedback berhasil disimpan.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# crypto news
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
            page_size=100
        )

        articles = all_articles.get('articles', [])

        def process_article(article):
            title = article.get('title') or ''
            description = article.get('description') or ''
            full_text = f"{title}. {description}".strip()

            if not full_text:
                return None

            # analysis = news_analyze(full_text)
            return {
                'title': title,
                'image': article.get('urlToImage'),
                'link': article.get('url'),
                'date': article.get('publishedAt'),
                # 'sentiment': analysis.get('sentiment'),
                # 'summary': analysis.get('summary')
            }

        # 🔁 Run sentiment analysis in parallel
        with ThreadPoolExecutor() as executor:
            news_data = list(filter(None, executor.map(process_article, articles)))

        cache.set('crypto_news_list', news_data, 3600)
        return Response(news_data)


# Crypto Insight
class CryptoInsightNewsListView(APIView):
    def get(self, request):
        cached_data = cache.get('crypto_insight_news')
        if cached_data:
            return Response(cached_data)

        api_key = os.getenv('CRYPTOCOMPARE_API_KEY')
        categories = 'BTC,ETH,USDT,BNB,SOL,XRP,DOGE,TON,ADA,AVAX'
        url = f'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={categories}&api_key={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return Response({"error": "Failed to fetch data from CryptoCompare", "details": str(e)}, status=500)

        articles = data.get('Data', [])

        def process_article(article):
            title = article.get('title') or ''
            if not title:
                return None

            return {
                'title': title,
                'link': article.get('url'),
                'date': datetime.utcfromtimestamp(article.get('published_on')).isoformat(),
                'source': article.get('source'),
                'tags': article.get('tags', ''),
                'image': f"{article.get('imageurl')}" if article.get('imageurl') else None
            }

        with ThreadPoolExecutor() as executor:
            insight_data = list(filter(None, executor.map(process_article, articles)))

        cache.set('crypto_insight_news', insight_data, 3600)
        return Response(insight_data)


# Crypto Press Release
class CryptoPressReleaseListView(APIView):
    def get(self, request):
        cached_data = cache.get('crypto_press_release')
        if cached_data:
            return Response(cached_data)

        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        press_articles = newsapi.get_everything(
            q='cryptocurrency press release OR crypto announcement',
            language='en',
            sort_by='publishedAt',
            page_size=5
        )

        articles = press_articles.get('articles', [])

        def process_article(article):
            title = article.get('title') or ''
            description = article.get('description') or ''
            full_text = f"{title}. {description}".strip()

            if not full_text:
                return None

            # analysis = news_analyze(full_text)
            return {
                'title': title,
                'image': article.get('urlToImage'),
                'link': article.get('url'),
                'date': article.get('publishedAt'),
                # 'sentiment': analysis.get('sentiment'),
                # 'summary': analysis.get('summary')
            }

        with ThreadPoolExecutor() as executor:
            press_data = list(filter(None, executor.map(process_article, articles)))

        cache.set('crypto_press_release', press_data, 3600)
        return Response(press_data)


# Crypto Regulation News
class CryptoRegulationNewsView(APIView):
    def get(self, request):
        cached_data = cache.get('crypto_regulation_news')
        if cached_data:
            return Response(cached_data)

        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        try:
            regulation_articles = newsapi.get_everything(
                q='cryptocurrency regulation OR crypto law OR crypto policy OR crypto ban',
                language='en',
                sort_by='publishedAt',
                page_size=8
            )
        except Exception as e:
            return Response({"error": "Failed to fetch regulation news", "details": str(e)}, status=500)

        articles = regulation_articles.get('articles', [])

        def process_article(article):
            title = article.get('title') or ''
            description = article.get('description') or ''
            full_text = f"{title}. {description}".strip()
            if not full_text:
                return None

            return {
                'title': title,
                'image': article.get('urlToImage'),
                'link': article.get('url'),
                'date': article.get('publishedAt')
            }

        with ThreadPoolExecutor() as executor:
            regulation_news = list(filter(None, executor.map(process_article, articles)))

        cache.set('crypto_regulation_news', regulation_news, 3600)
        return Response(regulation_news)