from django.contrib import admin
from .models import Hotel, RoomType, Room, Customer, Booking

myModels = [Hotel, RoomType, Room, Customer, Booking]
admin.site.register(myModels)