from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.UserSignUp.as_view(), name="signup"),
    path('profile/update/', views.actor_profile, name="edit_profile"),

]
