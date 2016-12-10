"""Admin pages for remotes."""
from django.contrib import admin

from .models import Source


class SourceAdmin(admin.ModelAdmin):
    """Basic admin for sources."""

    pass


admin.site.register(Source, SourceAdmin)
