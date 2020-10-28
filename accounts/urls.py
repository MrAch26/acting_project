from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(extra_context={'nav': 'login'}), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.UserSignUp.as_view(extra_context={'nav': 'signup'}), name="signup"),
    path('profile/update/', views.actor_profile, name="edit_profile"),
    path('profile/<username>/', views.get_user_profile, name='profile'),
    path('agent/update/', views.agent_profile, name="edit_agent"),
    path('project-autocomplete/', views.ProjectAutocomplete.as_view(create_field='name'), name='project_autocomplete'),
]
