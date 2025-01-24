from django.urls import path, include

urlpatterns = [
    path('api/location/', include('location.urls')),
]

