from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class OTP(models.Model):
    email=models.EmailField()
    otp=models.IntegerField()