# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from rest_framework import generics
from measurement.models import SensorData, TemperatureSensor
from .serializers import MeasurementSerializer, SensorDetailSerializer, SensorListSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


# Вариант решения 1.
class SensorViews(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            try:
                sensor = TemperatureSensor.objects.get(pk=pk)
                ser = SensorDetailSerializer(sensor)

            except TemperatureSensor.DoesNotExist:
                return Response({"error": "Датчик не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            sensor = TemperatureSensor.objects.all()
            ser = SensorDetailSerializer(sensor, many=True)

        return Response(ser.data)

    def post(self, request):

        ser = SensorDetailSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):

        try:
            sensor = TemperatureSensor.objects.get(pk=pk)
        except TemperatureSensor.DoesNotExist:
            return Response({"error": "Датчик не найден"}, status=status.HTTP_404_NOT_FOUND)
        ser = SensorDetailSerializer(sensor, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasurementViews(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):

        if pk is not None:
            try:
                meas = SensorData.objects.get(pk=pk)
                ser = MeasurementSerializer(meas)

            except TemperatureSensor.DoesNotExist:
                return Response({"error": "Датчик еще не предавал измерения"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            meas = SensorData.objects.all()
            ser = MeasurementSerializer(meas)

        return Response(ser.data)

    def post(self, request):
        ser = MeasurementSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


# Вариант решения 2.

class TemperatureSensorListCreateAPIView(generics.ListCreateAPIView):
    """
    Обработчик для получения списка температурных датчиков и создания нового датчика.
    """
    queryset = TemperatureSensor.objects.all()
    serializer_class = SensorListSerializer


class TemperatureSensorRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Обработчик для получения, обновления или удаления конкретного температурного датчика.
    """
    queryset = TemperatureSensor.objects.all()
    serializer_class = SensorDetailSerializer


class SensorDataCreateAPIView(generics.CreateAPIView):
    """
    Обработчик для создания новых записей данных сенсора.
    """
    queryset = SensorData.objects.all()
    serializer_class = MeasurementSerializer
