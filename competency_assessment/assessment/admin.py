from django.contrib import admin
from .models import User, AssessmentPeriod, Assessment, AssessmentResults, Idp, Strand, Competency, Rating, Notification


admin.site.register(User)
admin.site.register(AssessmentPeriod)
admin.site.register(Assessment)
admin.site.register(Competency)
admin.site.register(Strand)
admin.site.register(Rating)
admin.site.register(AssessmentResults)
admin.site.register(Notification)
admin.site.register(Idp)
admin.site.site_header = "HR Dashboard"
