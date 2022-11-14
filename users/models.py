from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("ko", "KOREAN")
        EN = ("en", "ENGLISH")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korean Won")
        USD = ("usd", "Dollar")

    first_name = models.CharField(
        max_length=150,
        editable=False,
        null=True,
        blank=True,
        default="",
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
        null=True,
        blank=True,
        default="",
    )
    avator = models.URLField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
