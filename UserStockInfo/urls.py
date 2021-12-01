from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import *


urlpatterns = [
    path('', UserStockInfoByUser.as_view()),
]