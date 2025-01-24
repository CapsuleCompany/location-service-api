from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Location
from .serializers import LocationSerializer


class LocationUpdateView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class LocationListView(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        provider = self.request.user
        return Location.objects.filter(provider=provider).order_by('-timestamp')
