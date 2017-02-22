"""Admin pages for remotes."""
from django.contrib import admin

from .models import Source, SourceConfig


class SourceAdmin(admin.ModelAdmin):
    """Basic admin for sources."""

    pass


class SourceConfigAdmin(admin.ModelAdmin):
    """Basic admin for sourceconfig."""

    pass

admin.site.register(Source, SourceAdmin)
admin.site.register(SourceConfig, SourceConfigAdmin)
