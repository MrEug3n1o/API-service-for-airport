from rest_framework import serializers
from django.db.models import Count
from django.utils import timezone
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


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )

    class Meta(AirplaneSerializer.Meta):
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)
    total_seats = serializers.SerializerMethodField()

    class Meta(AirplaneSerializer.Meta):
        fields = AirplaneSerializer.Meta.fields + ("total_seats",)

    def get_total_seats(self, obj):
        return obj.rows * obj.seats_in_row


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


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

    class Meta(RouteSerializer.Meta):
        fields = RouteSerializer.Meta.fields


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "crew", "departure_time", "arrival_time")


class FlightListSerializer(FlightSerializer):
    airplane_name = serializers.ReadOnlyField(source="airplane.name")
    route_info = serializers.ReadOnlyField(source="route.__str__")
    available_seats = serializers.SerializerMethodField()

    class Meta(FlightSerializer.Meta):
        fields = ("id", "route_info", "airplane_name", "departure_time", "arrival_time", "available_seats")

    def get_available_seats(self, obj):
        total_seats = obj.airplane.rows * obj.airplane.seats_in_row
        sold_tickets = obj.tickets.count()
        return total_seats - sold_tickets


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneDetailSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    available_seats = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + ("available_seats", "duration")

    def get_available_seats(self, obj):
        total_seats = obj.airplane.rows * obj.airplane.seats_in_row
        sold_tickets = obj.tickets.count()
        return total_seats - sold_tickets

    def get_duration(self, obj):
        return obj.arrival_time - obj.departure_time


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class OrderListSerializer(OrderSerializer):
    ticket_count = serializers.SerializerMethodField()

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ("ticket_count",)

    def get_ticket_count(self, obj):
        return obj.tickets.count()


class OrderDetailSerializer(OrderSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ("tickets",)

    def get_tickets(self, obj):
        tickets = obj.tickets.all()
        return [
            {
                "id": ticket.id,
                "row": ticket.row,
                "seat": ticket.seat,
                "flight_id": ticket.flight_id,
                "flight_info": str(ticket.flight.route)
            }
            for ticket in tickets
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")

    def validate(self, data):
        """Validate that the seat is within airplane limits"""
        flight = data.get('flight')

        if flight and 'row' in data and 'seat' in data:
            airplane = flight.airplane

            if data['row'] > airplane.rows:
                raise serializers.ValidationError(
                    f"Row must be between 1 and {airplane.rows}"
                )

            if data['seat'] > airplane.seats_in_row:
                raise serializers.ValidationError(
                    f"Seat must be between 1 and {airplane.seats_in_row}"
                )

        return data
