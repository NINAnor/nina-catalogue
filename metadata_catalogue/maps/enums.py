from django.db import models


class Visibility(models.TextChoices):
    PUBLIC = "public", "Public"
    PRIVATE = "private", "Private"
