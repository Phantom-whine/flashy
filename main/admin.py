from django.contrib import admin
from .models import Post, Likes, Comments

@admin.register(Post)
class PostAdmin(admin.ModelAdmin) :
    list_display = ['profile', 'content']

@admin.register(Likes)
class PostAdmin(admin.ModelAdmin) :
    list_display = ['profile', 'post']

@admin.register(Comments)
class PostAdmin(admin.ModelAdmin) :
    list_display = ['profile', 'post']


