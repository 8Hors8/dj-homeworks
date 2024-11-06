from django.db import models


class TemperatureSensor(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        return self.name


class SensorData(models.Model):
    sensor_id = models.ForeignKey(TemperatureSensor, related_name='measurements',
                                  to_field='id', on_delete=models.CASCADE)
    temperature = temperature = models.FloatField()
    date_of_measurement = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='sensor_images/', null=True, blank=True)

    def __str__(self):
        return f"Data for sensor {self.sensor_id.name} at {self.date_of_measurement}"
