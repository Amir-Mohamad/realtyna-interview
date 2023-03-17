from django.db import models
from django.core.validators import MinValueValidator
from .tasks import send_confirmation_email

class Listing(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Room(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_confirmation_email.delay(self.id)