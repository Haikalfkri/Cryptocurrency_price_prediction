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
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime

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
            # Get coin name from request body
            coin = request.data.get("coin")
            if not coin:
                return Response({"error": "Coin parameter is required"}, status=400)
            
            # check cache before making an API request
            cache_key = f"crypto_{coin}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data, status=200)

            # fetch data from coingecko api
            url = f"https://api.coingecko.com/api/v3/coins/{coin}"
            response = requests.get(url)

            if response.status_code != 200:
                return Response({"error": "Failed to fetch data from API"}, status=response.status_code)
            
            data = response.json()

            # extract data
            coin_data = {
                "Price": data["market_data"]["current_price"]["usd"],
                "MarketCap": data["market_data"]["market_cap"]["usd"],
                "24hVolume": data["market_data"]["total_volume"]["usd"],
                "FDV": data["market_data"]["fully_diluted_valuation"]["usd"],
                "TotalSupply": data["market_data"]["total_supply"],
                "MaxSupply": data["market_data"]["max_supply"],
                "CirculatingSupply": data["market_data"]["circulating_supply"],
                "MarketCapChangePercentage": data["market_data"]["market_cap_change_percentage_24h"],
                "Description": data["description"]["en"],
            }

            # cache data for 10 minutes
            cache.set(cache_key, coin_data, timeout=600)

            return Response(coin_data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)