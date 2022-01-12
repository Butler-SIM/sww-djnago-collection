from django.contrib import admin
from . import models


@admin.register(models.ChatModel)
class ChatApiAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'chatNo',
        'read',
        'post_username',
        'get_username',
        'send_message',
        'post_send_status',
        'get_send_status',
        'created_at',
    )

    list_display_links = (
        'id',
        'chatNo',
        'read',
        'post_username',
        'get_username',
        'send_message',
        'post_send_status',
        'get_send_status',
        'created_at',
    )

    search_fields = [
        'id',
        'chatNo',
        'read',
        'post_username',
        'get_username',
        'send_message',
        'post_send_status',
        'get_send_status',
        'created_at',
    ]

@admin.register(models.ChatBackupModel)
class ChatBackupApiAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'chatNo',
        'read',
        'post_username',
        'get_username',
        'send_message',
        'post_send_status',
        'get_send_status',
        'created_at',
    )

    list_display_links = (
        'id',
        'chatNo',
        'read',
        'post_username',
        'get_username',
        'send_message',
        'post_send_status',
        'get_send_status',
        'created_at',
    )

    search_fields = [
        'id',
        'chatNo',
        'read',
        'post_username',
        'get_username',
        'send_message',
        'post_send_status',
        'get_send_status',
        'created_at',
    ]
