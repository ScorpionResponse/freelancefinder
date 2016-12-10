"""Admin site configuration for the jobs app."""

from django.contrib import admin

from .models import Post, Job


class JobAdmin(admin.ModelAdmin):
    """The Job model needs no special admin configuration."""

    pass


class PostAdmin(admin.ModelAdmin):
    """The Post model needs no special admin configuration."""

    pass


admin.site.register(Job, JobAdmin)
admin.site.register(Post, PostAdmin)
