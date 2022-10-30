from django.db import models
from common.models import CommonModel

# Create your models here.
class Review(CommonModel):
    """Review from a User to Room or Experience"""

    user = models.ForeignKey(
        "users.User",  # 해석 Review모델은 user를 포인팅하고 있는 ForeignKey를 가지고 있다. -> # User는 review_set을 받는다.
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        related_name="reviews",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        related_name="reviews",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}"
