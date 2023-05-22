from django.urls import include, path
from rest_framework import routers
from account.views import *

router = routers.DefaultRouter()
router.register(r'user', UserViewset)
router.register(r'category', CategoryViewset)
router.register(r'product',ProductViewset)
router.register(r'image',ImageViewset)
router.register(r'specification',SpecificationViewset)
router.register(r'sizechart',SizechartViewset)
router.register(r'review',ReviewViewset)
router.register(r'servicerequest',ServiceRequestViewset)
router.register(r'cart',CartViewset)
router.register(r'favourite',FavViewset)
router.register(r'address',AddressViewset)
router.register(r'order',OrderViewset)
router.register(r'sizeguide', GlobleSizeViewset)
router.register(r'sitereview',SiteReviwViewset)
router.register(r'alert',AlertViewset)
router.register(r'coupon',CouponViewset)
router.register(r'offer',OfferViewset)

urlpatterns = [
    path("",include(router.urls))
]