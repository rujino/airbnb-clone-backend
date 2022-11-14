from rest_framework import serializers
from .models import Perk, Experience


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
