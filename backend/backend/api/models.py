from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# Role
class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Custom User manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        # set default role to user
        if role is None:
            role, _ = Role.objects.get_or_create(name='user')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        admin_role, _ = Role.objects.get_or_create(name='admin')

        user = self.create_user(username, email, password, role=admin_role)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# custom user
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

# crypto symbol from binance
class CryptoSymbols(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# user feedback
class UserFeedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    feedback = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    

# crypto news
class CryptoNews(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    sentiment = models.CharField(max_length=512)
    image = models.URLField(blank=True, null=True, max_length=1024)
    link = models.URLField(unique=True, max_length=1024)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title
    

# crypto insight news
class CryptoInsight(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=512)
    date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255)
    image = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=50, default='GENERAL')  # Nama coin seperti BTC, ETH, dll

    def __str__(self):
        return f"{self.category} - {self.title[:100]}"
    

class BaseCoinModel(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    close_time = models.BigIntegerField()
    quote_asset_volume = models.FloatField()
    num_trades = models.IntegerField()
    taker_buy_base_vol = models.FloatField()
    taker_buy_quote_vol = models.FloatField()

    class Meta:
        abstract = True


class BTCUSDT(BaseCoinModel): pass
class ETHUSDT(BaseCoinModel): pass
class BNBUSDT(BaseCoinModel): pass
class SOLUSDT(BaseCoinModel): pass
class XRPUSDT(BaseCoinModel): pass
class TONUSDT(BaseCoinModel): pass
class ADAUSDT(BaseCoinModel): pass
class DOGEUSDT(BaseCoinModel): pass
class AVAXUSDT(BaseCoinModel): pass
class LINKUSDT(BaseCoinModel): pass
class DOTUSDT(BaseCoinModel): pass
class MATICUSDT(BaseCoinModel): pass
class ICPUSDT(BaseCoinModel): pass
class LTCUSDT(BaseCoinModel): pass
class SHIBUSDT(BaseCoinModel): pass
class BCHUSDT(BaseCoinModel): pass
class UNIUSDT(BaseCoinModel): pass
class APTUSDT(BaseCoinModel): pass
class NEARUSDT(BaseCoinModel): pass
class XLMUSDT(BaseCoinModel): pass


class BaseCoinDetail(models.Model):
    time = models.DateTimeField(unique=True)
    open_price = models.FloatField(null=True)
    high_price = models.FloatField(null=True)
    low_price = models.FloatField(null=True)
    close_price = models.FloatField(null=True)
    volume_from = models.FloatField(null=True)
    volume_to = models.FloatField(null=True)
    market_cap = models.FloatField(null=True)
    supply = models.FloatField(null=True)
    max_supply = models.FloatField(null=True)
    circulating_supply = models.FloatField(null=True)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    percent_change_24h = models.FloatField(null=True, blank=True)
    percent_change_7d = models.FloatField(null=True, blank=True)


    class Meta:
        abstract = True

class BTCUSDTDetail(BaseCoinDetail): pass
class ETHUSDTDetail(BaseCoinDetail): pass
class BNBUSDTDetail(BaseCoinDetail): pass
class SOLUSDTDetail(BaseCoinDetail): pass
class XRPUSDTDetail(BaseCoinDetail): pass
class TONUSDTDetail(BaseCoinDetail): pass
class ADAUSDTDetail(BaseCoinDetail): pass
class DOGEUSDTDetail(BaseCoinDetail): pass
class AVAXUSDTDetail(BaseCoinDetail): pass
class LINKUSDTDetail(BaseCoinDetail): pass
class DOTUSDTDetail(BaseCoinDetail): pass
class MATICUSDTDetail(BaseCoinDetail): pass
class ICPUSDTDetail(BaseCoinDetail): pass
class LTCUSDTDetail(BaseCoinDetail): pass
class SHIBUSDTDetail(BaseCoinDetail): pass
class BCHUSDTDetail(BaseCoinDetail): pass
class UNIUSDTDetail(BaseCoinDetail): pass
class APTUSDTDetail(BaseCoinDetail): pass
class NEARUSDTDetail(BaseCoinDetail): pass
class XLMUSDTDetail(BaseCoinDetail): pass