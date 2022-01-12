from django.conf.urls.static import static
from django.urls import path
from api_server.settings import base
from chatapi.views import ChatView, check_chatNo, ajax_chat, chat_delete, chatNo_delete, user_chat_data, \
    get_chat_detail, hidden_chat

app_name = "chatapi"

urlpatterns = [
    path('', ChatView.as_view(), name="chatview"),
    path('chat_delete/', chat_delete, name="chat_delete"),
    path('chatNo_delete/', chatNo_delete, name="chatNo_delete"),
    path('check/', check_chatNo, name="check_chatNo"),
    path('ajax/', ajax_chat, name="ajax_chat"),
    path('user_chat_data/', user_chat_data, name="user_chat_data"),
    path('get_chat_detail/', get_chat_detail, name="get_chat_detail"),
    path('hidden_chat/', hidden_chat, name="hidden_chat"),
]
