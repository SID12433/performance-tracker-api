from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action
from datetime import datetime, timedelta


from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign
from employeeapi.serializer import RegistrationSerializer,TeamSerializer,ProjectDetailSerializer,ProjectAssignSerializer,TaskChartSerializer,TaskUpdateChartSerializer

class EmployeeCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="employee")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        
class TeamView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        qs = Teams.objects.filter(members=employee).distinct()
        serializer = TeamSerializer(qs, many=True)
        return Response(serializer.data)
    

class AssignedProjectsView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        qs = Project_assign.objects.filter(team__members=employee).distinct()
        serializer = ProjectAssignSerializer(qs, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Project_assign.objects.get(id=id)
        serializer=ProjectAssignSerializer(qs)
        return Response(data=serializer.data)
    
class ProjectDetailView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        emp_id=request.user.id
        qs=ProjectDetail.objects.filter(assigned_person=emp_id)
        serializer=ProjectDetailSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_id=request.user.id
        qs=ProjectDetail.objects.get(id=id,assigned_person=emp_id)
        serializer=ProjectDetailSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(methods=["post"],detail=True)
    def taskchart_add(self, request, *args, **kwargs):
        serializer=TaskChartSerializer(data=request.data)
        projectdetail_id=kwargs.get("pk")
        projectdetail_obj=ProjectDetail.objects.get(id=projectdetail_id)
        emp_id=request.user.id
        emp_obj=Employee.objects.get(id=emp_id)       
        if serializer.is_valid():
            start_date = datetime.now().date()
            ending_date = projectdetail_obj.projectassigned.project.end_date
            total_days = (ending_date - start_date).days if ending_date else None
            serializer.save(assigned_person=emp_obj,project_detail=projectdetail_obj,total_days=total_days,end_date=ending_date,)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class TaskChartView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        qs = TaskChart.objects.filter(assigned_person=employee)
        serializer = TaskChartSerializer(qs, many=True)
        return Response(serializer.data)
    
    
    @action(methods=["post"],detail=True)
    def taskupdates_add(self, request, *args, **kwargs):
        serializer=TaskUpdateChartSerializer(data=request.data)
        task_id=kwargs.get("pk")
        task_obj=TaskChart.objects.get(id=task_id)
        emp_id=request.user.id
        emp_obj=Employee.objects.get(id=emp_id)       
        if serializer.is_valid():
            serializer.save(updated_by=emp_obj,task=task_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    

    
class TaskUpdatesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        emp_id=request.user.id
        qs=TaskUpdateChart.objects.filter(updated_by=emp_id)
        serializer=TaskUpdateChartSerializer(qs,many=True)
        return Response(data=serializer.data)   
    
    
