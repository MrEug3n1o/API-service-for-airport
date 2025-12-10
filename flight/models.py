from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

latin_validator = RegexValidator(
    regex=r'^[A-Za-z]+$',
    message="Name must contain only Latin letters. No numbers and other symbols"
)

class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.airplane_type.name})"


class Crew(models.Model):
    first_name = models.CharField(max_length=255, validators=[latin_validator])
    last_name = models.CharField(max_length=255, validators=[latin_validator])

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255, validators=[latin_validator])
    closest_big_city = models.CharField(max_length=255, validators=[latin_validator])

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departure_routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrival_routes"
    )
    distance = models.IntegerField()

    class Meta:
        ordering = ["source__name", "destination__name"]
        unique_together = ["source", "destination"]

    def __str__(self):
        return f"{self.source.name} → {self.destination.name} ({self.distance} km)"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    crew = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"Flight #{self.id}: {self.route} at {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} at {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        ordering = ["row", "seat"]
        unique_together = ["flight", "row", "seat"]

    def __str__(self):
        return f"Ticket: row {self.row}, seat {self.seat} (Flight #{self.flight.id})"


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
