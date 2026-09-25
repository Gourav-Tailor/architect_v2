from django.contrib import admin
from django.urls import path, include
from workspace import views

urlpatterns = [
    # Primary Pages
    path('', views.index_view, name='home'),
    path('auth/', views.auth_view, name='auth'),
    
    # Unified Agent Studio Routes
    path('agent-studio/', views.agent_studio_view, name='agent_studio'),
    path('agent-studio/<str:project_id>/', views.agent_studio_view, name='agent_studio_project'),
    
    # Marketplace
    path('marketplace/', views.marketplace_view, name='marketplace'),

    # Admin & REST
    path('admin/', admin.site.urls),
    path('api/v1/workspace/', include('workspace.urls')),
    path('api-auth/', include('rest_framework.urls')),
]