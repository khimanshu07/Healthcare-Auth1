from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('edit/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),
    path('delete/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('my-posts/', views.my_blog_posts, name='my_blog_posts'),
    path('view/<int:post_id>/', views.view_blog_post, name='view_blog_post'),
    path('list/', views.blog_list, name='blog_list'),
    path('categories/', views.category_list, name='category_list'),
]