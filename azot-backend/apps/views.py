from django.core import serializers
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.serializers import ClientInSerializer, ClientOutSerializer

from apps.models import Client


# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        client = ClientInSerializer(data = request.data)
        if client.is_valid():
            instance = client.update(Client(), client.validated_data)
            return JsonResponse(ClientOutSerializer(instance).data, status=status.HTTP_201_CREATED)
        return JsonResponse(client.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        clients = Client.objects.all()
        return Response(serializers.serialize("json", clients), status=status.HTTP_200_OK)
