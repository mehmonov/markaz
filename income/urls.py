from django.urls import path
from .views import home,search,paymentStudents
urlpatterns = [
    path('',home,name='incomeHome'),
    path('searchStudents/',search,name='searchStudent'),
    path('paymentStudents/<int:student_id>',paymentStudents,name='paymentStudents'),
    
]
