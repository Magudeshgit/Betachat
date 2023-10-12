from django.db import models
from authentication.models import BetaUser

# Create your models here.


class ChatBase(models.Model):
    unique_id = models.CharField(max_length=40, unique=True)
    group_name = models.CharField(max_length=30)
    Users = models.ManyToManyField(BetaUser, related_name="rel_users")
    keyword=models.CharField(max_length=200)
    group_admin = models.ForeignKey(BetaUser, related_name='gadmin', on_delete=models.CASCADE)
    group_description = models.CharField(max_length=50)
    group_PIN = models.CharField(max_length=8)

    def __str__(self):
        return self.group_name
