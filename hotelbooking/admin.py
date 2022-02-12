from django.contrib import admin
from .models import Hotel, RoomType, Room, Customer, Booking

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Customer)
admin.site.register(Booking)