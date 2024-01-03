from django.shortcuts import render,redirect
from .models import Payment, Group,Student, Teacher,Admin, Teacher,Applicant, Boshliq,AlertMessages
from django.contrib.auth.decorators import login_required
from django.views.generic.dates import MonthArchiveView
from calendar import monthrange, Calendar
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import StudentSerializer
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login

def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('homePage')
            else:
                # Foydalanuvchi mavjud emas
                messages.error(request, 'Foydalanuvchi nomi yoki parol noto\'g\'ri')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})
@login_required
def home(request):
    user = request.user
    context = {}
    if not request.user.is_authenticated:
      return redirect('my_login')
    else:
        if Admin.objects.filter(user=user).exists():
            # The user is an admin
            applicants = Applicant.objects.filter(student__isnull=True)
            messages = AlertMessages.objects.filter(status='uncompleted')
            context = {
                'role':'admin',
                'applicants': applicants,
                'messages': messages
            }
            return render(request,template_name='admin/home.html',context=context)
        elif Teacher.objects.filter(user=user).exists():
            # The user is a teacher
            context['role'] = 'teacher'
            return redirect('teacher_home')
        elif Boshliq.objects.filter(user=user).exists():
            # The user is a Boshliq
            context['role'] = 'boshliq'
            return redirect('boshliqHome')
        else:
            return HttpResponse('tizimga kiring')

        return render(request, 'home.html', context)

def my_logout(request):
    # Foydalanuvchining sessiyasini o'chirish
    request.session.flush()

    # Bosh sahifaga yo'naltirish
    return redirect('login')
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        queryset = Student.objects.all()
        first_name = self.request.query_params.get('first_name')
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        return queryset
class GroupMonthArchiveView(MonthArchiveView):
    queryset = Group.objects.all()
    date_field = 'start_date'
    allow_future = True
    month_format = '%m'
    year_format = '%Y'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current year and month
        year = context['year']
        month = context['month']

        # Create a calendar object
        cal = Calendar()

        # Get the first and last days of the month
        first_day, last_day = monthrange(year, month)

        # Create a list of weeks
        weeks = cal.monthdatescalendar(year, month)

        # Create a list of days with groups
        calendar = []
        for week in weeks:
            calendar_week = []
            for day in week:
                groups = Group.objects.filter(start_date__year=day.year, start_date__month=day.month, start_date__day=day.day)
                calendar_week.append({'day': day, 'groups': groups})
            calendar.append(calendar_week)

        # Add the calendar to the context
        context['calendar'] = calendar

        return context


def workers_profile(request):
    return render(request, template_name='home/profile.html')