from django.contrib import admin

from tutorial.models import Tutorial, Series


class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_of', 'creator')
    search_fields = ('name', 'description', 'type_of', 'creator__user__username')


class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'description', 'author__user__username')


admin.site.register(Series, SeriesAdmin)
admin.site.register(Tutorial, TutorialAdmin)
