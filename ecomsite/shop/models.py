from django.db import models
from django.contrib.auth.models import User
from utils.model_abstracts import TotalQuantity


class Products(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    Category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=200)
    stock = models.IntegerField(default=10)
    def check_stock(self, qty):
        # used to check if order quantity exceeds stock levels
        if int(qty) > self.stock:
            return False
        return True
    def __str__(self):
        return self.title

class Cart( TotalQuantity):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cart_products:
          
          self.total = sum(item.total for item in self.cart_products.all())
          self.quantity = sum(item.quantity for item in self.cart_products.all())
          print('quantity:',self.quantity,"       total:",self.total)
          print(self.total) 
        super().save(*args, **kwargs)

class CartProduct( TotalQuantity):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product_id = models.IntegerField()
    product_title = models.CharField(max_length=200)
    product_price = models.FloatField()

    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        self.total = self.product_price * self.quantity
        self.cart.save()
        super().save(*args, **kwargs)

class UserOrder( TotalQuantity):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total = sum(item.total for item in self.order_products.all())
        self.quantity = sum(item.quantity for item in self.order_products.all())
        print(self.total)

class OrderProduct( TotalQuantity):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE, related_name='order_products')
    product_id = models.IntegerField()
    product_title = models.CharField(max_length=200)
    product_price = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total = self.product_price * self.quantity
        self.order.save()
