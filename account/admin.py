from django.contrib import admin

from account.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductSpecification)
admin.site.register(ProductImage)
admin.site.register(ProductDimension)
admin.site.register(Review)
admin.site.register(ServiceRequest)
admin.site.register(ProductAttribute)
admin.site.register(Cart)
admin.site.register(Favourite)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(GlobleSize)
admin.site.register(SiteReview)
admin.site.register(Alerts)