from django.db import models
from authentication.models import BetaUser
from django.utils import timezone



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
    
class ChatMessages(models.Model):
    chat_group = models.ManyToManyField(ChatBase)
    user = models.ManyToManyField(BetaUser)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.timestamp) 
    
# MGCloud Integrations
class MGCloudIndex(models.Model):
    chat_room = models.ForeignKey(ChatBase, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100 )
    user_sent = models.ManyToManyField(BetaUser)
    timestamp = models.DateTimeField(default=timezone.now)
    MGCID = models.IntegerField()

    def __str__(self):
        return str(self.file_name)