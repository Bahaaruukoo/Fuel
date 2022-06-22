from asyncio.windows_events import NULL
from operator import mod
from pyexpat import model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Gasstation(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    identifier = models.CharField(max_length=120)

    def __str__(self):
        return self.identifier

class gas_offer(models.Model):
    file_number = models.CharField(max_length=20, blank=True)
    plate_number = models.CharField(max_length=10, blank=True)
    date = models.DateField(default=timezone.now)
    permited_amount = models.IntegerField()
    qr_code = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, default=None)
    
    def __str__(self):
        return self.plate_number + self.qr_code

class dailyUsage(models.Model):
    vehicle = models.ForeignKey(gas_offer, on_delete=models.DO_NOTHING)
    used_amount = models.IntegerField()
    left_amount = models.IntegerField()
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.used_amount )

class log_table(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    vehicle = models.ForeignKey(gas_offer, on_delete=models.DO_NOTHING)
    gasstation = models.ForeignKey(Gasstation,null=True, on_delete=models.SET_NULL)
    date = models.DateField(default=timezone.now)
    filled_amount = models.IntegerField()
    over_draw = models.IntegerField(null=True, default=0)

    def __str__(self):
        return str(self.gasstation) +"  " + str(self.filled_amount) + " litters"