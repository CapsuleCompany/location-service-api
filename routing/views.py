from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Route, RouteStop
from .serializers import RouteSerializer
from .utils import get_optimized_route


class RouteCreateView(APIView):
    """
    Creates and optimizes a delivery route.
    """

    def post(self, request):
        data = request.data
        origin = data.get("origin")
        stops = data.get("stops", [])
        destination = data.get("destination")

        # Validate input
        if not origin or not destination or not stops:
            return Response({"error": "Missing required fields."}, status=400)

        # Optimize the route
        optimized_route = get_optimized_route(origin, stops, destination)

        # Extract optimized waypoint order
        waypoint_order = optimized_route["routes"][0].get("waypoint_order", [])

        # Reorder stops based on Google’s optimization
        sorted_stops = [stops[i] for i in waypoint_order]

        # Save Route to database
        route = Route.objects.create(
            name=data.get("name", ""),
            origin_address=origin["address"],
            origin_latitude=origin["latitude"],
            origin_longitude=origin["longitude"],
            destination_address=destination["address"],
            destination_latitude=destination["latitude"],
            destination_longitude=destination["longitude"],
        )

        # Save each stop in order
        for stop in sorted_stops:
            RouteStop.objects.create(route=route, **stop)

        return Response(
            {"route_id": route.id, "optimized_route": optimized_route}, status=201
        )
