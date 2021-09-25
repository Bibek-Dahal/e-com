from django.contrib import admin
from .models import*
from .forms import SkuChecker
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','cid','customer','full_name','temporary_address','shipping_address','date_joined']

@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(SubCatagory)
class SubCatagoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','catagory','subcatagory','title','Description','marked_price','discount_price','is_stock','is_active']

@admin.register(ProductVariationsOptions)
class ProductVariationsOptionsAdmin(admin.ModelAdmin):
    list_display = ['id','product','name']

@admin.register(ProductVariationValue)
class ProductVariationValueAdmin(admin.ModelAdmin):
    list_display = ['id','product_variation_option','product_variation_value']

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    model = ProductInventory
    form = SkuChecker
    fields = ['product','combination_string','quantity']
    list_display = ['id','product','combination_string','sku','quantity']

@admin.register(Product_image)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id','product','image']





