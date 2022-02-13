from django.db import models
from django.utils import timezone

class Hotel(models.Model):
    id = models.AutoField( primary_key = True )
    name = models.CharField( max_length = 100 )
    address = models.TextField( )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.name

class RoomType(models.Model):
    id = models.AutoField( primary_key = True )
    name = models.CharField( max_length = 50 )
    price = models.DecimalField( max_digits = 6, decimal_places = 2 )
    max_guest = models.PositiveSmallIntegerField( default = 1)
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.name

class Customer(models.Model):
    id = models.AutoField( primary_key = True )
    name = models.CharField( max_length = 60 )
    email = models.CharField( max_length = 100 )
    phone = models.CharField( max_length = 9 )
    country_code = models.CharField( max_length = 3 )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.name

class Room(models.Model):
    num = models.PositiveSmallIntegerField( primary_key = True )
    type = models.ForeignKey( RoomType, on_delete = models.DO_NOTHING )
    hotel = models.ForeignKey( Hotel, on_delete = models.DO_NOTHING )
    is_bookable = models.BooleanField( )
    created_date = models.DateTimeField( default=timezone.now )


    def __num__(self):
        return self.num

class Booking(models.Model):
    locator = models.CharField( primary_key = True, max_length = 10 )
    room_type = models.ForeignKey( RoomType, on_delete = models.DO_NOTHING  )
    num_guest = models.IntegerField( )
    customer = models.ForeignKey( Customer, on_delete = models.DO_NOTHING  )
    total_price = models.DecimalField( max_digits = 7, decimal_places = 2 )
    room_num = models.ForeignKey( Room, on_delete = models.DO_NOTHING  )
    checkin_date = models.DateField( )
    checkout_date = models.DateField( )
    created_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return self.locator

    def formatCheckinDate(self):
        return self.checkin_date.strftime('%d/%m/%Y')
    
    def formatCheckinOut(self):
        return self.checkout_date.strftime('%d/%m/%Y')

