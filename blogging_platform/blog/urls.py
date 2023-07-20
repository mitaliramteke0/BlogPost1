from django.urls import path
from . import views

urlpatterns = [
    path('blog_list/', views.blog_list, name='blog_list'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),  # Blog detail view with primary key (pk)
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),



]
