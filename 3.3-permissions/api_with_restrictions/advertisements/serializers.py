from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, FavoriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',
                  )
        read_only_filds = ['creator']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        instance = self.instance
        user = self.context['request'].user

        # Проверка изменения статуса на 'OPEN'
        new_status = data.get('status', instance.status if instance else None)

        # Если новое объявление или обновляется статус
        if new_status == 'OPEN':
            user_open_ads_count = Advertisement.objects.filter(
                creator=user, status='OPEN'
            ).count()

            # Проверка лимита открытых объявлений
            if user_open_ads_count >= 10:
                raise ValidationError(
                    "Нельзя перевести объявление в статус 'OPEN', так как у вас уже 10 открытых объявлений."
                )

        return data


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAdvertisement
        fields = ['id', 'user', 'advertisement', 'created_at']
        read_only_fields = ['user']

    def validate(self, data):
        advertisement = data.get('advertisement')
        user = self.context['request'].user

        if advertisement.creator == user:
            raise serializers.ValidationError(
                "Вы не можете добавить свое объявление в избранное."
            )
        return data
