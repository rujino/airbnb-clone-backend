from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework import status
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer

# Create your views here.
class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)  # many 의미가 뭐였찌
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )  # partial=True 는 부분적으로 업데이트 하겠다는 의미
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(dir(request.user))  # 모든 view들은 request.user를 가지고있다.
        if request.user.is_authenticated:  # 이 request를 보내는 유저가 로그인 중인지 확인
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                print(request.data)
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if (
                        category.kind == Category.CategoryKindChoices.EXPERIENCES
                    ):  # 만약 유저가 보낸 카테로기가 Room카테고리가 아니라면 error 발생
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                room = serializer.save(
                    owner=request.user,
                    category=category,
                )  # serializer는 누가 room의 owner인지 모르기때문에 알려주기 위해선 적어줘야한다.
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:  # Many to Many를 코드로 구현해 보았다.
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)  # amenity는 room 에다가 직접 붙이는 군...
                    except Amenity.DoesNotExist:
                        room.delete()
                        raise ParseError(f"Amenity with id {amenity_pk} not found")
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
