from Account.serializers import JWT_ENCODE_HANDLER, JWT_PAYLOAD_HANDLER
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer

# Create your views here.

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


'''
    CASE 1
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
            result['message'] = '존재하지 않는 회원입니다.'
        else:
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                token = JWT_ENCODE_HANDLER(payload)
            except:
                result['success'] = False
                result['message'] = '토큰의 정보를 가져오지 못했습니다.'

        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid()

        result['user'] = serializer.data
        result['token'] = token

        return Response(result, content_type='application/json')