from django.urls import re_path
from .consumers import NotificationConsumer



print("WebSocket routing loaded")
websocket_urlpatterns = [
    re_path(r"ws/notification/$", NotificationConsumer.as_asgi()),
]