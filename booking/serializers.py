from django.contrib.auth.models import User
from .models import Room, Booking
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BookingSerializer(serializers.Serializer):
    room_name = serializers.CharField(max_length=30)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    def create(self, validated_data):
        room_name = validated_data['room_name']
        start = validated_data['checking_date']
        end = validated_data['checkout_date']
        room = Room.objects.get(title=room_name)

        booking = Booking.objects.create(
            room=room,
            customer=self.context['request'].user,
            checking_date=start,
            checkout_date=end
        )
        return booking


class SingUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=55)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password']



