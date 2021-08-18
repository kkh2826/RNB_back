from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


'''
    CASE 1 :
    User 직렬화를 위한 선언
'''
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

'''
    CASE 2 :
    유효성 검증만 처리 후, 인자값에 대한 결과값 반환.
'''
class LoginUserAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        if username == "":
            raise serializers.ValidationError(
                '사용자 ID를 입력해 주세요.'
            )

        if len(password) < 8:
            raise serializers.ValidationError(
                '비밀번호는 최소 8자리 입니다.'
            )

        return attrs


