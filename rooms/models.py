from django.db import models
from common.models import CommonModel

# Create your models here.
class Room(CommonModel):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(
        max_length=180,
        default="",
    )

    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )
    pet_friendly = models.BooleanField(
        default=True,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",  # User는 room_set을 받는다.
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )

    category = models.ForeignKey(
        "categories.Category",  # Category는 room_set을 받는다.
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):  # 매개변수에 꼭 self일 필요는 없다 아무 문자나 넣어도 됨
        return self.name

    def total_amenities(self):  # 매개변수에 꼭 self일 필요는 없다 아무 문자나 넣어도 됨
        print(self)
        return self.amenities.count()

    def rating(room):
        count = room.reviews.count()
        if count == 0:
            return "No Review"
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"):  # 쿼리 최적화 8.0 강의
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Amenity(CommonModel):
    """Amenity Definition"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
