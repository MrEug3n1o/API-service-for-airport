from rest_framework import serializers
from .models import (
    AirplaneType, Airplane, Crew, Airport,
    Route, Flight, Order, Ticket
)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
            "airplane_type_name"
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    source_name = serializers.ReadOnlyField(source="source.name")
    destination_name = serializers.ReadOnlyField(source="destination.name")

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance", "source_name", "destination_name")


class FlightSerializer(serializers.ModelSerializer):
    airplane_name = serializers.ReadOnlyField(source="airplane.name")
    route_info = serializers.ReadOnlyField(source="route.__str__")
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "departure_time",
            "arrival_time",
            "airplane_name",
            "route_info"
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")
