from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path('<int:page>', views.main, name='root_paginate'),
    path('author/<str:author_fullname>/', views.author_detail, name='author_detail'),
    path('tag/<str:tag_name>', views.tag_detail, name='tag_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='quotes/login.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='user_logout'),
    path('add-quote/', views.add_quote, name='add_quote'),
    path('add-author/', views.add_author, name='add_author'),
]
