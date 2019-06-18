from django.contrib import admin

from vote.models import Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'content_type',)


admin.site.register(Vote, VoteAdmin)
