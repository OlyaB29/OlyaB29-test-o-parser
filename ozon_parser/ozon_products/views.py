from rest_framework.response import Response
from rest_framework import viewsets
from .models import Products
from .serializers import ProductSerializer
from ozon_products.tasks import get_products
from . import constants


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        products_count = int(request.data.get("products_count", constants.DEFAULT_NUM))
        task=get_products.delay(products_count)
        print(task.id)
        return Response(f"Парсинг товаров в количестве {products_count} запущен")

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        if request.GET.get("last_products"):
            last_date = queryset.first().date
            queryset = queryset.filter(date = last_date)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)




