import uuid
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


def default_location():
    """Default to (0,0) for missing location data"""
    return Point(0.0, 0.0, srid=4326)


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Country(BaseModel):
    """Stores country information with ISO codes and region details."""
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=10, default="en", help_text="Primary language code")
    timezone = models.CharField(max_length=50, default="UTC", help_text="Default timezone")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = "Country"


class State(BaseModel):
    """Stores state/province information. Not all countries have states."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")

    def __str__(self):
        return f"{self.name}, {self.country.code}"

    class Meta:
        db_table = "State"


class City(BaseModel):
    """Stores city information, allowing direct links to a country (for cities without states)."""
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities", blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        if self.state:
            return f"{self.name}, {self.state.name}, {self.country.code}"
        return f"{self.name}, {self.country.code}"

    class Meta:
        db_table = "City"


class Address(BaseModel):
    """Stores addresses and links them to users, tenants, and businesses."""
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20)

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="addresses")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="addresses", blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="addresses")

    location = models.PointField(geography=True, srid=4326, default=default_location)
    is_valid = models.BooleanField(default=False)

    user_id = models.UUIDField(null=True, blank=True, help_text="UUID from user-api JWT")
    tenant_id = models.UUIDField(null=True, blank=True, help_text="External Tenant ID")
    is_billing = models.BooleanField(default=False, help_text="Marks as billing address")
    is_default = models.BooleanField(default=False)

    language = models.CharField(max_length=10, blank=True, null=True, help_text="Preferred language for the address")
    timezone = models.CharField(max_length=50, blank=True, null=True, help_text="Timezone of the address location")

    class Meta:
        indexes = [
            models.Index(fields=["postal_code", "city", "state"]),
            models.Index(fields=["location"], name="location_idx"),  # ✅ Spatial Index for faster lookup
        ]
        unique_together = ["address_line_1", "address_line_2", "city", "state", "country", "postal_code", "user_id"]
        db_table = "Address"

    def __str__(self):
        return f"{self.address_line_1}, {self.city.name}, {self.state.name if self.state else ''}, {self.country.code}"


class Coordinates(BaseModel):
    """Stores latitude and longitude separately if needed."""
    latitude = models.FloatField(help_text="Latitude coordinate")
    longitude = models.FloatField(help_text="Longitude coordinate")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="coordinates")

    class Meta:
        db_table = "coordinates"

    def __str__(self):
        return f"Lat: {self.latitude}, Lon: {self.longitude}"