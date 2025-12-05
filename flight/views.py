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
from serializers import (
    AirplaneTypeSerializer,
)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


