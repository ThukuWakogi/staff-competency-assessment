from django.db import models
from django.contrib.auth.models import AbstractUser, User as AuthUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=60)
    job_grade = models.IntegerField()


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    level = models.ForeignKey('Level', blank=True, null=True, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email


class Competency(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Strand(models.Model):
    name = models.CharField(max_length=250)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AssessmentPeriod(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    initiating_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Rating(models.Model):
    name = models.CharField(max_length=250)
    rating = models.IntegerField()

    def __str__(self):
        return self.name


class Assessment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment_period = models.ForeignKey(AssessmentPeriod, on_delete=models.CASCADE)
    is_assessed_by_manager = models.BooleanField(default=False)
    is_assessed_after_norming = models.BooleanField(default=False)


class AssessmentResults(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    comments = models.TextField(blank=True)


class Idp(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    actions = models.TextField()
    resources = models.TextField()
    target = models.CharField(max_length=250)
    progress_indicator = models.CharField(max_length=500)
    nature_of_support = models.TextField()


class Notification(models.Model):
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    action = models.CharField(max_length=250)
    is_seen = models.CharField(max_length=200)

    def __str__(self):
        return self.action


class DirectManager(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direct_manager')
