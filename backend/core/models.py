"""
Data models for CleanMail by Samod.

Four models:
  - User: custom user, NOT extending AbstractUser. Uses UUID PK.
  - ValidationTask: tracks a CSV validation job. Uses UUID PK.
  - EmailResult: individual email validation result. Uses BigAutoField PK.
  - CreditTransaction: ledger entry for credit changes. Uses UUID PK.
"""

import uuid

from django.db import models


class User(models.Model):
    """
    Custom user model for CleanMail.

    Does NOT extend Django's AbstractUser. Authentication is handled
    exclusively through magic links + JWT tokens.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Correo electrónico",
    )
    nombre = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Nombre",
    )
    plan = models.CharField(
        max_length=20,
        default="free",
        verbose_name="Plan",
    )
    creditos = models.IntegerField(
        default=100,
        verbose_name="Créditos disponibles",
        help_text="Bono de bienvenida: 100 créditos.",
    )
    magic_token = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="Token mágico",
    )
    magic_token_exp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Expiración del token mágico",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último acceso",
    )

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self) -> str:
        return self.email

    @property
    def is_authenticated(self) -> bool:
        """Required by DRF to treat this object as an authenticated user."""
        return True


class ValidationTask(models.Model):
    """
    Represents a CSV validation job submitted by a user.

    Tracks progress counters and final status.
    """

    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("procesando", "Procesando"),
        ("completado", "Completado"),
        ("error", "Error"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tareas",
        verbose_name="Usuario",
    )
    nombre_archivo = models.CharField(
        max_length=255,
        verbose_name="Nombre del archivo",
    )
    total_correos = models.IntegerField(
        default=0,
        verbose_name="Total de correos",
    )
    procesados = models.IntegerField(
        default=0,
        verbose_name="Procesados",
    )
    validos = models.IntegerField(
        default=0,
        verbose_name="Válidos",
    )
    invalidos = models.IntegerField(
        default=0,
        verbose_name="Inválidos",
    )
    desechables = models.IntegerField(
        default=0,
        verbose_name="Desechables",
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="pendiente",
        verbose_name="Estado",
    )
    es_gratuita = models.BooleanField(
        default=False,
        verbose_name="Es gratuita",
        help_text="La primera tarea con ≤500 correos es gratuita.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de finalización",
    )

    class Meta:
        db_table = "validation_tasks"
        ordering = ["-created_at"]
        verbose_name = "Tarea de validación"
        verbose_name_plural = "Tareas de validación"

    def __str__(self) -> str:
        return f"{self.nombre_archivo} ({self.estado})"


class EmailResult(models.Model):
    """
    Individual email validation result linked to a ValidationTask.

    Uses BigAutoField (BIGSERIAL) for high-volume performance.
    """

    ESTADO_CHOICES = [
        ("valido", "Válido"),
        ("invalido", "Inválido"),
        ("desechable", "Desechable"),
    ]

    MOTIVO_CHOICES = [
        ("sintaxis", "Error de sintaxis"),
        ("sin_mx", "Sin registro MX"),
        ("dominio_temporal", "Dominio temporal/desechable"),
        ("formato_invalido", "Formato inválido"),
    ]

    id = models.BigAutoField(
        primary_key=True,
        verbose_name="ID",
    )
    tarea = models.ForeignKey(
        ValidationTask,
        on_delete=models.CASCADE,
        related_name="resultados",
        verbose_name="Tarea",
    )
    correo = models.CharField(
        max_length=255,
        verbose_name="Correo electrónico",
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="",
        verbose_name="Estado",
    )
    motivo = models.CharField(
        max_length=50,
        choices=MOTIVO_CHOICES,
        null=True,
        blank=True,
        verbose_name="Motivo",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    class Meta:
        db_table = "email_results"
        ordering = ["id"]
        verbose_name = "Resultado de correo"
        verbose_name_plural = "Resultados de correos"

    def __str__(self) -> str:
        return f"{self.correo} → {self.estado}"


class CreditTransaction(models.Model):
    """
    Ledger entry tracking every credit change for a user.

    Positive ``cantidad`` = income (purchase, bonus).
    Negative ``cantidad`` = expense (usage).
    """

    TIPO_CHOICES = [
        ("compra", "Compra"),
        ("uso", "Uso"),
        ("bonus", "Bonus"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transacciones",
        verbose_name="Usuario",
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo",
    )
    cantidad = models.IntegerField(
        verbose_name="Cantidad",
        help_text="Positivo = ingreso, negativo = gasto.",
    )
    referencia = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Referencia",
    )
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Descripción",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    class Meta:
        db_table = "credit_transactions"
        ordering = ["-created_at"]
        verbose_name = "Transacción de créditos"
        verbose_name_plural = "Transacciones de créditos"

    def __str__(self) -> str:
        sign = "+" if self.cantidad >= 0 else ""
        return f"{self.usuario.email}: {sign}{self.cantidad} ({self.tipo})"
