"""Admin site configuration for the jobs app."""

from django.contrib import admin

from .models import Post, Job


def remove_tags(modeladmin, request, queryset):
    """Remove tags."""
    queryset.update(tags=None)
remove_tags.short_description = "Remove Tags"


class JobAdmin(admin.ModelAdmin):
    """The Job model needs no special admin configuration."""

    model = Job
    list_display = ('title', 'tags', 'created', 'modified')
    fields = ('title', 'description', 'tags', 'created', 'modified')
    actions = [remove_tags]


class PostAdmin(admin.ModelAdmin):
    """The Post model needs no special admin configuration."""

    model = Post
    list_display = ('title', 'source', 'subarea', 'is_job_posting', 'is_freelance', 'processed', 'created')
    fields = ('title', 'url', 'source', 'subarea', 'description', 'unique', 'is_job_posting', 'is_freelance', 'processed', 'created', 'modified')


admin.site.register(Job, JobAdmin)
admin.site.register(Post, PostAdmin)
