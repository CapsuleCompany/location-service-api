from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ViewSet):
    """
    List, create, retrieve, update, and delete addresses for the authenticated user.
    """

    def list(self, request):
        queryset = Address.objects.filter(user_id=self.request.user.user_id)
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AddressSerializer(data=request.data, context={"user": self.request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk, user_id=self.request.user.user_id)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def update(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk, user_id=self.request.user.user_id)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        address = get_object_or_404(Address, pk=pk, user_id=self.request.user.user_id)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)