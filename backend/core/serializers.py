"""
DRF serializers — CleanMail by Samod.

Output serializers for each model plus input serializers for API endpoints.
"""

from rest_framework import serializers

from core.models import CreditTransaction, EmailResult, User, ValidationTask


# =============================================================================
# Model serializers (output)
# =============================================================================


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a user (safe for the user themselves)."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nombre",
            "plan",
            "creditos",
            "created_at",
            "last_login",
        ]
        read_only_fields = fields


class ValidationTaskSerializer(serializers.ModelSerializer):
    """Serializer for validation task list and detail views."""

    progreso = serializers.SerializerMethodField()

    class Meta:
        model = ValidationTask
        fields = [
            "id",
            "nombre_archivo",
            "total_correos",
            "procesados",
            "validos",
            "invalidos",
            "desechables",
            "estado",
            "es_gratuita",
            "progreso",
            "created_at",
            "completed_at",
        ]
        read_only_fields = fields

    def get_progreso(self, obj: ValidationTask) -> float:
        """Return completion percentage (0–100)."""
        if obj.total_correos == 0:
            return 0.0
        return round((obj.procesados / obj.total_correos) * 100, 1)


class EmailResultSerializer(serializers.ModelSerializer):
    """Serializer for individual email validation results."""

    class Meta:
        model = EmailResult
        fields = [
            "id",
            "correo",
            "estado",
            "motivo",
            "created_at",
        ]
        read_only_fields = fields


class CreditTransactionSerializer(serializers.ModelSerializer):
    """Serializer for credit transaction history."""

    class Meta:
        model = CreditTransaction
        fields = [
            "id",
            "tipo",
            "cantidad",
            "referencia",
            "descripcion",
            "created_at",
        ]
        read_only_fields = fields


# =============================================================================
# Input serializers
# =============================================================================


class MagicLinkRequestSerializer(serializers.Serializer):
    """Input for requesting a magic link."""

    email = serializers.EmailField(
        max_length=255,
        help_text="Correo electrónico del usuario.",
        error_messages={
            "required": "El correo electrónico es obligatorio.",
            "invalid": "Formato de correo electrónico inválido.",
            "blank": "El correo electrónico no puede estar vacío.",
        },
    )
    nombre = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        default="",
        help_text="Nombre del usuario (opcional).",
    )


class MagicLinkVerifySerializer(serializers.Serializer):
    """Input for verifying a magic link token."""

    token = serializers.CharField(
        max_length=64,
        help_text="Token recibido en el enlace mágico.",
        error_messages={
            "required": "El token es obligatorio.",
            "blank": "El token no puede estar vacío.",
        },
    )


class SingleValidateSerializer(serializers.Serializer):
    """Input for validating a single email address."""

    email = serializers.CharField(
        max_length=255,
        help_text="Correo electrónico a validar.",
        error_messages={
            "required": "El correo electrónico es obligatorio.",
            "blank": "El correo electrónico no puede estar vacío.",
        },
    )


class TaskDiagnosticSerializer(serializers.Serializer):
    """Output for the task diagnostic endpoint."""

    total_correos = serializers.IntegerField()
    validos = serializers.IntegerField()
    invalidos = serializers.IntegerField()
    desechables = serializers.IntegerField()
    porcentaje_validos = serializers.FloatField()
    porcentaje_invalidos = serializers.FloatField()
    porcentaje_desechables = serializers.FloatField()
