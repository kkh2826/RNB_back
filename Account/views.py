import json
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import AllowAny, IsAuthenticated 
from django.http import HttpResponse

from .serializers import UserSerializer, LoginUserAccountSerializer
from rest_framework.views import APIView

from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER



@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def index(request): 
    return HttpResponse('hello')



'''
    CASE 1 :
    UserSerializer로 직렬화
'''
class LoginUserAccount(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request):  

        result = {
            'user': None,
            'token': '',
            'success': True,
            'message': ''
        }
        token = ''

        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            result['success'] = False
            result['message'] = '존재하지 않은 회원입니다.'
        else:
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                token = JWT_ENCODE_HANDLER(payload)
            except:
                result['message'] = '토큰의 정보를 가져오지 못했습니다.'
                result['success'] = False


        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid()

        result['user'] = serializer.data
        result['token'] = token

        return Response(result, content_type='application/json')


'''
    CASE 2:
    유효성 검증 처리 후, 직렬화를 통해 데이터 반환
    유효성 검증 에러 시, 400 에러 반환
'''
class LoginUserAccount(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginUserAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = ''
        token = ''

        username = serializer.data['username']
        password = serializer.data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            message = 'ID와 비밀번호를 확인해주세요.'
            success = False
        else:
            userSerializer = UserSerializer(user, data=serializer.data)
            userSerializer.is_valid()
            success = True

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
        except:
            message = '토큰의 정보를 가져오지 못했습니다.'

        response = {
            'user': userSerializer.data,
            'token': token,
            'success': success,
            'message': message
        }

        return HttpResponse(json.dumps(response), content_type='application/json')

