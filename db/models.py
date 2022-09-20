from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()

    class Meta:
        verbose_name_plural = "buses"  # admin page

    def __str__(self):
        return self.info


class Trip(models.Model):
    source = models.CharField(max_length=63, db_index=True)
    destination = models.CharField(max_length=63)
    departure = models.DateTimeField()
    bus = models.ForeignKey("Bus", on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["source", "destination"]),
            models.Index(fields=["departure"])
        ]

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.departure})"


class Ticket(models.Model):
    seat = models.IntegerField()
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["seat", "trip"], name="unique_ticket_seat_trip")
        ]

    def __str__(self):
        return f"{self.trip} - (seat: {self.seat})"

    def clean(self):
        if not (1 <= self.seat <= self.trip.bus.num_seats):
            raise ValidationError({
                "seat": f"seat must be in range [1, {self.trip.bus.num_seats}], not {self.seat}"
            })

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # сортування даних від останнього заказу

    def __str__(self):
        return str(self.created_at)
