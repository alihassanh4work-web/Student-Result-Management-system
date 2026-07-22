"""
URL configuration for SchoolResultManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from schoolresultsystem.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='home'),
    path('admin_login/',admin_login,name='admin_login'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('create_class/',create_class,name='create_class'),
    path('logout/',admin_logout,name='admin_logout'),
    path('manage_class/',manage_class,name='manage_class'),
    path('edit_class/<int:class_id>/',edit_class,name='edit_class'),
    path('create_subject/',create_subject,name='create_subject'),
    path('manage_subject/',manage_subject,name='manage_subject'), 
    path('subject_edit/<int:subject_id>/',subject_edit,name='subject_edit'),
    path('subject_combination/',subject_combination,name='subject_combination'),
    path('manage_subject_combination/',manage_subject_combination,name='manage_subject_combination'),
    path('create_student/',Add_student,name='Add_student'),
    path('manage_student/',manage_student,name='manage_student'),
    path('edit_student/<int:student_id>/',edit_student,name='edit_student'),
    path('Add_Notice/',Add_Notice,name='Add_Notice'),
    path('manage_notice/',manage_notice,name='manage_notice'),
    path('Add_result/',Add_result,name='Add_result'),
    path( "get_students_subjects/",get_students_subjects,name="get_students_subjects"),
    path('manage_result/',manage_result,name='manage_result'),
    path("edit_result/<int:student_id>/",edit_result,name="edit_result"),    
    path("change_password/",change_password,name="change_password"),
    path("student_login/",student_login, name="student_login"),
    path("student_result/",student_result, name="student_result"),

]

