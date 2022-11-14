from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializers import RoomListSerializer


class WishlistsSerializer(ModelSerializer):

    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
