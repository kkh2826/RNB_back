from django.urls import path, include

urlpatterns = [
    path('stockinfo/', include('StockInfo.urls')),
]