from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Profile(AbstractUser):
    """ Custom User Model """
    correo = models.EmailField()
    contraseña = models.CharField(max_length=16, blank=False, null=True)
    # avatar = models.ImageField(blank=True)