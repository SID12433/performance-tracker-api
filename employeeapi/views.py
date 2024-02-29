from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action


from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign
from employeeapi.serializer import RegistrationSerializer,TeamSerializer

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