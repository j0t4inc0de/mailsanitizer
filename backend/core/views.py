"""
API views — CleanMail by Samod.

All endpoint logic for authentication (magic links + JWT), email validation
(single & bulk CSV), task management, credits, and webhooks.
"""

import csv
import io
import logging
import secrets
import time
import threading
from datetime import datetime, timedelta, timezone

import redis
import requests as http_requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.auth_backend import generate_jwt
from core.models import CreditTransaction, EmailResult, User, ValidationTask
from core.serializers import (
    CreditTransactionSerializer,
    MagicLinkRequestSerializer,
    MagicLinkVerifySerializer,
    SingleValidateSerializer,
    UserSerializer,
    ValidationTaskSerializer,
)
from core.services.payment_service import process_payment_event, verify_webhook_signature
from core.validators import validate_email

logger = logging.getLogger(__name__)


# =============================================================================
# In-memory rate limiter for single validation (per IP, 30/min)
# =============================================================================

_rate_lock = threading.Lock()
_rate_store: dict[str, list[float]] = {}  # ip → [timestamps]
_RATE_LIMIT = 30
_RATE_WINDOW = 60  # seconds


def _check_rate_limit(ip: str) -> bool:
    """
    Return ``True`` if the IP is within the rate limit, ``False`` otherwise.

    Cleans up stale entries on each call.
    """
    now = time.time()
    with _rate_lock:
        timestamps = _rate_store.get(ip, [])
        # Prune old entries
        timestamps = [t for t in timestamps if now - t < _RATE_WINDOW]
        if len(timestamps) >= _RATE_LIMIT:
            _rate_store[ip] = timestamps
            return False
        timestamps.append(now)
        _rate_store[ip] = timestamps
        return True


def _get_client_ip(request) -> str:
    """Extract the client IP from the request, respecting X-Forwarded-For."""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


# =============================================================================
# Redis helper
# =============================================================================

def _get_redis():
    """Return a Redis client using the configured URL."""
    return redis.from_url(settings.REDIS_URL)


# =============================================================================
# Auth views
# =============================================================================


class MagicLinkRequestView(APIView):
    """
    POST /api/auth/magic-link/

    Creates a magic token, saves it to the user (creating the user if it
    doesn't exist), and calls the n8n webhook to send the magic link email.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = MagicLinkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip().lower()
        nombre = serializer.validated_data.get("nombre", "").strip() or None

        # Find or create the user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"nombre": nombre},
        )

        # Update nombre if provided and user already existed
        if not created and nombre and not user.nombre:
            user.nombre = nombre

        # Generate a secure magic token (64-char hex)
        token = secrets.token_hex(32)
        user.magic_token = token
        user.magic_token_exp = datetime.now(timezone.utc) + timedelta(minutes=15)
        user.save(update_fields=["magic_token", "magic_token_exp", "nombre"])

        # Build the magic link URL
        magic_link = f"{settings.FRONTEND_URL}/auth/verify?token={token}"

        # Call n8n webhook to send the email
        webhook_url = settings.N8N_MAGIC_LINK_WEBHOOK
        if webhook_url:
            try:
                http_requests.post(
                    webhook_url,
                    json={
                        "email": email,
                        "magic_link": magic_link,
                        "nombre": user.nombre or "",
                    },
                    timeout=10,
                )
            except http_requests.RequestException:
                logger.exception(
                    "Error al enviar magic link vía n8n para %s", email
                )
        else:
            logger.warning(
                "N8N_MAGIC_LINK_WEBHOOK no configurado. Token para %s: %s",
                email,
                token,
            )

        return Response(
            {"mensaje": "Enlace mágico enviado. Revisa tu correo electrónico."},
            status=status.HTTP_200_OK,
        )


class MagicLinkVerifyView(APIView):
    """
    POST /api/auth/verify/

    Verifies the magic token and returns a JWT if valid.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = MagicLinkVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]

        try:
            user = User.objects.get(magic_token=token)
        except User.DoesNotExist:
            return Response(
                {"error": True, "detalle": "Token inválido o ya utilizado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check expiration
        if user.magic_token_exp is None or user.magic_token_exp < datetime.now(timezone.utc):
            return Response(
                {"error": True, "detalle": "El token ha expirado. Solicita uno nuevo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Invalidate the magic token (single-use)
        user.magic_token = None
        user.magic_token_exp = None
        user.last_login = datetime.now(timezone.utc)
        user.save(update_fields=["magic_token", "magic_token_exp", "last_login"])

        # Generate JWT
        jwt_token = generate_jwt(user)

        return Response(
            {
                "token": jwt_token,
                "usuario": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class UserMeView(APIView):
    """
    GET /api/auth/me/

    Returns the authenticated user's profile and credit balance.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# =============================================================================
# Validation views
# =============================================================================


class SingleValidateView(APIView):
    """
    POST /api/validate/single/

    Validates a single email address. No authentication required.
    Rate limited to 30 requests per minute per IP.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        # Rate limiting
        client_ip = _get_client_ip(request)
        if not _check_rate_limit(client_ip):
            return Response(
                {
                    "error": True,
                    "detalle": "Límite de solicitudes excedido. Máximo 30 por minuto.",
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = SingleValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        result = validate_email(email)

        return Response(
            {
                "correo": email.strip().lower(),
                "estado": result["estado"],
                "motivo": result["motivo"],
            },
            status=status.HTTP_200_OK,
        )


class UploadCSVView(APIView):
    """
    POST /api/validate/upload/

    Accepts a CSV file, creates a ValidationTask, stores the raw emails
    as EmailResult rows (with empty estado), and enqueues the task to
    Redis for background processing.

    If this is the user's first task and the file contains ≤500 emails,
    the task is marked as ``es_gratuita=True``.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response(
                {"error": True, "detalle": "No se proporcionó ningún archivo CSV."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Size check (10 MB)
        if csv_file.size > 10 * 1024 * 1024:
            return Response(
                {"error": True, "detalle": "El archivo excede el límite de 10 MB."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse CSV
        try:
            decoded = csv_file.read().decode("utf-8", errors="replace")
        except Exception:
            return Response(
                {"error": True, "detalle": "No se pudo leer el archivo. Asegúrate de que sea UTF-8."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        emails = self._extract_emails(decoded)

        if not emails:
            return Response(
                {"error": True, "detalle": "No se encontraron correos electrónicos en el archivo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Determine if this is the user's first task and ≤500 emails
        user = request.user
        is_first_task = not ValidationTask.objects.filter(usuario=user).exists()
        es_gratuita = is_first_task and len(emails) <= 500

        # Create the task
        task = ValidationTask.objects.create(
            usuario=user,
            nombre_archivo=csv_file.name or "archivo.csv",
            total_correos=len(emails),
            es_gratuita=es_gratuita,
        )

        # Bulk-create EmailResult rows with 'pendiente' estado
        email_results = [
            EmailResult(tarea=task, correo=email, estado='pendiente')
            for email in emails
        ]
        EmailResult.objects.bulk_create(email_results, batch_size=1000)

        # Enqueue to Redis
        try:
            r = _get_redis()
            r.lpush("cleanmail:tasks", str(task.id))
        except Exception:
            logger.exception("Error al encolar tarea %s en Redis", task.id)
            task.estado = "error"
            task.save(update_fields=["estado"])
            return Response(
                {"error": True, "detalle": "Error interno al encolar la tarea. Intenta de nuevo."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "mensaje": "Archivo recibido. La validación ha comenzado.",
                "tarea": ValidationTaskSerializer(task).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def _extract_emails(csv_text: str) -> list[str]:
        """
        Auto-detect the column containing email addresses in CSV text.

        Strategy:
          1. Sniff the dialect.
          2. Read headers — look for columns named email, correo, e-mail, mail.
          3. If no header match, scan first data row for values containing '@'.
          4. Extract all values from the identified column.
        """
        try:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(csv_text[:4096])
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(io.StringIO(csv_text), dialect)

        rows = list(reader)
        if not rows:
            return []

        # Try to identify the email column by header name
        header_keywords = {"email", "correo", "e-mail", "mail", "correo electrónico", "correo_electronico"}
        header = rows[0]
        email_col_index = None

        for idx, col_name in enumerate(header):
            if col_name.strip().lower() in header_keywords:
                email_col_index = idx
                break

        data_start = 0

        if email_col_index is not None:
            # Header row found — data starts at row 1
            data_start = 1
        else:
            # No header match — scan first few rows for '@' to find the column
            for row in rows[:5]:
                for idx, value in enumerate(row):
                    if "@" in value:
                        email_col_index = idx
                        break
                if email_col_index is not None:
                    break

            # Check if first row looks like a header (no '@' in identified column)
            if email_col_index is not None and "@" not in rows[0][email_col_index]:
                data_start = 1

        if email_col_index is None:
            # Fallback: if single column, treat every cell as a potential email
            if all(len(row) == 1 for row in rows[:10]):
                email_col_index = 0
                # Check if first row is a header
                if "@" not in rows[0][0]:
                    data_start = 1
            else:
                return []

        # Extract and deduplicate emails
        seen = set()
        emails = []
        for row in rows[data_start:]:
            if email_col_index < len(row):
                email = row[email_col_index].strip().lower()
                if email and "@" in email and email not in seen:
                    seen.add(email)
                    emails.append(email)

        return emails


# =============================================================================
# Task views
# =============================================================================


class TaskListView(APIView):
    """
    GET /api/tasks/

    Lists all validation tasks for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = ValidationTask.objects.filter(usuario=request.user)
        serializer = ValidationTaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetailView(APIView):
    """
    GET /api/tasks/<id>/

    Returns details of a specific task including progress counters.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = ValidationTask.objects.get(id=task_id, usuario=request.user)
        except ValidationTask.DoesNotExist:
            return Response(
                {"error": True, "detalle": "Tarea no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(ValidationTaskSerializer(task).data)


class TaskDiagnosticView(APIView):
    """
    GET /api/tasks/<id>/diagnostic/

    Returns aggregated statistics for a completed task. Always free.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = ValidationTask.objects.get(id=task_id, usuario=request.user)
        except ValidationTask.DoesNotExist:
            return Response(
                {"error": True, "detalle": "Tarea no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        total = task.total_correos or 1  # avoid division by zero

        return Response({
            "total_correos": task.total_correos,
            "validos": task.validos,
            "invalidos": task.invalidos,
            "desechables": task.desechables,
            "porcentaje_validos": round((task.validos / total) * 100, 1),
            "porcentaje_invalidos": round((task.invalidos / total) * 100, 1),
            "porcentaje_desechables": round((task.desechables / total) * 100, 1),
        })


class TaskDownloadView(APIView):
    """
    GET /api/tasks/<id>/download/

    Returns a CSV file with all validation results for the task.

    Credit rules:
      - If ``es_gratuita`` is True → free download, no credits deducted.
      - Otherwise → deduct credits equal to ``total_correos`` and create
        a CreditTransaction.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = ValidationTask.objects.get(id=task_id, usuario=request.user)
        except ValidationTask.DoesNotExist:
            return Response(
                {"error": True, "detalle": "Tarea no encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if task.estado != "completado":
            return Response(
                {"error": True, "detalle": "La tarea aún no ha finalizado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        # Check if download already paid for (idempotency via referencia)
        download_ref = f"download:task:{task.id}"
        already_paid = CreditTransaction.objects.filter(
            usuario=user, referencia=download_ref
        ).exists()

        if not task.es_gratuita and not already_paid:
            cost = task.total_correos
            if user.creditos < cost:
                return Response(
                    {
                        "error": True,
                        "detalle": (
                            f"Créditos insuficientes. Necesitas {cost} créditos, "
                            f"tienes {user.creditos}."
                        ),
                    },
                    status=status.HTTP_402_PAYMENT_REQUIRED,
                )

            # Deduct credits
            user.creditos -= cost
            user.save(update_fields=["creditos"])

            CreditTransaction.objects.create(
                usuario=user,
                tipo="uso",
                cantidad=-cost,
                referencia=download_ref,
                descripcion=f"Descarga de resultados: {task.nombre_archivo}",
            )

        # Build CSV response
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        safe_name = task.nombre_archivo.replace('"', "")
        response["Content-Disposition"] = f'attachment; filename="resultados_{safe_name}"'

        writer = csv.writer(response)
        writer.writerow(["correo", "estado", "motivo"])

        results = task.resultados.all().values_list("correo", "estado", "motivo")
        for correo, estado, motivo in results.iterator(chunk_size=1000):
            writer.writerow([correo, estado, motivo or ""])

        return response


# =============================================================================
# Credit views
# =============================================================================


class CreditBalanceView(APIView):
    """
    GET /api/credits/balance/

    Returns the authenticated user's current credit balance.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "creditos": request.user.creditos,
            "plan": request.user.plan,
        })


class CreditHistoryView(APIView):
    """
    GET /api/credits/history/

    Returns the credit transaction history for the authenticated user.
    Paginated by DRF's default pagination.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = CreditTransaction.objects.filter(usuario=request.user)
        # Manual pagination to work with APIView
        from rest_framework.pagination import PageNumberPagination

        paginator = PageNumberPagination()
        paginator.page_size = 25
        page = paginator.paginate_queryset(transactions, request)
        serializer = CreditTransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# =============================================================================
# Webhook views
# =============================================================================


class LemonSqueezyWebhookView(APIView):
    """
    POST /api/webhooks/lemonsqueezy/

    Receives webhook events from LemonSqueezy. Verifies the HMAC-SHA256
    signature, parses the event, and credits the user's account.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        signature = request.META.get("HTTP_X_SIGNATURE", "")
        secret = settings.LEMONSQUEEZY_WEBHOOK_SECRET

        if not verify_webhook_signature(request.body, signature, secret):
            return Response(
                {"error": True, "detalle": "Firma inválida."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            event_data = request.data
            process_payment_event(event_data)
        except ValueError as exc:
            logger.warning("Error procesando evento de pago: %s", exc)
            return Response(
                {"error": True, "detalle": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            logger.exception("Error inesperado procesando webhook de LemonSqueezy.")
            return Response(
                {"error": True, "detalle": "Error interno procesando el evento."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"recibido": True}, status=status.HTTP_200_OK)
