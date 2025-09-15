from channels.generic.websocket import AsyncWebsocketConsumer
import json

# class NotificationConsumer(AsyncWebsocketConsumer):
#     print("goooooo")
#     async def connect(self):
#         self.user = self.scope["user"]
#         if self.user.is_authenticated:
#             self.group_name = f"user_{self.user.id}"
#             await self.channel_layer.group_add(self.group_name, self.channel_name)
#             await self.accept()
#         else:
#             await self.close()

#     async def disconnect(self, close_code):
#         if hasattr(self, "group_name"):
#             await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def notify(self, event):
#         await self.send(text_data=json.dumps(event["content"]))



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")

        if self.user and self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"✅ WebSocket connected: user {self.user.id}")
        else:
            print("❌ WebSocket connection rejected (unauthenticated)")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(f"🔌 WebSocket disconnected: user {self.user.id}")

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["content"]))





















# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Accept all connections for testing
#         await self.accept()
#         print(f"WebSocket connected: {self.channel_name}")

#         # Optionally, add to a test group
#         self.group_name = "test_group"
#         await self.channel_layer.group_add(self.group_name, self.channel_name)


# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Accept all connections for testing
#         await self.accept()
#         print(f"WebSocket connected: {self.channel_name}")

#     async def disconnect(self, close_code):
#         print(f"WebSocket disconnected: {self.channel_name}")

#     async def notify(self, event):
#         await self.send(text_data=json.dumps(event["content"]))

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         print("WS connected")

#         # Send a test message immediately
#         await self.send(text_data=json.dumps({
#             "message": "Hello from Django Channels!"
#         }))
    # async def connect(self):
    #     await self.accept()
    #     print(f"WebSocket connected: {self.channel_name}")


