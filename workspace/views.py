from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, ChatMessage, AgentComponent
from .serializers import ProjectSerializer, ChatMessageSerializer, AgentComponentSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import uuid
from .models import Project, AgentComponent, ChatMessage

def index_view(request):
    """Homepage Dashboard showing real projects"""
    projects = Project.objects.all().order_by('-updated_at')
    return render(request, 'workspace/dashboard.html', {'projects': projects})

def auth_view(request):
    if request.method == 'POST':
        request.session['is_authenticated'] = True
        return redirect('home')
    return render(request, 'workspace/auth.html')

def agent_studio_view(request, project_id=None):
    """Agent Studio with dynamic workflow loading"""
    projects = Project.objects.all()
    
    if project_id:
        active_project = get_object_or_404(Project, id=project_id)
    else:
        active_project = projects.first()

    agents = AgentComponent.objects.filter(project=active_project) if active_project else []
    messages = ChatMessage.objects.filter(project=active_project) if active_project else []

    context = {
        'projects': projects,
        'active_project': active_project,
        'agents': agents,
        'messages': messages,
    }
    return render(request, 'workspace/agent_studio.html', context)

def marketplace_view(request):
    """Marketplace with template previews"""
    templates = [
        {
            'slug': 'customer-support',
            'title': 'Intercom-Style Copilot',
            'category': 'Customer Support',
            'framework': 'Lyzr Core',
            'description': 'Autonomous ticket router with database grounding and human escalation.',
            'agents_count': 3,
            'project_id': '8f29d10a-422f-488b-8a8f-28721bf9012a'
        },
        {
            'slug': 'github-reviewer',
            'title': 'GitHub PR Code Inspector',
            'category': 'Developer Tools',
            'framework': 'CrewAI',
            'description': 'Inspects pull requests, checks git diffs, and leaves automated inline reviews.',
            'agents_count': 2,
            'project_id': '3b9a10f8-1122-4a09-9021-ff8910019283'
        },
        {
            'slug': 'lead-outreach',
            'title': 'B2B Prospect Research Agent',
            'category': 'Sales & Marketing',
            'framework': 'LangChain',
            'description': 'Crawls target company websites and drafts tailored executive outreach.',
            'agents_count': 2,
            'project_id': '5c1022e1-90aa-4331-8930-dd1019280191'
        }
    ]
    return render(request, 'workspace/marketplace.html', {'templates': templates})

def logout_view(request):
    request.session.flush()
    return redirect('auth')

def studio_view(request, project_id=None):
    """Main Agentic Builder / Vibe-Coding Workspace"""
    return render(request, 'workspace/studio.html', {'project_id': project_id or str(uuid.uuid4())})

def agent_builder_view(request):
    """Visual Agent & Node Configuration Section"""
    return render(request, 'workspace/agent_builder.html')



# 2. Dummy Feature Flow APIs
def mock_github_sync(request):
    return JsonResponse({
        "status": "success",
        "repos": ["architect-demo-app", "agentic-support-bot", "ai-crm-workflow"],
        "connected": True
    })

def mock_deploy_status(request):
    return JsonResponse({
        "status": "deployed",
        "live_url": "https://preview-app-x82f.architect.app",
        "build_time": "14s",
        "logs": ["Validating agent nodes...", "Building frontend...", "Deploying container...", "Live!"]
    })

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def prompt_build(self, request, pk=None):
        """Simulates vibe-coding generation flow for building UI and agents."""
        project = self.get_object()
        user_prompt = request.data.get('prompt', '')

        # 1. Log User Message
        ChatMessage.objects.create(project=project, sender='USER', content=user_prompt)

        # 2. Mock Agent Response & Generated Code/UI
        assistant_reply = f"Building agentic UI components and workspace setup based on: '{user_prompt}'"
        generated_code = f"# Auto-generated for {project.title}\nfrom lyzr import Agent\n\nagent = Agent(role='Support Specialist', prompt='{user_prompt}')\n"
        
        msg = ChatMessage.objects.create(
            project=project,
            sender='AGENT',
            content=assistant_reply,
            code_snippet=generated_code
        )

        return Response({
            'status': 'Generated',
            'chat': ChatMessageSerializer(msg).data,
            'ui_preview': {
                'component': 'SupportDashboard',
                'layout': 'Sidebar + Main Canvas',
                'preview_html': f'<div class="p-4 bg-gray-100 rounded">Generated interface preview for: {user_prompt}</div>'
            }
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def connect_github(self, request, pk=None):
        """Mocks GitHub repo integration."""
        project = self.get_object()
        repo_name = request.data.get('repo_name', f"architect-app-{project.id.hex[:6]}")
        
        project.github_repo_url = f"https://github.com/{request.user.username}/{repo_name}"
        project.save()

        return Response({
            'message': 'GitHub repository linked successfully.',
            'github_url': project.github_repo_url
        })

    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        """Mocks full app deployment process."""
        project = self.get_object()
        project.status = 'DEPLOYED'
        project.live_deployment_url = f"https://{project.id.hex[:8]}.architect.app"
        project.save()

        return Response({
            'message': 'App successfully deployed!',
            'live_url': project.live_deployment_url,
            'status': project.status
        })