from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(State)
admin.site.register(CouponCode)
admin.site.register(Order)