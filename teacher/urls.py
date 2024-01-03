from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='teacher_home'),
    path('attendance_teacher_get/',views.attendance,name='attendance_student'),
    path('attendance_submit/',views.attendance_submit,name='attendance_submit')
]
