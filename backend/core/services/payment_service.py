"""
Payment service — CleanMail by Samod.

Handles webhook signature verification and credit provisioning for two
payment providers:

- **LemonSqueezy** — HMAC-SHA256 over raw body, ``order_created`` event.
- **Paddle** — HMAC-SHA256 over raw body, ``transaction.completed`` event.
"""

import hashlib
import hmac
import logging

from django.conf import settings

from core.models import CreditTransaction, User

logger = logging.getLogger(__name__)


# =============================================================================
# LemonSqueezy
# =============================================================================

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify the HMAC-SHA256 signature of a LemonSqueezy webhook payload.

    Args:
        payload: Raw request body bytes.
        signature: The ``X-Signature`` header value from the webhook.
        secret: The webhook signing secret.

    Returns:
        ``True`` when the computed digest matches the provided signature.
    """
    if not signature or not secret:
        return False

    expected = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


def process_payment_event(event_data: dict) -> None:
    """
    Process a LemonSqueezy ``order_created`` event.

    Looks up the product variant ID from the event payload, maps it to
    a credit amount using the settings mapping, finds or creates the
    user by email, and credits their account.

    Args:
        event_data: The parsed JSON body of the webhook event.

    Raises:
        ValueError: If the variant is unknown or the user email is missing.
    """
    variant_credits = settings.LEMONSQUEEZY_VARIANT_CREDITS

    # Extract relevant fields from the LemonSqueezy event
    meta = event_data.get("meta", {})
    event_name = meta.get("event_name", "")

    attributes = event_data.get("data", {}).get("attributes", {})
    user_email = attributes.get("user_email", "").strip().lower()
    user_name = attributes.get("user_name", "")

    # Get the first line item's variant ID
    first_item = (attributes.get("first_order_item", {}) or {})
    variant_id = str(first_item.get("variant_id", ""))

    if not user_email:
        logger.error(
            "Webhook de pago sin correo de usuario. Evento: %s", event_name
        )
        raise ValueError("Correo de usuario no proporcionado en el evento de pago.")

    credits_to_add = variant_credits.get(variant_id)
    if credits_to_add is None:
        logger.warning(
            "Variante desconocida '%s' en evento de pago para %s.",
            variant_id,
            user_email,
        )
        raise ValueError(
            f"Variante de producto desconocida: {variant_id}"
        )

    # Find or create the user
    user, created = User.objects.get_or_create(
        email=user_email,
        defaults={"nombre": user_name or None},
    )

    if created:
        logger.info("Usuario creado automáticamente por pago: %s", user_email)

    # Credit the user's account
    user.creditos += credits_to_add
    user.save(update_fields=["creditos"])

    # Record the transaction
    order_id = event_data.get("data", {}).get("id", "")
    CreditTransaction.objects.create(
        usuario=user,
        tipo="compra",
        cantidad=credits_to_add,
        referencia=f"lemonsqueezy:order:{order_id}",
        descripcion=f"Compra de {credits_to_add} créditos (variante {variant_id})",
    )

    logger.info(
        "Acreditados %d créditos al usuario %s (pedido %s).",
        credits_to_add,
        user_email,
        order_id,
    )


# =============================================================================
# Paddle
# =============================================================================

def verify_paddle_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    """
    Verify the HMAC-SHA256 signature of a Paddle webhook notification.

    Paddle sends the signature in the ``Paddle-Signature`` header using the
    format ``ts=<timestamp>;h1=<hex_digest>``. We verify by computing
    HMAC-SHA256 over ``ts:<timestamp>:<raw_body>`` with the secret key.

    Args:
        payload: Raw request body bytes.
        signature_header: The full ``Paddle-Signature`` header value.
        secret: The Paddle webhook secret key.

    Returns:
        ``True`` when the computed digest matches the ``h1`` component.
    """
    if not signature_header or not secret:
        return False

    # Parse header: "ts=1234567890;h1=abc123..."
    parts = dict(part.split("=", 1) for part in signature_header.split(";") if "=" in part)
    ts = parts.get("ts", "")
    h1 = parts.get("h1", "")

    if not ts or not h1:
        return False

    signed_payload = f"{ts}:{payload.decode('utf-8', errors='replace')}".encode("utf-8")
    expected = hmac.new(
        key=secret.encode("utf-8"),
        msg=signed_payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, h1)


def process_paddle_event(event_data: dict) -> None:
    """
    Process a Paddle ``transaction.completed`` event.

    Extracts the customer email and the price ID from the first line item,
    maps it to a credit amount, and credits the user's account.

    Paddle v2 payload structure (simplified)::

        {
          "event_type": "transaction.completed",
          "data": {
            "id": "txn_xxx",
            "customer": {"email": "user@example.com"},
            "items": [
              {"price": {"id": "pri_xxx"}}
            ]
          }
        }

    Args:
        event_data: The parsed JSON body of the Paddle webhook event.

    Raises:
        ValueError: If the price ID is unknown or the user email is missing.
    """
    price_credits = settings.PADDLE_PRICE_CREDITS

    event_type = event_data.get("event_type", "")
    data = event_data.get("data", {})

    # Extract customer email
    customer = data.get("customer", {})
    user_email = customer.get("email", "").strip().lower()

    if not user_email:
        logger.error("Paddle webhook sin correo de usuario. Evento: %s", event_type)
        raise ValueError("Correo de usuario no proporcionado en el evento de Paddle.")

    # Extract price ID from first line item
    items = data.get("items", [])
    price_id = ""
    if items:
        price_id = str(items[0].get("price", {}).get("id", ""))

    credits_to_add = price_credits.get(price_id)
    if credits_to_add is None:
        logger.warning(
            "Price ID desconocido '%s' en evento Paddle para %s.",
            price_id,
            user_email,
        )
        raise ValueError(f"Price ID de Paddle desconocido: {price_id}")

    # Find or create the user
    user, created = User.objects.get_or_create(
        email=user_email,
        defaults={},
    )

    if created:
        logger.info("Usuario creado automáticamente por pago Paddle: %s", user_email)

    # Credit the user's account
    user.creditos += credits_to_add
    user.save(update_fields=["creditos"])

    # Record the transaction
    transaction_id = data.get("id", "")
    CreditTransaction.objects.create(
        usuario=user,
        tipo="compra",
        cantidad=credits_to_add,
        referencia=f"paddle:transaction:{transaction_id}",
        descripcion=f"Compra de {credits_to_add} créditos vía Paddle (price {price_id})",
    )

    logger.info(
        "Acreditados %d créditos al usuario %s (transacción Paddle %s).",
        credits_to_add,
        user_email,
        transaction_id,
    )
