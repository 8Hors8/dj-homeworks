from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerReadOnly
from advertisements.serializers import UserSerializer, AdvertisementSerializer
from .permissions import IsOwnerForDelete


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsOwnerReadOnly()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwnerForDelete()]

        return super().get_permissions()
