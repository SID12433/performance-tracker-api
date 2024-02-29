from rest_framework import serializers
from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign


class RegistrationSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Employee
        fields=["id","Firstname","lastname","email_address","phoneno","position","username","password"]

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)
    
    
class TeamSerializer(serializers.ModelSerializer):
    teamlead=serializers.CharField(read_only=True)
    class Meta:
        model=Teams
        fields="__all__"