from django.shortcuts import render, redirect, get_object_or_404
from .models import Travel_Option, Booking
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

    
def register_view(request): 
    if request.method == ["POST"]:
        form = RegistrationForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request,user)
            
            return redirect("home page")   
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):    
    if request.method == ["POST"]:
        data = request.POST
        form = AuthenticationForm(request,data )
        if form.is_valid:
            user = form.get_user()
            login(request,user)
            return redirect("home page")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):   
    logout(request)
    return redirect("login")

def travel_list_view(request):
    travels = Travel_Option.objects.all()
    travel_type = request.GET.get('type')
    From = request.GET.get('From')
    To = request.GET.get('To')

    if travel_type:
        travels = travels.filter(type=travel_type)
    if From:
        travels = travels.filter(From__icontains=From)
    if To:
        travels = travels.filter(To__icontains=To)
    return render(request, 'travel_list.html', {'travels': travels})



def travel_booking(request,travel_id):
    travel = get_object_or_404(Travel_Option,pk = travel_id)
    if request.method == "POST":
        seats = int(request.POST.get("seats"))
        if seats <=0:
            return {"message":"seats must be greater than 0"},redirect('travel_booking',travel_id = travel_id)
        if seats > travel.available_seats:
            return {"message":"Not enough seats available."},redirect('book_travel', travel_id=travel_id)
    
        total_price = seats * travel.price
        Booking.objects.create(
            users=request.user,
            travel_option=travel,
            seats=seats,
            total_price=total_price
        )
        travel.available_seats -= seats
        travel.save()
        return redirect('my_bookings')
    
    return render(request, 'book_travel.html', {'travel': travel})

def booking_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_bookings.html', {'bookings': bookings})


def cancel_booking(request,booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, users=request.user)

    if booking.status == 'Cancelled':
        print( "Booking is already cancelled.")
    else:
        booking.status = 'Cancelled'
        booking.save()

        # Return seats back
        booking.travel_option.available_seats += booking.seats
        booking.travel_option.save()  
    
    return redirect('my_bookings')