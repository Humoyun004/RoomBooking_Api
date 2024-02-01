from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()
    description = models.TextField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    checking_date = models.DateTimeField(blank=True, null=True)
    checkout_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.room} booked from - {self.customer.username} at - {self.checking_date}"



