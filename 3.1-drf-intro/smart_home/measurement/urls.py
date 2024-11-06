from django.urls import path

from measurement.views import SensorViews, MeasurementViews

from measurement.views import TemperatureSensorListCreateAPIView, TemperatureSensorRetrieveUpdateAPIView, \
    SensorDataCreateAPIView


# urlpatterns = [
#     path('sensors/', SensorViews.as_view(), name='sensors-create'),
#     path('sensors/<str:pk>/', SensorViews.as_view(), name='sensor-retrieve-update'),
#     path('measurements/', MeasurementViews.as_view(), name='sensor-data-create'),
#
# ]

urlpatterns = [
    path('sensors/', TemperatureSensorListCreateAPIView.as_view(), name='sensors-create'),
    path('sensors/<str:pk>/', TemperatureSensorRetrieveUpdateAPIView.as_view(),
         name='sensor-retrieve-update'),
    path('measurements/', SensorDataCreateAPIView.as_view(), name='sensor-data-create')
]
