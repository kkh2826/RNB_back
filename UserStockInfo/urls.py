from django.urls import path, include

from .views import *

urlpatterns = [
    path('', UserStockInfoByUser.as_view()),
]