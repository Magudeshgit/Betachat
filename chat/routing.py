from django.urls import re_path
from . import consumers

websocket_urlspatterns = [
    #r'ws/chat/(?P<name>\w+)/$'
    re_path(r'ChatRoom/(?P<room_id>[\w-]+)/$', consumers.ChatConsumer.as_asgi())
]