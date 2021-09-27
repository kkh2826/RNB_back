from django.urls import path, include

urlpatterns = [
    path('stockinfo/', include('StockInfo.urls')),
    path('account/', include('Account.urls')),
]