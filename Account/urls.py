from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from .views import *

urlpatterns = [
    path("rest-auth/", include('rest_auth.urls')),

    # 로그인방법 2가지
    path("rest-auth/registration/", include('rest_auth.registration.urls')),
    path('login/', obtain_jwt_token),
    path('', index),

    path('mylogin/', LoginUserAccount.as_view())
]