import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.checks import messages
from .models import Message
from .Serializers import MessageSerialzer


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def fetch_messages(self):
        messages = Message.last_10_messages()
        serializer = MessageSerialzer(messages, many=True)
        content = {
            'messages' : serializer.data
        }
        self.send_message(content)
        pass

    async def new_message(self, data):
        message = Message.objects.create(
            to_group_id = 1,
            from_user_id = 4,
            s3_url_link = data['message'],
        )
        serializer = MessageSerialzer(message, many=True)
        content = {
            'command' : 'new_message',
            'message' : serializer.data
        }
        self.send_chat_message(content)
        pass

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }
    
    async def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            print(self.room_name)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            
        except Exception as e:
            print('erorrr', e)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # we need to send the type of command from client
        print(text_data)
        text_data_json = json.loads(text_data)
        self.commands[text_data_json['command']](self, text_data_json)

    async def send_chat_message(self, message):
        # message = text_data_json['message']
        # username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
            }
        )
    
    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chatroom_message(self, event):
        message = event['message']
        # username = event['username']
        await self.send(text_data=json.dumps({
            'message' : message,
        }))
    

    pass

