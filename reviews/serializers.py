from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer(read_only=True)  # read_only를 해야 is_valid가 유효해진다.

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )
