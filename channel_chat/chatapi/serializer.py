from rest_framework import serializers
from chatapi.models import ChatModel,ChatBackupModel


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = "__all__"


class ChatBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBackupModel
        fields = "__all__"
