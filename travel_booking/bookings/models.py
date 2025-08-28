from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Travel_Option(models.Model):
    travel_options = [("bus","bus"),
                      ("train","train"),
                      ("Flight","Flight"),
                      ]
    type = models.CharField(max_length=10, choices= travel_options)
    From = models.CharField( max_length=100)
    To = models.CharField( max_length=100)
    date_time = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.type}: {self.source} → {self.destination}"
    
class Booking(models.Model):
    booking_status = [("confirmed","confirmed"),
                      ("failed","Failed"),
                      ]
    booking_id = models.AutoField(primary_key=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(Travel_Option, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=booking_status, default='Confirmed')

    def __str__(self):
        return f"Booking {self.id} - {self.user.username}"

