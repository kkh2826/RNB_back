from django.contrib.auth.models import User
from Account.serializers import JWT_ENCODE_HANDLER, JWT_PAYLOAD_HANDLER
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserSerializer

# Create your views here.

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

result = {
            'user': None,
            'token': '',
            'success': True,
            'message': ''
        }


'''
    회원가입
'''
class RegisterUserAccount(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        # 기본 제약사항 체크
        if len(username) < 4:
            result['message'] = 'ID는 4자리 이상입니다.'
            result['success'] = False
        if len(password) < 8:
            result['message'] = '비밀번호는 8자리 이상입니다.'
            result['success'] = False
        if '@' not in email or email.count('@') > 1:
            result['message'] = 'Email 형식이 아닙니다.'
            result['success'] = False

        if not result['success']:
            return Response(result, content_type='application/json')

        # 기본 제약사항 통과
        user = authenticate(username=username, password=password)

        # 회원 정보 체크
        if user is not None:
            result['success'] = False
            result['message'] = '해당 ID는 이미 존재합니다.'


        if User.objects.filter(email=email).count() > 0:
            result['success'] = False
            result['message'] = '해당 Email로 가입된 정보가 존재합니다.'

        if not result['success']:
            return Response(result, content_type='application/json')

        user = User.objects.create_user(username, email, password)
        user = UserSerializer(user)

        result['user'] = user.data

        return Response(result, content_type='application/json')


'''
    로그인
'''
class LoginUserAccount(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

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

'''
    Token 유효기간 테스트 클래스
'''
class TokenVerifyUserToken(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        
        user = User.objects.get(username=request.user.username)        
        serializer = UserSerializer(user)

        return Response(serializer.data, content_type='application/json')