from django.db import models
from django.contrib.auth.models import AbstractUser, User as AuthUser
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone

# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=60)
    job_grade = models.IntegerField()

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    level = models.ForeignKey('Level', blank=True, null=True, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.email