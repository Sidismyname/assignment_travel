from django.urls import path, include 
from . import views

urlpatterns = [
    path('',views.travel_list_view,name="home page"),
    path('register',views.register_view,name="register"),
    path('login',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),
    path('book/<int:travel_id>',views.travel_booking,name="book_travel"),
    path('my_bookings',views.booking_view,name="my_bookings"),
    path('cancel/<int:booking_id>',views.cancel_booking,name="cancel_booking"),

]