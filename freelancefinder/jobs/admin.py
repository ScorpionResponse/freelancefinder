"""Admin site configuration for the jobs app."""

from django.contrib import admin

from .models import Post, Job


def remove_tags(modeladmin, request, queryset):
    """Remove tags."""
    for obj in queryset:
        obj.tags.clear()
remove_tags.short_description = "Remove Tags"


class JobAdmin(admin.ModelAdmin):
    """The Job model needs no special admin configuration."""

    model = Job
    list_display = ('title', 'tag_list', 'created', 'modified')
    fields = ('title', 'description', 'tags')
    readonly_fields = ('created', 'modified')
    actions = [remove_tags]

    def get_queryset(self, request):
        """Prefetch the tags data to make this more efficient."""
        return super(JobAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        """Concatenate all tags for each job."""
        return u", ".join(o.name for o in obj.tags.all())


class PostAdmin(admin.ModelAdmin):
    """The Post model needs no special admin configuration."""

    model = Post
    list_display = ('title', 'source', 'subarea', 'is_job_posting', 'is_freelance', 'processed', 'created')
    fields = ('title', 'url', 'source', 'subarea', 'description', 'unique', 'is_job_posting', 'is_freelance', 'processed')
    readonly_fields = ('created', 'modified')


admin.site.register(Job, JobAdmin)
admin.site.register(Post, PostAdmin)
