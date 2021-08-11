import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # self.room_name = self.scope['url_route']['kwargs']['room_name']
            # self.room_group_name = 'chat_%s' % self.room_name

            # print(self.room_name)
            # await self.channel_layer.group_add(
            #     'test',
            #     self.channel_name
            # )

            # await self.channel_layer.group_add(
            #     'test1',
            #     self.channel_name
            # )
            print(self.scope['user'])
            await self.accept()
            self.joined_rooms = [1]
            for room in self.joined_rooms:
                await self.channel_layer.group_add(
                    'group_' + str(room),
                    self.channel_name
                )

            
        except Exception as e:
            print('erorrr', e)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print(self.scope['url_route']['kwargs']['room_name'])
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        

        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        count=3
        print(self.scope)
        group = text_data_json['group']
        self.room_group_name = group
        print(self.channel_name)
        print(self.channel_layer,self.room_group_name)
        # await self.channel_layer.group_add(
        #         self.room_group_name,
        #         self.channel_name
        #     )
        try:
            await self.channel_layer.group_send(
                'group_' + str(group),
                {
                    'type': 'chatroom_message',
                    'message': message,
                    'username': username,
                    'id':count+1,
                    'group': group
                }
            )
            # await self.channel_layer.group_send(
            #     'test1',
            #     {
            #         'type': 'chatroom_message',
            #         'message': message,
            #         'username': username,
            #         'id':count+1,
            #         'group': 'test1'
            #     }
            # )
            
        except Exception as e:
            print(e)

    async def chatroom_message(self, event):
        # self.room_name = 'test'
        # self.room_group_name = 'chat_test'
        message = event['message']
        username = event['username']
        id = event['id']
        group = event['group']
        await self.send(text_data=json.dumps({
            'id':id,
            'message': message,
            'username': username,
            'group': group,
        }))

    pass
