from django.urls import path, include
from .import views
from rest_framework import routers


app_name = 'ozon_products'

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, 'products')


urlpatterns = [
    path('', include(router.urls)),
]



