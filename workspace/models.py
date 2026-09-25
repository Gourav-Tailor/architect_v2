import uuid
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPES = [
        ('NON_TECH', 'Business Executive / Non-Technical'),
        ('DEV', 'Developer / Technical'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role_type = models.CharField(max_length=20, choices=USER_TYPES, default='NON_TECH')
    github_access_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role_type})"


class Project(models.Model):
    FRAMEWORK_CHOICES = [
        ('LANGCHAIN', 'LangChain'),
        ('CREWAI', 'CrewAI'),
        ('AUTOGEN', 'AutoGen'),
        ('LYZR', 'Lyzr Core'),
        ('CUSTOM', 'Custom Python/FastAPI'),
    ]
    STATUS_CHOICES = [
        ('BUILDING', 'Building UI/Agent'),
        ('READY', 'Ready'),
        ('DEPLOYED', 'Deployed'),
        ('FAILED', 'Deployment Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    framework = models.CharField(max_length=50, choices=FRAMEWORK_CHOICES, default='LYZR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BUILDING')
    github_repo_url = models.URLField(blank=True, null=True)
    live_deployment_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('USER', 'User'),
        ('AGENT', 'Architect Assistant'),
        ('SYSTEM', 'System Log'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    code_snippet = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class AgentComponent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='agents')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=255)
    goal = models.TextField()
    tools = models.JSONField(default=list)  # e.g., ["WebSearch", "DatabaseQuery"]
    created_at = models.DateTimeField(auto_now_add=True)