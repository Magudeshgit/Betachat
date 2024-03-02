from django.contrib import admin
from .models import ChatBase, ChatMessages, MGCloudIndex
# Register your models here.

admin.site.register(ChatBase)
admin.site.register(ChatMessages)
admin.site.register(MGCloudIndex)