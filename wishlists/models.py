from django.db import models
from common.models import CommonModel

# Create your models here.
class Wishlist(CommonModel):
    """Wishlist Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wishlists",
        null=True,
        blank=True,
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlists",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    def __str__(self) -> str:
        return self.name
