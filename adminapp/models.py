from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# User model
class customUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
        