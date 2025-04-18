import json
from datetime import timedelta, datetime
import base64
import io
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
from .serializers import LoginSerializer, RegisterSerializer
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.cache import cache

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


# Create your views here.

matplotlib.use('Agg')

# Authentications


class RegisterView(APIView):
    def post(self, request):
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
                refresh = RefreshToken.for_user(user)
                response = Response({
                    "access": str(refresh.access_token),
                    "role": user.role.name,
                    "username": user.username,
                    "email": user.email,
                })

                # store refresh token in HttpOnly cookie
                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                )

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
            # Get refresh token from HttpOnly cookie
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response({
                    "error": "Refresh token is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # blacklist the refresh token
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            # Create response and delete refresh_token cookie
            response = Response(
                {"message": "User logged out successfully"}, status=status.HTTP_200_OK)
            response.delete_cookie("refresh_token")
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

# fetch historical data for chart


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


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()


from datetime import datetime, timedelta
import json
from openai import OpenAI  # adjust this import based on your OpenAI library version

client = OpenAI()  # initialize your OpenAI client here

def price_prediction_analysis(coin, future_predictions):
    today = datetime.today()

    date_price_pairs = [
        {
            "date": (today + timedelta(days=i)).strftime('%Y-%m-%d'),
            "price": float(round(price, 2))
        }
        for i, price in enumerate(future_predictions)
    ]

    data_text = json.dumps(date_price_pairs, indent=2)

    prompt = f"""
    You are an expert financial analyst.

    Based on the following predicted prices for {coin}, provide an expert analysis for each day.
    For each prediction, give:
    - "date": the date of the prediction
    - "predicted_price": the predicted price (as given)
    - "trend": one of "Uptrend", "Downtrend", or "Sideways"
    - "action": one of "Buy", "Hold", or "Sell"
    - "reason": a short explanation why the model might be predicting this price based on recent trends, past data, or momentum (50-100 words)

     At the end, return a final item:
    {{
        "prediction_summary": "Summarize all predictions and give general advice."
    }}

    Use only the following predicted prices:
    {data_text}

    Return the result as a valid JSON array. Do not include markdown or explanation.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content

    try:
        prediction_analysis = json.loads(content)
    except json.JSONDecodeError:
        prediction_analysis = [{"error": "Failed to parse OpenAI response as JSON"}]

    return prediction_analysis


def sentiment_analysis(coin, no_of_days):
    today = datetime.today()

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
            }, index=x_test.index[100:])

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

            # fig3 = plt.figure(figsize=(15, 6))
            # plt.plot(range(1, no_of_days + 1), future_predictions,
            #          marker='o', color='red', label='Future Predictions')
            # plt.title('Future Close Price Predictions')
            # plt.xlabel('Days Ahead')
            # plt.ylabel('Predicted Close Price')
            # plt.grid(alpha=0.3)
            # plt.legend()
            # future_plot = plot_to_base64(fig3)
            # plt.close(fig3)

            result = {
                "original_plot": original_plot,
                "predicted_plot": predicted_plot,
                "future_plot": future_predictions,
            }

            # sentiment analysis
            sentiment_data = price_prediction_analysis(coin, future_predictions)
            result["predict_price_analysis"] = sentiment_data

            # cache the result
            cache.set(cache_key, result, timeout=60 * 60)

            return Response(result, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
