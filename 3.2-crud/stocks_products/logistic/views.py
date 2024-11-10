from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend

from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=True, methods=['delete'], url_path='remove-position/(?P<product_id>[^/.]+)')
    def remove_position(self, request, pk=None, product_id=None):
        try:
            # Находим позицию по складу и продукту
            stock = self.get_object()  # Получаем склад по ID (pk)
            position = StockProduct.objects.get(stock=stock, product_id=product_id)
            position.delete()
            return Response({"detail": "Позиция удалена"}, status=status.HTTP_204_NO_CONTENT)
        except StockProduct.DoesNotExist:
            return Response({"detail": "Позиция не найдена"}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        queryset = super().get_queryset()

        product_id = self.request.query_params.get('product')
        product_search = self.request.query_params.get('search')


        if product_id:
            queryset = queryset.filter(products__id=product_id)

        if product_search:
            queryset = queryset.filter(
                products__title__icontains=product_search
            ) | queryset.filter(
                products__description__icontains=product_search
            )

        return queryset
