from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class UserStockInfo(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    stockCode = models.CharField(max_length=6)
    buysellFlag = models.SmallIntegerField(default=0, null=True)
    buyDate = models.DateTimeField(auto_now_add=True, null=True)
    buyAmount = models.IntegerField(null=True)
    buyPrice = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username + '-' + self.stockCode