from django.urls import path, include
from .views import *

urlpatterns = [
    #path('<str:market>/', StockBaseInfoByFinanceDataReader.as_view()),
    #path('<str:market>/', StockBaseInfoByCrawling.as_view()),
    path('<str:market>/', StockBaseInfoByPYKRX.as_view()),
    path('search/<str:stockName>/', StockBaseInfoByStockName.as_view()),
]