from django.urls import path

from .views import RoomView, BookingApiView, RoomDetailView, SignUp

urlpatterns = [
    path('rooms/', RoomView.as_view(), name='RoomView'),
    path('book/room/', BookingApiView.as_view(), name='BookingCreateApiView'),
    path('room/<str:room_name>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('signup/', SignUp.as_view(), name='signup'),
]

