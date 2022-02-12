from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from .models import Booking, RoomType, Room, Customer
from datetime import datetime    


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

@login_required(login_url='/accounts/login/')
def new_booking(request):
    return render(
        request,
        'hotelbooking/new_booking.html',
        {'in_date': str(datetime.now()), 'out_date': str(datetime.now()), 'num_guests': 1}
    )

def error_404_view(request):
    return redirect('/')

def get_room_types_available(request):
    in_date = request.GET['in_date']
    out_date = request.GET['out_date']
    num_guests = request.GET['num_guests']
    room_types_available = RoomType.objects.filter(max_guest__gte=num_guests, room__is_bookable=True).exclude(booking__checkin_date__lte=out_date, booking__checkout_date__gt=in_date)
    return render(
        request,
        'hotelbooking/new_booking.html', 
        {'room_types_available' : room_types_available, 'in_date': in_date, 'out_date': out_date, 'num_guests': num_guests}
    )

def booking_contact_data(request):
    in_date = request.GET['in_date']
    out_date = request.GET['out_date']
    num_guests = request.GET['num_guests']
    room_type = request.GET['room_type']
    return render(
        request,
        'hotelbooking/booking_contact_data.html',
        {'in_date': in_date, 'out_date': out_date, 'num_guests': num_guests, 'room_type': room_type}
    )

def save_booking(request):
    in_date = request.POST['in_date']
    out_date = request.POST['out_date']
    num_guests = request.POST['num_guests']
    room_type = request.POST['room_type']
    name = request.POST['name']
    email = request.POST['email']
    country_code = request.POST['country_code']
    phone = request.POST['phone']

    booking_instance = RequestContext(Booking.objects.create(
        locator = "AAAB123456",
        room_type = RoomType.objects.get(id=room_type),
        num_guest = num_guests,
        customer = Customer.objects.get(id=1),
        total_price = 300,
        room_num = Room.objects.get(num=220),
        checkin_date = in_date,
        checkout_date = out_date,
        created_date = str(datetime.now()),
    ))
    return render(
        request,
        '/',
        {booking_instance}
    )
    

