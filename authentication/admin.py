from django.contrib import admin
from django.contrib.auth.models import Group
from .models import BetaUser
from django.contrib.sessions.models import Session
# Register your models here.

admin.site.unregister(Group)

admin.site.register(BetaUser)
admin.site.register(Session)
