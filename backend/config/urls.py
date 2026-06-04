"""
URL configuration for CleanMail by Samod.

Routes all API traffic under /api/ to the core app.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
