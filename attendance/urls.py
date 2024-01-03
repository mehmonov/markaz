from django.urls import path
from .views import attendanceList,home
urlpatterns = [
    path('',home,name='attendancehome'),
    path('attendanceList/',attendanceList,name='attendanceList')
    
]
