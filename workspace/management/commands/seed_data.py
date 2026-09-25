from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workspace.models import Project, AgentComponent, ChatMessage

class Command(BaseCommand):
    help = 'Seeds realistic data for Architect 2.0 evaluation'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # 1. Create Demo User
        user, _ = User.objects.get_or_create(username='alex_dev', email='alex.executive@architect.demo')
        user.set_password('demo1234')
        user.save()

        # Clear old projects to maintain clean demo state
        Project.objects.all().delete()

        # 2. Seed Realistic Projects
        p1 = Project.objects.create(
            id='8f29d10a-422f-488b-[a-f0-9]{4}-[a-f0-9]{12}' if False else '8f29d10a-422f-488b-8a8f-28721bf9012a',
            owner=user,
            title='Customer Support Copilot',
            description='Multi-agent support ticket routing with ground-truth database lookup.',
            framework='LYZR',
            status='DEPLOYED',
            github_repo_url='https://github.com/alex-dev/support-copilot',
            live_deployment_url='https://support-copilot.architect.app'
        )

        p2 = Project.objects.create(
            id='3b9a10f8-1122-4a09-[a-f0-9]{4}-[a-f0-9]{12}' if False else '3b9a10f8-1122-4a09-9021-ff8910019283',
            owner=user,
            title='GitHub Automated PR Inspector',
            description='Autonomous agent reviewing pull requests and running lint checks.',
            framework='CREWAI',
            status='READY',
            github_repo_url='https://github.com/alex-dev/pr-inspector'
        )

        p3 = Project.objects.create(
            id='5c1022e1-90aa-4331-[a-f0-9]{4}-[a-f0-9]{12}' if False else '5c1022e1-90aa-4331-8930-dd1019280191',
            owner=user,
            title='B2B Lead Research Pipeline',
            description='Web crawling agent identifying key executives and drafting outreach emails.',
            framework='LANGCHAIN',
            status='BUILDING'
        )

        # 3. Seed Agents for Project 1 (Support Copilot)
        AgentComponent.objects.create(
            project=p1,
            name='Intent Classifier Router',
            role='System Orchestrator',
            goal='Classify incoming user query into billing, technical support, or human escalation.',
            tools=['RegexParser', 'JSONFormatter']
        )
        AgentComponent.objects.create(
            project=p1,
            name='Knowledge Base Retriever',
            role='RAG Specialist',
            goal='Search vector database for technical docs matching ticket description.',
            tools=['VectorSearch', 'DocumentStore']
        )
        AgentComponent.objects.create(
            project=p1,
            name='Escalation Manager',
            role='Slack Notifier',
            goal='Notify on-call engineers if issue severity is High.',
            tools=['SlackWebHook', 'PagerDutyAPI']
        )

        # 4. Seed Chat History
        ChatMessage.objects.create(
            project=p1,
            sender='USER',
            content='Build an agentic support workflow that routes high priority billing tickets.'
        )
        ChatMessage.objects.create(
            project=p1,
            sender='AGENT',
            content='Configured 3 agents: Intent Classifier, Knowledge Base Retriever, and Escalation Manager. Live workflow ID active: wf_8f29d10a.',
            code_snippet='from lyzr import AgentWorkflow, RouterNode\n\nworkflow = AgentWorkflow(id="wf_8f29d10a")'
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 3 projects, agents, and chat history!'))