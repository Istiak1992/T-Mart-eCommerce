from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Gender)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Customer)
admin.site.register(Cart)

admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(SliderImage)
admin.site.register(Review)





