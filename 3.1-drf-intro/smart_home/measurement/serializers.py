from rest_framework import serializers, generics

from measurement.models import SensorData, TemperatureSensor


# TODO: опишите необходимые сериализаторы

class MeasurementSerializer(serializers.ModelSerializer):
    sensor_id = serializers.PrimaryKeyRelatedField(queryset=TemperatureSensor.objects.all(),
                                                   write_only=True)

    class Meta:
        model = SensorData
        fields = ['sensor_id', 'temperature', 'date_of_measurement', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('sensor_id', None)
        return representation


class SensorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureSensor
        fields = ['id', 'name', 'description', 'created_at']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = TemperatureSensor
        fields = ['id', 'name', 'description', 'created_at', 'measurements']
