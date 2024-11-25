from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadOnlyForDelete
from advertisements.serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(
                Q(creator=user) | Q(status__in=['OPEN', 'CLOSED'])
            )
        return self.queryset.filter(status='OPEN')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Добавляем количество объявлений в ответ
        response_data = {
            'total_count': queryset.count(),
            'results': serializer.data
        }
        return Response(response_data)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsOwnerOrReadOnlyForDelete()]
        elif self.action == 'destroy':
            return [IsOwnerOrReadOnlyForDelete()]
        return super().get_permissions()


class FavoriteAdvertisementViewSet(ModelViewSet):
    """ViewSet для избранных объявлений."""
    queryset = FavoriteAdvertisement.objects.all()
    serializer_class = FavoriteAdvertisementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
