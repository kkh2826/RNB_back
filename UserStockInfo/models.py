from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

# Create your models here.
class UserStockInfo(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    stockCode = models.CharField(max_length=6)
    stateType = models.SmallIntegerField(default=0)
    buyDate = models.DateTimeField(auto_now_add=True)
    buyAmount = models.IntegerField()
    buyPrice = models.IntegerField()

    def __str__(self):
        return self.user.username + '-' + self.stockCode