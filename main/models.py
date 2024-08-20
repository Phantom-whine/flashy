from django.db import models
from account.models import Profile
from django.utils import timezone

class NotHidden(models.Manager) :
    def get_queryset(self, *args, **kwargs) :
        pass


class Post(models.Model) :
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, default=None)
    created_at = models.DateField(default=timezone.now)
    hidden = models.BooleanField(default=False)

    class Meta :
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]

class Likes(models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_p')

    class Meta :
        indexes = [
            models.Index(fields=['post', 'profile'])
        ]
    
class Comments(models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(null=True)

    class Meta :
        indexes = [
            models.Index(fields=['post', 'profile'])
        ]