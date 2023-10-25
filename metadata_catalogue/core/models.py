from django.db import models


class OrmQExtension(models.Model):
    """Extends OrmQ with a name field"""

    orm_q = models.OneToOneField("django_q.OrmQ", on_delete=models.CASCADE, related_name="extension")
    name = models.CharField("name", max_length=255)

    def __str__(self):
        return self.name
