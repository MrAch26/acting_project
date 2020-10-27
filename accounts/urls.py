from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('profile/<pk>', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.UserSignUp.as_view(), name="signup"),
    path('profile/update/', views.actor_profile, name="edit_profile"),
    path('agent/update/', views.agent_profile, name="edit_agent"),
    path('project-autocomplete/', views.ProjectAutocomplete.as_view(create_field='name'), name='project_autocomplete'),


]
