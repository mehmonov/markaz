from django.shortcuts import render, redirect
from django.utils import timezone
from home.models import Teacher, Group, Student, Payment, Attendance, Admin, AlertMessages
from django.utils.timezone import make_aware
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.utils import timezone

# Create your views here.

def home(request):
    teacher = request.user.teacher
    groups = Group.objects.filter(teacher=teacher)
    num_groups = groups.count()
    students = Student.objects.filter(group__in=groups).distinct()
    num_students = students.count()
    today = timezone.now().date()
    payments = Payment.unconfirmed_objects.filter(student__in=students, date__month=today.month, group__in=groups)
    num_payments = payments.count()
    today_groups = groups.filter(day_of_week__overlap=[today.strftime('%A')])    
    context = {
        'num_groups': num_groups,
        'num_students': num_students,
        'num_payments': num_payments,
        'today_groups': today_groups,
    }
    return render(request, 'teacher/home.html', context)


def attendance(request):
    teacher = request.user.teacher
    now = timezone.localtime()
    current_groups = Group.objects.filter(
        teacher=teacher,
        time__lte=(now + timedelta(hours=3)).time(),
        day_of_week__contains=now.strftime('%A'),
        start_date__lte=now.date(),
        end_date__gte=now.date()
    )
    
    context = {
        'current_groups': current_groups,
    }
    print(current_groups)
    return render(request, 'teacher/attendance.html', context)
@require_POST
def attendance_submit(request):
    group_id = request.POST.get('group_id')
    attendance = request.POST.getlist('attendance')
    group = Group.objects.get(id=group_id)
    missed_students = []
    for student in group.students.all():
        should_attend = str(student.id) in attendance
        Attendance.objects.create(student=student, date=timezone.now().date(), group=group, should_attend=should_attend)
        if not should_attend:
            missed_students.append(student)
    alert = AlertMessages
    if missed_students:
        message = 'missed_student'
        admins = Admin.objects.all()
        for admin in admins:
            for student in missed_students:
                alert.objects.create(to=admin.user, ffrom=request.user, student=student, group=group.name, message=message)
    
    return redirect('attendance_student')

