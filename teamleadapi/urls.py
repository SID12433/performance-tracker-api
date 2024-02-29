from django.urls import path
from teamleadapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("team",views.TeamView,basename="team-create")
router.register("employee",views.EmployeesView,basename="employee")
router.register("projects",views.ProjectView,basename="projects-list")
router.register("assignedprojects",views.AssignedProjectView,basename="assignedprojects-list")
router.register("projectdetail",views.ProjectDetailView,basename="projectdetail")
router.register("taskchart",views.TaskChartView,basename="taskchart")
router.register("taskupdates",views.TaskUpdatesChartView,basename="taskupdates")



urlpatterns = [
    path("register/",views.TeamleadCreateView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),

]  +router.urls