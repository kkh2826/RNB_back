from django.urls import path, include
from .views import *

urlpatterns = [
    # Install한 모듈을 사용하기 위해 URL Route 표시
    path('rest-auth/', include('rest_auth.urls')),

    # 회원가입 (http://127.0.0.1:8000/api/account/회원가입URL/)
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('registration/', RegisterUserAccount.as_view()),

    # 로그인 (http://127.0.0.1:8000/api/account/로그인URL/)
    path('login/', LoginUserAccount.as_view()),

    # 테스크 URL(Token 유효기간)
    path('TokenVerify/', TokenVerifyUserToken.as_view()),
]