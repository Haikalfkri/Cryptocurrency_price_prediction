from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.cache import cache

from .serializers import LoginSerializer, RegisterSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

import requests
import pandas as pd
import numpy as np
import yfinance as yf
# Create your views here.

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
            response = Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
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


