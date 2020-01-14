from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone

# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=60)
    job_grade = models.IntegerField()


class UserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given name and password.
        """ 
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefautl('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a Superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


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
