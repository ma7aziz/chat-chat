import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatMessage
import datetime
# Set up logging
logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # Send the last 50 messages to the user upon connection
        last_50_messages = ChatMessage.objects.filter(room_name=self.room_name).order_by('-timestamp')[:50]
        for message in reversed(last_50_messages):
            self.send(text_data=json.dumps({
                'username': message.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        username = text_data_json.get("username", "Anonymous")
        timestamp = text_data_json.get('timestamp')

        # Save the message to the database
        chat_message = ChatMessage(room_name=self.room_name, username=username, message=message )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "username": username , "timestamp":timestamp
            }
        )

    def chat_message(self, event):
        print('EVENT:' , event)
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        self.send(text_data=json.dumps({
            "username": username,
            "message": message ,
            "timestamp" : timestamp
            
        }))
