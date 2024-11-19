from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.permissions import IsOwnerReadOnly, IsAdminUser
from advertisements.serializers import UserSerializer, AdvertisementSerializer, FavoriteAdvertisementSerializer
from .permissions import IsOwnerForDelete


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return self.queryset.filter(Q(creator=user) | Q(status__in=['OPEN', 'CLOSED']))
        return self.queryset.filter(status='OPEN')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        elif self.action == 'create':
            return [IsAuthenticated()]

        elif self.action in ['update', 'partial_update']:

            if self.request.user.is_superuser:
                return [IsAdminUser()]
            return [IsOwnerReadOnly()]

        elif self.action == 'destroy':

            if self.request.user.is_superuser:
                return [IsAdminUser()]
            return [IsAuthenticated(), IsOwnerForDelete()]

        return super().get_permissions()


class FavoriteAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = FavoriteAdvertisement.objects.all()
    serializer_class = FavoriteAdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        advertisement_id = self.request.data.get('advertisement')

        if advertisement_id:

            try:
                advertisement = Advertisement.objects.get(id=advertisement_id)
            except Advertisement.DoesNotExist:
                raise serializers.ValidationError("Объявление не найдено.")

            if advertisement.creator == self.request.user:
                raise serializers.ValidationError("Вы не можете добавить свое объявление в избранное.")

        serializer.save(user=self.request.user)

    def get_queryset(self):

        return self.queryset.filter(user=self.request.user)
