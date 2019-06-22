from django.contrib import admin

from author.models import Author, Bookmark


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'authenticated',)


admin.site.register(Bookmark)
admin.site.register(Author, AuthorAdmin)
