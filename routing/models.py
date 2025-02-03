from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    origin_address = models.CharField(max_length=255)
    origin_latitude = models.FloatField()
    origin_longitude = models.FloatField()
    destination_address = models.CharField(max_length=255)
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class RouteStop(models.Model):
    route = models.ForeignKey(Route, related_name="stops", on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    delivery_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["delivery_time"]
