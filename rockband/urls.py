from django.urls import path, include, re_path
from django.shortcuts import render
from . import views

app_name = 'rockband'
urlpatterns = [
    path('', views.user_login, name='login'),
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    path('show_user/', views.show_user, name='show_user'),
    path('register/', views.register, name="register"),
    path('register_user/', views.register_user, name= 'register_user'),
    path('index/', views.index, name='index'),
    path('<int:question_id>/detail', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('blog/', views.blog.as_view(), name = 'blog'),      
    path('<int:pk>/', views.Postdetail.as_view(), name = 'post'),
]