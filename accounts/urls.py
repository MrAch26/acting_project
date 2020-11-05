from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from .views import UpdateWorkHistory, DeleteWorkHistory

urlpatterns = [
    path('login/', LoginView.as_view(extra_context={'nav': 'login'}), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.UserSignUp.as_view(extra_context={'nav': 'signup'}), name="signup"),
    path('profile/actor/update/', views.edit_actor_profile, name="edit_actor"),
    path('profile/agent/update/', views.edit_agent_profile, name="edit_agent"),
    path('profile/actor/<username>/', views.show_actor_profile, name='actor_profile'),
    path('profile/agent/<username>/', views.show_agent_profile, name='agent_profile'),
    path('project-autocomplete/', views.ProjectAutocomplete.as_view(create_field='name'), name='project_autocomplete'),

    path('edit_workhistory/<int:pk>', UpdateWorkHistory.as_view(), name='work-history-edit'),
    path('delete_workhistory/<int:pk>', DeleteWorkHistory.as_view(), name='work-history-delete'),


]
