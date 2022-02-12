from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('new_booking', views.new_booking, name='new_booking'),
    path('authenticate_user', views.authenticate_user, name='authenticate_user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('get_room_types_available', views.get_room_types_available, name='get_room_types_available'),

]

