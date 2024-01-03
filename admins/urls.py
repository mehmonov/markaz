from .views import adminHome,newApplicant,applicantList,filter_applicants,transfer_applicant,studentList,createGroup,student_group_change, add_students_to_group,groupList, groupEdit,group_detail,leave_group, group_payments, student_detail
from django.urls import path
urlpatterns = [
    path('',adminHome,name='adminHome'),
    path('newApplicant/',newApplicant,name='newApplicant'),
    path('applicantList/',applicantList,name='applicantList'),
    path('filter_applicants/',filter_applicants,name='filter_applicants'),
    path('transfer_applicant/<int:application_id>/', transfer_applicant, name='transfer_applicant'),
    path('studentList/',studentList,name='studentList'),
    path('createGroup/',createGroup,name='createGroup'),
    path('student_group_change/<int:student_id>/',student_group_change,name='student_group_change'),
    path('groupList/',groupList,name='groupList'),
    path('student_detail/<int:student_id>/',student_detail,name='student_detail'),
    path('group_payments/',group_payments,name='group_payments'),
    path('group_detail/<int:group_id>/',group_detail,name="group_detail"),
    path('groupEdit/<int:group_id>/',groupEdit,name='groupEdit'),
    path('group/<int:group_id>/add_students/', add_students_to_group, name='add_students_to_group'),
    path('leave_group/<int:group_id>/<int:student_id>/', leave_group, name='leave_group'),
    
]
