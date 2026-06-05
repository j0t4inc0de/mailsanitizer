"""
URL routing for the core app — CleanMail by Samod.

All paths are relative to /api/ (mounted in config.urls).
"""

from django.urls import path

from core.views import (
    CreditBalanceView,
    CreditHistoryView,
    LemonSqueezyWebhookView,
    MagicLinkRequestView,
    MagicLinkVerifyView,
    PaddleWebhookView,
    SingleValidateView,
    TaskDetailView,
    TaskDiagnosticView,
    TaskDownloadView,
    TaskListView,
    UploadCSVView,
    UserMeView,
)

app_name = "core"

urlpatterns = [
    # ── Authentication ──────────────────────────────────────────────────
    path("auth/magic-link/", MagicLinkRequestView.as_view(), name="magic-link-request"),
    path("auth/verify/", MagicLinkVerifyView.as_view(), name="magic-link-verify"),
    path("auth/me/", UserMeView.as_view(), name="user-me"),

    # ── Email validation ────────────────────────────────────────────────
    path("validate/single/", SingleValidateView.as_view(), name="validate-single"),
    path("validate/upload/", UploadCSVView.as_view(), name="validate-upload"),

    # ── Tasks ───────────────────────────────────────────────────────────
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<uuid:task_id>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<uuid:task_id>/diagnostic/", TaskDiagnosticView.as_view(), name="task-diagnostic"),
    path("tasks/<uuid:task_id>/download/", TaskDownloadView.as_view(), name="task-download"),

    # ── Credits ─────────────────────────────────────────────────────────
    path("credits/balance/", CreditBalanceView.as_view(), name="credit-balance"),
    path("credits/history/", CreditHistoryView.as_view(), name="credit-history"),

    # ── Webhooks ────────────────────────────────────────────────────────
    path("webhooks/lemonsqueezy/", LemonSqueezyWebhookView.as_view(), name="webhook-lemonsqueezy"),
    path("webhooks/paddle/", PaddleWebhookView.as_view(), name="webhook-paddle"),
]
