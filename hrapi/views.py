from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action


from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign
from hrapi.serializer import RegistrationSerializer,EmployeeSerializer,TeamleadSerializer,TeamsSerializer,ProjectSerializer,ProjectAssignSerializer,ProjectDetailSerializer,TaskChartSerializer,TaskUpdatesChartSerializer,PerformanceTrackSerializer


class HrCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="hr")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        

class EmployeesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    

class TeamleadView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=TeamLead.objects.all()
        serializer=TeamleadSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TeamLead.objects.get(id=id)
        serializer=TeamleadSerializer(qs)
        return Response(data=serializer.data)
    

class TeamsView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    # def create(self,request,*args,**kwargs):
    #     serializer=TeamsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    
    def list(self,request,*args,**kwargs):
        qs=Teams.objects.all()
        serializer=TeamsSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Teams.objects.get(id=id)
        serializer=TeamsSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(detail=True, methods=["post"])
    def team_approval(self, request, *args, **kwargs):
        team_id = kwargs.get("pk")
        team_obj = Teams.objects.get(id=team_id)
        team_obj.is_approved = True
        team_obj.save()
        serializer = TeamsSerializer(team_obj)
        return Response(serializer.data)
    
    
class ProjectView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    def list(self,request,*args,**kwargs):
        qs=Projects.objects.all()
        serializer=ProjectSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Projects.objects.get(id=id)
        serializer=ProjectSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Projects.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Projects removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "Projects not found"}, status=status.HTTP_404_NOT_FOUND)
  


class ProjectAssignView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Project_assign.objects.all()
        serializer=ProjectAssignSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Project_assign.objects.get(id=id)
        serializer=ProjectAssignSerializer(qs)
        return Response(data=serializer.data)
      
        
    
class ProjectDetailView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=ProjectDetail.objects.all()
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
    
    def list(self,request,*args,**kwargs):
        qs=TaskChart.objects.all()
        serializer=TaskChartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
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
    
    
class PerformanceTrackView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self,request,*args,**kwargs):
        serializer=PerformanceTrackSerializer(data=request.data)
        hr_id=request.user.id
        hr_obj=Hr.objects.get(id=hr_id)
        if serializer.is_valid():
            serializer.save(hr=hr_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    
    

    
    
    

    