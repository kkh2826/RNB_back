from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserStockInfo

class UserStockInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStockInfo
        fields = ['id', 'stockCode', 'buysellFlag', 'buyDate', 'buyAmount', 'buyPrice']

    # def create(self, request, *args, **kwargs):
    #     is_many = isinstance(request.data, list)
        

    # def update(self, instance, validated_data):
    #     instance.stockCode = validated_data.get('stockCode', instance.stockCode)
    #     instance.buysellFlag = validated_data.get('buysellFlag', instance.buysellFlag)
    #     instance.buyDate = validated_data.get('buyDate', instance.buyDate)
    #     instance.buyAmount = validated_data.get('buyAmount', instance.buyAmount)
    #     instance.buyPrice = validated_data.get('buyPrice', instance.buyPrice)
    #     return instance