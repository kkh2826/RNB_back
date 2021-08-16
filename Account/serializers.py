from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class LoginUserAccountSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):

        message = ''
        success = True

        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)

        if user is None:
            message = 'ID와 비밀번호를 확인해주세요.'
            success = False

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                '로그인 오류입니다. 잠시 후에 시도해주세요'
            )


        return {
            'user': user,
            'token': jwt_token,
            'message': message,
            'success': success
        }
    