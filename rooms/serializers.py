from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


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
        read_only=True,
        many=True,
    )  # 리스트로 받기 때문에(여러개) many=True 넣어 줘야함
    category = CategorySerializer(
        read_only=True,
    )

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )  # related_name="photos" 이것 때문에 photo라고 이름을 주면 안되는 건가????
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )  # reverse serializer에 의해 가능 roo.reviews <= 이것이 가능하기에 때문에 "자동"으로 가능

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):  # 항상 get_에 계산하려는 속성의 이름을 붙여야함
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user  # True, False 반환


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )  # 필드에 추가해 줘야 작동

    def get_rating(self, room):  # 항상 get_에 계산하려는 속성의 이름을 붙여야함
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
