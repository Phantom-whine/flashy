from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile/', null=True, default='profile/gradient.jfif')
    joined = models.DateField(default=timezone.now)
    email = models.CharField(max_length=50)

    def __str__(self) :
        return str(self.user.email)