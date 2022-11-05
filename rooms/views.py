from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "hello! this title comes from django",
        },
    )


def see_one_room(request, room_pk):  # 두번째 파라미터는 rooms.urls 의 그것과 같아야 한다.
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
