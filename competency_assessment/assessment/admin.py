from django.contrib import admin
from .models import User, Assessment_period, Assessment,Assessment_results, Idp, Strand, Competency, Rating


admin.site.register(User)
admin.site.register(Assessment_period)
admin.site.register(Assessment)
admin.site.register(Competency)
admin.site.register(Strand)
admin.site.register(Rating)
admin.site.register(Assessment_results)
admin.site.register(Idp)
admin.site.site_header = "HR Dashboard"
