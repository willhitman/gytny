import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

User = get_user_model()

import logging
logger = logging.getLogger(__name__)

class WebSocketJWTAuthMiddleware(BaseMiddleware):
    """Custom middleware to authenticate WebSocket connections using JWT."""

    async def __call__(self, scope, receive, send):
        # Ensure old database connections are closed
        close_old_connections()

        headers = dict(scope.get("headers", []))

        # Extract the Authorization header if present
        auth_header = headers.get(b"authorization", None)

        if auth_header:
            # Extract token from 'Bearer <token>'
            token = auth_header.decode("utf-8").split("Bearer ")[-1]
            logger.info(f"Extracted token: {token}")  # Log the token

            if token:
                user = await self.get_user(token)
                if user:
                    scope["user"] = user  # Attach the user to the scope
                    logger.info(f"Authenticated user: {user}")
                else:
                    logger.warning("Invalid token or user not found")
            else:
                logger.warning("No authorization header found")

        # Continue to the next middleware in the stack
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            # Decode the JWT token and retrieve the user from the payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["userId"])
            return user
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return None  # Invalid token, return anonymous user
