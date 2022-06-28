from django.contrib import admin

# Register your models here.
from .models import * #Gas_offer, Gasstation, DailyUsage, log_table, Audited, Compensation

admin.site.register(Gas_offer)
admin.site.register(Gasstation)
admin.site.register(DailyUsage)
admin.site.register(log_table)
admin.site.register(Audited)
admin.site.register(Fuel)
