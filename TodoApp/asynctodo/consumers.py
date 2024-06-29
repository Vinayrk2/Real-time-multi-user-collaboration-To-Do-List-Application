from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
import json

class TodoConsumer(WebsocketConsumer):
    @sync_to_async
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'create':
            # Handle create action
            self.create_todo(data)
        elif action == 'delete':
            # Handle delete action
            self.delete_todo(data)

    def create_todo(self, data):
        # Logic to create a new todo item
        # Example: Save data to database, then send a message back to the client
        self.send(text_data=json.dumps({
            'action': 'create',
            'id': data.get('id'),
            'text': data.get('text')
        }))

    def delete_todo(self, data):
        # Logic to delete a todo item
        # Example: Remove data from database, then send a message back to the client
        self.send(text_data=json.dumps({
            'action': 'delete',
            'id': data.get('id')
        }))