"""
Admin site configuration — CleanMail by Samod.

Registers all models with useful ``list_display`` columns for the
Django admin interface.
"""

from django.contrib import admin

from core.models import CreditTransaction, EmailResult, User, ValidationTask


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin view for User."""

    list_display = ("email", "nombre", "plan", "creditos", "created_at", "last_login")
    list_filter = ("plan",)
    search_fields = ("email", "nombre")
    readonly_fields = ("id", "created_at")
    ordering = ("-created_at",)

    def changelist_view(self, request, extra_context=None):
        """Agrega un mini-dashboard de estadísticas al cargar la lista de usuarios."""
        from django.contrib import messages
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        weekly = User.objects.filter(created_at__gte=now - timedelta(days=7)).count()
        monthly = User.objects.filter(created_at__gte=now - timedelta(days=30)).count()
        
        # Evitamos duplicar el mensaje en cada recarga
        storage = messages.get_messages(request)
        for _ in storage:
            pass 
        
        messages.info(
            request, 
            f"📊 DASHBOARD DE CRECIMIENTO: Has conseguido {weekly} usuarios nuevos en los últimos 7 días, y {monthly} en los últimos 30 días."
        )
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(ValidationTask)
class ValidationTaskAdmin(admin.ModelAdmin):
    """Admin view for ValidationTask."""

    list_display = (
        "id",
        "usuario",
        "nombre_archivo",
        "total_correos",
        "procesados",
        "estado",
        "es_gratuita",
        "created_at",
        "completed_at",
    )
    list_filter = ("estado", "es_gratuita")
    search_fields = ("nombre_archivo", "usuario__email")
    readonly_fields = ("id", "created_at")
    ordering = ("-created_at",)


@admin.register(EmailResult)
class EmailResultAdmin(admin.ModelAdmin):
    """Admin view for EmailResult."""

    list_display = ("id", "tarea", "correo", "estado", "motivo", "created_at")
    list_filter = ("estado", "motivo")
    search_fields = ("correo",)
    raw_id_fields = ("tarea",)
    ordering = ("-id",)


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    """Admin view for CreditTransaction."""

    list_display = (
        "id",
        "usuario",
        "tipo",
        "cantidad",
        "referencia",
        "descripcion",
        "created_at",
    )
    list_filter = ("tipo",)
    search_fields = ("usuario__email", "referencia", "descripcion")
    readonly_fields = ("id", "created_at")
    ordering = ("-created_at",)
