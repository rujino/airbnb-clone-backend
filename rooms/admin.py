from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all prices to zero")
def reset_prices(
    model_admin,
    request,
    rooms,
):  # action은 3개의 매개변수가 필요하다. ==> model_admin(여기에선 RoomAdmin), request(액션을 요청하는 user에 대한 정보를 가짐), queryset(관리자창에서 선택한 체크박스 요소들, 아무 arg넣어도됨)
    for room in rooms.all():
        print(f"room: {room}")
        room.price = 0
        room.save()


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )

    search_fields = ("owner__username",)  # 검색창 만들어짐  # user에서 username을 검색 ##중요##

    """
    search_fields = () 에서 더 다양한 검색 패턴
    ^name: ^는 startwith랑 같은 의미 name으로 시작하는 것을 검색
    =name: =는 exact의 의미
    name: 아무것도 없을땐 contains의 의미
    """

    # def total_amenities(self, room):   매개변수에 꼭 self일 필요는 없다 아무 문자나 넣어도 됨
    #     print(room.amenities.all())
    #     return room.amenities.count()

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
        "category",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
