import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from channels.db import database_sync_to_async

User = get_user_model()

class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'websocket':
            query_string = scope.get("query_string", b"").decode()
            params = parse_qs(query_string)
            token = params.get("token", [None])[0]

            scope["user"] = AnonymousUser()
            if token:
                try:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                    user_id = payload.get("user_id")
                    scope["user"] = await self.get_user(user_id)
                except Exception as e:
                    print("JWT decode error:", e)

        return await self.app(scope, receive, send)

    @staticmethod
    @database_sync_to_async
    def get_user(user_id):
        from django.contrib.auth.models import AnonymousUser
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
