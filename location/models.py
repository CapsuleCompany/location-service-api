from django.contrib.gis.db import models
from django.utils.timezone import now

class Location(models.Model):
    # Reference to an external provider, can also integrate via an API
    provider_id = models.CharField(max_length=255, help_text="ID of the provider from the User Microservice")
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(default=now, help_text="Time of the location update")

    def __str__(self):
        return f"Provider {self.provider_id} - {self.latitude}, {self.longitude} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),  # Efficient geospatial queries
        ]


class Address(models.Model):
    linked_entity_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID of the linked entity (e.g., user, service)"
    )
    linked_entity_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Type of the entity (e.g., 'user', 'service')"
    )

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="US")
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.country}"

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
        ]
