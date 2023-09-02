from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatBase
from asgiref.sync import sync_to_async
import  json
import random

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = self.room_id
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'status' : '102'
        }))
        
    async def process_groups(self):
        chatrooms = await sync_to_async(ChatBase.objects.all)()
        DUPLICATION = False
        async for room in chatrooms:
            if room.unique_id == self.room_id:
                DUPLICATION = True 
                print(DUPLICATION, room.unique_id, self.room_id)
        if DUPLICATION is False:  
            chatbase = await sync_to_async(ChatBase.objects.create)(
                #unique_id=uid[:3]+'-'+uid[3:6]+'-'+uid[6:9],
                group_name=self.room_group_name,
                group_admin=self.scope['user']
                )
            await sync_to_async(chatbase.Users.set)([self.scope['user'].id])
            print('ChatBase created')


    async def send_to_group(self, group_name, message):
        await self.channel_layer.group_send(group_name, 
                                            {
                                                'type': 'group_message',
                                                'message': message
                                            })
    async def group_message(self, event):
        message=event['message']
        await self.send(text_data=json.dumps({
            'type':'chatmsg',
            'username': data['USER'],
            'message':message
        }))


    async def receive(self, text_data):
        global data
        data=json.loads(text_data)
        print('raw', text_data)
        print('grp: ', self.room_group_name)
        await self.send_to_group(self.room_group_name, data['MESSAGE'])
        