from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializers
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status
# Create your views here.


def register(request):
  form = UserCreationForm(request.POST or None)
  if request.method == 'POST' and form.is_valid():
    form.save()
    username = form.cleaned_data.get('username')
    messages.success(request,f'Welcome {username} your account created')
    return redirect('users:login')
  return render(request,'users/register.html',{"form":form})
  
class CustomLoginView(ObtainAuthToken):
  serializer_class = LoginSerializers
  def post(self,request,*arrgs,**kwargs):
    serializer = self.serializer_class(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
      username = serializer.validated_data['username']
      password = serializer.validated_data['password']
      user = authenticate(request,username=username, password=password)

      if user:
        login(request, user)
        token,create = Token.objects.get_or_create(user = user)
        print('request suceesss')
        return Response({'token': token.key, 'user_id': user.id},status=status.HTTP_200_OK)
      else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


