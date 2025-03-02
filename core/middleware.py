import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

User = get_user_model()


class WebSocketJWTAuthMiddleware(BaseMiddleware):
    """Custom middleware to authenticate WebSocket connections using JWT."""

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])

        # Extract the Authorization header
        auth_header = headers.get(b"authorization", None)

        if auth_header:
            token = auth_header.decode("utf-8").split("Bearer ")[-1]
            user = await self.get_user(token)
            if user:
                scope["user"] = user  # Attach the user to the scope

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["userId"])
            return user
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return None  # Invalid token, return anonymous user
