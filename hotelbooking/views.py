from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import F
from .models import Booking, RoomType, Room, Customer
from datetime import datetime, timedelta
import random
import string 
from urllib.parse import urlencode
from hashlib import blake2b
from django.contrib import messages

def generate_hash(text):
    hash = blake2b(digest_size=10)
    hash.update(text.encode('utf-8'))
    return hash.hexdigest()

def login_user(request):
    return render(request, 'registration/login.html', {})

def authenticate_user(request):
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
    now = datetime.now()
    return render(
        request,
        'hotelbooking/new_booking.html',
        {'in_date': now.strftime("%d-%m-%Y"), 'out_date': str( datetime.now().date() + timedelta(days=1)), 'num_guests': 1}
    )

def dif_between_dates(start_date, end_date):
    dif_in_out_date = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
    return dif_in_out_date


def get_room_types_available(request):
    try:
        in_out_range = request.GET['in_out_range'].split(" - ")
        in_date = in_out_range[0]
        out_date = in_out_range[1]
    except Exception as e:
        messages.error(request, str("Invalid dates"))
        return redirect(get_url_home())
    try:
        num_guests = request.GET['num_guests']
        dif_in_out_date = dif_between_dates(in_date,out_date)
        room_types_available = RoomType.objects.filter(max_guest__gte=num_guests, room__is_bookable=True).exclude(
        booking__checkin_date__lte=out_date, booking__checkout_date__gt=in_date).order_by('id').annotate(total=F('price') * dif_in_out_date.days)
        return render(
            request,
            'hotelbooking/new_booking.html', 
            {'room_types_available' : room_types_available, 'in_out_range': in_date + " - " + out_date, 'in_date': in_date, 'out_date': out_date, 'num_guests': num_guests }
        )
    except Exception as e:
        messages.error(request, str(e))
        return render(
            request,
            'hotelbooking/new_booking.html', 
            {'num_guests': num_guests}
        )

def booking_contact_data(request):
    try:
        in_out_range = request.GET['in_out_range'].split(" - ")
        in_date = in_out_range[0]
        out_date = in_out_range[1]
        datetime.strptime(in_date, '%Y-%m-%d') 
        datetime.strptime(out_date, '%Y-%m-%d') 
    except Exception as e:
        messages.error(request, str("Invalid dates"))
        return redirect(get_url_home())

    try:
        num_guests = request.GET['num_guests']
        room_type = request.GET['room_type']
        total = request.GET['total']
        room_type_instance = RoomType.objects.filter(id=room_type, max_guest__gte=num_guests).get()

        return render(
            request,
            'hotelbooking/booking_contact_data.html',
            {'in_date': in_date, 'out_date': out_date, 'num_guests': num_guests, 'room_type': room_type, 'room_type_name': room_type_instance.name, 'total': total}
        )
    except Exception as e:
        messages.error(request,  'Error: %s' % e.msg)
        return redirect(get_url_home())

def create_or_update_customer(name, email, country_code, phone):
    try:
        customer_instance = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        try:
            customer_instance = Customer(name=name, email=email, country_code=country_code, phone=phone)
            customer_instance.save()
        except  Exception as e:
            raise Exception('Error saving customer: %s' % e.msg)
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

    try:
        customer_instance = create_or_update_customer(name, email, country_code, phone)
    except Exception as e:     
        messages.error(request, e.msg)
        return redirect(get_url_home())

    try:
        room_type_instance = RoomType.objects.filter(id=room_type, max_guest__gte=num_guests).get()
    except:
        messages.error(request, 'Error with num of guests in this type of room')
        return redirect(get_url_home())        

    room = Room.objects.filter( type=room_type, is_bookable=True).exclude(booking__checkin_date__lte=out_date, booking__checkout_date__gt=in_date).order_by('num').first()
    if room:
        booking_instance = new_record_booking(num_guests, room, room_type_instance, customer_instance, in_date, out_date)
        try:
            booking_instance.save()
        except Exception as e:     
            messages.error(request, 'Error saving booking: %s' % e.msg)
            return redirect(get_url_home())
    
    else:
        booking_instance = {}
        messages.error(request, 'Booking error: Any room available')
        return redirect(get_url_home())
    
    messages.success(request, 'Booking saved')
    return redirect(get_url_home())
    
def get_url_home():
    return reverse('booking_list')

def new_record_booking(num_guests, room, room_type_instance, customer_instance, in_date, out_date):
    try:
        dif_in_out_date = dif_between_dates(in_date,out_date)
        total = dif_in_out_date.days * room_type_instance.price
        now=datetime.now()
        return Booking(
            locator = generate_hash(now.strftime("%c")+str(num_guests)+str(room.num)),
            room_type = room_type_instance,
            num_guest = num_guests,
            customer = customer_instance,
            total_price = total,
            room_num = room,
            checkin_date = in_date,
            checkout_date = out_date,
            created_date = str(now),
        )
    except Exception as e:     
        raise Exception('Error saving booking: %s' % e.msg)
