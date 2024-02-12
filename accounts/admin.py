from django.contrib import admin

# Register your models here.
# exam_scheduler/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Invigilator, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 
                    'date_of_birth', 'user_type', 
                    'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class StudentAdmin(UserAdmin):
    model = Student
    list_display = ('username', 'email', 'first_name', 'last_name', 
                    'date_of_birth', 'user_type', 
                    'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class InvigilatorAdmin(UserAdmin):
    model = Invigilator
    list_display = ('username', 'email', 'first_name', 'last_name', 
                    'date_of_birth', 'user_type', 
                    'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Invigilator, InvigilatorAdmin)
admin.site.register(Profile)

