from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Perk, Experience
from bookings.models import Booking
from .serializer import PerkSerializer, ExperienceSerializer
from bookings.serializers import (
    CreateExperienceBookingSerializer,
    PublicExperienceBookingSerializer,
    PublicExperienceBookingSerializer,
)


# Create your views here.
class Perks(APIView):
    def get(self, request):
        perks = Perk.objects.all()
        serializer = PerkSerializer(perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_objects(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_objects(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_objects(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_objects(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):
    def get(self, request):
        all_experience = Experience.objects.all()
        serializer = ExperienceSerializer(all_experience, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            experience = serializer.save()
            serializer = ExperienceSerializer(experience)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperiencesDetail(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            if request.user != experience.host:
                raise PermissionDenied
            experience = serializer.save(host=request.user)
            serializer = ExperienceSerializer(experience)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencesPerksDetail(APIView):
    def get(self, request, pk):
        experience = Experience.objects.get(pk=pk)
        perks = experience.perks
        serializer = PerkSerializer(perks, many=True)
        return Response(serializer.data)


class ExperienceBookings(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        booking = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
        )
        serializer = PublicExperienceBookingSerializer(
            booking,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if request.uesr == experience.host:
            raise PermissionDenied
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicExperienceBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
