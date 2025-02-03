from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ViewSet):
    """
    List and create addresses for the authenticated user.
    """
    def list(self, request):
        queryset = Address.objects.filter(
            user_id=self.request.user.user_id
        )
        serializer = AddressSerializer(
            queryset, many=True
        )
        return Response(serializer.data)

    def create(self, request):
        serializer = AddressSerializer(data=request.data, context={"user": self.request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
