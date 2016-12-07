from django.contrib import admin

from .models import Post, Job


class JobAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Job, JobAdmin)
admin.site.register(Post, PostAdmin)
