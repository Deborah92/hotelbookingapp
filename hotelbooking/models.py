from django.db import models
from django.utils import timezone

class Hotel(models.Model):
    id = models.AutoField( primary_key = True )
    name = models.TextField( max_length = 100 )
    address = models.TextField( )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.name

class RoomType(models.Model):
    id = models.AutoField( primary_key = True )
    name = models.TextField( max_length = 50 )
    price = models.DecimalField( max_digits = 6, decimal_places = 2 )
    max_guest = models.PositiveSmallIntegerField( default = 1)
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.name

class Customer(models.Model):
    id = models.AutoField( primary_key = True )
    name = models.TextField( max_length = 60 )
    email = models.TextField( max_length = 100 )
    phone = models.TextField( max_length = 9 )
    country_code = models.TextField( max_length = 3 )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.name

class Room(models.Model):
    num = models.PositiveSmallIntegerField( primary_key = True )
    type = models.ForeignKey( RoomType, on_delete = models.DO_NOTHING )
    hotel = models.ForeignKey( Hotel, on_delete = models.DO_NOTHING )
    is_bookable = models.BooleanField( )
    created_date = models.DateTimeField( default=timezone.now )


    def __str__(self):
        return self.num

class Booking(models.Model):
    localizador = models.IntegerField( primary_key = True )
    room_type = models.ForeignKey( RoomType, on_delete = models.DO_NOTHING  )
    num_guest = models.IntegerField( )
    customer = models.ForeignKey( Customer, on_delete = models.DO_NOTHING  )
    total_price = models.DecimalField( max_digits = 7, decimal_places = 2 )
    room_num = models.ForeignKey( Room, on_delete = models.DO_NOTHING  )
    checkin_date = models.DateTimeField( )
    checkout_date = models.DateTimeField( )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.id

