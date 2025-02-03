import requests
from django.conf import settings

# GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"


def get_optimized_route(origin, stops, destination):
    """
    Calls Google Maps Directions API to get an optimized route.
    """
    waypoints = "|".join([f"{stop['latitude']},{stop['longitude']}" for stop in stops])

    url = f"https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": f"{origin['latitude']},{origin['longitude']}",
        "destination": f"{destination['latitude']},{destination['longitude']}",
        "waypoints": f"optimize:true|{waypoints}",
        "key": GOOGLE_MAPS_API_KEY,
    }

    response = requests.get(url, params=params)
    return response.json()
