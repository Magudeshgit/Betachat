from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatBase, ChatMessages
from authentication.models import BetaUser
from asgiref.sync import sync_to_async
import  json
import random

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_unique_id = self.scope['url_route']['kwargs']['room_id']
        self.room_id = await sync_to_async(ChatBase.objects.get)(unique_id=self.room_unique_id)
        self.room_id=self.room_id.id
        self.room_group_name = self.room_unique_id
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'status' : '102'
        }))

    async def send_to_group(self, group_name, message):
        await self.channel_layer.group_send(group_name, 
                                            {
                                                'type': 'group_message',
                                                'message': message
                                            })
    async def group_message(self, event):
        aa = await sync_to_async(ChatBase.objects.get)(id=self.room_id)
        bb= await sync_to_async(BetaUser.objects.get)(id=self.scope['user'].id)

        message=event['message']
        Chatmessage = await sync_to_async(ChatMessages.objects.create)(content = message['data'])
        await sync_to_async(Chatmessage.chat_group.set)([aa])         
        await sync_to_async(Chatmessage.user.set)([bb])    
    
        await self.send(text_data=json.dumps({
            'type':'chatmsg',
            'username': data['USER'],
            'message':message
        }))
    



    async def receive(self, text_data):
        global data
        data=json.loads(text_data)
        #print(data)
        await self.send_to_group(self.room_group_name, data['MESSAGE'])
        