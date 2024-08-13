from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('like/', views.like_view, name='like'),
    path('post/', views.post, name='post'),
    path('edit-post/<int:id>', views.edit, name='edit-post'),
    path('edit/<int:id>', views.edit_post, name='edit'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('comments/<int:id>', views.retrieve_comment, name='comments'),
    path('post/comment/', views.post_comment, name='post_comment'),
    path('delete/<int:id>', views.delete_post, name='delete'),
]