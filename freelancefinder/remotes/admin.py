"""Admin pages for remotes."""
from django.contrib import admin

from .models import Source, SourceConfig


class SourceAdmin(admin.ModelAdmin):
    """Basic admin for sources."""

    model = Source

    list_display = ('code', 'name', 'url', 'harvest_type')
    search_fields = ('name',)
    list_filter = ('harvest_type',)


class SourceConfigAdmin(admin.ModelAdmin):
    """Basic admin for sourceconfig."""

    model = SourceConfig

    list_display = ('source', 'config_key', 'config_value')
    search_fields = ('source',)
    list_filter = ('source__name',)


admin.site.register(Source, SourceAdmin)
admin.site.register(SourceConfig, SourceConfigAdmin)
