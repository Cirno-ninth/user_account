from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('confirm/', views.user_confirm),
    path('email_login/', views.email_login),
    path('forgot_password/', views.forgot_password),
    path('set_password/', views.set_password),
]
