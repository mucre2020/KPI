from django.contrib import admin
from .models import Division, Unit, KPI, UserProfile

admin.site.register(Division)
admin.site.register(Unit)
admin.site.register(KPI)
admin.site.register(UserProfile)