from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import DurationField, ExpressionWrapper, F
from .models import Booking, RoomType, Room, Customer
from datetime import datetime
import random
import string 
from urllib.parse import urlencode

def generate_random_alphanumeric_string(length):
    random_alp_numeric_str = string.ascii_letters + string.digits
    return ''.join(random.choice(random_alp_numeric_str) for i in range(length))

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
    room_types_available = RoomType.objects.filter(max_guest__gte=num_guests, room__is_bookable=True).exclude(booking__checkin_date__lte=out_date, booking__checkout_date__gt=in_date).order_by('id')

    # room_types_available = RoomType.objects.annotate(
    #             duration=ExpressionWrapper(F('booking__checkout_date')-F('booking__checkin_date'),output_field=DurationField())).filter(
    #     max_guest__gte=num_guests, room__is_bookable=True).exclude(
    #         booking__checkin_date__lte=out_date, booking__checkout_date__gt=in_date).order_by('id')
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

def create_or_update_customer(name, email, country_code, phone):
    try:
        customer_instance = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        customer_instance = Customer(name=name, email=email, country_code=country_code, phone=phone)
        customer_instance.save()

    return customer_instance
    

def save_booking(request):
    in_date = request.POST['in_date']
    out_date = request.POST['out_date']
    num_guests = request.POST['num_guests']
    room_type = request.POST['room_type']
    name = request.POST['name']
    email = request.POST['email']
    country_code = request.POST['country_code']
    phone = request.POST['phone']
    error=''

    customer_instance = create_or_update_customer(name, email, country_code, phone)

    room = Room.objects.filter( type=room_type, is_bookable=True).exclude(booking__checkin_date__lte=out_date, booking__checkout_date__gt=in_date).first()
    if room:
        booking_instance = Booking(
            locator = generate_random_alphanumeric_string(10),
            room_type = RoomType.objects.get(id=room_type),
            num_guest = num_guests,
            customer = customer_instance,
            total_price = 300,
            room_num = room,
            checkin_date = in_date,
            checkout_date = out_date,
            created_date = str(datetime.now()),
        )
        try:
            booking_instance.save()
        except Exception as e:     
            error='Error saving booking: %s' % e.msg
    
    else:
        booking_instance = NULL
        error='Booking error: Any room available'
    
    base_url = reverse('booking_list')
    query_string = ''
    if error:
        query_string = urlencode({'error': error})
    url = '{}?{}'.format(base_url, query_string) 
    return redirect(url)
    

