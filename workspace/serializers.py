from rest_framework import serializers
from .models import Project, ChatMessage, AgentComponent


class AgentComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentComponent
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    agents = AgentComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'title', 'description', 'framework', 
            'status', 'github_repo_url', 'live_deployment_url', 
            'created_at', 'messages', 'agents'
        ]
        read_only_fields = ['owner']