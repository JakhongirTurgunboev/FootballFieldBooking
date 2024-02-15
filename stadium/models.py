from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from account.models import CustomUser

# Create your models here.


class FootballField(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()
    contact = models.CharField(max_length=250)
    price_per_hour = models.DecimalField(max_digits=15, decimal_places=2)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class FootballFieldImages(models.Model):
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.football_field}'


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    football_field = models.ForeignKey(FootballField, on_delete=models.CASCADE)
    booking_start_time = models.DateTimeField()
    booking_duration_in_hours = models.FloatField(default=1)

    def __str__(self):
        return f'{self.football_field}'

    def clean(self):
        # Check for intersection with existing bookings
        booking_end_time = self.booking_start_time + timedelta(hours=self.booking_duration_in_hours)

        existing_bookings = Booking.objects.filter(
            football_field=self.football_field,
            booking_start_time__lt=booking_end_time,
            booking_start_time__gte=self.booking_start_time
        ).exclude(id=self.id)

        if existing_bookings.exists():
            raise ValidationError("Booking intersects with existing bookings.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving
        super().save(*args, **kwargs)
