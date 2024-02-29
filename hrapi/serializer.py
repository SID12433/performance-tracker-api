from rest_framework import serializers
from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign


class RegistrationSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Hr
        fields=["id","name","username","email_address","password","phoneno"]

    def create(self, validated_data):
        return Hr.objects.create_user(**validated_data)
    
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["id","Firstname","lastname","email_address","phoneno","position","user_type","in_team"]
        

class TeamleadSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeamLead
        fields=["id","name","email_address","phoneno","user_type"]
        

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teams
        fields="__all__"
        
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Projects
        fields="__all__"
        

class ProjectAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project_assign
        fields="__all__"
 
 
class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectDetail
        fields="__all__"
        
        
class TaskChartSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskChart
        fields="__all__"
        

class TaskUpdatesChartSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskUpdateChart
        fields="__all__"
    
    
class PerformanceTrackSerializer(serializers.ModelSerializer):
    hr=serializers.CharField(read_only=True)
    class Meta:
        model=Performance_assign
        fields="__all__"
