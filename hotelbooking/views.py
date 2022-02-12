from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Booking, RoomType, Room

def login_user(request):
    return render(request, 'registration/login.html', {})

def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request)
    if user is not None:
        login(request, user)
        bookings = Booking.objects.all()
        return render(request, 'hotelbooking/booking_list.html', {'bookings': bookings})
    else:
        return render(request, 'hotelbooking/login/login.html', {})

def logout(request):
    # if request.method == "POST":
    #     logout(request)

    return redirect('/accounts/logout')

@login_required(login_url='/accounts/login/')
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'hotelbooking/booking_list.html', {'bookings': bookings})

def new_booking(request):
    if request.user.is_authenticated:
        return render(request, 'hotelbooking/new_booking.html', {})
    else:
        return render(request, 'hotelbooking/errors/error_404.html', {})

def error_404_view(request):
    return redirect('/')

def get_room_types_available(request):
    #room_types_available = RoomType.objects.all()
    in_date = request.GET['in_date']
    out_date = request.GET['out_date']
    num_guests = request.GET['num_guests']
    room_types_available = RoomType.objects.filter(max_guest=num_guests, room__is_bookable=True).exclude(booking__checkin_date__lte=out_date, booking__checkout_date__gt=in_date)
    return render(
        request,
        'hotelbooking/new_booking.html', 
        {'room_types_available' : room_types_available, 'in_date': in_date, 'out_date': out_date, 'num_guests': num_guests})


    

