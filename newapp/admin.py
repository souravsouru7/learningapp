from django.contrib import admin
from .models import Product,UserProfile,PurchasedProduct
# Register your models here.
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(PurchasedProduct)