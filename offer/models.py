from datetime import date
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Fuel(models.Model):
    fuelType = (
            ('benzene', 'Benzene'),
            ('petrol', 'Petrol')
        )
  
    fuel_type = models.CharField(max_length=40, choices=fuelType)
    price = models.DecimalField(decimal_places=2, max_digits=30)
    date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.fuel_type 

class Gasstation(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    identifier = models.CharField(max_length=120)

    def __str__(self):
        return self.identifier

class Gas_offer(models.Model):
    file_number = models.CharField(max_length=20, blank=True)
    plate_number = models.CharField(max_length=10, blank=True)
    date = models.DateField(default=timezone.now)
    permited_amount = models.IntegerField()
    fuel = models.ForeignKey(Fuel, on_delete=models.DO_NOTHING)
    qr_code = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, default=None)
    
    def __str__(self):
        return self.plate_number + self.qr_code

class DailyUsage(models.Model):
    vehicle = models.ForeignKey(Gas_offer, on_delete=models.DO_NOTHING)
    used_amount = models.IntegerField()
    left_amount = models.IntegerField()
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.used_amount )


class Audited(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    gasstation = models.ForeignKey(Gasstation, on_delete=models.DO_NOTHING)
    compensated_benzen = models.IntegerField()
    money_for_benzene = models.DecimalField(max_digits=12, decimal_places=2)
    compensated_petrol = models.IntegerField(default=0)
    money_for_petrol = models.DecimalField(max_digits=12, decimal_places=2)
    total_compensated_fuel = models.IntegerField(default=0)
    total_money_compansated = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    audit_date_from = models.DateField(null=True, blank=True)
    audit_date_to = models.DateField(null=True, blank=True)

    compansating_agent = models.ForeignKey(User,null=True, blank=True, on_delete=models.DO_NOTHING, related_name='auditor') #Auditor
    compensated_date = models.DateField( null=True, blank=True)
    money_reciever = models.TextField(null=True, blank=True, max_length=250)

    def __str__(self):
        return self.gasstation.name + ": " + str(self.total_money_compansated) + " --on: " + str(self.date) + "     ("+str(self.audit_date_from) + " - " + str(self.audit_date_to) +")"

class Compensation(models.Model):
    financer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='financer',  null=True, blank=True) #Auditor
    date = models.DateField(default=timezone.now)
    total_money = models.DecimalField(max_digits=12, decimal_places=2, default = 0)
    audit = models.ForeignKey(Audited, on_delete=models.DO_NOTHING, null=True, blank=True)
    gasstation = models.ForeignKey(Gasstation, on_delete=models.DO_NOTHING, related_name='gasstation',  null=True, blank=True)
   
    def __str__(self):
        return " Birr: " + str(self.total_money) + " to::::=> " + self.gasstation.name  
    
class log_table(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL) #cashier
    vehicle = models.ForeignKey(Gas_offer, on_delete=models.DO_NOTHING, related_name='vehicle')
    gasstation = models.ForeignKey(Gasstation,null=True, on_delete=models.SET_NULL)
    date = models.DateField(default=timezone.now)
    filled_amount = models.IntegerField()
    over_draw = models.IntegerField(null=True, default=0)
    fuel = models.ForeignKey(Fuel, on_delete=models.DO_NOTHING, related_name='fuel')
    audited = models.ForeignKey(Audited, null=True, blank=True, on_delete=models.DO_NOTHING)
    compensated = models.ForeignKey(Compensation, null=True, blank=True, on_delete=models.DO_NOTHING)
    dailyBalanceDone = models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return str(self.gasstation) +"  " + str(self.filled_amount) + " litters"
