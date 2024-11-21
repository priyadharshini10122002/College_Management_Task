from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('staff/student_list/',StaffView.as_view(),name="student_list" ), #Done
    path('staff/edit_student/',StaffView.as_view(),name="edit_student" ), #Done
    path('staff/create_student/',StaffView.as_view(),name="create_student" ), #Done
    
    path('staff/add_students/',StaffView.as_view(),name="add_students" ),#Done

    path('student/view-info/',StudentView.as_view(),name="view-info" ),#Done
    path('student/edit-info/',StudentView.as_view(),name="edit-info" ),#Done

    path('student/subjects/',SubjectView.as_view(),name="subjects" ),#Done
    
]


