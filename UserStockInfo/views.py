from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import UserStockInfo

from .serializers import UserStockInfoSerializer

# Create your views here.
class UserStockInfoByUser(APIView):
    '''
        사용자의 주식정보를 가져온다.
    '''

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        userStockInfo = UserStockInfo.objects.filter(user__username=request.user.username)
        serializer = UserStockInfoSerializer(userStockInfo, many=True)
        return Response(serializer.data, content_type='application/json')