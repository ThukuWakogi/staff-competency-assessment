from django.contrib import admin
from .models import User, Assessment_period, Assessment


admin.site.register(User)
admin.site.register(Assessment_period)
admin.site.register(Assessment)
admin.site.site_header = "HR Dashboard"
