from rest_framework import serializers
from django.contrib.auth.models import User
class LoginSerializers(serializers.ModelSerializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True, style={'input_type': 'password'})
  class Meta:
      model = User
      fields = ['username', 'password']