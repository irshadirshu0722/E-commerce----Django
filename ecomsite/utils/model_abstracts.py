import uuid
from django.db import models


class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True

class TotalQuantity(models.Model):
    total = models.FloatField(null=True,default=0.0)
    quantity = models.IntegerField(null=True,default=0)
    class Meta:
        abstract = True