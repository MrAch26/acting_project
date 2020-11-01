from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('job_opp/', views.JobOppList.as_view(), name='job_opp'),
    path('job_opp/create_job_opp/', views.create_job_opp, name='create_job_opp'),
    path('job_opp/details/<pk>', views.details_job_opp, name='details_job_opp'),
    path('job_opp/update/<pk>', views.update_job_opp, name='update_job_opp'),
    path('job_opp/delete/<pk>', views.DeleteJobOpp.as_view(), name='delete_job_opp'),


]