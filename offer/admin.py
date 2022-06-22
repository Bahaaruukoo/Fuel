from django.contrib import admin

# Register your models here.
from .models import gas_offer, Gasstation, dailyUsage, log_table

admin.site.register(gas_offer)
admin.site.register(Gasstation)
admin.site.register(dailyUsage)
admin.site.register(log_table)
