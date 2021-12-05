from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserStockInfo


class UserStockInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStockInfo
        fields = ['id', 'stockCode', 'buysellFlag', 'buyDate', 'buyAmount', 'buyPrice']

    def create(self, validated_data):

        if UserStockInfo.objects.filter(user=validated_data['user'], stockCode=validated_data['stockCode']).count() > 0:
            answer = UserStockInfo.objects.filter(user=validated_data['user'], stockCode=validated_data['stockCode']).update(**validated_data)
        else:
            answer = UserStockInfo.objects.create(**validated_data)

        return answer
