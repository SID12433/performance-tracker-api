from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action


from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign
from teamleadapi.serializer import RegistrationSerializer,ProjectSerializer,TeamSerializer,EmployeeSerializer,ProjectAssignSerializer,ProjectDetailSerializer,TaskChartSerializer,TaskUpdatesChartSerializer


class TeamleadCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="teamlead")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    
class EmployeesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        # qs=Employee.objects.filter(in_team=False)
        qs=Employee.objects.all()
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    
    
class TeamView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        teamlead_id = request.user.id
        teamlead_obj = TeamLead.objects.get(id=teamlead_id)
        
        if serializer.is_valid():
            employee_ids = request.data.get('members', [])
            employees_already_in_team = Employee.objects.filter(id__in=employee_ids, in_team=True)
            if employees_already_in_team.exists():
                error_msg="selected employees are already part of a team and cannot be added to yours."
                return Response(data={"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
            team = serializer.save(teamlead=teamlead_obj)
            employees_added_to_team = team.members.all()
            employees_added_to_team.update(in_team=True)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        teamlead_id = request.user.id
        teamlead_obj = TeamLead.objects.get(id=teamlead_id)
        try:
            team = Teams.objects.get(teamlead=teamlead_obj)
        except Teams.DoesNotExist:
            return Response(data={"message": "Team not found for this team lead."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeamSerializer(team)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Teams.objects.get(id=id)
        serializer=TeamSerializer(qs)
        return Response(data=serializer.data)
    
    
class ProjectView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Projects.objects.all()
        serializer=ProjectSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Projects.objects.get(id=id)
        serializer=ProjectSerializer(qs)
        return Response(data=serializer.data)
     
    @action(methods=["post"],detail=True)
    def project_assign(self,request,*args,**kwargs):
        serializer=ProjectAssignSerializer(data=request.data)
        project_id=kwargs.get("pk")
        project_obj=Projects.objects.get(id=project_id)
        teamlead=request.user.id
        teamlead_obj=TeamLead.objects.get(id=teamlead)
        team_obj=Teams.objects.get(teamlead=teamlead_obj)
        if team_obj.is_approved==True:
            if serializer.is_valid():
                project_obj.project_status="Ongoing"
                project_obj.save()
                serializer.save(project=project_obj,teamlead=teamlead_obj,team=team_obj)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(data={"message": "Team is not approved by the Hr, so team cannot accept projects."}, status=status.HTTP_404_NOT_FOUND)
    

class AssignedProjectView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        teamlead_id=request.user.id
        qs=Project_assign.objects.filter(teamlead=teamlead_id)
        serializer=ProjectAssignSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Projects.objects.get(id=id)
        serializer=ProjectSerializer(qs)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def assign_to_emp(self, request, *args, **kwargs):
        serializer=ProjectDetailSerializer(data=request.data)
        projectassign_id=kwargs.get("pk")
        projectassign_obj=Project_assign.objects.get(id=projectassign_id)
        teamlead=request.user.id
        teamlead_obj=TeamLead.objects.get(id=teamlead)       
        if serializer.is_valid():
            serializer.save(teamlead=teamlead_obj,projectassigned=projectassign_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        
    @action(methods=["post"],detail=True)
    def project_completed(self, request, *args, **kwargs):
        assignedproject_id = kwargs.get("pk")
        try:
            assignproject_obj = Project_assign.objects.get(id=assignedproject_id)
        except Project_assign.DoesNotExist:
            return Response({"message": "project not found"}, status=status.HTTP_404_NOT_FOUND)
        assignproject_obj.project.project_status = "completed"
        assignproject_obj.project.save()
        return Response({"message": "project completed marked success"}, status=status.HTTP_200_OK)
        
        
class ProjectDetailView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        teamlead_id=request.user.id
        qs=ProjectDetail.objects.filter(teamlead=teamlead_id)
        serializer=ProjectDetailSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ProjectDetail.objects.get(id=id)
        serializer=ProjectDetailSerializer(qs)
        return Response(data=serializer.data)
    

class TaskChartView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        teamlead_id = request.user.id
        qs = TaskChart.objects.filter(project_detail__teamlead=teamlead_id)
        serializer = TaskChartSerializer(qs, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TaskChart.objects.get(id=id)
        serializer=TaskChartSerializer(qs)
        return Response(data=serializer.data)
    
    
class TaskUpdatesChartView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=TaskUpdateChart.objects.all()
        serializer=TaskUpdatesChartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TaskUpdateChart.objects.get(id=id)
        serializer=TaskUpdatesChartSerializer(qs)
        return Response(data=serializer.data)
    
    
    


  

    
     
    
        
        
