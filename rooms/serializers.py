from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(
        read_only=True
    )  # 간단하네, 변수는 DB의 것과 같아야 한다., read_only=True는 post해서 저장할때 owner의 정보를 요구하지 않는다.
    amenities = AmenitySerializer(
        read_only=True, many=True
    )  # 리스트로 받기 때문에(여러개) many=True 넣어 줘야함
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
