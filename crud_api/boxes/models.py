from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import OneToOneField
from users.models import User

# Create your models here.
class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()

    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "boxes"

class BoxLimits(models.Model):
    A1 = models.FloatField(default=100.0)
    V1 = models.FloatField(default=1000.0)
    L1 = models.FloatField(default=100.0)
    L2 = models.FloatField(default=50.0)

    class Meta:
        db_table = "limits"