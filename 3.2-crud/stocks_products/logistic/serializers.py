from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        for position_data in positions:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        new_positions = validated_data.pop('positions', [])
        existing_positions = {position.product_id: position for position in instance.positions.all()}

        for position_data in new_positions:
            product_id = position_data['product'].id
            quantity = position_data.get('quantity')
            price = position_data.get('price')

            if product_id in existing_positions:
                position = existing_positions[product_id]
                position.quantity = quantity if quantity is not None else position.quantity
                position.price = price if price is not None else position.price
                position.save()
            else:
                StockProduct.objects.create(stock=instance, **position_data)
        return instance
