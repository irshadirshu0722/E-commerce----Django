from django.contrib import admin
from .models import Products,UserOrder,Cart,CartProduct,OrderProduct
# Register your models here.

admin.site.site_title = 'ABC Shoping'
admin.site.site_header = 'E-commerce site'
admin.site.index_title = 'Manage ABC Shopping'


class ProductAdmin(admin.ModelAdmin):
  def change_category_to_default(self,request,queryset):
    queryset.update(Category = "default")
  change_category_to_default.short_description = "Default Category"
  list_display = ('title','price','discount_price','Category')
  search_fields = ('title',)
  actions = ('change_category_to_default',)
  fields = ('title','price') #hide fields
  list_editable = ('price',"Category")

class OrderProductAdmin(admin.ModelAdmin):
  list_display = ('product_title','order','product_price','quantity')

admin.site.register(Products,ProductAdmin)
admin.site.register(UserOrder)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(OrderProduct,OrderProductAdmin)
