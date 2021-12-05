from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import UserStockInfo

from .serializers import UserStockInfoSerializer

import json


'''
    결과값 초기화 함수
'''
def InitResult() :
    result = {
        'success': True,
        'message': ''
    }

    return result

# Create your views here.
class UserStockInfoByUser(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    '''
        사용자의 주식정보를 가져온다.
    '''

    def get(self, request):
        userStockInfo = UserStockInfo.objects.filter(user__username=request.user.username)
        serializer = UserStockInfoSerializer(userStockInfo, many=True)
        return Response(serializer.data, content_type='application/json')

    '''
        사용자의 주식정보를 저장한다.
    '''

    def post(self, request):

        result = InitResult()

        userStockInfo = json.loads(request.body)
        user = User.objects.get(username=request.user.username)

        for userStock in userStockInfo["UserStockInfo"]:
            try:
                userStockSerializer = UserStockInfoSerializer(data=userStock)
                userStockSerializer.is_valid()
                userStockSerializer.save(user=user)
            except:
                result['success'] = False
                result['message'] = "저장실패"
                return Response(result, content_type='application/json')

        result['success'] = True
        result['message'] = "저장성공"
        
        return Response(result, content_type='application/json')


    def delete(self, request):

        result = InitResult()

        userStockInfo = json.loads(request.body)

        userStockInfo = userStockInfo["UserStockInfo"]
        user = User.objects.get(username=request.user.username)

        try:
            UserStockInfo.objects.filter(user=user, stockCode=userStockInfo["stockCode"]).delete()
        except:
            result['success'] = False
            result['messsage'] = "삭제실패"
            return Response(result, content_type='application/json')

        result['success'] = True
        result['message'] = '삭제성공'

        return Response(result, content_type='application/json')