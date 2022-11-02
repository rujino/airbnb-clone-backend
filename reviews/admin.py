from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),  # 튜플의 첫번째는 url에 표시될 arg 두번째는 관리자창에서 보이는 arg
            ("greate", "Great"),
            ("awsome", "Awsome"),
        ]

    def queryset(self, request, queryset):  # queryset은 당연히 Review의 쿼리셋이겠지??
        print(request.GET)  # request.GET으로 url을 직접 읽는것도 가능하지만
        word = self.value()  # django는 url을 직접 읽지 않고도 할 수 있는 숏컷을 준비해둠
        print(self.value())
        if word:
            return queryset.filter(
                payload__contains=word
            )  # 관리자 필터를 선택하지 않으면 value가 none이라 오류를 냄
        else:
            queryset


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
