from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.utils.representation import serializer_repr

from .models import (
    AirplaneType,
    Airplane,
    Crew,
    Airport,
    Route,
    Flight,
    Order,
    Ticket
)
from .serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailListSerializer,
)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailListSerializer
        return AirplaneSerializer

