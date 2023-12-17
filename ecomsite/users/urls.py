from django.urls import path,include
from .views import register,CustomLoginView
from django.contrib.auth.views import LoginView,LogoutView


app_name = 'users'
urlpatterns = [
  path('register/',register,name='register'),
  path('loginpage/',LoginView.as_view(template_name="users/login.html"),name='login'),
  path('logincheck/',CustomLoginView.as_view(),name='logincheck'),
  path('logout/',LogoutView.as_view(template_name='users/logout.html'),name='logout'),
  
  ]