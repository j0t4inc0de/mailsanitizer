"""
Payment service — CleanMail by Samod.

Handles LemonSqueezy webhook signature verification and credit provisioning
based on product variant IDs.
"""

import hashlib
import hmac
import logging

from django.conf import settings

from core.models import CreditTransaction, User

logger = logging.getLogger(__name__)


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
