from django.contrib import admin
from .models import User, Assessment_period


admin.site.register(User)
admin.site.register(Assessment_period)
admin.site.site_header = "HR Dashboard"
