from django.urls import path
from employeeapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("projectdetail",views.ProjectDetailView,basename="projectdetail")
router.register("assignedprojects",views.AssignedProjectsView,basename="assignedprojects-list")
router.register("taskchart",views.TaskChartView,basename="taskchart")
router.register("taskupdateschart",views.TaskUpdatesView,basename="taskupdateschart")

urlpatterns = [
    path("register/",views.EmployeeCreateView.as_view(),name="signup"),
    path('token/',views.CustomAuthToken.as_view(), name='token'),
    path("teamview/",views.TeamView.as_view(),name="teamview"),
    
    
] +router.urls