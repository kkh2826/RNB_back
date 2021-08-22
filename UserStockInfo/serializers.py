from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserStockInfo


class UserStockInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserStockInfo
        fields = ['id', 'stockCode', 'stateType', 'buyDate', 'buyAmount', 'buyPrice']