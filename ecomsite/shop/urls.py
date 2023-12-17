from django.urls import path,include
from .views import CartView
app_name = 'users'

urlpatterns = [
  path('getcart/',CartView.as_view(),name='getcart')
]