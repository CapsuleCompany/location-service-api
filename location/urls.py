from django.urls import path
from .views import LocationUpdateView, LocationListView

urlpatterns = [
    path('update/', LocationUpdateView.as_view(), name='location-update'),
    path('list/', LocationListView.as_view(), name='location-list'),
]
