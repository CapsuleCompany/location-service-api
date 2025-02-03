from rest_framework import serializers
from .models import Route, RouteStop


class RouteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStop
        fields = ["address", "latitude", "longitude", "delivery_time"]


class RouteSerializer(serializers.ModelSerializer):
    stops = RouteStopSerializer(many=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "name",
            "origin_address",
            "origin_latitude",
            "origin_longitude",
            "destination_address",
            "destination_latitude",
            "destination_longitude",
            "stops",
        ]
