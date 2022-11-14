from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(
    serializers.ModelSerializer
):  # 유저에게 받는 데이터 생성용 serializer
    check_in = serializers.DateField()  # 필수가 아니었던 데이터를 필수로 하기위해 오버라이드
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("nono!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("nono!")
        return value

    """chaeckout이 checkin보다 많아야함"""

    def validate(self, data):
        print(data)
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "check in should be smaller than check out"
            )

        if Booking.objects.filter(
            check_in__lte=data["check_out"], check_out__gte=data["check_in"]
        ).exists():
            raise serializers.ValidationError("already booking exists")
        return data

    """in과 out사이에 다른 booking이 있는지 확인"""


class CreateExperienceBookingSerializer(
    serializers.ModelSerializer
):  # 유저에게 받는 데이터 생성용 serializer
    experience_time = serializers.DateTimeField()  # 필수 필드

    class Meta:
        model = Booking
        fields = (
            "experience",
            "experience_time",
            "guests",
        )


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "room",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class PublicExperienceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience",
            "experience_time",
            "guests",
        )
