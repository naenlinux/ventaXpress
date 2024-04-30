from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ProductoConsumer(WebsocketConsumer):
    def connect(self):
        # Aquí puedes implementar lógica de conexión si es necesario
        #print('conexion exitosa WS desde almaceb')
        
        self.room_name = 'productos'
        self.room_group_name = f"productos_{self.room_name}"
        
           # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Aquí puedes implementar lógica de desconexión si es necesario
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

     # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))