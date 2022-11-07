from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:  # create 메소드와 update 메소드도 자동으로 만듬
        model = Category
        # exclude = ("created_at",)  # create_at 제외하고 보여주기

        # fields = "__all__"     # 전부 보여주기
        fields = (
            "name",
            "kind",
        )
