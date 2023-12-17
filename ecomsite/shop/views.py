from django.shortcuts import render,redirect
from rest_framework.response import Response

from .models import CartProduct, OrderProduct, UserOrder, Products
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import APIException
from .serializers import AddTOCartSerializers,CartSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from rest_framework import status
# Create your views here.

class ThisItemNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Item Not Found"
    default_code = 'Not Found'

# API request

class AddTOCartVIew(generics.CreateAPIView):
  queryset = CartProduct.objects.all()
  serializer_class = AddTOCartSerializers
  permission_classes = [IsAuthenticated]

  def create(self,request,*args,**kwargs):
    data = JSONParser().parse(request)
    product_id = data['product_id']
    quantity = data['quantity']
    item_data = { 'product_id': product_id, 'quantity': quantity}
    serializer = self.get_serializer(data=item_data)
    serializer.is_valid(raise_exception=True)
    try:
      cart = request.user.cart
    except Cart.DoesNotExist:
      cart = Cart.objects.create(user = request.user)
    is_product_already_exist = CartProduct.objects.filter(cart=cart,product_id=product_id).first()
    if is_product_already_exist:
      is_product_already_exist.quantity+=1
      is_product_already_exist.save()
      
    else:
      try:
        product = Products.objects.filter(pk=product_id).first()
      except Products.DoesNotExist:
        raise ThisItemNotFoundException
      CartProduct.objects.create(
        cart=cart,product_id=product_id,
        quantity=quantity,
        product_price = product.discount_price,
        product_title = product.title,
      ).save()


    return Response(serializer.data,status=status.HTTP_201_CREATED)

class CartView(generics.RetrieveAPIView):
  serializer_class = CartSerializer
  permission_classes = [IsAuthenticated,]
  def get_object(self):
    cart,created = Cart.objects.get_or_create(user = self.request.user)
    return cart




  
def Homeview(request):
  objects = Products.objects.all()

  item_name = request.GET.get('item_name')
  print(item_name,'________________')
  if item_name is not None:
    objects = Products.objects.filter(title__icontains=item_name)
  
  # paginator code
  paginator  = Paginator(objects,6)
  page = request.GET.get('page')
  objects = paginator.get_page(page)


  
  return render(request,'shop/home.html',{'product_objects':objects})
  


class ProductDetailView(DetailView):
  model = Products
  template_name = 'shop/detail.html'
  context_object_name = 'product_object'
  
def checkoutView(request):
  if request.method == 'POST':
    name = request.POST.get('name','')
    email = request.POST.get('email','')
    address = request.POST.get('address','')
    city = request.POST.get('city','')
    state = request.POST.get('state','')
    zipcode = request.POST.get('zipcode','')
    order = UserOrder(user = request.user,name=name,email=email,address=address,city=city,state=state,zipcode=zipcode)
    order.save()
    cart = Cart.objects.filter(user = request.user).first()
    products = cart.cart_products.all()
    for product in products:
      OrderProduct.objects.create(
        order=order,product_id=product.product_id,
        quantity=product.quantity,
        product_price = product.product_price,
        product_title = product.product_title,
      ).save()
    cart.delete()
    new_cart = Cart(user=request.user)
    new_cart.save()
    
    return redirect('home')
  try:
    cart = Cart.objects.filter(user = request.user).first()
    products = cart.cart_products.all()
    if not products:
      return redirect('home')
  except:
    return redirect('users:login')
  print(products,'cart products')
  return render(request,'shop/checkout.html',context={'products':products,"cart":cart})