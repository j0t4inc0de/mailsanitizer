"""
Custom JWT authentication backend — CleanMail by Samod.

Provides:
  - ``generate_jwt(user)`` — creates a signed JWT for a User instance.
  - ``decode_jwt(token)`` — decodes and validates a JWT, returning claims.
  - ``JWTAuthentication`` — DRF authentication class that reads the
    ``Authorization: Bearer <token>`` header and resolves the user.
"""

import logging
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from core.models import User

logger = logging.getLogger(__name__)


def generate_jwt(user: User) -> str:
    """
    Generate a signed JWT for the given user.

    The token embeds the user's UUID and email and expires after
    ``settings.JWT_EXPIRATION_HOURS`` hours.

    Args:
        user: A ``core.models.User`` instance.

    Returns:
        The encoded JWT string.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "iat": now,
        "exp": now + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Args:
        token: The encoded JWT string.

    Returns:
        The decoded claims dictionary.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is malformed or tampered.
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])


class JWTAuthentication(BaseAuthentication):
    """
    DRF authentication class that extracts a JWT from the
    ``Authorization: Bearer <token>`` header and resolves the
    corresponding ``core.models.User``.
    """

    keyword = "Bearer"

    def authenticate(self, request):
        """
        Attempt to authenticate the request using a Bearer JWT.

        Returns:
            ``(user, decoded_payload)`` on success, or ``None`` when
            no Authorization header is present.

        Raises:
            AuthenticationFailed: When the token is present but invalid.
        """
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token = parts[1]

        try:
            payload = decode_jwt(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("El token ha expirado. Inicie sesión de nuevo.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token inválido.")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationFailed("Token inválido: falta el ID de usuario.")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("Usuario no encontrado.")

        return (user, payload)

    def authenticate_header(self, request):
        """Return the WWW-Authenticate header value for 401 responses."""
        return self.keyword
