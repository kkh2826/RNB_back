import json
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import AllowAny, IsAuthenticated 
from django.http import HttpResponse

from .serializers import LoginUserAccountSerializer
from rest_framework.views import APIView
from rest_framework import generics

from django.contrib.auth.models import User
from django.core import serializers



@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def index(request): 
    return HttpResponse('hello')


class LoginUserAccount(generics.GenericAPIView):
    serializer_class = LoginUserAccountSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwrags):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        data = serializer.validated_data

        token = data.get('token')
        user = data.get('user')
        success = data.get('success')
        message = data.get('message')

        response = {
            'token': token,
            'success': success,
            'message': message,
            'user': {
                'pk': user.pk,
                'username': user.username,
                'email': user.email
            }
        }

        return HttpResponse(json.dumps(response), content_type='application/json')



# class LoginUserAccount(APIView):
    
#     permission_classes = [AllowAny]
#     serializer_class = LoginUserAccountSerializer

#     def post(self, request, *args, **kwargs):
        
#         serializer = LoginUserAccountSerializer(data=request.data)

#         if not serializer.is_valid(raise_exception=True):
#             return HttpResponse({"message": "Request Body Error."})

#         response = {
#             'success': True,
#             'context': serializer.data
#         }

#         print(response['context'])

#         return HttpResponse(response['context'])





