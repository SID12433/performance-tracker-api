from django.contrib import admin
from hrapi.models import Hr,Teams,ProjectDetail,TaskChart,Performance_assign,CustomUser

# Register your models here.


admin.site.register(Hr)
admin.site.register(CustomUser)
admin.site.register(Performance_assign)

