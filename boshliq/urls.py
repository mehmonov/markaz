from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='boshliqHome'),
    path('all_students/',views.studentList,name='all_students'),
    path('all_incomes/',views.all_incomes,name='all_incomes'),
    path('all_groups/',views.all_groups,name='all_groups'),
    path('get_groups/',views.get_groups,name='get_groups'),
    path('salary/',views.salary,name='salary'),
    path('salary_filter/',views.salary_filter,name='salary_filter'),
    path('today_check_payments',views.today_check_payments,name='today_check_payments'),
    path('confirm_payments',views.confirm_payments,name='confirm_payments'),
    path('all_incomes_filter/',views.all_incomes_filter,name='all_incomes_filter'),
]