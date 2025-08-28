

# Create your tests here.
from django.utils import timezone
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Travel_Option, Booking
from datetime import datetime, timedelta

class BookingTests(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = Client()

        
        self.travel = Travel_Option.objects.create(
            type="Flight",
            From="Delhi",
            To="Mumbai",
            date_time=timezone.now(),
            price=5000,
            available_seats=50,
        )

    def test_user_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser",
            "email": "new@example.com",
            "password1": "password123!",
            "password2": "password123!",
        })
        print("Form errors:", response.context["form"].errors)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_login(self):
        login = self.client.login(username="testuser", password="password123")
        self.assertTrue(login)

    def test_travel_list_view(self):
        response = self.client.get(reverse("home page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delhi")

    def test_booking_creation(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("book_travel", args=[self.travel.id]), {
            "seats": 2
        })
        self.assertEqual(response.status_code, 302)  # Redirect to my_bookings
        booking = Booking.objects.get(users=self.user)
        self.assertEqual(booking.seats, 2)
        self.assertEqual(booking.total_price, 10000)
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 48)

    def test_booking_cancellation(self):
        self.client.login(username="testuser", password="password123")
        booking = Booking.objects.create(
            users=self.user,
            travel_option=self.travel,
            seats=2,
            total_price=10000,
        )
        response = self.client.get(reverse("cancel_booking", args=[booking.booking_id]))
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "Cancelled")
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 52)
