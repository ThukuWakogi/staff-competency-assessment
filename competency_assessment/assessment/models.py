from django.db import models
from django.contrib.auth.models import AbstractUser, User as AuthUser

# Create your models here.

class User(AbstractUser):
    pass


class Competency(models.Model):
    name = models.CharField(max_length=250)

class Strand(models.Model):
    name = models.CharField(max_length=250)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
 

class Assessment_period(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    initiating_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Rating(models.Model):
    name =models.CharField(max_length=250)   
    rating = models.IntegerField()

class Assessment(models.Model):
    user_id = models
    assessment_period = models.ForeignKey(Assessment_period, on_delete= models.CASCADE)
    is_assessed_by_manager = models.BooleanField(default=False)
    is_assessed_after_norming = models.BooleanField(default=False)

class Assessment_results(models.Model):
    assessment =models.ForeignKey(Assessment, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    strand =models.ForeignKey(Strand, on_delete=models.CASCADE)
    rating =models.ForeignKey(Rating, on_delete=models.CASCADE)

class Idp(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    actions = models.TextField()
    resources = models.TextField()
    target = models.CharField(max_length=250)
    progress_indicator= models.CharField(max_length=500)
    nature_of_support = models.TextField()


class Notifications(models.Model):
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)  
    action = models.CharField(max_length=250)
    is_seen = models.CharField(max_length=200)


class Direct_manager(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direct_manager')


