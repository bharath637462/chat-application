from django.contrib import admin

from chat.models import ChatMessage, Profile, User


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'receiver', 'message', 'is_read', 'created_at']


admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Profile)
admin.site.register(User)
