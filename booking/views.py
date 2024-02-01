from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User

from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer, SingUpSerializer


# Create your views here.
class RoomView(ListAPIView):
    def get(self, request, *args, **kwargs):
        today = now()

        room = Room.objects.all()
        available_rooms = room.filter(is_booked=False)
        reserved_rooms = room.filter(is_booked=True)
        serializer_available = RoomSerializer(available_rooms, many=True)
        serializer_reserved = RoomSerializer(reserved_rooms, many=True)

        response = {
            "available": serializer_available.data,
            "reserved": serializer_reserved.data,
            "date": today,
        }

        return Response(response, status=status.HTTP_200_OK)


class RoomDetailView(APIView):
    def get(self, request, room_name):
        room = Room.objects.get(title=room_name)
        is_free = not room.is_booked

        return Response({
            "room": room.id,
            "room_name": room_name,
            "is_free": is_free,
            "description": room.description
        }, status=status.HTTP_200_OK)


class BookingApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data, context={'request': request})

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication qilishingiz kerak bolmasa dastur ishlamaydi!'}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            room_name = serializer.validated_data['room_name']
            start = serializer.validated_data['start']
            end = serializer.validated_data['end']

            try:
                room = Room.objects.get(title=room_name)
            except Room.DoesNotExist:
                return Response({
                    "message": f"{room_name} honasi topilmadi yoki mavjud emas xona nomi kiritildi!",
                }, status=status.HTTP_404_NOT_FOUND)

            if room.is_booked:
                available_from = end
                return Response({
                    "message": f"{room_name} honasi allaqachon boshqa bir mijoz tomonidan band qilingan!",
                    "available_from": available_from,
                }, status=status.HTTP_409_CONFLICT)

            else:
                room.is_booked = True
                room.save()
                Booking.objects.create(
                    room=room,
                    customer=request.user,
                    checking_date=start,
                    checkout_date=end
                )

                return Response({
                    'message': 'Booking successful for you',
                    'room': room.capacity,
                    'room_name': room.title,
                    'start': start,
                    'end': end
                }, status=status.HTTP_201_CREATED)


class SignUp(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SingUpSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        username = User.objects.get(username=request.data['username'])

        return Response({
            'message': f"{username}, Siz ro'yxat dan muvaffaqiyatli otdingiz! Endi Login qilib token oling."
        })







