from django.contrib import admin
from django.urls import path
from . import views
app_name="student"
urlpatterns = [
    path('login/', views.login_user,name="login"),
    path('register/', views.register,name="register"),
    path('Forgot_Username/Password/', views.Forgot, name="Forgot"),
    path('create_profile/', views.createprofile, name="createprofile"),
    
]
