from collections import OrderedDict
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import CartProduct,Products,Cart

# used add extra own exception
class NotEnoughStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'There is not enough stock'
    default_code = 'invalid'

#used check the item exist exception
class ThisItemNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Item Not Found"
    default_code = 'Not Found'
    

class AddTOCartSerializers(serializers.ModelSerializer):
  class Meta:
    model = CartProduct
    fields = ('product_id','quantity')
  
  def validate(self, attrs):
    item_id = attrs.get('product_id')
    try:
      product = Products.objects.get(pk=item_id)
    except Products.DoesNotExist:
        raise ThisItemNotFoundException
    quantity = attrs.get("quantity")
    if not product.check_stock(quantity):
      raise NotEnoughStockException
    return attrs
  
class CartProduct(serializers.ModelSerializer):
  class Meta:
    model = CartProduct
    fields = '__all__'
class CartSerializer(serializers.ModelSerializer):
  cart_products = CartProduct(many=True, read_only=True)

  class Meta:
    model = Cart
    fields = ('total','quantity','cart_products')
