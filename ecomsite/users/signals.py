from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from shop.models import Cart

@receiver(post_save,sender=User)
def build_profile(sender,instance,created,**kwargs):
  if created:
    print('creating cart')
    Token.objects.create(user = instance)
    cart = Cart(user=instance)
    cart.save()

