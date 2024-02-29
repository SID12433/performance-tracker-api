from django.urls import path
from employeeapi import views
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path("register/",views.EmployeeCreateView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path("teamview/",views.TeamView.as_view(),name="teamview"),
    
    
]