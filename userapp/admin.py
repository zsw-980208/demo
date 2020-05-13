from django.contrib import admin

# Register your models here.
from userapp.models import UserInfo,Student,Employee

admin.site.register(UserInfo)
admin.site.register(Student)
admin.site.register(Employee)