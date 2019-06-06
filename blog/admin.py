from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timestamp', 'draft')
    search_fields = ('title', 'author__user__username', 'description')


admin.site.register(Post, PostAdmin)
