from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','direction','content','timestamp']

class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id','state']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id','state','messages']
